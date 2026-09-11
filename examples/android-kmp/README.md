# Android KMP Example

This example shows how the generic system becomes an Android learning unit without publishing anyone's personal status.

## Topic

Kotlin Multiplatform compilation model and project structure.

## Learning Unit

| Field | Example |
|---|---|
| Boundary | Module, Target, Source Set, Compilation and iOS Target hierarchy |
| Core question | Why can one Kotlin codebase produce Android JVM bytecode and iOS Native binaries? |
| Sources | Kotlin Multiplatform official documentation and project build files |
| Verification | Explain the Target to Compilation relationship and reason about commonMain visibility |
| Canonical answer | Explain Source Set coverage and platform API boundaries |
| Writeback | Article, one Topic State, evidence for each answer, next handoff |

## Minimal source example

~~~kotlin
// commonMain
expect fun platformName(): String

// androidMain
actual fun platformName(): String = "Android"

// iosMain
actual fun platformName(): String = "iOS"
~~~

The learner should explain that commonMain is compiled as part of each applicable target compilation; it is not a standalone JVM module that can freely import Android or JDK-only APIs.

## Example acceptance prompt

Why does placing android.util.Log in commonMain fail? Explain from Source Set coverage, Target, Compilation, and backend constraints rather than merely saying “commonMain cannot call Android APIs.”
