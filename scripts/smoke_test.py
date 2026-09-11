"""Run a dependency-free end-to-end test of Bootstrap and Local Runtime."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.local import LocalAdapter, LearningRuntime, LocalAdapterError, build_config  # noqa: E402


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="learning-evidence-os-") as directory:
        root = Path(directory)
        adapter = LocalAdapter(root)
        adapter.save_config(
            build_config(
                profile="generic",
                mode="study",
                storage_root=root,
                sources=["local://demo"],
                requested_adapters=["local", "notion"],
            )
        )
        runtime = LearningRuntime(adapter)
        topic = runtime.create_topic("消息分发与生命周期边界", "Looper、MessageQueue、Handler 与生命周期清理")
        article = runtime.save_article(topic["id"], "消息分发学习文章", "背景 → 机制 → 边界 → 验收", version="v1")
        node = runtime.save_node(
            topic["id"],
            "消息分发与生命周期边界",
            article_id=article["id"],
            locator="#message-dispatch",
        )
        question = runtime.save_question(
            topic["id"],
            "Handler 的消息是如何被处理的？",
            "解释 Looper、MessageQueue、Handler 的消息分发因果链和生命周期边界。",
            node_id=node["id"],
        )
        answer = runtime.save_canonical_answer(
            question["id"],
            "Handler 把消息投递到关联 Looper 的 MessageQueue，由 Looper 驱动分发。",
            "Handler 关联一个 Looper 和它的 MessageQueue；发送消息只是入队，Looper.loop() 从队列取出消息并调用 Handler 处理。线程退出、生命周期结束或持有关系不当时，需要关注消息滞留和清理边界。",
            boundaries=["没有 Looper 的线程不能直接按默认方式创建 Handler", "延迟消息可能延长对象存活"],
        )
        session = runtime.start_session(topic["id"], scope="消息入队、取出、分发和生命周期边界")
        try:
            runtime.record_evidence(
                session["id"],
                question["id"],
                "answer-does-not-exist",
                "这条记录不应该被保存",
            )
        except LocalAdapterError:
            pass
        else:
            raise AssertionError("Evidence 在没有 Canonical Answer 时不应写入")
        assert adapter.counts()["evidence"] == 0
        evidence = runtime.record_evidence(
            session["id"],
            question["id"],
            answer["id"],
            "消息先进入队列，Looper 再取出交给 Handler；生命周期清理还需要再解释。",
            prompt_level="independent",
            round_rating="R3",
            mistakes=["没有展开消息持有关系"],
            follow_up_result="需要复测延迟消息导致的生命周期边界",
        )
        presentation = runtime.final_sync(
            session["id"],
            long_term_mastery="L2",
            coverage_confidence="C2",
            review_items=["解释延迟消息与对象存活的关系"],
            next_handoff="复测 Handler 生命周期清理边界",
            next_action="复测 Handler 生命周期清理边界",
        )
        state = adapter.require("topic_state", topic["stateId"])
        saved_session = adapter.require("session", session["id"])
        assert adapter.require("article", article["id"])["version"] == "v1"
        assert adapter.require("article", article["id"])["nodeLinks"][0]["target"] == node["id"]
        assert adapter.require("node", node["id"])["answerIds"] == [answer["id"]]
        assert adapter.require("question", question["id"])["nodeId"] == node["id"]
        assert adapter.require("answer", answer["id"])["id"] == evidence["answerId"]
        assert state["longTermMastery"] == "L2"
        assert state["latestRoundRating"] == "R3"
        assert saved_session["finalSync"]["status"] == "verified"
        assert presentation["nextAction"] == "复测 Handler 生命周期清理边界"
        assert adapter.load_config()["capabilities"]["notion"]["status"] == "planned_not_implemented"
        print(json.dumps({"status": "PASS", "objects": adapter.counts(), "root": str(root)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
