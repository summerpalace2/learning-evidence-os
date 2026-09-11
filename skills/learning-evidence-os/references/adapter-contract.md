# Adapter Contract

Adapters connect the Core objects to persistent stores. They do not decide mastery, technical truth, or next-topic choice.

## Required behavior

Every adapter must declare:

- objects it can read and write;
- identity and stable link strategy;
- authorization method and minimum permission;
- idempotency or duplicate-prevention strategy;
- conflict policy;
- failure output;
- local fallback behavior;
- whether the operation is a read, draft, or external mutation.

## Default mapping

| Adapter | Recommended objects |
|---|---|
| Local | Markdown articles, JSON or SQLite state, local source index |
| Notion | Topic State, Knowledge nodes, Session, Evidence, Acceptance board, handoff, navigation |
| Google Drive | Source material, long-form documents, versioned references |
| Google Sheets | Reusable normalized question assets and question maturity |

## Safety rule

An adapter failure cannot become an implicit successful writeback. The agent must report the failed object, preserve a minimal temporary record, and request or wait for authorized retry.
