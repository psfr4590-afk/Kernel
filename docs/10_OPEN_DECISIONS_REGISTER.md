# Kernel Open Decisions Register

Status: ACTIVE DESIGN REGISTER.

This file prevents unresolved design choices from being accidentally treated as settled architecture.

| ID | Decision | Status |
|---|---|---|
| OD-001 | Implementation language | UNKNOWN |
| OD-002 | Database/storage engine | UNKNOWN |
| OD-003 | Event serialization | UNKNOWN |
| OD-004 | Cryptographic primitives | UNKNOWN |
| OD-005 | Identity protocol | UNKNOWN |
| OD-006 | Credential/key management | UNKNOWN |
| OD-007 | Policy language | UNKNOWN |
| OD-008 | Policy evaluation engine | UNKNOWN |
| OD-009 | Authorization token format | UNKNOWN |
| OD-010 | Delegation semantics | UNKNOWN |
| OD-011 | Revocation semantics | UNKNOWN |
| OD-012 | Transaction model | UNKNOWN |
| OD-013 | IPC/transport | UNKNOWN |
| OD-014 | Execution adapter API | UNKNOWN |
| OD-015 | Idempotency strategy | UNKNOWN |
| OD-016 | Event ordering guarantees | UNKNOWN |
| OD-017 | Recovery/reconciliation model | UNKNOWN |
| OD-018 | State materialization model | UNKNOWN |
| OD-019 | Audit integrity mechanism | UNKNOWN |
| OD-020 | Retention/archival policy | UNKNOWN |
| OD-021 | Redaction/privacy model | UNKNOWN |
| OD-022 | Administrative/emergency authority | UNKNOWN |
| OD-023 | Deployment topology | UNKNOWN |
| OD-024 | Model-provider integration boundary | UNKNOWN |
| OD-025 | External-effect trust assumptions | UNKNOWN |

## Decision Rule

No decision should be marked settled merely because an implementation happened to choose an option.

A decision becomes architectural when its rationale, alternatives, consequences, and relationship to the invariants are documented.

Each settled decision should receive an ADR or equivalent durable record.
