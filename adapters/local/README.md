# Local Adapter

Local Adapter 是当前唯一已经实现并经过端到端测试的存储实现。它不依赖 Notion、Google、SQLite 或任何第三方 Python 包，默认使用每个对象一个 JSON 文件的方式保存状态。

## 快速运行

在仓库根目录执行：

```powershell
python -m runtime.local.cli init
python -m runtime.local.cli status
python scripts/smoke_test.py
```

`init` 会询问 Profile、学习模式、资料位置和已有 Adapter。没有可用外部连接器时，系统会明确选择 `local-json`，不会伪造 Notion 或 Google 写回成功。

默认目录：

```text
.learning-evidence/
├── config.json
└── objects/
    ├── topics/
    ├── nodes/
    ├── articles/
    ├── questions/
    ├── answers/
    ├── sessions/
    ├── evidence/
    ├── topic-states/
    ├── presentations/
    └── handoffs/
```

行为审计需要时，还可以使用 `acceptance-rounds/` 和 `coverage-findings/` 保存多轮验收与地图缺口。

## 能力边界

当前实现支持配置保存、对象读写、稳定 ID、原子 JSON 写入、标准答案先于 Evidence、Topic State、控制视图、handoff 和 Final Sync。文章正文暂以 JSON 字段保存，后续可增加 Markdown 文件投影。

Notion、Google Drive 和 Google Sheets 目前只有 Adapter Contract 和职责说明，尚未实现连接器；选择它们不会改变本地已验证的持久化结果。
