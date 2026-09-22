# Kernel Execution and Recovery Boundary

Status: FOUNDATIONAL DESIGN. Intended contract, not implemented behavior.

## 1. Purpose

The execution boundary is where authorized intent can become a consequential effect. It is therefore the point at which authority must be enforced rather than merely described.

## 2. Execution Contract

An execution adapter MUST receive enough information to establish:

- principal
- authorized operation
- target/scope
- conditions
- authorization reference
- operation identity/idempotency information
- required context

It MUST NOT infer broader authority from the proposal.

## 3. Pre-Execution Check

Immediately before consequential execution, the boundary SHOULD verify authorization applicability where the operation's threat model requires it.

At minimum, it must reject missing, invalid, expired, out-of-scope, or otherwise unusable authorization.

## 4. Effect Boundary

The adapter is responsible for producing an actual effect and returning an outcome.

The adapter MUST NOT convert a denied decision into execution.

The adapter MUST NOT broaden an authorized scope.

## 5. Outcome States

The architecture must distinguish at least:

- not attempted
- blocked before execution
- attempted
- succeeded
- failed
- partially completed
- outcome unknown

"Unknown" is a valid state, not a bug to hide.

## 6. Idempotency

Operations that can be retried MUST define whether repeated execution is safe.

Where possible, an operation identifier SHOULD support deduplication.

Idempotency cannot be assumed globally because different effects have different semantics.

## 7. Partial Effects

If an operation can partially succeed, the outcome model MUST represent partial completion and define reconciliation.

## 8. Process Failure

If the process terminates during execution, recovery MUST NOT assume either success or failure without evidence.

## 9. External Systems

External effects may have weaker transactional guarantees than local state.

The boundary therefore needs explicit reconciliation semantics for:

- timeout
- network loss
- remote acceptance without response
- remote rejection without local confirmation
- duplicate submission
- delayed response

## 10. Recovery

Recovery MUST:

1. load durable evidence;
2. identify interrupted operations;
3. classify known/unknown outcomes;
4. apply operation-specific reconciliation;
5. preserve uncertainty where evidence is insufficient;
6. emit recovery/reconciliation evidence;
7. update state only according to defined authority rules.

## 11. Recovery Must Not Escalate

Recovery routines MUST NOT acquire broader authority merely because the system is in an exceptional state.

## 12. Administrative Paths

Debug, maintenance, repair, bootstrap, migration, and emergency mechanisms require explicit boundaries, attribution, logging, and scope.

"Internal" is not a substitute for authorization.

## 13. Open Decisions

Adapter API, sandboxing, process isolation, timeout semantics, transaction strategy, rollback, compensation, distributed execution, and external-effect reconciliation remain unresolved.
