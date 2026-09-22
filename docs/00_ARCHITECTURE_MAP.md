# Kernel: Complete Architecture Map

Status: FOUNDATIONAL SKETCH. This document defines the intended architecture, not implemented behavior.

## 1. Purpose

Kernel is a local-first governed execution and durability substrate for AI-driven systems.

Central rule:

> Intelligence proposes; the kernel authorizes.

Kernel exists to prevent a proposal, model output, prompt, role label, memory record, capability, or presentation layer from becoming authority merely by existing.

## 2. System Boundary

The conceptual boundary is:

Intelligence → Proposal → Identity/Context → Governance/Policy → Authorization → Execution → Event → State

External systems may provide models, applications, tools, data, users, devices, or services. Kernel governs consequential interactions at its boundary.

Kernel does not become the model, planner, crawler, RAG system, UI, or provider.

## 3. Planes

### Intelligence Plane
Produces interpretation, predictions, plans, candidate actions, and other proposals. It has no inherent kernel authority.

### Identity and Context Plane
Establishes who or what is acting, under which session, context, scope, and attributable principal.

### Governance Plane
Evaluates applicable policy, constraints, authority, risk, scope, and required approvals.

### Authorization Plane
Produces an explicit authorization decision bound to a specific principal, operation, resource/scope, policy context, and validity boundary.

### Execution Plane
Performs only effects permitted by an authorization decision and reports the actual outcome.

### Durability Plane
Records consequential events and state transitions with lineage sufficient for reconstruction.

### Observation Plane
Exposes trustworthy evidence about proposals, decisions, executions, events, failures, and state without making presentation state authoritative.

## 4. Core Objects

- Principal: attributable identity for an actor.
- Proposal: requested or model-produced candidate operation.
- Context: information governing interpretation and evaluation.
- Policy: rules and constraints used by governance.
- Capability: an available mechanism or operation.
- Authorization: explicit permission for a bounded effect.
- Execution: an attempted consequential operation.
- Event: durable record of a significant occurrence.
- State: current materialized representation.
- Audit Record: evidence supporting reconstruction and review.
- Resource: object, service, namespace, or target affected by an operation.

Exact schemas remain implementation decisions.

## 5. Non-Equivalences

Proposal ≠ authorization.
Capability ≠ permission.
Identity ≠ role text.
Memory ≠ truth.
State ≠ history.
Execution success ≠ authorization.
Policy definition ≠ policy evaluation.
Logged activity ≠ complete auditability.
Model confidence ≠ authority.
UI visibility ≠ governance.
Persistence ≠ validity.

## 6. Authority Flow

1. An actor or intelligence source produces a proposal.
2. Kernel establishes attributable identity and applicable context.
3. Governance determines whether the proposal is eligible for authorization.
4. Authorization explicitly permits, denies, or requires additional conditions.
5. Execution verifies that the authorization applies before producing the effect.
6. Execution emits outcome evidence.
7. Durable events establish lineage.
8. State is derived or updated from authoritative event/state rules.
9. Observation exposes evidence without silently changing authority.

## 7. Trust Boundaries

Trust must be explicit at every boundary:

- external intelligence
- user/application input
- identity claims
- policy/configuration
- capability providers
- execution adapters
- persistence
- event consumers
- observation interfaces
- recovery/import paths

No boundary is trusted merely because it is internal.

## 8. Failure Domains

The architecture distinguishes:

request received
→ request parsed
→ identity established
→ proposal accepted
→ policy evaluated
→ authorization issued/denied
→ execution attempted
→ effect succeeded/failed/uncertain
→ event persisted
→ state committed/rejected/uncertain
→ recovery/reconciliation

A failure at one stage must not be silently represented as success at another.

## 9. Durability Rule

For consequential behavior, the system must preserve enough evidence to answer:

Who acted?
What was proposed?
Under what context?
Which policy applied?
What authorization existed?
What execution was attempted?
What effect occurred?
What event recorded it?
What state followed?
What remains uncertain?

## 10. Recovery Model

Recovery is not merely restarting a process. It must reconcile durable evidence with materialized state and identify ambiguity rather than inventing certainty.

Unknown, partial, duplicated, conflicting, or interrupted outcomes must have explicit representations.

## 11. Security Posture

Kernel must not depend on an intelligence source voluntarily following governance. Inputs may be malformed, contradictory, manipulated, stale, adversarial, overconfident, or incorrect.

The kernel's boundary is therefore enforcement-oriented rather than instruction-oriented.

## 12. Construction Dependency Graph

Architecture
→ invariants
→ contracts
→ identity/authority
→ policy/governance
→ authorization
→ event model
→ persistence/durability
→ execution boundary
→ recovery
→ observation
→ verification
→ implementation
→ integration
→ hardening

A later layer must not quietly redefine an earlier authority decision.

## 13. Explicit Unknowns

This sketch intentionally does not decide:

- implementation language
- database
- serialization
- cryptographic primitives
- process model
- IPC
- API framework
- policy language
- identity schema
- authorization algorithm
- event schema
- storage topology
- deployment topology
- model provider integration

These require separate contracts and evidence.
