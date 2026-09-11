"""Minimum end-to-end Core workflow backed by LocalAdapter."""

from __future__ import annotations

from datetime import datetime, timezone
import re
from typing import Any, Dict, Iterable, List, Optional
from uuid import uuid4

from .adapter import LocalAdapter, LocalAdapterError


class RuntimeErrorBase(RuntimeError):
    """Raised when a Core invariant would be violated."""


RATING = re.compile(r"^[LR][0-5]$")
COVERAGE = re.compile(r"^C[0-4]$")
PROMPTS = {"independent", "light_prompt", "strong_prompt", "answer_repetition", "recognition"}


class LearningRuntime:
    """Persist a small but real Topic → Answer → Evidence → State flow."""

    def __init__(self, adapter: LocalAdapter):
        self.adapter = adapter
        self.adapter.initialize()

    def create_topic(self, title: str, scope: str, *, profile: Optional[str] = None) -> Dict[str, Any]:
        topic_id = _id("topic")
        state_id = _id("state")
        topic = {
            "id": topic_id,
            "title": title,
            "profile": profile or self._profile(),
            "scope": scope,
            "articleIds": [],
            "nodeIds": [],
            "stateId": state_id,
            "createdAt": _now(),
        }
        state = {
            "id": state_id,
            "topicId": topic_id,
            "longTermMastery": "L0",
            "coverageConfidence": "C0",
            "latestRoundRating": None,
            "lifecycle": "active",
            "reviewItems": [],
            "nextHandoff": "",
            "history": [],
            "updatedAt": _now(),
        }
        self.adapter.save("topic_state", state)
        self.adapter.save("topic", topic)
        return topic

    def save_article(
        self, topic_id: str, title: str, body: str, *, version: str = "v1", source_links: Iterable[Dict[str, Any]] = ()
    ) -> Dict[str, Any]:
        topic = self.adapter.require("topic", topic_id)
        article = {
            "id": _id("article"),
            "topicId": topic_id,
            "title": title,
            "version": version,
            "body": body,
            "sourceLinks": list(source_links),
            "nodeLinks": [],
            "status": "draft",
            "updatedAt": _now(),
        }
        self.adapter.save("article", article)
        topic["articleIds"].append(article["id"])
        self.adapter.update("topic", topic)
        return article

    def save_node(
        self,
        topic_id: str,
        title: str,
        *,
        kind: str = "checkpoint",
        article_id: Optional[str] = None,
        locator: str = "",
    ) -> Dict[str, Any]:
        topic = self.adapter.require("topic", topic_id)
        node = {
            "id": _id("node"),
            "topicId": topic_id,
            "title": title,
            "kind": kind,
            "articleLinks": [],
            "answerIds": [],
            "createdAt": _now(),
        }
        if article_id:
            article = self.adapter.require("article", article_id)
            if not locator:
                raise RuntimeErrorBase("Node 连接 Article 时必须提供稳定 locator")
            link = {
                "kind": "article-section",
                "target": article_id,
                "version": article["version"],
                "locator": locator,
            }
            node["articleLinks"].append(link)
            article.setdefault("nodeLinks", []).append({
                "kind": "node",
                "target": node["id"],
                "version": article["version"],
                "locator": locator,
            })
            self.adapter.update("article", article)
        self.adapter.save("node", node)
        topic.setdefault("nodeIds", []).append(node["id"])
        self.adapter.update("topic", topic)
        return node

    def save_question(
        self,
        topic_id: str,
        original_question: str,
        normalized_question: str,
        *,
        kind: str = "mechanism-and-boundary",
        node_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        topic = self.adapter.require("topic", topic_id)
        if node_id:
            self.adapter.require("node", node_id)
        question = {
            "id": _id("question"),
            "topicId": topic_id,
            "originalQuestion": original_question,
            "normalizedQuestion": normalized_question,
            "kind": kind,
            "nodeId": node_id,
            "maturity": "candidate",
            "createdAt": _now(),
        }
        self.adapter.save("question", question)
        topic.setdefault("questionIds", []).append(question["id"])
        self.adapter.update("topic", topic)
        return question

    def save_canonical_answer(
        self,
        question_id: str,
        short_answer: str,
        complete_answer: str,
        *,
        deep_expansion: str = "",
        boundaries: Iterable[str] = (),
        follow_ups: Iterable[str] = (),
    ) -> Dict[str, Any]:
        question = self.adapter.require("question", question_id)
        answer = {
            "id": _id("answer"),
            "questionId": question_id,
            "shortAnswer": short_answer,
            "completeAnswer": complete_answer,
            "deepExpansion": deep_expansion,
            "boundaries": list(boundaries),
            "followUps": list(follow_ups),
            "validationState": "draft",
            "createdAt": _now(),
        }
        self.adapter.save("answer", answer)
        node_id = question.get("nodeId")
        if node_id:
            node = self.adapter.require("node", node_id)
            node.setdefault("answerIds", []).append(answer["id"])
            self.adapter.update("node", node)
        return answer

    def start_session(self, topic_id: str, *, scope: str, mode: Optional[str] = None) -> Dict[str, Any]:
        self.adapter.require("topic", topic_id)
        session = {
            "id": _id("session"),
            "topicId": topic_id,
            "mode": mode or self._mode(),
            "actualScope": scope,
            "status": "started",
            "evidenceIds": [],
            "writebackOrder": [],
            "createdAt": _now(),
        }
        self.adapter.save("session", session)
        return session

    def record_evidence(
        self,
        session_id: str,
        question_id: str,
        answer_id: str,
        raw_answer: str,
        *,
        prompt_level: str = "independent",
        round_rating: str = "R0",
        mistakes: Iterable[str] = (),
        follow_up_result: str = "",
    ) -> Dict[str, Any]:
        session = self.adapter.require("session", session_id)
        self.adapter.require("topic", session["topicId"])
        self.adapter.require("answer", answer_id)
        if prompt_level not in PROMPTS:
            raise RuntimeErrorBase(f"无效提示等级：{prompt_level}")
        if not _is_rating(round_rating, "R"):
            raise RuntimeErrorBase(f"无效单轮表现等级：{round_rating}")
        evidence = {
            "id": _id("evidence"),
            "sessionId": session_id,
            "questionId": question_id,
            "answerId": answer_id,
            "rawAnswer": raw_answer,
            "promptLevel": prompt_level,
            "roundRating": round_rating,
            "mistakes": list(mistakes),
            "followUpResult": follow_up_result,
            "createdAt": _now(),
        }
        self.adapter.save("evidence", evidence)
        session["evidenceIds"].append(evidence["id"])
        session["writebackOrder"] = ["freeze_facts", "canonical_answer", "session", "evidence"]
        self.adapter.update("session", session)
        return evidence

    def final_sync(
        self,
        session_id: str,
        *,
        long_term_mastery: str,
        coverage_confidence: str,
        review_items: Iterable[str],
        next_handoff: str,
        next_action: str,
        lifecycle: str = "in_review",
    ) -> Dict[str, Any]:
        session = self.adapter.require("session", session_id)
        topic = self.adapter.require("topic", session["topicId"])
        state = self.adapter.require("topic_state", topic["stateId"])
        evidence = [self.adapter.require("evidence", item) for item in session["evidenceIds"]]
        if not evidence:
            raise RuntimeErrorBase("Final Sync 需要至少一条 Evidence")
        for item in evidence:
            answer = self.adapter.require("answer", item["answerId"])
            if answer.get("questionId") != item.get("questionId"):
                raise RuntimeErrorBase("Evidence 的 questionId 与 Canonical Answer 不一致")
        if not _is_rating(long_term_mastery, "L"):
            raise RuntimeErrorBase(f"无效长期掌握等级：{long_term_mastery}")
        if not COVERAGE.fullmatch(coverage_confidence):
            raise RuntimeErrorBase(f"无效地图覆盖等级：{coverage_confidence}")
        review = list(review_items)
        state["longTermMastery"] = long_term_mastery
        state["coverageConfidence"] = coverage_confidence
        state["latestRoundRating"] = evidence[-1]["roundRating"]
        state["lifecycle"] = lifecycle
        state["reviewItems"] = review
        state["nextHandoff"] = next_handoff
        state["history"].append({
            "sessionId": session_id,
            "evidenceIds": session["evidenceIds"],
            "roundRating": evidence[-1]["roundRating"],
            "recordedAt": _now(),
        })
        state["updatedAt"] = _now()
        self.adapter.update("topic_state", state)

        topic["lastSessionId"] = session_id
        topic["nextHandoff"] = next_handoff
        self.adapter.update("topic", topic)

        handoff = {
            "id": f"handoff-{topic['id']}",
            "topicId": topic["id"],
            "sessionId": session_id,
            "nextAction": next_action,
            "status": "open" if next_action else "invalid",
            "updatedAt": _now(),
        }
        self.adapter.update("handoff", handoff) if self.adapter.get("handoff", handoff["id"]) else self.adapter.save("handoff", handoff)

        presentation = {
            "id": "control-center",
            "view": "Learning Control Center",
            "currentTopicId": topic["id"],
            "currentStateId": state["id"],
            "currentStage": "in_review" if review else "ready_for_next_unit",
            "nextAction": next_action,
            "updatedAt": _now(),
        }
        self.adapter.update("presentation", presentation) if self.adapter.get("presentation", "control-center") else self.adapter.save("presentation", presentation)

        session["status"] = "in_review" if review else "completed"
        session["finalSync"] = {"status": "verified", "updatedAt": _now()}
        session["writebackOrder"] = [
            "freeze_facts", "canonical_answer", "session", "evidence", "nodes_and_article",
            "topic_state", "control_center", "question_bank_candidate", "bidirectional_navigation", "final_sync",
        ]
        self.adapter.update("session", session)
        return presentation

    def status(self) -> Dict[str, Any]:
        config = self.adapter.load_config()
        return {"configured": config is not None, "config": config, "counts": self.adapter.counts()}

    def _profile(self) -> str:
        config = self.adapter.load_config() or {}
        return str(config.get("profile", "generic"))

    def _mode(self) -> str:
        config = self.adapter.load_config() or {}
        return str(config.get("mode", "study"))


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12]}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _is_rating(value: str, prefix: str) -> bool:
    return bool(re.fullmatch(rf"{prefix}[0-5]", value))
