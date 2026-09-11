# Contributing

## 基本原则

贡献应当增强可验证学习，而不是增加新的状态混乱。提交前请确认：

1. 技术知识、用户状态、原始证据和展示视图没有混写；
2. AI 给出的标准答案没有被当作用户掌握证据；
3. 新增领域 Profile 不把个人历史或私有连接器信息写成通用规则；
4. 新增 Adapter 明确权限、失败降级、输入输出与数据边界；
5. 新增模板可以独立阅读，并保留来源、版本和验收入口。

## 本地运行验证

涉及 Skill 路由、对象写回或 Adapter 行为的改动，至少执行：

```powershell
python scripts/smoke_test.py
python -m runtime.local.cli init --non-interactive --profile generic --mode study --adapters local
```

第二条命令只应在临时或已忽略的 `.learning-evidence/` 目录中运行。未实现的外部 Adapter 必须标为 `planned_not_implemented`，不能用文档存在代替实际能力。

## Pull Request 检查

- 使用清晰的 Markdown 标题与相对链接；
- 所有示例均已脱敏；
- 更新协议时同步更新 Skill 路由、受影响模板与版本记录；
- 不提交 Token、私有 Workspace URL、真实面试逐字稿或个人学习状态；
- 若改动影响执行语义，请补充一个可复现的行为验证场景。
