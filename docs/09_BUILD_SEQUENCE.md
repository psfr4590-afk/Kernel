# Kernel Construction Sequence

Status: ARCHITECTURAL ROADMAP. No implementation status is implied.

## Phase 0: Foundation
Produce architecture map, terminology, invariants, authority contract, evidence model, and explicit unknowns.

## Phase 1: Identity and Authority
Define principal, identity evidence, context, delegation, authorization, validity, and denial semantics.

Exit evidence: contracts and adversarial tests exist for authority boundaries.

## Phase 2: Governance
Define policy representation, evaluation semantics, policy versioning, conditions, approvals, and decision provenance.

Exit evidence: governance decisions are attributable and distinguishable from execution.

## Phase 3: Event and Durability
Define event schema, causation/correlation, persistence, integrity, ordering, replay, retention, and state materialization.

Exit evidence: restart and persistence-failure tests demonstrate defined guarantees.

## Phase 4: Execution Boundary
Define adapter contract, pre-execution checks, effect semantics, idempotency, partial outcomes, timeouts, and external reconciliation.

Exit evidence: no tested consequential path bypasses authorization.

## Phase 5: Recovery
Define interrupted-operation classification, reconciliation, uncertainty, compensation/rollback where applicable, and recovery authority.

Exit evidence: fault-injection tests cover interruption windows.

## Phase 6: Observation and Audit
Define evidence views, reconstruction, access control, minimization, integrity, and export.

Exit evidence: independent reconstruction can be performed from durable evidence.

## Phase 7: Verification
Build structural, contract, behavioral, adversarial, durability, and regression suites.

Exit evidence: each invariant maps to demonstrated evidence.

## Phase 8: Integration
Connect intelligence adapters, application systems, and external effect mechanisms without weakening the kernel boundary.

Exit evidence: end-to-end traces show proposal through authorization, execution, event, and state.

## Phase 9: Hardening
Perform threat review, failure review, dependency review, data-handling review, recovery review, and adversarial regression.

Exit evidence: unresolved risks are explicitly documented rather than hidden.

## Phase 10: Implementation
Only after the above contracts stabilize should implementation choices be finalized where the contracts require them.

This sequence intentionally prevents technology choices from silently becoming architecture.
