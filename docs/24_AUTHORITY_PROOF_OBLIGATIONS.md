# Authority Proof Obligations

## Purpose

The Kernel must make consequential effects depend on a demonstrable chain of authority and evidence.

## Canonical proof chain

Principal -> Request -> Proposal -> Context -> PolicyEvaluation -> Authorization -> Execution validation -> Effect -> Outcome -> Event -> State.

## Obligations

### P-001 Attribution
Every consequential effect MUST be attributable to a validated Principal.

### P-002 Proposal integrity
The executed operation MUST correspond to the authorized proposal or a formally defined normalized representation. Changed parameters require renewed validation.

### P-003 Governance provenance
Authorization MUST identify the policy and evaluation basis that permitted it.

### P-004 Scope confinement
Execution MUST remain inside operation, resource, parameter, time, quantity, and delegation constraints.

### P-005 Capability separation
Technical availability MUST NOT satisfy an authority requirement.

### P-006 Freshness
Authorization MUST be valid at the consequential execution boundary, including required revocation checks.

### P-007 Non-forgeability
Model output, callers, adapters, storage records, or transport messages MUST NOT manufacture valid authority by producing authority-shaped data.

### P-008 Effect binding
The actual effect MUST be bound to the validated operation and resource.

### P-009 Outcome integrity
Success, failure, acknowledgement, timeout, and unknown status MUST remain distinguishable.

### P-010 Durable evidence
Consequential operations MUST leave durable evidence according to the durability contract.

### P-011 Recovery honesty
Recovery MUST preserve uncertainty where evidence cannot establish whether an external effect occurred.

### P-012 Administrative authority
Administrative and emergency operations MUST have explicit, attributable authority and MUST NOT become undocumented bypass channels.

## Current implementation evidence

The first verified vertical slice provides executable evidence for a substantial subset of these obligations:

- P-001: identity is authenticated before consequential execution.
- P-002/P-004/P-008: authorization binds the operation, resource, and canonical consequential parameters; modified parameters are rejected.
- P-006: authorization freshness and durable revocation are enforced at the execution boundary.
- P-009/P-011: terminal outcomes remain distinct from UNKNOWN, and recovery does not invent success.
- P-010: consequential attempts and terminal outcomes are durably recorded with ordered, integrity-protected events.
- Duplicate handling: durable principal-scoped idempotency prevents a duplicate effect and rejects conflicting reuse of an idempotency key.

P-003 remains bounded by the current governance interface and deferred policy-language/evaluator decisions. P-007, P-012, and broader administrative/model-output bypass surfaces require continued adversarial verification as additional interfaces are implemented.

## Bypass analysis

Every effect-capable path must answer: who is the principal, what proposal is being executed, which policy decision permits it, what authorization covers the exact operation and target, where is authorization enforced, what prevents bypass, and what survives a crash?

An UNKNOWN answer is an architectural gap.

## Boundary tests

Verification must attempt execution with no identity, forged identity, no proposal, no authorization, expired/revoked authorization, wrong resource, modified parameters, broader scope, replayed request, model-generated authority data, direct adapter access, recovery paths, and unauthorized administrative paths.

The currently implemented subset is backed by executable regression tests; boundary categories not yet implemented remain explicit verification obligations.

## Status

ARCHITECTURAL PROOF OBLIGATIONS WITH PARTIAL VERIFIED IMPLEMENTATION EVIDENCE.

These obligations remain the standard for evaluating new code. Verified implementation evidence must never be inferred from documentation alone.
