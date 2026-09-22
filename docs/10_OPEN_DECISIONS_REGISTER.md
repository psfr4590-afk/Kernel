# Kernel Open Decisions Register

Status: ACTIVE DESIGN REGISTER.

This file prevents unresolved design choices from being accidentally treated as settled architecture.

| ID | Decision | Status |
|---|---|---|
| OD-001 | Implementation language | ACCEPTED: Python (ADR-001) |
| OD-002 | Database/storage engine | ACCEPTED: SQLite (ADR-002) |
| OD-003 | Event serialization | ACCEPTED: Canonical JSON with strict schema/immutability contract (ADR-003) |
| OD-004 | Cryptographic primitives | ACCEPTED: AES-256 via `cryptography`, authenticated construction required (ADR-004) |
| OD-005 | Identity protocol | UNKNOWN |
| OD-006 | Credential/key management | ACCEPTED: Encrypted local key store using AES-256 (ADR-006) |
| OD-007 | Policy language | UNKNOWN |
| OD-008 | Policy evaluation engine | UNKNOWN |
| OD-009 | Authorization token format | ACCEPTED: Short-lived, explicitly scoped authorization bound to identity with expiration (ADR-009) |
| OD-010 | Delegation semantics | UNKNOWN |
| OD-011 | Revocation semantics | UNKNOWN |
| OD-012 | Transaction model | UNKNOWN |
| OD-013 | IPC/transport | UNKNOWN |
| OD-014 | Execution adapter API | UNKNOWN |
| OD-015 | Idempotency strategy | UNKNOWN |
| OD-016 | Event ordering guarantees | UNKNOWN |
| OD-017 | Recovery/reconciliation model | UNKNOWN |
| OD-018 | State materialization model | ACCEPTED: Snapshots plus event replay (ADR-018) |
| OD-019 | Audit integrity mechanism | ACCEPTED: Cryptographic hash of canonical protected representation (ADR-019) |
| OD-020 | Retention/archival policy | ACCEPTED: Retention classes with periodic lossless compression (ADR-020) |
| OD-021 | Redaction/privacy model | ACCEPTED: Strictly controlled sensitive storage boundary (ADR-021) |
| OD-022 | Administrative/emergency authority | UNKNOWN |
| OD-023 | Deployment topology | UNKNOWN |
| OD-024 | Model-provider integration boundary | ACCEPTED: Multiple providers behind explicit intelligence boundaries (ADR-024) |
| OD-025 | External-effect trust assumptions | ACCEPTED: Authenticate external systems without granting inherent trust (ADR-025) |

## Decision Rule

No decision should be marked settled merely because an implementation happened to choose an option.

A decision becomes architectural when its rationale, alternatives, consequences, and relationship to the invariants are documented.

Each settled decision should receive an ADR or equivalent durable record.
