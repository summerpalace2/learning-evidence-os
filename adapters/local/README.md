# Local Adapter

Local Adapter 是无第三方依赖的默认实现。

建议目录：

~~~text
local-state/
├── topics/
├── evidence/
├── sessions/
├── answers/
├── articles/
└── handoff.md
~~~

使用稳定 ID、相对链接和可审阅的 Markdown/JSON。每次写回仍遵循 Core 的事实冻结与 Final Sync 顺序。
