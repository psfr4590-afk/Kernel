# Kernel Event and Durability Model

Status: FOUNDATIONAL DESIGN. Intended model, not implemented behavior.

## 1. Purpose

Kernel treats durable evidence as a first-class architectural concern. State describes what the system currently believes; events preserve evidence of what occurred.

## 2. Event Lifecycle

A consequential operation follows:

Proposal → Decision → Execution Attempt → Outcome → Event → State Transition

The architecture MUST preserve the distinction between these stages.

## 3. Event Categories

At minimum, the model anticipates:

- lifecycle events
- identity/context events
- proposal events
- policy evaluation events
- authorization events
- execution events
- outcome events
- state transition events
- recovery/reconciliation events
- security/integrity events

Exact taxonomy remains open.

## 4. Event Properties

A consequential event SHOULD carry:

- unique event identifier
- event type
- timestamp
- principal/actor attribution
- operation/resource references
- correlation/causation identifiers
- authorization reference where applicable
- payload or payload reference
- schema/version identifier
- provenance
- integrity metadata
- persistence status

Exact representation is unresolved.

## 5. Causation and Correlation

Causation answers which event caused this event.

Correlation answers which broader operation or workflow this event belongs to.

The two concepts SHOULD remain distinct.

## 6. Append and Mutation

If an event is treated as historical evidence, it SHOULD be immutable after acceptance, or mutations MUST preserve verifiable history.

State MAY be mutable when its derivation rules permit it.

## 7. State Materialization

State SHOULD be understood as a materialized representation derived from authoritative evidence and rules.

The system MUST define whether a given state field is:

- authoritative;
- derived;
- cached;
- advisory;
- externally sourced.

## 8. Atomicity

Where effect and event persistence cannot be atomic, the architecture MUST define the uncertainty window.

Examples:

- effect succeeded, event not persisted;
- event persisted, effect failed;
- process terminated between effect and recording;
- duplicate retry after uncertain outcome.

No generic retry policy may assume these cases are equivalent.

## 9. Recovery

Recovery MUST use durable evidence and operation-specific reconciliation rules.

Recovery MUST NOT fabricate missing events or infer successful effects solely because an expected state exists.

## 10. Retention

Retention policy must distinguish operational convenience from evidentiary requirements. Deletion, compaction, archival, and redaction MUST preserve whatever lineage the architecture requires for its defined guarantees.

Exact retention periods are UNKNOWN.

## 11. Audit Reconstruction

A reviewer SHOULD be able to trace:

who → proposed what → under which context → what policy evaluated → what authorization existed → what was attempted → what happened → what was recorded → what state resulted.

## 12. Event Schema Versioning

Event schemas MUST be versioned if incompatible changes are possible.

Readers MUST define behavior for unknown or newer event versions.

## 13. Integrity

The architecture must define whether events require hashes, signatures, authenticated storage, append-only guarantees, or other integrity controls. No particular mechanism is selected by this sketch.

## 14. Unknowns

Open decisions include event ordering guarantees, clock strategy, storage engine, transaction boundaries, replay semantics, compaction, archival, redaction, encryption, and cross-process durability.
