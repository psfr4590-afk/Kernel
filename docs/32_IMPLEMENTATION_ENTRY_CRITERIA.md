# Implementation Entry Criteria

This is a pre-implementation gate, not a production-readiness claim.

## Required architecture

1. Kernel responsibilities and exclusions are documented.
2. Authority contracts prohibit ambient and self-granted authority.
3. Core object schemas and relationships are defined.
4. Valid and forbidden state transitions are explicit.
5. Failure, denial, partial completion, and UNKNOWN are distinct.
6. Recovery and reconciliation semantics are explicit.
7. Durable evidence and state reconstruction semantics are defined.
8. Security properties have verification methods.
9. Interfaces and bypass rules are defined.
10. Resource allocation and capability semantics are defined.
11. Isolation boundaries for workloads, extensions, models, and adapters are defined.
12. Scheduling semantics cover lifecycle, priority, deadlines, cancellation, concurrency, and resource limits.
13. Memory semantics cover provenance, mutation, retention, and reconstruction.
14. Platform dependencies and enforcement primitives are identified.
15. Configuration and administrative authority are explicit and auditable.
16. Material technology decisions have ADRs.
17. Critical invariants have planned verification with no invented coverage.

## Implementation stop conditions

Work MUST pause for architectural clarification when code requires undocumented authority, undefined transitions, unsupported recovery assumptions, durability semantics that cannot be met, a framework-induced prohibited dependency, a changed security assumption, or an unresolved decision that becomes unavoidable.

## Entry artifact

Before implementation, the repository should contain the architecture map, object schemas, state transitions, authority proofs, traceability matrix, ADR framework, topology, failure taxonomy, recovery matrix, security catalog, scenarios, and this gate.

## Current status

The pre-implementation gate has been superseded by the executable implementation baseline.

Phases 0 through 5 are established, and the first Phase 6 vertical slice is implemented and verified. Phase 7 recovery/resilience work is partially implemented and verified for interruption, persistence failure, uncertainty, duplicate handling, replay, revocation, authorization expiry enforcement, and state rematerialization.

This document remains the entry-gate contract for architectural scope. It must not be read as a claim that every listed domain is implemented. The current implementation boundary and evidence are maintained in `docs/39_IMPLEMENTATION_BASELINE.md` and `docs/25_CONTRACT_TRACEABILITY_MATRIX.md`.

The remaining architecture is implemented only as design where explicitly marked UNKNOWN or deferred. Code must stop for clarification when a remaining implementation would require an unresolved architectural decision or would weaken an established authority, durability, integrity, or recovery invariant.
