# Kernel Construction Sequence

Status: ARCHITECTURAL ROADMAP. Implementation order aligned with the whole-program engineering protocol.

## Phase 0: Foundation
Establish architecture, terminology, invariants, authority contract, evidence model, and explicit unknowns.

## Phase 1: Authority Contracts
Finalize principal, identity evidence, context, proposal, governance, authorization, validity, denial, and proof obligations.

Exit evidence: contracts and adversarial test definitions exist for authority boundaries.

## Phase 2: Governance and Decision Contracts
Finalize policy representation, evaluation semantics, policy versioning, conditions, approvals, and decision provenance required by the first implementation slice.

Exit evidence: governance decisions are attributable and distinguishable from execution.

## Phase 3: Durability and State Contracts
Finalize event schema, causation/correlation, persistence semantics, integrity requirements, ordering, replay, state materialization, and recovery evidence required by the first implementation slice.

Exit evidence: restart and persistence-failure behavior is defined.

## Phase 4: Execution Boundary
Finalize the effect-boundary contract, pre-execution checks, outcome semantics, idempotency requirements, and adapter boundary required for the first executable effect.

Exit evidence: no designed consequential path bypasses authorization.

## Phase 5: Implementation Entry
Settle only the implementation-blocking ADRs. Establish the repository's executable structure, dependency policy, configuration model, reproducible development/test commands, and initial test harness.

Exit evidence: a minimal executable skeleton exists without weakening the architectural contracts.

## Phase 6: Vertical Slice Implementation
Implement the smallest complete end-to-end path:

request -> identity -> context -> proposal -> governance -> authorization -> execution boundary -> outcome -> event -> state.

Include denial, invalid authorization, scope mismatch, and bypass tests.

Exit evidence: the slice is implemented and its applicable contracts are verified by executable tests.

## Phase 7: Recovery and Resilience
Implement interruption, persistence failure, restart, uncertainty, reconciliation, duplicate handling, and state reconstruction according to the established contracts.

Exit evidence: fault-injection and recovery tests demonstrate the defined guarantees.

## Phase 8: Observation, Administration, and Extensions
Implement governed observation/audit, administrative boundaries, resource controls, scheduling, isolation, IPC, memory, and extension/model interfaces as required by the integrated design.

Exit evidence: each introduced boundary has contract, failure, security, and regression evidence.

## Phase 9: Integration
Connect intelligence providers, application interfaces, external adapters, and other effect mechanisms without weakening the Kernel boundary.

Exit evidence: end-to-end traces demonstrate proposal through authorization, execution, outcome, event, and state.

## Phase 10: Hardening and Final Verification
Perform adversarial review, failure review, dependency review, data-handling review, recovery review, performance evaluation where justified, security regression, documentation verification, and operational verification.

Exit evidence: unresolved risks remain explicit; verified claims are backed by reproducible evidence.

Implementation is therefore not postponed until after hardening. Hardening validates the implemented system against the architecture.
