# Kernel Invariants and Authority Contract

Status: FOUNDATIONAL DESIGN CONTRACT. Normative terms describe intended architecture, not current implementation.

## 1. Normative Language

MUST: required for architectural conformance.
MUST NOT: prohibited.
SHOULD: expected unless a documented architectural reason exists.
SHOULD NOT: discouraged unless justified.
MAY: permitted without being required.

## 2. Authority Contract

Kernel MUST maintain a distinction between:

proposal → governance evaluation → authorization → execution → durable evidence.

No intermediate representation may erase that distinction.

## 3. Invariants

### K-INV-001: No Ambient Authority
No component MUST receive consequential authority merely because it can invoke code, access an object, emit model output, or reach an adapter.

Verification: authority-boundary tests and adversarial bypass tests.

### K-INV-002: Proposal Is Not Permission
A proposal MUST NOT authorize itself.

Verification: submit proposals containing authority claims, role claims, policy overrides, or fabricated approvals and verify that authorization remains independently evaluated.

### K-INV-003: Explicit Authorization
Every consequential execution MUST have an applicable authorization decision.

The authorization MUST be bound to the operation and relevant scope. An unrelated or stale authorization MUST NOT satisfy the requirement.

### K-INV-004: Identity Independence
Identity MUST be established independently of untrusted model-generated claims.

Role text, prompt content, metadata, or natural-language assertions MUST NOT by themselves establish principal authority.

### K-INV-005: Capability Is Not Permission
Availability of a capability MUST NOT imply permission to use it.

### K-INV-006: Governance Is Distinct From Execution
A governance decision MUST be distinguishable from the subsequent execution result.

A successful execution does not retroactively make an unauthorized operation authorized.

### K-INV-007: Event Lineage
Consequential state changes MUST have attributable event lineage.

### K-INV-008: State Is Not History
Materialized state MUST NOT be treated as the complete historical record unless the architecture explicitly proves that property.

### K-INV-009: Failure Is Information
The system MUST distinguish authorization failure, execution failure, persistence failure, and uncertain outcome.

### K-INV-010: Audit Is Evidence
An audit record MUST derive from authoritative evidence rather than solely from mutable UI or presentation state.

### K-INV-011: Reconstruction
For consequential operations, the architecture MUST preserve sufficient evidence to reconstruct principal, proposal, context, policy evaluation, authorization, execution attempt, outcome, event lineage, and resulting state.

### K-INV-012: Representation Independence
Changing serialization, transport, UI, prompt format, or object representation MUST NOT create authority that did not previously exist.

### K-INV-013: Fail Closed at the Authority Boundary
When required authorization evidence is absent, invalid, expired, ambiguous, or outside scope, consequential execution MUST NOT proceed.

The treatment of already-started operations requires a separate execution/recovery contract.

### K-INV-014: Atomicity Boundaries Are Explicit
Where authorization, execution, event persistence, and state mutation cannot be atomic, the architecture MUST define the resulting intermediate and recovery states.

### K-INV-015: Duplicate Handling
Retries MUST NOT silently create additional consequential effects when the operation is intended to be idempotent. Idempotency requirements must be operation-specific.

### K-INV-016: No Silent Authority Escalation
A component MUST NOT broaden principal, scope, capability, resource, duration, or effect beyond the authorization it received.

### K-INV-017: Policy Versioning
Where policy changes can affect interpretation of a consequential decision, the evidence MUST identify which policy version or rule set was evaluated.

### K-INV-018: Evidence Integrity
Durable evidence used for governance, recovery, or audit MUST have defined integrity and provenance requirements.

### K-INV-019: Observation Does Not Mutate Authority
Reading, displaying, exporting, or summarizing governance evidence MUST NOT silently alter the authorization state.

### K-INV-020: Recovery Does Not Invent Success
Recovery MUST distinguish known success, known failure, and unknown outcome. Unknown MUST NOT be rewritten as success merely to restore convenient state.

## 4. Authorization Object Requirements

An authorization SHOULD identify at minimum:

- principal
- operation
- target/resource
- scope
- policy context/version
- issuance time
- validity window
- conditions
- decision identifier
- provenance
- revocation/invalidity status where applicable

Exact schema is unresolved.

## 5. Execution Preconditions

Before consequential execution, the execution boundary MUST establish:

1. an attributable principal;
2. a specific operation;
3. an identified target/scope;
4. applicable authorization;
5. authorization validity;
6. required conditions;
7. sufficient evidence context;
8. a defined failure/recovery path.

## 6. Forbidden Bypasses

The implementation MUST NOT provide an alternate route that allows consequential effects to bypass the authority boundary, including:

- direct adapter invocation that skips authorization;
- hidden privileged execution paths;
- model-generated authorization tokens accepted without independent validation;
- role strings treated as credentials;
- mutable UI state treated as permission;
- recovery routines that mark unverified effects successful;
- administrative/debug paths that silently weaken production invariants.

Testing and explicitly scoped administrative controls are separate concerns and must be documented.

## 7. Observable Evidence

The system SHOULD make it possible to correlate:

proposal ID
→ identity/principal
→ context
→ policy evaluation
→ authorization decision
→ execution attempt
→ execution outcome
→ event ID
→ state transition
→ recovery/reconciliation.

Correlation identifiers and exact event schemas remain implementation choices.

## 8. Contract Boundaries

This contract intentionally leaves unresolved:

- exact identity technology;
- cryptographic signing format;
- policy language;
- authorization algorithm;
- transaction model;
- database;
- message transport;
- execution adapter interface;
- event serialization;
- retention;
- key management.

Those choices MUST conform to these invariants rather than redefine them.

## 9. Conformance Rule

An implementation conforms only when behavior, tests, and evidence demonstrate that the invariant is enforced. Documentation alone is not proof.
