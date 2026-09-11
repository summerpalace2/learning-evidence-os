# Core Protocol

## 1. Purpose and normative language

This protocol is the reusable core of an evidence-based learning system. It is domain-neutral: Android, algorithms, language learning, certifications, and professional practice can implement it through a Profile.

- **Must** means the task cannot be marked formally complete if the requirement is missing.
- **Should** is the default behavior; deviations need a recorded reason.
- **May** is optional and depends on scope, learner needs, and available tools.

The system optimizes for real understanding, assessment value, open-world coverage, personal adaptation, and persistence integrity.

## 2. Objects and state boundaries

### 2.1 Knowledge hierarchy

A Profile may define a hierarchy, but the default is:

1. Domain: a long-term area such as Android or English.
2. Topic: a boundary-stable unit that can have a complete article and multiple learning rounds.
3. Checkpoint: an independently testable mechanism, concept, boundary, API, scenario, or question.

Topics are not calendar days. Checkpoints are not mechanical slices of an article.

### 2.2 Four persistent boundaries

| Object | Contains | Must not overwrite |
|---|---|---|
| Knowledge | Technical truth, boundaries, sources, versions, article locations | Learner evidence |
| State | Current topic status, current task, long-term mastery, review flags | Raw history |
| Evidence | Original answers, prompts, feedback, assessments, retests | Canonical answer |
| Presentation | Dashboards, navigation, summaries, current task cards | The durable objects above |

### 2.3 Canonical object vocabulary

The Core uses stable object names even when an Adapter maps them to different pages, files, rows, or database records.

| Object | Minimum responsibility |
|---|---|
| Topic | Boundary-stable unit that can have an article and multiple rounds |
| Node | Knowledge-map concept, mechanism, dependency, or independently testable checkpoint |
| Article | Complete understanding map with sources, versions, causal chain, and acceptance entry |
| Question | Normalized reusable question, kept separate from learner performance |
| Answer | Canonical short, complete, and deep explanation for a Question |
| Session | One learning, review, retest, interview, or coverage-audit activity |
| Evidence | Learner raw answer, prompt level, mistakes, R, and follow-up result |
| Topic State | Current accumulated L/R/C, lifecycle, review flags, and next handoff |
| Presentation | Control center, board, dashboard, and navigation views over the durable objects |

Adapters may combine or split storage records, but they must preserve these semantic boundaries and stable links.

### 2.4 Independent dimensions

| Dimension | Meaning |
|---|---|
| L | Long-term learner mastery. Default L0–L5 moves from uncontacted to transferable understanding. |
| R | Performance in one answer or assessment. Default R0–R5 moves from unable to transfer. |
| C | Confidence that the scoped knowledge map has adequate source, structure, question, and version coverage. Default C0–C4. |
| Content state | Index only, content skeleton, learning note, canonical answer. |
| Answer state | Pending validation, partially validated, validated, learner-ready canonical answer. |

An AI answer is a Knowledge asset. It is never learner Evidence by itself.

## 3. Loop A: Coverage Discovery

Use this loop to answer: **what may the current map be missing?**

1. Scope the audit. Do not expand indefinitely.
2. Create an independent candidate map before trusting existing nodes.
3. Diff sources, current map, articles, question bank, interview evidence, and version changes.
4. Critique omissions, shallow explanations, incorrect boundaries, duplicate nodes, and stale claims.
5. Apply Candidate Gate: stable boundary, reuse value, training value, and relevance.
6. Apply Placement Gate. Classify each increment as one or more of:
   - **A**: a new independent knowledge node;
   - **B**: a checkpoint or depth extension of an existing node;
   - **C**: a reusable question or question variant;
   - **D**: a cross-topic bridge or dependency;
   - **E**: a rule, behavior, or version boundary;
   - **F**: a source or version conflict;
   - **G**: a duplicate, low-value, or short-lived detail.
7. Write back only the minimum candidate data needed, then re-check the scoped structure and question coverage.

Discovery output changes C and candidate placement. It does not prove user mastery.

## 4. Loop B: Learning Verification

Use this loop to answer: **what can the learner now do independently?**

