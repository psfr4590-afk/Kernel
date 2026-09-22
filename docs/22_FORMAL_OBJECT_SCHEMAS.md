# Formal Object Schemas

## Purpose

This document turns the conceptual objects in the Kernel sketch into implementation-neutral engineering contracts. It defines identity, authority, provenance, mutability, sensitivity, and versioning requirements without prematurely selecting a programming language, database, serialization format, or wire protocol.

Exact field types remain an implementation decision.

## Schema conventions

- Required means an object cannot be valid without the field.
- Optional means absence is meaningful and must not be silently replaced with a fabricated value.
- Immutable means the value cannot be changed after authoritative acceptance.
- Descriptive means the field describes context but does not grant authority.
- Authority-bearing means the field participates in an authorization decision or proves authority.
- Sensitive means disclosure or mutation requires additional controls.
- Every persisted object MUST have an explicit schema version.
- Every authority-bearing object MUST have provenance sufficient to identify its issuer and validation basis.

## Core objects

### Principal

Required: principal identifier, principal kind, authentication status/evidence, lifecycle status, schema version.

Optional: display metadata, delegation parent, credential references, attributes.

The principal identifier and issuer lineage are immutable after issuance. Display metadata is descriptive. Credential and authentication evidence is sensitive. A model-generated identity claim MUST NOT become a Principal merely because it is serialized as identity data.

### Request

Required: request identifier, receipt timestamp, source/interface, raw or canonical input reference, schema version.

Optional: caller metadata, deadline, correlation identifier, idempotency key.

A Request is attributable input, not authorization.

### Proposal

Required: proposal identifier, originating request, proposed operation, target/resource reference, parameters or parameter reference, provenance, schema version.

Optional: intelligence source, confidence metadata, requested priority, requested deadline, rationale.

Proposal authority is NONE. A Proposal MUST remain distinguishable from the authorization that may later permit it.

### Context

Required: context identifier, source references, validity/freshness metadata, schema version.

Optional: environmental facts, resource state, prior events, external evidence.

Staleness and uncertainty MUST be represented rather than hidden.

### Policy

Required: policy identifier, version, scope, issuer/owner, effective status, rule definition/reference, schema version.

Optional: expiry, precedence, explanatory metadata, test vectors.

Active policy versions MUST remain reconstructable.

### PolicyEvaluation

Required: evaluation identifier, policy version(s), proposal reference, context reference, outcome, evaluator identity/version, timestamp, schema version.

Outcomes: eligible/allow, deny, indeterminate, evaluation failure.

An evaluation MUST NOT be silently conflated with execution authorization.

### Authorization

Required: authorization identifier, authorized principal, operation, target/resource scope, constraints, issuer, issuance time, expiry/lifetime semantics, policy/evaluation references, schema version.

Optional: delegation chain, nonce, revocation reference, usage limits.

All authority-bearing fields require validation. Authorization MUST be independently verifiable at the execution boundary.

### Capability

Required: capability identifier, operation class, provider/adapter identity, lifecycle status, schema version.

Optional: resource requirements, platform constraints, metadata.

A Capability MUST NOT imply permission.

### ExecutionAttempt

Required: attempt identifier, authorization reference, operation/resource binding, executor identity, start evidence, schema version.

Optional: process/runtime identifiers, adapter version, timeout, retry lineage.

An execution attempt MUST NOT create authority retroactively.

### Outcome

Required: outcome identifier, attempt reference, outcome class, observation timestamp, evidence references, schema version.

Outcome classes: not attempted, blocked, attempted, succeeded, failed, partially completed, unknown.

UNKNOWN is a first-class outcome.

### Event

Required: event identifier, event type, schema version, timestamp, actor/source, subject, causation reference when applicable, correlation reference when applicable, payload/reference, integrity evidence.

Events are immutable after durable acceptance and MUST preserve lineage sufficient for required reconstruction.

### State

Required: state identifier, subject, state version, materialization basis, schema version.

Optional: derived fields, indexes, cache metadata.

State is a materialized view or checkpoint, not automatically the authoritative historical record.

### AuditRecord

Required: audit identifier, evidence references, reconstruction/query basis, integrity metadata, schema version.

An AuditRecord MUST identify the evidence from which it was derived.

### Resource

Required: resource identifier, resource class, ownership/trust classification, lifecycle status, schema version.

Optional: location, provider, quotas, metadata.

Resource identity and authorization scope MUST be independently validated.

## Cross-object rules

References MUST be explicit and typed. Authority MUST NOT be inherited merely through containment, serialization, naming, transport, or storage. Transformations between objects MUST preserve provenance. Replacing a field with an equivalent-looking representation MUST NOT change its authority semantics.

## Unresolved implementation choices

Concrete data types, serialization, cryptographic encoding, database representation, indexing, retention, and transport remain open until corresponding ADRs settle them.
