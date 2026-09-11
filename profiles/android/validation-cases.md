# Android Profile 验证用例

这些用例使用 Android 的 Handler/Looper 消息分发与生命周期边界作为领域场景，验证 Learning Evidence OS 的 Core 行为；它们不是 Android 工程测试，也不包含任何个人学习状态。

真正可执行的最小闭环见仓库根目录的 `scripts/smoke_test.py`。下面的场景说明 Profile 应如何约束教学事实和验收证据。

## Case 1：Double Loop 保持 C、L、R 分离

**设置：** Coverage Discovery 发现现有地图没有覆盖 Looper、MessageQueue、Handler 关联关系和生命周期清理边界；随后用户回答消息分发问题。

**预期：**

- 地图缺口被分类为 `A` 或 `E`，只影响覆盖置信度 `C`；
- 用户回答产生独立 Evidence 和 `R`；
- 一次回答不能直接提升长期掌握 `L`；
- 地图缺口可以产生下一学习单元，但不能作为掌握证据。

## Case 2：标准答案先于评价保存

**设置：** 系统先创建“消息如何从入队走到 Handler 处理”的规范问题和标准答案，再开始验收用户回答。

**预期：**

- Evidence 关闭前，独立 Answer 已存在；
- Answer 覆盖 Looper、MessageQueue、Handler、线程关联和生命周期边界的因果链；
- 用户原话保持独立，不被标准答案覆盖。

## Case 3：多轮验收累计保存

**设置：** 第一轮测试消息入队和取出，第二轮测试线程退出，第三轮测试延迟消息与对象生命周期。

**预期：**

- 三轮都链接到同一个 Topic；
- 每一轮保留自己的问题、原话、提示程度、R、错误和复测项；
- 新一轮不能覆盖旧 Evidence；
- 未完成的边界使 Topic 保持 `in_review`。

## Case 4：文章、节点和证据双向导航

**设置：** Topic 指向解释消息分发机制的 Article 段落，Article 段落反向指向 Node、Answer 和 Evidence。

**预期：**

- 链接包含文章版本和稳定定位；
- Node → Article 与 Article → Node 都能解析到目标位置；
- 文章移动时，两端链接必须一起修复；
- 失效链接必须被报告为完整性错误。

## Case 5：Final Sync 留下唯一下一步

**设置：** 用户能解释消息分发主体流程，但没有解释延迟消息导致的生命周期边界。

**预期：**

- Topic State 保留未解决边界；
- 控制视图展示真实的 L/R/C，不夸大 L；
- handoff 只留下一个可执行的复测动作；
- 主题状态为 `partial` 或 `in_review`，而不是虚假的完成。

## Case 6：Adapter 失败不能变成假成功

**设置：** 外部 Adapter 在更新 Topic State 时失败，但本地 Evidence 已经保存。

**预期：**

- 本地临时记录保留事实、Answer、Session 和 Evidence；
- 明确报告失败对象和未完成写回；
- 不声称 `completed` 或 Final Sync 成功；
- 后续授权重试可以按稳定 ID 幂等执行。
