# 私有归档说明

原始 `Android个人知识库_全景架构与运行协议` Word 文档是本项目的设计来源之一。它包含个人运行状态、真实系统入口和外部服务超链接，因此不属于公开仓库内容。

## 保存方式

请把原始 Word、个人 Notion 导出、Drive/Sheets 导出和真实学习记录保存在仓库之外，例如：

```text
private-archive/
├── source-word/
├── notion-export/
├── drive-export/
└── learner-evidence/
```

`private-archive/` 不应被复制进公开仓库或公开 ZIP。公开包中的 `assets/diagrams/` 只保留可复用的协议图示，不代表任何个人状态或外部服务授权。

## 发布前检查

在分享仓库、ZIP 或脱敏文档前，逐项确认：

- 没有 Notion、Drive、Sheets 的个人 URL、页面 ID、文件 ID 或二维码；
- 没有 OAuth Token、Cookie、API Key、邮箱、用户名或本地绝对路径；
- 没有真实面试逐字稿、个人掌握等级、当前任务和历史状态；
- DOCX 的 `word/_rels/*.rels`、批注、页眉页脚和文档属性中没有私有信息；
- 图表只表达通用职责、流程和对象边界；
- README、Profile、示例和模板中的链接都能在脱离个人工作区后解释清楚。

如需公开一份 Word 版说明，应先重建脱敏副本，再做 DOCX 超链接、元数据和渲染检查。不要直接把个人运行文档改名后上传。
