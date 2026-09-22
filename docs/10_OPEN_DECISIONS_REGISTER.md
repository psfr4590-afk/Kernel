# Kernel Open Decisions Register

Status: ACTIVE DESIGN REGISTER.

This file prevents unresolved design choices from being accidentally treated as settled architecture.

| ID | Decision | Status |
|---|---|---|
| OD-001 | Implementation language | ACCEPTED: Python (ADR-001) |
| OD-002 | Database/storage engine | ACCEPTED: SQLite (ADR-002) |
| OD-003 | Event serialization | ACCEPTED: Canonical JSON with strict schema/immutability contract (ADR-003) |
| OD-004 | Cryptographic primitives | ACCEPTED: AES-256 via `cryptography`, authenticated construction required (ADR-004) |
| OD-005 | Identity protocol | ACCEPTED: Cryptographic identity with OS/process binding for local attribution (ADR-005) |
| OD-006 | Credential/key management | ACCEPTED: Encrypted local key store using AES-256 (ADR-006) |
| OD-007 | Policy language | UNKNOWN: Deliberately deferred until implementation requirements make the choice necessary |
| OD-008 | Policy evaluation engine | UNKNOWN: Deliberately deferred with policy language |
| OD-009 | Authorization token format | ACCEPTED: Short-lived, explicitly scoped authorization bound to identity with expiration (ADR-009) |
| OD-010 | Delegation semantics | ACCEPTED: Restricted, bounded, attributable delegation (ADR-010) |
| OD-011 | Revocation semantics | ACCEPTED: Expiration plus immediate durable revocation (ADR-011) |
| OD-012 | Transaction model | ACCEPTED: Atomic event/state commit boundary where supported, with event history authoritative (ADR-012) |
| OD-013 | IPC/transport | ACCEPTED: Structured transport semantics with pluggable transport; direct calls initially (ADR-013) |
| OD-014 | Execution adapter API | ACCEPTED: Structured operation adapter contract (ADR-014) |
| OD-015 | Idempotency strategy | ACCEPTED: Composite operation identity, authorization-bound execution identity, and durable uniqueness (ADR-015) |
| OD-016 | Event ordering guarantees | ACCEPTED: Global durable event sequence plus causation/correlation metadata (ADR-016) |
| OD-017 | Recovery/reconciliation model | ACCEPTED: Evidence-first recovery with replay, reconciliation, and governed resolution (ADR-017) |
| OD-018 | State materialization model | ACCEPTED: Snapshots plus event replay (ADR-018) |
| OD-019 | Audit integrity mechanism | ACCEPTED: Cryptographic hash of canonical protected representation (ADR-019) |
| OD-020 | Retention/archival policy | ACCEPTED: Retention classes with periodic lossless compression (ADR-020) |
| OD-021 | Redaction/privacy model | ACCEPTED: Strictly controlled sensitive storage boundary (ADR-021) |
| OD-022 | Administrative/emergency authority | ACCEPTED: Scoped, expiring break-glass authority with durable evidence (ADR-022) |
| OD-023 | Deployment topology | ACCEPTED: Single-process/local-first initially with topology-independent contracts (ADR-023) |
| OD-024 | Model-provider integration boundary | ACCEPTED: Multiple providers behind explicit intelligence boundaries (ADR-024) |
| OD-025 | External-effect trust assumptions | ACCEPTED: Authenticate external systems without granting inherent trust (ADR-025) |

## Decision Rule

No decision should be marked settled merely because an implementation happened to choose an option.

A decision becomes architectural when its rationale, alternatives, consequences, and relationship to the invariants are documented.

Each settled decision should receive an ADR or equivalent durable record.

## Remaining Deliberate Unknowns

Only the policy representation and policy evaluation mechanism remain intentionally unresolved:

- OD-007 Policy language
- OD-008 Policy evaluation engine

These are coupled decisions and will be resolved when implementation requirements, policy complexity, or verification needs make the choice materially necessary. Their current UNKNOWN status is intentional and must not be treated as an implementation omission.
