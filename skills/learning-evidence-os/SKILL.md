---
name: learning-evidence-os
description: Run evidence-based personalized learning systems across technical, interview, language, or professional domains. Use when a user asks to start or continue structured learning, create a learning article, assess understanding, conduct a mock interview, audit knowledge coverage, or write back learning evidence. Do not use for a one-off explanation unless the user asks to incorporate it into a learning system.
---

# Learning Evidence OS

Operate a learning system in which technical knowledge, learner state, answer assets, historical evidence, and presentation views are separate objects. The objective is durable understanding, not completion metrics or a single correct response.

## Non-negotiable invariants

1. Do not treat reading, an AI-generated answer, or one correct response as mastery.
2. Keep Knowledge, State, Evidence, and Presentation separate.
3. Keep long-term mastery L, one-round performance R, and coverage confidence C separate.
4. Capture a canonical answer before evaluating whether the learner can reproduce it.
5. Recover formal state before making a personalized next-topic or mastery decision.
6. Ask one question at a time during live acceptance unless the user explicitly requests a worksheet.
7. Preserve raw answers and evidence. Never rewrite history into an ideal answer.
8. External stores are optional adapters. Do not claim persistence unless the write succeeds.
9. Use the domain Profile to determine technical truth, terminology, source policy, and assessment detail.
10. Do not convert a learner-specific habit, private schema, or past failure into a universal rule.

## First-run Bootstrap

Do not assume that the user has Notion, Google, a pre-existing Profile, or a writable external store. On the first persistent learning request, run a small setup conversation before planning:

1. Ask for the learning domain/Profile, preferred mode (`study`, `interview`, `exam`, or `practice`), source locations, and available storage/connectors.
2. Detect which requested capabilities are actually available in the current environment. Never treat an Adapter README, a user claim, or a remembered connection as a successful capability check.
3. Default to the implemented Local JSON Adapter when no verified external Adapter is available.
4. Save the setup result outside the public repository. The local reference implementation is `python -m runtime.local.cli init`; it writes `.learning-evidence/config.json`.
5. Show the user a capability summary. Mark unavailable persistence as `planned_not_implemented`, `temporary`, or `unpersisted`; do not claim writeback or Final Sync success.

If the skill is installed as a standalone folder and the repository runtime is not present, it can still guide a temporary conversation, but it must explicitly say that no persistent writeback was performed. Repository-relative Profiles and Schemas are optional resources, not hidden runtime dependencies.

## Route the request

Read [Core Protocol](references/core-protocol.md) for every in-system task. Then load only the relevant additional reference. Use the active Profile for domain truth and the active Adapter for persistence; neither may override the Core invariants.

| User intent | Required route |
|---|---|
| Start, continue, resume, what next | Core Protocol sections 2, 4, 8; recover current state before planning |
| Teach or explain as part of the system | Core Protocol sections 4, 5, 6; use the active Profile |
| Produce a complete learning article | Core Protocol section 5; use Article and Canonical Answer templates |
| Test, retest, voice acceptance, mock interview | Core Protocol sections 4, 6, 7; record answer evidence before updating State |
| Coverage audit or map-gap discovery | Core Protocol section 3; classify increments before creating nodes |
| Use interview mode | Core Protocol sections 6, 7, 8; preserve short/complete answers separately from learner performance |
| Create or update a domain | [Profile Contract](references/profile-contract.md) |
| Connect Notion, Drive, Sheets, or local storage | [Adapter Contract](references/adapter-contract.md) |

## Runtime sequence

1. Identify the domain Profile and whether the request is a one-off or a persistent learning task.
2. If this is the first persistent task, complete Bootstrap and capability checks before making a plan.
3. Read the current protocol and the minimum state, handoff, topic, article location, and recent evidence needed for the decision.
4. If state or persistence is unavailable, clearly mark the decision as temporary and do not manufacture long-term status.
5. Run a scoped Coverage Discovery pass when a new source, new question, contradiction, or obvious gap affects selection.
6. Build one Learning Unit with an explicit boundary, sources, verification method, writeback targets, and next handoff.
7. Teach using the complete causal chain required by the Profile. Preserve the standard answer as a separate asset before evaluating the learner.
8. Verify live. Ask one question at a time unless a worksheet was requested; adapt depth to the learner answer; capture independence, prompts, mistakes, and follow-up result.
9. Keep L, R, C, content state, answer state, and evidence strength separate when summarizing the result.
10. Write back in the prescribed order. Perform Final Sync before formally closing a unit or topic.

## External mutation boundary

Reading connected sources is allowed when available and relevant. Creating or updating Notion pages, Google files, sheets, repositories, or other external records requires task-specific user authorization. If authorization or a connector is unavailable, keep a temporary session record marked `temporary` or `unpersisted`, report the affected object, and never claim that the writeback or Final Sync succeeded.

## Completion gate

Before saying that a unit or topic is complete, verify:

- the factual record and raw answer are preserved;
- the canonical answer exists before learner evaluation is closed;
- the correct R and evidence strength are recorded without silently raising L;
- required Knowledge, State, Evidence, and Presentation links are updated;
- navigation and version locators still work in both directions;
- the next handoff is executable; and
- Final Sync re-read the current state and recorded any failed persistence.

If any item is missing, report the work as partial or in review and leave the next action visible.

## References

- [Core Protocol](references/core-protocol.md): universal operating contract.
- [Profile Contract](references/profile-contract.md): how to add Android, language, algorithms, or other domain implementations.
- [Adapter Contract](references/adapter-contract.md): storage boundaries and safe failure behavior.
- [Quality Gates](references/quality-gates.md): protocol review before formal closure.
- Android Profile（仓库内可选资源：`profiles/android/README.md`）：具体领域实现。
- Object Model（仓库内可选资源：`schemas/object-model.json`）：对象和关系词汇。
- [Runtime Bootstrap](references/runtime-bootstrap.md)：首次配置、能力检查和本地运行规则。
