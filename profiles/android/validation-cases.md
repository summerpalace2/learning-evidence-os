# Android Profile Validation Cases

These cases are intentionally small and de-personalized. They verify the Core behavior with the Kotlin Multiplatform compilation model and do not publish any learner history.

Use the fixture in [examples/android-kmp/validation-fixture.json](../../examples/android-kmp/validation-fixture.json) as the expected object shape. A real Adapter may store the same objects as Markdown files, JSON/SQLite rows, Notion pages, or another backend.

## Case 1: Double Loop keeps C, L, and R separate

**Setup:** A Coverage Discovery pass finds that the current KMP map does not explain the relationship between Target, Compilation, Source Set, and backend constraints. The learner then answers the `commonMain` API-boundary question.

**Expected result:**

- the discovery result is classified as `A` or `E` and changes coverage state C;
- the learner answer creates Evidence with an independent `R` value;
- one answer does not silently raise long-term mastery L;
- a discovered map gap can trigger the next unit, but it does not become proof of mastery.

## Case 2: Canonical Answer is saved before evaluation

**Setup:** The system creates a normalized question about why `android.util.Log` is not available in `commonMain`, then produces a short and complete canonical answer.

**Expected result:**

- the Answer exists before the Evidence record is closed;
- the Answer contains the causal chain: Source Set coverage → Target → Compilation → platform API boundary;
- the learner's raw answer remains separate, even when it is incomplete or incorrect.

## Case 3: Acceptance Board accumulates rounds

**Setup:** Round 1 tests Source Set visibility. Round 2 tests the Target/Compilation relationship. Round 3 tests transfer to a new project structure.

**Expected result:**

- all rounds remain linked to one Topic;
- each round keeps its own questions, raw-answer summaries, prompt levels, R values, corrections, and retest items;
- the latest round does not overwrite earlier evidence;
- Topic Closeout remains open until the required checkpoints and Final Sync pass.

## Case 4: Navigation is bidirectional and versioned

**Setup:** The Topic points to an Article section explaining Source Set coverage. The Article section points back to the Node, Answer, and Evidence.

**Expected result:**

- the link stores an article version and precise locator;
- Node → Article and Article → Node both resolve to the intended section;
- if the article moves, both directions are repaired in the same writeback;
- stale links are reported as an integrity failure, not silently ignored.

## Case 5: Final Sync leaves one executable next step

**Setup:** The session finishes with a correct explanation of the compilation relationship but an unresolved platform-boundary edge case.

**Expected result:**

- Topic State retains the unresolved boundary;
- the control view shows the current L/R/C summary without inflating L;
- handoff contains one concrete retest or next Learning Unit;
- the session is `partial` or `in_review` when required persistence is incomplete.

## Case 6: Adapter failure never becomes fake success

**Setup:** The external Adapter fails while updating Topic State after Evidence has been captured locally.

**Expected result:**

- the local temporary record preserves the facts, Answer, Session, and Evidence;
- the failed object and missing write are reported explicitly;
- no `completed` status or successful Final Sync is claimed;
- a later authorized retry can replay the idempotent write without duplicating Evidence.
