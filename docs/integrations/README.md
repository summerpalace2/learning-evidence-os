# Integrations

连接器属于基础设施层，不是 Learning Evidence OS 的决策层。Core 只依赖统一对象和可验证结果，不依赖某个 SaaS。

| 集成 | 适合保存 | 不保存 | 状态 |
|---|---|---|---|
| [Local](../../adapters/local/README.md) | Markdown、JSON、SQLite、本地索引 | 多人协同的唯一真相 | 可作为默认起点 |
| [Notion](../../adapters/notion/README.md) | 控制中心、节点、Session、Evidence、验收板、handoff | 完整资料仓库 | 需授权 |
| [Google Drive](../../adapters/google-drive/README.md) | 长文、资料、源码快照、来源版本 | 掌握等级 | 需授权 |
| [Google Sheets](../../adapters/google-sheets/README.md) | 去个人化题库、题目成熟度 | 个人表现结论 | 需授权 |

任何连接器写入必须由用户任务授权；失败时必须降级为临时状态，不能假装完成 Final Sync。
