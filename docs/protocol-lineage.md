# V5.0 Source Lineage

本仓库的通用 Core 来自 Android Knowledge Learning V5.0 的工程化拆分，而不是重新发明另一套并行规则。

| V5.0 原始章节 | 仓库位置 | 迁移方式 |
|---|---|---|
| 执行摘要与总体架构 | README、docs/architecture.md | 用公开项目语言说明问题、职责和边界 |
| Notion 状态层 | Core Protocol 2、Adapter Contract | 抽象为 State、Evidence、Presentation 与可选 Notion Adapter |
| Google 资产层 | Adapter Contract、docs/integrations | 抽象为来源与题库的可选 Adapter |
| ChatGPT 与 Skill | skills/learning-evidence-os/SKILL.md | 转为可安装的执行入口与外部写入边界 |
| 最小充分上下文 | Core Protocol 4、docs/architecture.md | 保留状态恢复门与 Learning Unit |
| Double Loop | Core Protocol 3–4、README 图示 | 原样保留方法论，移除 Android 专属名词 |
| 文章生产 | Core Protocol 5、templates/learning-article.md | 保留七阶段、因果链、代码与图片质量门 |
| 标准答案与面试库 | Core Protocol 6–7、templates | 保留答案资产与用户表现分离 |
| 验收、导航与写回 | Core Protocol 7–9、templates | 保留 Round、Final Sync、Topic Closeout 与双向导航 |
| Android 专属规则 | profiles/android | 作为可替换 Profile，而非 Core 规则 |

原始 Word 文档属于私有资料，不随公开包发布；公开包只保留由它提炼出的通用协议、脱敏图示和 [私有归档说明](archive/README.md)。公开仓库不记录 Notion、Drive、Sheets 的个人入口。
