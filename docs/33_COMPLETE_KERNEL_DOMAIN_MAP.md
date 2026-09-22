# Complete Kernel Domain Map

## Purpose

This document expands the Kernel beyond governance into the complete controlled substrate. The Kernel is the coordination and enforcement layer connecting platform resources, computation, memory, state, communication, authority, recovery, and observation.

## Domain map

### 1. Platform Abstraction
Owns the narrow interface to the host operating system and hardware: processes, clocks, randomness, filesystems, networking, devices, CPU, memory, accelerators, and platform lifecycle.

It MUST expose only explicitly defined primitives to higher domains.

### 2. Resource Management
Represents CPU, RAM, GPU/accelerator, storage, network, files, devices, processes, sockets, and external resources.

Responsibilities: discovery, ownership, allocation, quotas, reservations, leases, accounting, exhaustion, release, and isolation.

Resource availability is not permission.

### 3. Isolation
Contains workloads and untrusted components.

Responsibilities: process/container boundaries where available, filesystem/network restrictions, credential separation, resource limits, lifecycle containment, and escape detection.

Isolation is a security boundary, not merely a performance feature.

### 4. Execution
Controls actual computation and consequential effects.

Responsibilities: task creation, invocation, cancellation, timeout, termination, adapter calls, effect binding, outcome capture, and enforcement at the effect boundary.

Execution cannot authorize itself.

### 5. Scheduling
Determines when authorized work receives resources.

Responsibilities: queues, priorities, deadlines, concurrency, fairness policy, cancellation, starvation handling, backpressure, resource-aware dispatch, and admission control.

Scheduling decides when eligible work runs, not whether it is permitted.

### 6. IPC and Eventing
Provides controlled communication.

Responsibilities: commands, messages, events, queues, delivery, correlation, causation, ordering, replay semantics, backpressure, and failure handling.

Transport does not confer authority.

### 7. Task and Lifecycle Management
Tracks work from creation through completion, cancellation, interruption, shutdown, and restart.

Responsibilities include task identity, parent/child relationships, checkpoints, cancellation propagation, and lifecycle evidence.

### 8. State
Maintains materialized current state.

Responsibilities: state transitions, versions, snapshots, consistency, derived views, checkpoints, invalidation, and reconstruction.

State is not history.

### 9. Memory
Manages information retained for future computation.

Memory domains may include working context, durable memory, episodic/event-derived memory, semantic/derived memory, configuration memory, and externally sourced evidence.

Every memory class needs explicit provenance, authority, mutation, retention, and privacy semantics.

Memory is not automatically truth.

### 10. Persistence
Provides durable storage for events, state, identity records, configuration, policy, evidence, and other explicitly classified records.

Responsibilities: transactions, durability, corruption detection, indexes, backups, restoration, migration, retention, and archival.

Storage technology must not silently define architectural truth.

### 11. Recovery
Restores operation after crashes, corruption, dependency failure, interruption, and uncertainty.

Responsibilities: startup recovery, event replay, state rebuild, reconciliation, retry governance, degraded mode, and uncertainty preservation.

Recovery is governed execution plus evidence analysis, not a bypass.

### 12. Identity
Establishes who or what is acting.

Responsibilities: principals, credentials, authentication evidence, sessions, delegation, revocation, lifecycle, and identity provenance.

Identity is independent of model-generated claims.

### 13. Security and Integrity
Protects authority, secrets, evidence, components, configuration, and boundaries.

Responsibilities: cryptographic verification, secret isolation, integrity checks, secure lifecycle, trust establishment, tamper detection, and fail-closed behavior.

Encryption alone is not authorization.

### 14. Context
Builds the evidence available to decision and execution.

Responsibilities: environmental state, resource state, prior events, external evidence, freshness, provenance, conflict, and uncertainty.

Context must preserve source and confidence/trust classification without confusing confidence with authority.

### 15. Proposal
Normalizes requested work into an explicit operation.

Responsibilities: operation identity, target binding, parameter validation, provenance, transformation lineage, and rejection.

Proposal is the bridge between intent and governed execution, not permission.

### 16. Governance
Determines whether proposed work satisfies policy and constraints.

Responsibilities: policy selection, policy versioning, evaluation, conflict handling, denial, indeterminate outcomes, and governance evidence.

Governance is separate from execution.

### 17. Authorization
Creates explicit bounded permission.

Responsibilities: scope, principal, target, operation, constraints, lifetime, revocation, delegation, usage limits, and independent validation.

Authorization is the enforceable bridge to the effect boundary.

### 18. Configuration
Controls system behavior and policy inputs.

Responsibilities: bootstrap, configuration hierarchy, validation, provenance, effective versions, secrets, controlled mutation, rollback, and integrity.

Configuration that changes authority is itself governed.

### 19. Administration
Provides controlled human/system administrative operations.

Responsibilities: maintenance, policy changes, lifecycle control, recovery intervention, diagnostics, emergency operations, and accountability.

Administrative power must have explicit authority and evidence.

### 20. Intelligence Boundary
Connects models and other proposal-generating intelligence to the Kernel.

Responsibilities: invocation boundary, model identity, input/output contracts, output validation, resource limits, isolation, provenance, and proposal submission.

The intelligence layer may propose. It does not receive authority merely by generating text, code, tool syntax, or an authorization-shaped object.

### 21. Interfaces
Defines external APIs, commands, local IPC, adapters, internal contracts, versioning, compatibility, validation, and error semantics.

Interfaces expose capabilities of the Kernel but do not redefine its authority model.

### 22. Observation
Provides operational visibility, diagnostics, audit evidence, health, metrics, traces, and reconstruction views.

Observation is downstream of authoritative evidence and cannot manufacture authority or history.

## Cross-cutting systems

These span every domain:

- provenance and lineage
- integrity
- time and clock semantics
- versioning
- privacy and redaction
- concurrency
- error/failure classification
- lifecycle
- configuration
- testing and verification
- resource accounting
- auditability

## Canonical control flow

Platform -> Resources -> Isolation -> Execution

Intelligence -> Proposal -> Context -> Governance -> Authorization -> Scheduling -> Execution

Execution -> Outcome -> Event -> Persistence -> State -> Memory/Observation

Recovery intersects Persistence, State, Events, External Effects, and governed Execution.

Identity and Security constrain every authority-bearing boundary.

## What makes this a kernel

The domains are not independent applications. The Kernel exists to enforce the contracts between them.

The defining property is controlled transition across boundaries:

**intent is not effect, capability is not permission, computation is not authority, state is not history, observation is not truth, and recovery is not exemption.**
