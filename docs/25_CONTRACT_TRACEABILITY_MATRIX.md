# Contract Traceability Matrix

## Purpose

This matrix connects architecture requirements to implementation and verification evidence. UNKNOWN is used deliberately where evidence does not yet exist.

| Requirement | Source | Implementation target | Verification | Status |
|---|---|---|---|---|
| No ambient authority | K-INV-001 | Authority boundary | bypass tests | VERIFIED for first consequential slice |
| Proposal != permission | K-INV-002 | Proposal/Governance | contract tests | VERIFIED for first consequential slice |
| Explicit authorization | K-INV-003 | Authorization/effect boundary | proof tests | VERIFIED for first consequential slice |
| Identity independence | K-INV-004 | Identity subsystem | forged identity tests | VERIFIED for implemented identity boundary |
| Capability != permission | K-INV-005 | Resource/capability | abuse tests | VERIFIED for filesystem slice |
| Governance != execution | K-INV-006 | Domain interfaces | integration tests | VERIFIED for current execution boundary |
| Event lineage | K-INV-007 | Event store | reconstruction tests | VERIFIED for current event model |
| State != history | K-INV-008 | Materializer | rebuild tests | VERIFIED for current state rematerialization |
| Failure is information | K-INV-009 | Outcome model | fault injection | VERIFIED for current failure/recovery paths |
| Audit is evidence | K-INV-010 | Audit subsystem | evidence tests | VERIFIED for current event evidence/integrity |
| Reconstruction | K-INV-011 | Recovery/storage | recovery tests | VERIFIED for current replay/rematerialization paths |
| Representation independence | K-INV-012 | Boundaries | mutation tests | VERIFIED for canonical parameter binding in current slice |
| Fail closed | K-INV-013 | Effect boundary | adversarial tests | VERIFIED for current authorization/execution boundary |
| Explicit atomicity | K-INV-014 | Transaction layer | crash tests | VERIFIED for current SQLite event/state and authorization issuance boundaries |
| Duplicate handling | K-INV-015 | Intake/execution | replay tests | VERIFIED for current durable operation claims |
| No silent escalation | K-INV-016 | Authority transitions | privilege tests | VERIFIED for current authorization boundary |
| Policy versioning | K-INV-017 | Policy store | historical tests | UNKNOWN, policy storage/evaluator deferred |
| Evidence integrity | K-INV-018 | Event/audit | tamper tests | VERIFIED for current event integrity model |
| Observation non-authority | K-INV-019 | Observation | mutation tests | UNKNOWN, observation/admin interface not yet implemented |
| Recovery no invented success | K-INV-020 | Recovery | uncertainty tests | VERIFIED for current recovery model |

## Domain traceability

Platform, resources, isolation, execution, scheduling, IPC/eventing, state, memory, persistence, security, identity, governance, authorization, intelligence boundary, interfaces, observation, lifecycle, and configuration each require their own implementation evidence and verification suite.

The statuses above apply only to the current implemented/verified scope. They do not imply that the entire eventual Kernel satisfies the invariant across future or unimplemented domains.

## Status vocabulary

- UNKNOWN: not established.
- DESIGNED: contract exists.
- IMPLEMENTED: code exists and satisfies the defined contract.
- VERIFIED: implementation passed defined verification.
- REGRESSED: previously verified behavior no longer satisfies the contract.

The Kernel is now IMPLEMENTED and VERIFIED for the documented first vertical slice, while the broader architecture remains partially implemented and contains explicit deferred boundaries.
