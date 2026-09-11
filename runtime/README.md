# Runtime

这里放可以实际执行的运行时实现。当前只有 `runtime/local`，它是无第三方依赖的 Local JSON Runtime。

运行要求：Python 3.9 或更高版本。

## 运行

从仓库根目录执行：

```powershell
python -m runtime.local.cli init
python -m runtime.local.cli status
python scripts/smoke_test.py
```

首次 `init` 会询问 Profile、学习模式、资料位置和用户已有的 Adapter。当前只有 `local` 的读写能力经过实现和测试；Notion、Google Drive、Google Sheets 等会被登记为 `planned_not_implemented`，不会被误认为已经接入。

## 当前 API 闭环

`LearningRuntime` 提供以下最小操作：

```text
create_topic
→ save_article
→ save_node / save_question
→ save_canonical_answer
→ start_session
→ record_evidence
→ final_sync
```

每个对象都以稳定 ID 保存到 `.learning-evidence/objects/`，每次 JSON 写入使用临时文件 + 原子替换。`record_evidence` 要求 Answer 已存在，`final_sync` 重新读取并校验 Evidence、L/R/C 和下一步 handoff。

这不是已经完成的 SaaS 平台，也不是外部连接器实现；它是一个可以真实运行、验证 Core 写回顺序和安全降级的本地基线。
