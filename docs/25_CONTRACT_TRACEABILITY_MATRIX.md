# Contract Traceability Matrix

## Purpose

This matrix connects architecture requirements to future implementation and verification evidence. UNKNOWN is used deliberately where evidence does not yet exist.

| Requirement | Source | Implementation target | Verification | Status |
|---|---|---|---|---|
| No ambient authority | K-INV-001 | Authority boundary | bypass tests | UNKNOWN |
| Proposal != permission | K-INV-002 | Proposal/Governance | contract tests | UNKNOWN |
| Explicit authorization | K-INV-003 | Authorization/effect boundary | proof tests | UNKNOWN |
| Identity independence | K-INV-004 | Identity subsystem | forged identity tests | UNKNOWN |
| Capability != permission | K-INV-005 | Resource/capability | abuse tests | UNKNOWN |
| Governance != execution | K-INV-006 | Domain interfaces | integration tests | UNKNOWN |
| Event lineage | K-INV-007 | Event store | reconstruction tests | UNKNOWN |
| State != history | K-INV-008 | Materializer | rebuild tests | UNKNOWN |
| Failure is information | K-INV-009 | Outcome model | fault injection | UNKNOWN |
| Audit is evidence | K-INV-010 | Audit subsystem | evidence tests | UNKNOWN |
| Reconstruction | K-INV-011 | Recovery/storage | recovery tests | UNKNOWN |
| Representation independence | K-INV-012 | Boundaries | mutation tests | UNKNOWN |
| Fail closed | K-INV-013 | Effect boundary | adversarial tests | UNKNOWN |
| Explicit atomicity | K-INV-014 | Transaction layer | crash tests | UNKNOWN |
| Duplicate handling | K-INV-015 | Intake/execution | replay tests | UNKNOWN |
| No silent escalation | K-INV-016 | Authority transitions | privilege tests | UNKNOWN |
| Policy versioning | K-INV-017 | Policy store | historical tests | UNKNOWN |
| Evidence integrity | K-INV-018 | Event/audit | tamper tests | UNKNOWN |
| Observation non-authority | K-INV-019 | Observation | mutation tests | UNKNOWN |
| Recovery no invented success | K-INV-020 | Recovery | uncertainty tests | UNKNOWN |

## Domain traceability

Platform, resources, isolation, execution, scheduling, IPC/eventing, state, memory, persistence, security, identity, governance, authorization, intelligence boundary, interfaces, observation, lifecycle, and configuration each require their own implementation evidence and verification suite.

## Status vocabulary

- UNKNOWN: not established.
- DESIGNED: contract exists.
- IMPLEMENTED: code exists and satisfies the defined contract.
- VERIFIED: implementation passed defined verification.
- REGRESSED: previously verified behavior no longer satisfies the contract.

The Kernel architecture is currently DESIGNED, not IMPLEMENTED.
