# Kernel Reference Architecture

Status: COMPLETE PRE-IMPLEMENTATION REFERENCE SKETCH.

This document combines the preceding contracts into one implementation-neutral reference architecture.

## 1. Core Pipeline

The canonical flow is:

REQUEST
→ INTAKE
→ IDENTITY
→ CONTEXT
→ PROPOSAL
→ GOVERNANCE
→ AUTHORIZATION
→ EXECUTION
→ OUTCOME
→ EVENT
→ STATE
→ OBSERVATION

Recovery intersects the pipeline wherever durable evidence indicates an interrupted or uncertain operation.

## 2. Control Plane

The control plane contains:

- identity;
- policy;
- governance;
- authorization;
- configuration;
- administration;
- security/integrity controls.

Its purpose is to decide what may happen.

## 3. Effect Plane

The effect plane contains:

- execution boundary;
- adapters;
- external resources;
- outcome collection.

Its purpose is to make authorized effects happen and report what actually happened.

## 4. Evidence Plane

The evidence plane contains:

- event persistence;
- provenance;
- lineage;
- state materialization;
- audit;
- recovery evidence.

Its purpose is to preserve and reconstruct what happened.

## 5. Intelligence Boundary

Intelligence sits outside the authority model unless explicitly represented as an independently authenticated principal.

Models may propose.

Models do not become authoritative because they generated a proposal.

## 6. Enforcement Boundary

The most important physical implementation property is that the execution path cannot obtain consequential effect without satisfying the authority contract.

The architecture should make bypass difficult by construction rather than relying solely on developer discipline.

## 7. Durability Boundary

The system must define which evidence is durable before it claims reconstruction or recovery guarantees.

## 8. Recovery Boundary

Recovery is a governed subsystem, not an exception to governance.

Recovery actions require attribution and defined authority.

## 9. Observation Boundary

Observation reads and derives evidence but does not redefine authority.

## 10. Dependency Direction

Conceptually:

Intelligence → Proposal interfaces
Identity → Governance
Context → Governance
Governance → Authorization
Authorization → Execution
Execution → Events
Events → State
Evidence → Observation
Recovery → Evidence + governed execution

No layer should depend upward on presentation state to determine authority.

## 11. Core Safety Invariants

The reference architecture preserves:

- no ambient authority;
- no self-authorizing intelligence;
- explicit bounded authorization;
- identity independent of model claims;
- capability/permission separation;
- event lineage;
- explicit uncertainty;
- no silent authority escalation;
- governed recovery;
- evidence-based audit.

## 12. Implementation Readiness

This reference architecture is sufficient to begin detailed interface and schema design, but it is NOT evidence of implementation readiness for a production system.

The next work should convert conceptual objects into precise contracts, state transition tables, schemas, ADRs, and executable verification requirements before implementation.
