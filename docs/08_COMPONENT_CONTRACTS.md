# Kernel Component Contracts

Status: ARCHITECTURAL SKELETON. Interfaces are conceptual and intentionally implementation-neutral.

## 1. Intelligence Adapter

Input: system context and allowed interface information.

Output: proposal(s).

Must not receive implicit authority through the adapter itself.

## 2. Proposal Intake

Responsibilities:

- validate proposal structure;
- assign/validate operation identity;
- preserve origin/provenance;
- bind proposal to principal/context where applicable;
- reject malformed or unsupported proposals.

## 3. Identity Service

Responsibilities:

- establish principal;
- validate identity evidence;
- resolve delegation where supported;
- expose attributable identity to governance and execution.

It must not derive authority from model text.

## 4. Context Resolver

Responsibilities:

- gather applicable context;
- identify relevant resource/scope;
- resolve policy/environment information;
- preserve provenance and freshness where required.

## 5. Policy/Governance Engine

Responsibilities:

- evaluate proposal against applicable policy;
- produce an attributable decision;
- identify conditions and evidence;
- distinguish denial from evaluation failure.

It does not itself execute the operation.

## 6. Authorization Service

Responsibilities:

- transform a valid governance decision into bounded authorization where permitted;
- bind authorization to principal, operation, resource/scope, conditions, validity, and provenance;
- support validation/revocation semantics as defined by the implementation.

## 7. Execution Boundary

Responsibilities:

- enforce authorization preconditions;
- invoke the appropriate adapter;
- constrain scope;
- capture outcome;
- expose uncertainty.

## 8. Execution Adapter

Responsibilities:

- interact with a specific external or internal effect mechanism;
- honor the supplied scope;
- return outcome evidence;
- avoid hidden authority escalation.

## 9. Event Store

Responsibilities:

- durably persist required events;
- preserve lineage/integrity requirements;
- support retrieval/reconstruction;
- expose persistence failure explicitly.

## 10. State Store/Materializer

Responsibilities:

- maintain defined current state;
- apply authoritative transitions;
- distinguish derived/cache/advisory data;
- support recovery/rebuild as specified.

## 11. Recovery Coordinator

Responsibilities:

- identify interrupted operations;
- classify uncertainty;
- reconcile according to operation-specific rules;
- emit recovery evidence;
- never manufacture success.

## 12. Audit/Observation Interface

Responsibilities:

- expose evidence;
- provide correlation/reconstruction;
- distinguish authoritative records from derived views;
- enforce access control and data minimization.

## 13. Administrative Boundary

Responsibilities:

- provide explicitly governed maintenance/recovery capabilities;
- preserve attribution;
- record consequential administrative actions;
- prevent emergency mechanisms from becoming invisible bypasses.

## 14. Dependency Rule

Components may depend on contracts, but no component may redefine the authority semantics of another layer by convention.

Exact module boundaries remain an implementation decision.
