"""Validate the public Android KMP fixture and its core behavior invariants."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "object-model.json"
FIXTURE = ROOT / "examples" / "android-kmp" / "validation-fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(str(exc))

    if "$defs" not in schema:
        fail("schema has no $defs section")
    for name in ("topic", "node", "article", "question", "answer", "session", "evidenceItem"):
        if name not in schema["$defs"]:
            fail(f"schema is missing $defs/{name}")

    topics = {item["id"]: item for item in data.get("topics", [])}
    nodes = {item["id"]: item for item in data.get("nodes", [])}
    articles = {item["id"]: item for item in data.get("articles", [])}
    questions = {item["id"]: item for item in data.get("questions", [])}
    answers = {item["id"]: item for item in data.get("answers", [])}
    evidence = {item["id"]: item for item in data.get("evidence", [])}

    if not topics or not nodes or not articles or not questions or not answers or not evidence:
        fail("fixture must contain all core object collections")

    for topic in topics.values():
        state = topic.get("state", {})
        if not re.fullmatch(r"L[0-5]", state.get("longTermMastery", "")):
            fail(f"invalid L state on {topic['id']}")
        if not re.fullmatch(r"C[0-4]", state.get("coverageConfidence", "")):
            fail(f"invalid C state on {topic['id']}")
        if not re.fullmatch(r"R[0-5]", state.get("latestRoundRating", "")):
            fail(f"invalid R state on {topic['id']}")

    for item in data.get("coverageFindings", []):
        if item.get("classification") not in set("ABCDEFG"):
            fail(f"invalid A-G classification on {item.get('id')}")

    for answer in answers.values():
        if answer["questionId"] not in questions:
            fail(f"answer {answer['id']} points to a missing question")
        if not answer.get("shortAnswer") or not answer.get("completeAnswer"):
            fail(f"answer {answer['id']} is not complete")

    for item in evidence.values():
        if item["questionId"] not in questions:
            fail(f"evidence {item['id']} points to a missing question")
        if item.get("answerId") not in answers:
            fail(f"evidence {item['id']} has no canonical answer")
        if item.get("promptLevel") not in {
            "independent",
            "light_prompt",
            "strong_prompt",
            "answer_repetition",
            "recognition",
        }:
            fail(f"invalid prompt level on {item['id']}")

    for node in nodes.values():
        for link in node.get("articleLinks", []):
            if link.get("target") not in articles or not link.get("locator"):
                fail(f"node {node['id']} has an incomplete article link")

    for article in articles.values():
        for link in article.get("nodeLinks", []):
            if link.get("target") not in nodes or not link.get("locator"):
                fail(f"article {article['id']} has an incomplete node link")

    rounds = data.get("acceptanceRounds", [])
    if not rounds or len({round_["roundNumber"] for round_ in rounds}) != len(rounds):
        fail("acceptance rounds must be cumulative and uniquely numbered")
    if any(round_["topicId"] not in topics for round_ in rounds):
        fail("acceptance round points to a missing topic")

    order = data.get("writebackOrder", [])
    required_order = ["canonical_answer", "session", "evidence", "final_sync"]
    if any(step not in order for step in required_order):
        fail("writeback order is missing a required step")
    if order.index("canonical_answer") > order.index("evidence"):
        fail("canonical answer must precede evidence")

    if not data.get("presentation", {}).get("nextAction"):
        fail("Final Sync fixture has no executable next action")

    print("Fixture validation: PASS")
    print(f"topics={len(topics)} nodes={len(nodes)} answers={len(answers)} evidence={len(evidence)}")


if __name__ == "__main__":
    main()