1. Restore current protocol, profile, current board, handoff, Topic State, article location, recent evidence, and review flags.
2. Select one Learning Unit using L, R, C, dependencies, learning value, user time, and unresolved boundaries.
3. Build recognition with sources, examples, causal explanation, and the Profile-specific technical chain.
4. Verify live with one question at a time. Follow the answer into process, cause, boundary, counterexample, trade-off, and transfer when appropriate.
5. Grade evidence: independent answer, light prompt, strong prompt, answer repetition, or recognition only.
6. Write back in the required order.

Only independent explanation plus boundary or transfer evidence can normally justify advanced mastery.

### Learning Unit contract

Every formal unit must state:

- target topic or scoped boundary;
- question to resolve;
- source set and version;
- expected depth;
- acceptance method;
- writeback targets;
- next handoff.

## 5. Article production contract

A formal learning article is a complete understanding map, not a list of tips. It must include technical truth, causal chain, localized learner annotations, and interview or assessment expression.

1. Freeze scope, goals, sources, versions, and exclusions.
2. Define knowledge boundaries, dependencies, confusions, and the final question the article should answer.
3. Normalize technical truth across authoritative sources and record conflicts.
4. Build the complete chain: background, concepts, dependencies, internal mechanism, execution flow, engineering mapping, boundaries, mistakes, expression, acceptance.
5. Add learner-specific annotations beside the relevant section only. Never upgrade mastery by annotation.
6. Produce canonical answers and follow-up prompts for high-value checkpoints.
7. Render and inspect code, diagrams, links, and navigation.
8. Publish only when scope, causal chain, boundaries, sources, answer consistency, learner evidence labeling, and bidirectional navigation all pass.

## 6. Canonical answer contract

When the agent provides a formal answer suitable for an interview, exam, review, or professional explanation, preserve it before assessing the learner.

Each answer asset should include:

- original and normalized question;
- a short direct answer;
- a 60–90 second complete answer;
- deeper mechanism or engineering expansion;
- key terms and causal chain;
- boundaries, misconceptions, counterexamples, and trade-offs;
- likely follow-ups;
- sources, version, validation state;
- linked Topic, Checkpoint, article location, and whether the learner independently reproduced it.

## 7. Assessment and interview contract

Keep the normalized reusable question separate from a learner's historical performance.

The generic processing pipeline is:

~~~text
Input → Parse → Evaluate → Standardize → Persist → Next Loop
~~~

An assessment board is created only for a complete Topic, a scoped cross-checkpoint assessment, or a formal retest. It accumulates rounds rather than creating a new top-level board for each small correction.

Each round records scope, sources, questions, learner answer summaries, independence, R, mistakes, corrections, article locations, retest tasks, overall conclusion, linked Session, Evidence, and next handoff.

## 8. Writeback and closure

Write in this order:

1. Freeze the factual record: question, raw answer, sources, prompts, time, and completion.
2. Save or update canonical answers.
3. Save the Learning Session.
4. Save Evaluation Evidence.
5. Update the minimum Knowledge nodes and article locations permitted by the evidence gate.
6. Update Topic State: L, R summary, C, lifecycle, unresolved boundaries, review items, and next candidate.
7. Update the control view and current handoff.
8. Admit only reusable, de-personalized questions to the shared question bank.
9. Repair node-to-article and article-to-node navigation.
10. Run Final Sync by re-reading the current control state and handoff.

Do not mark a unit complete if Final Sync, required evidence, or next action is missing.

## 9. Navigation and versioning

Every article-backed node should store an article root, unique section locator, article version, canonical-answer location, linked evidence, and linked assessment round. Article changes must repair both directions in the same change.

One project version has one current protocol. Historical protocols are evidence and migration references, not stacked runtime rules.

## 10. Failure and privacy rules

- If persistent stores are unavailable, label judgments as temporary and preserve a minimal session record for later writeback.
- If sources conflict, store the conflict, version, adopted conclusion, and reason.
- If a fact is uncertain, leave it uncertain; do not invent status or mastery.
- Public repositories contain only generic contracts, sanitized templates, public sources, and sample data.
- Credentials, private URLs, live learner state, and real interview transcripts remain outside version control.
