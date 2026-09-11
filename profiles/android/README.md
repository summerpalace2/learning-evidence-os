# Android Profile

Android Profile 是 Learning Evidence OS 的首个领域实现。它把通用 Core 用于 Android、Java、Kotlin、JVM、并发、Framework、网络、存储、性能、架构、算法与客户端面试。

## 领域边界

| 层级 | Android Profile 中的含义 |
|---|---|
| Domain | Kotlin、Java、Android Framework、并发、网络、性能等长期方向 |
| Topic | 例如 Handler/Looper 消息分发、协程调度、Binder 调用链 |
| Checkpoint | 例如 Source Set 可见性、Compilation、Handler 消息分发、CHM 桶处理 |

一个 Topic 必须能形成完整文章并支持多轮验收。Checkpoint 只有在可以独立追问、迁移或复测时才单独建立。

## 技术真相来源

默认优先级如下：

1. Android Developers、Kotlin 官方文档、JDK 文档；
2. AOSP 或 Kotlin/Gradle 源码及对应版本；
3. 官方 Release Notes、AGP/Kotlin 版本迁移资料；
4. 高质量工程文章和课程；
5. 真实面试题与用户对话，仅作为问题与学习证据，不替代技术真相。

版本冲突必须记录采用结论、来源版本和理由。

## Android 文章的完整链路

正式文章通常需要解释：

~~~text
问题背景
  → 概念定义
  → 前置依赖
  → 编译或运行机制
  → 执行流程
  → Android 工程映射
  → API、版本和边界
  → 常见误区与诊断
  → 20 秒 / 60–90 秒面试表达
  → 用户验收入口
~~~

代码必须使用语言标识，例如 Kotlin、Java、Gradle Kotlin DSL、XML、Shell；流程图或架构图应插入可读图片，并保留正文解释。

~~~kotlin
// 正确示例：Markdown 中的代码块必须标记语言。
expect fun platformName(): String
~~~

## Android 面试表达

每个高价值题目至少保存：

- 原题与标准化题干；
- 20 秒结论；
- 60–90 秒完整回答；
- 深入机制、源码或工程展开；
- 边界、反例、取舍与版本；
- 用户原始回答、提示程度、R、错误类型与复测结果。

默认追问方向包括因果、源码位置、生命周期、API 行为、性能、稳定性、工程取舍与陌生场景迁移。

## 当前 V5.0 参考

- [通用 Core 协议](../../skills/learning-evidence-os/references/core-protocol.md)
- [Android Profile 验证用例](validation-cases.md)
- [私有 Word 归档说明](../../docs/archive/README.md)

原始 V5.0 Word 文档只作为方法论来源保存在仓库外。公开包不包含个人状态、真实面试记录、Notion/Drive/Sheets 链接或页面 ID。
