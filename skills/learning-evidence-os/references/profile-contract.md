# Domain Profile Contract

A Profile turns the generic Learning Evidence OS into a useful domain implementation without changing Core invariants.

## Required profile content

1. **Scope**: what is included and explicitly excluded.
2. **Knowledge hierarchy**: domains, topics, checkpoints, dependencies, and confusing neighbors.
3. **Truth policy**: authoritative source order, version handling, and conflict resolution.
4. **Teaching routes**: what a complete causal chain looks like for the domain.
5. **Assessment rubric**: how L and R are observed in this domain.
6. **Answer format**: interview, exam, oral, code-review, or practical demonstration expectations.
7. **Question-bank policy**: what counts as reusable and how duplicates are merged.
8. **Connector mapping**: optional field mappings, navigation policy, and state-recovery source.
9. **Privacy boundary**: which data stays private and which examples are safe to publish.

## What a Profile must not do

- Override the separation of Knowledge, State, Evidence, and Presentation.
- Promote mastery from article completion or an AI answer.
- Require a specific vendor connector when a local fallback is possible.
- Treat one learner's past mistake as universal evidence.

The repository's first concrete implementation is the optional Android Profile at `profiles/android/README.md`. A standalone Skill installation may not include that repository path; if it is absent, do not pretend that Android-specific technical truth has been loaded.
