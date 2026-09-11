# Runtime Bootstrap

这份参考只描述可验证的首次配置和 Local-first 运行方式。它不假设任何 SaaS、OAuth 或模型连接。

## 必问配置

首次进入正式学习前，询问：

- 学习领域和 Profile；
- 学习模式：`study`、`interview`、`exam` 或 `practice`；
- 已有资料位置；
- 用户实际拥有并希望使用的存储或连接器；
- 是否导入历史状态；
- 个人数据保存位置和是否允许外部写入。

如果用户不确定，使用 `generic + study + local-json`，不要阻塞第一次运行。

## 能力矩阵

能力检查必须区分三种状态：

- `implemented`：当前运行时确实可以读写，并且有测试证明；
- `planned_not_implemented`：仓库有契约或设计，但没有可调用实现；
- `unavailable`：用户想用，但当前环境不可访问。

只有 `implemented` 可以进入正式持久化。其他状态可以参与临时对话，但必须在 Session 或最终回复中标记未持久化对象。

## 本地运行

仓库根目录执行：

```powershell
python -m runtime.local.cli init
python -m runtime.local.cli status
python scripts/smoke_test.py
```

`init` 是交互式 Bootstrap；自动化环境可以使用：

```powershell
python -m runtime.local.cli init --non-interactive --profile generic --mode study --adapters local
```

Local Adapter 使用 `.learning-evidence/config.json` 和 `.learning-evidence/objects/`。该目录属于个人运行数据，已被 `.gitignore` 忽略，不应提交到公开仓库。

## 最小成功标准

配置完成后必须能够：

1. 创建 Topic 和 Topic State；
2. 保存 Article；
3. 在 Evidence 之前保存 Canonical Answer；
4. 保存 Session 和原始 Evidence；
5. 更新 L/R/C、reviewItems 和下一步 handoff；
6. 重新读取状态，确认 Final Sync 为 `verified`。

如果任一步失败，保留已经写入的本地事实并报告失败对象；不能把失败改写为 `completed`。
