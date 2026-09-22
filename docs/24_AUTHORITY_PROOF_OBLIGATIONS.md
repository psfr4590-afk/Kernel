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

## Bypass analysis

Every effect-capable path must answer: who is the principal, what proposal is being executed, which policy decision permits it, what authorization covers the exact operation and target, where is authorization enforced, what prevents bypass, and what survives a crash?

An UNKNOWN answer is an architectural gap.

## Boundary tests

Future verification must attempt execution with no identity, forged identity, no proposal, no authorization, expired/revoked authorization, wrong resource, modified parameters, broader scope, replayed request, model-generated authority data, direct adapter access, recovery paths, and unauthorized administrative paths.

Each must produce an inspectable result consistent with the authority contract.

## Status

These are proof obligations, not evidence that implementation already satisfies them.
