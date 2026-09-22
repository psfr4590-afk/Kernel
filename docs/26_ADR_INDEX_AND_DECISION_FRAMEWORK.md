# ADR Index and Decision Framework

Architecture decisions must be explicit rather than accidental consequences of a convenient library.

## ADR structure

Every settled decision should record status, date, context, problem, decision, alternatives, rationale, invariant impact, security impact, durability/recovery impact, operational consequences, migration consequences, reversal conditions, verification plan, and related contracts.

## Decision index

- ADR-001 implementation language — ACCEPTED
- ADR-002 storage/database technology — ACCEPTED
- ADR-003 event serialization — ACCEPTED
- ADR-004 cryptographic primitives — ACCEPTED
- ADR-005 identity protocol — ACCEPTED
- ADR-006 key management — ACCEPTED
- ADR-007 policy language — DEFERRED / UNKNOWN
- ADR-008 policy evaluation engine — DEFERRED / UNKNOWN
- ADR-009 authorization representation — ACCEPTED
- ADR-010 delegation semantics — ACCEPTED
- ADR-011 revocation semantics — ACCEPTED
- ADR-012 transaction model — ACCEPTED
- ADR-013 IPC/transport — ACCEPTED
- ADR-014 execution adapter API — ACCEPTED
- ADR-015 idempotency strategy — ACCEPTED
- ADR-016 event ordering — ACCEPTED
- ADR-017 recovery/reconciliation — ACCEPTED
- ADR-018 state materialization — ACCEPTED
- ADR-019 audit integrity — ACCEPTED
- ADR-020 retention/archival — ACCEPTED
- ADR-021 redaction/privacy — ACCEPTED
- ADR-022 administrative/emergency authority — ACCEPTED
- ADR-023 deployment topology — ACCEPTED
- ADR-024 model-provider integration — ACCEPTED
- ADR-025 external-effect trust assumptions — ACCEPTED

## Decision gate

A technology choice becomes architectural when it materially affects invariants, authority, failure semantics, durability, recovery, or security. Such a choice requires an ADR.

## Prohibited shortcuts

A database must not silently define durability semantics. Middleware must not silently define authority. Plugin installation must not imply permission. Queue delivery must not be treated as execution success. Encryption must not be treated as authorization.

## Remaining deliberate unknowns

Policy language and policy evaluation remain intentionally unresolved. They are coupled decisions and will be settled when implementation requirements, policy complexity, or verification needs make the mechanism materially necessary.

The absence of an ADR for those two decisions is therefore deliberate, not an omission.
