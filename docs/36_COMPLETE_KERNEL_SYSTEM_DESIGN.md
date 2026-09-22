# Kernel: Complete End-to-End System Design

Status: ARCHITECTURAL SPECIFICATION / PRE-IMPLEMENTATION  
Authority: This document is the complete integrated design target for Kernel. Existing architecture documents remain supporting rationale and traceability; this document is the single end-to-end description of how the complete system is intended to behave.

## 1. System Definition

Kernel is a local-first governed execution and durability system that places a hard authority boundary between intelligence and consequential action.

Its governing rule is:

> Intelligence proposes; the Kernel authorizes.

Kernel exists to make consequential execution conditional on explicit identity, context, governance, authorization, resource ownership, execution controls, durable evidence, and recoverable state. It is not an LLM runtime, agent framework, planner, crawler, RAG system, prompt framework, model provider, or generic tool runner.

The system accepts requests from humans, applications, models, services, scheduled work, or other authenticated principals. It determines who or what is responsible for the request, establishes the relevant context, converts or validates the requested intent into a bounded proposal, evaluates applicable governance, issues explicit authorization when permitted, allocates only permitted resources, executes through a constrained effect boundary, records what happened as durable evidence, materializes state from that evidence, and exposes observations without allowing observation itself to acquire authority.

No component may skip the authority chain merely because it is trusted, local, internal, automated, administrative, or technically capable.

The complete conceptual path is:

REQUEST -> INTAKE -> IDENTITY -> CONTEXT -> PROPOSAL -> GOVERNANCE -> AUTHORIZATION -> RESOURCE CHECK -> DISPATCH -> EXECUTION -> OUTCOME -> EVENT -> STATE -> OBSERVATION

Recovery is not a separate shortcut around this path. Recovery uses durable evidence to determine what is known, what is unknown, what may be reconciled, and what action, if any, remains authorized.

## 2. What Kernel Actually Guarantees

Kernel guarantees process discipline, not magical truth.

It can guarantee that a consequential operation cannot cross the Kernel's enforced effect boundary without a valid authorization satisfying the required constraints. It can guarantee that authorization is distinct from proposal, capability, identity, policy, and observation. It can guarantee that material state is derived from durable evidence according to defined transition rules. It can preserve provenance and lineage. It can refuse unsafe transitions when required evidence is absent. It can distinguish failure from denial and uncertainty from success.

Kernel cannot guarantee that an external system tells the truth, that a compromised operating system is honest, that a remote service honors a request, that an external side effect is reversible, or that a model produces a good proposal. Those become explicit trust assumptions and uncertainty states rather than invisible assumptions.

The system therefore prefers an honest UNKNOWN to a fabricated SUCCESS.

## 3. The Trusted Kernel Boundary

The irreducible Kernel is the smallest component set that must remain authoritative regardless of implementation technology.

The trusted computing base consists of:

1. identity verification and principal binding;
2. proposal validation and provenance binding;
3. context validity and freshness enforcement;
4. governance and policy evaluation;
5. authorization issuance and validation;
6. resource ownership and allocation enforcement;
7. the execution/effect enforcement boundary;
8. durable event integrity and authoritative evidence handling;
9. state transition validation and materialization;
10. recovery and reconciliation authority;
11. security, integrity, secret, and configuration controls required to protect those functions.

Everything else is replaceable infrastructure or an integration.

A database is not the Kernel. A model is not the Kernel. A scheduler is not the Kernel. A UI is not the Kernel. An adapter is not the Kernel. A plugin is not the Kernel. A transport is not the Kernel. These components may be necessary, but their implementation must not redefine authority.

The decisive boundary is physical and logical: no consequential effect may occur through a Kernel-controlled resource unless the effect path can demonstrate the authorization required for that effect.

If a component can cause the effect without passing that boundary, it is outside Kernel's authority model and must either be isolated, explicitly treated as an external trust boundary, or not be represented as Kernel-governed execution.

## 4. Principal, Identity, and Responsibility

Every request has a principal.

A principal may be a human, service, model runtime, plugin, scheduled process, administrator, recovery process, or another explicitly recognized actor.

Authentication establishes identity. Identity does not automatically establish permission.

A principal record contains a stable identity, authentication method or evidence, lifecycle state, authority domain, provenance, and relevant version information. Roles are attributes or governance inputs, not authority by themselves. A string claiming "admin" has no authority merely because it says "admin."

The system binds each request to an authenticated principal before authorization.

Delegation creates a bounded authority relationship. Delegation must specify issuer, delegate, scope, constraints, validity interval, provenance, and revocation behavior. A delegate cannot grant itself authority that its delegator did not possess.

Revocation invalidates future use of affected authority according to the defined freshness model. Already-attempted external effects are not magically undone by revocation.

Administrative authority is itself modeled, authenticated, scoped, logged, and governed. There is no invisible superuser path.

## 5. Request and Proposal

A request expresses desired work. A proposal is the Kernel-valid representation of work that could potentially be authorized.

A request may originate outside the Kernel and may contain arbitrary text, parameters, model output, tool syntax, or application data. None of these are authority.

The intake process:

1. receives the request;
2. assigns a durable request identity;
3. records source and provenance;
4. validates structural requirements;
5. authenticates the principal;
6. resolves required context;
7. creates or validates a proposal;
8. binds proposal parameters to the request and provenance;
9. prevents untracked transformation;
10. submits the proposal for governance.

A model may generate a proposal, but the model does not authorize it.

A proposal contains an intended operation, target resources, parameters, expected effect class, requested capabilities, constraints, provenance, principal binding, context reference, and schema version. Any transformation from raw model output or application input into a proposal is itself attributable and must not silently add authority.

If proposal normalization changes meaning, the transformation is recorded.

Malformed, ambiguous, stale, incomplete, or unverifiable proposals are denied or rejected before effect execution.

## 6. Context

Authorization decisions depend on context.

Context includes only information relevant to the decision and must carry provenance and freshness metadata. Examples include resource ownership, current policy version, principal status, environmental constraints, task state, time validity, dependency state, and external evidence.

Context is not automatically truth. Each context value has a source and trust classification.

The Kernel distinguishes:

- known valid context;
- known invalid context;
- stale context;
- missing context;
- conflicting context;
- untrusted context;
- externally asserted context.

When required context cannot be established, the system does not silently substitute assumptions.

Context is evaluated for freshness at the point where its validity matters. A previously valid authorization does not become immortal merely because it was once issued.

## 7. Governance and Policy

Governance defines what the system permits under specified conditions.

Policy definition and policy evaluation are separate concepts. A policy may exist in configuration, but its applicability and result must be determined against a concrete principal, proposal, context, resource, time, and policy version.

A policy evaluation produces one of:

- ALLOW;
- DENY;
- INDETERMINATE;
- EVALUATION_FAILURE.

ALLOW is not itself execution. It is an input to authorization.

Conflicting policies are resolved through explicitly defined precedence rules. No component may invent precedence at runtime.

Every authorization-bearing policy decision records the policy identity and version used to reach the result.

Policy changes are durable configuration events. They do not retroactively rewrite history.

## 8. Authorization

Authorization is an explicit, bounded, verifiable grant.

An authorization identifies:

- the principal;
- the request and proposal;
- the relevant context;
- the policy evaluation;
- permitted operation;
- permitted resources;
- parameter constraints;
- resource limits;
- validity interval;
- delegation chain where applicable;
- authorization identifier;
- policy and schema versions;
- revocation/freshness requirements;
- provenance and integrity evidence.

Authorization is scoped to the actual effect.

A capability describes what an actor or component can technically perform. Permission describes what it is currently authorized to perform. Capability never substitutes for permission.

Execution must revalidate authorization immediately before crossing the effect boundary, subject to the transaction model.

Authorization may be denied because of identity failure, policy denial, stale context, expired authority, revoked authority, resource exhaustion, concurrency conflict, malformed parameters, integrity failure, or other explicit conditions.

No execution path may infer authorization from:

- model output;
- role names;
- UI controls;
- internal module access;
- possession of credentials;
- previous successful execution;
- scheduler priority;
- local process identity;
- database access;
- a capability alone.

## 9. Resources

Kernel treats resources as governed objects, not merely operating-system conveniences.

Resources include CPU time, memory, storage, GPU or accelerator capacity, processes, file areas, network access, IPC endpoints, devices, external services, credentials, and other consequential capacities.

Every resource has an owner or authority domain, lifecycle, allocation rules, constraints, and accounting identity.

Allocation may use quotas, reservations, leases, limits, concurrency bounds, and priority rules. A resource being available does not mean the current principal is allowed to use it.

The resource manager answers:

- who owns the resource;
- who may delegate its use;
- what amount may be consumed;
- for how long;
- under what conditions;
- what happens when the limit is reached;
- how consumption is measured;
- how allocation is released;
- what happens if the owning task dies;
- what evidence records allocation and release.

Resource exhaustion is an explicit failure state. It is not an authorization bypass.

Resource accounting is attributable to principal, request, task, authorization, and execution attempt wherever practical.

## 10. Tasks and Lifecycle

Every executable unit has a durable task identity and lifecycle.

A task may be created from an authorized proposal, scheduled work, recovery operation, or explicitly authorized administrative action.

The task lifecycle tracks creation, queued state, dispatch, execution attempt, completion, failure, cancellation, interruption, reconciliation, and terminal closure.

Parent/child relationships are explicit. Child work inherits only explicitly defined authority and resource constraints. It does not automatically inherit unrestricted parent authority.

Cancellation is an authorization-bearing control operation. Cancellation requests do not imply that an already-completed external effect can be reversed.

If a parent dies, child behavior follows an explicit supervision policy. Possible behaviors include termination, orphan continuation under independent authority, pause, or reconciliation. None is implicit.

No task may continue indefinitely because a supervisor disappeared.

## 11. Scheduling and Dispatch

Scheduling determines when authorized work receives execution opportunity. Scheduling does not create authority.

The scheduler operates on already-authorized work.

Scheduling supports:

- priority;
- fairness;
- quotas;
- concurrency limits;
- deadlines;
- reservations;
- backpressure;
- cancellation;
- retry eligibility;
- dependency ordering;
- resource availability.

A higher-priority task cannot override authorization.

A task that loses authorization while queued is removed or blocked before effect execution.

A task that exceeds its resource or deadline constraints is stopped or marked according to defined failure semantics.

Starvation, queue overload, scheduler failure, and duplicate dispatch are observable and durable where they affect correctness.

Dispatch produces an execution attempt identity. One authorization may permit multiple attempts only when the authorization explicitly permits retry/repetition and the operation is safe under its idempotency model.

## 12. Isolation

Isolation prevents one component from acquiring authority or resources belonging to another merely through implementation proximity.

Isolation boundaries apply to:

- model runtimes;
- plugins;
- adapters;
- child processes;
- external commands;
- filesystem areas;
- network access;
- credentials;
- memory;
- IPC;
- devices;
- administrative operations.

Credentials are not inherited merely because a process is a child.

Filesystem and network access are explicitly scoped.

Plugins cannot access Kernel internals simply because they run in the same process unless the design explicitly makes that access part of the trusted computing base.

An adapter failure must not become a Kernel privilege escalation.

The isolation mechanism may differ by platform, but the architectural contract does not: unauthorized code must not obtain consequential authority through ambient access.

## 13. IPC and Internal Communication

Internal communication is treated as a security and correctness boundary.

Messages have identity, source, destination, type, schema version, causation/correlation identifiers, provenance, and integrity requirements.

The system defines whether each message requires:

- acknowledgement;
- ordering;
- deduplication;
- replay protection;
- expiration;
- retry;
- cancellation;
- dead-letter handling.

A message saying "execute this" is not authority. The receiving authority boundary must validate the associated authorization independently.

Message delivery failure is distinguishable from execution failure.

Duplicate messages must not create duplicate external effects unless repeated execution is explicitly authorized and safe.

## 14. Model Runtime Boundary

Models are intelligence providers, not authority providers.

A model runtime receives explicitly permitted input context and resource limits. The Kernel records model identity, model version, runtime version, relevant configuration, and invocation provenance where required for reproducibility and audit.

The model may produce text, structured output, proposed actions, tool descriptions, or other data.

All model output is untrusted input until it passes proposal validation.

The Kernel controls:

- what context the model receives;
- what resources it may consume;
- what interfaces it may call;
- whether it may stream;
- how cancellation works;
- how output is bounded;
- how model identity is recorded;
- how output is transformed into proposals.

A model cannot directly call an effect adapter merely because the model generated a syntactically valid command.

If the model runtime is compromised, the authority chain remains intact provided the runtime is correctly isolated.

## 15. Execution and Effect Boundary

Execution begins only after authorization and resource validation.

The execution boundary converts an authorized operation into an attempt against a controlled resource or adapter.

Before effect:

1. validate task identity;
2. validate authorization integrity;
3. validate authorization freshness;
4. validate principal binding;
5. validate resource binding;
6. validate parameters;
7. validate resource limits;
8. validate cancellation/deadline status;
9. validate adapter identity/version;
10. establish an execution attempt;
11. durably record the attempt boundary as required by the transaction model;
12. perform the effect.

The adapter receives only the authority and parameters required for the specific operation.

The adapter cannot widen scope.

The execution result is one of:

- NOT_ATTEMPTED;
- BLOCKED;
- ATTEMPTED;
- SUCCEEDED;
- FAILED;
- PARTIAL;
- UNKNOWN.

UNKNOWN means the Kernel cannot establish whether the external effect occurred. UNKNOWN is not failure and is not success.

## 16. External Systems

External systems are independent trust boundaries.

A remote request contains a unique operation identity where the external protocol supports it. Kernel uses idempotency keys, conditional operations, transaction identifiers, or equivalent mechanisms when available.

The system records:

- destination;
- adapter;
- request identity;
- request parameters or protected representation;
- authorization;
- send/attempt time;
- remote acknowledgement;
- response;
- timeout;
- connection outcome;
- reconciliation evidence.

Remote acceptance does not automatically equal final external completion unless the remote protocol defines it as such.

When response is lost, Kernel enters an uncertainty state rather than automatically retrying a potentially non-idempotent operation.

Reconciliation may query the external system, inspect durable evidence, use a provider operation ID, or require explicit administrative resolution. Reconciliation itself is governed.

Compensation is a new authorized operation. It is not an automatic undo primitive.

## 17. Durable Events

Events are the authoritative historical record of what Kernel knows occurred.

Events are append-oriented and immutable after acceptance except through explicitly modeled correction or supersession mechanisms.

Each event contains:

- event identity;
- event type;
- schema version;
- timestamp(s);
- causation identifier;
- correlation identifier;
- principal;
- request/task/execution identity where relevant;
- source;
- payload;
- provenance;
- integrity evidence.

The event stream records meaningful lifecycle facts, authorization decisions, configuration changes, security events, resource events, execution outcomes, recovery decisions, and administrative actions.

State is derived from events and validated transitions. State is not a replacement for history.

An event-store failure is not silently converted into "state updated successfully."

If an effect occurs but the corresponding event cannot be durably recorded, the system enters a defined evidence-gap condition and recovery process. It does not erase the fact that the effect may have occurred.

## 18. State

State is a materialized representation of current system knowledge.

State includes task status, resource allocations, authorization status, principal status, policy references, recovery status, and other current representations.

State must never be treated as the sole historical source when event evidence exists.

Materialization is deterministic with respect to the defined event history, schema versions, and materialization rules.

Corrupted or stale state can be rebuilt from authoritative events where the required evidence remains available.

State repair creates evidence of the repair. It does not rewrite history.

## 19. Memory

Kernel may expose several memory classes, but none is inherently authoritative merely because it is called memory.

Working memory contains transient task context.

Durable task memory contains explicitly retained task information.

Episodic memory represents prior interactions or events.

Derived memory contains computed summaries, embeddings, indexes, caches, or other secondary representations.

Configuration memory contains governed configuration.

Evidence memory contains durable records whose authority is defined by the evidence model.

Memory entries carry provenance and classification. Derived memory cannot silently become authoritative evidence.

Mutation, retention, forgetting, conflict resolution, deletion, redaction, and reconstruction are explicit operations.

A model's recollection is not evidence.

A cached authorization is not necessarily current authorization.

An embedding is not a source of truth.

## 20. Secrets and Cryptographic Integrity

Secrets are isolated from ordinary application data.

The design separates:

- credentials;
- signing keys;
- encryption keys;
- authentication evidence;
- application data;
- audit evidence.

Keys have lifecycle states including creation, active use, rotation, retirement, revocation, and destruction where applicable.

Cryptographic mechanisms protect confidentiality, integrity, authenticity, or provenance according to the threat model. Cryptography is not used as decoration.

Event integrity must make unauthorized modification detectable.

Key loss is treated as a recovery problem. Key compromise is treated as a security incident.

Cryptographic algorithm and serialization choices remain implementation decisions until formal ADRs settle them, but the security properties they must provide are fixed by this design.

## 21. Configuration and Bootstrap

Configuration is classified by authority impact.

Ordinary configuration may change behavior without changing authority.

Governance configuration changes policy and therefore requires stronger controls.

Security configuration affects trust boundaries and requires explicit provenance.

Bootstrap configuration establishes the initial conditions under which Kernel trusts anything else.

Secure startup establishes:

1. the Kernel's own identity;
2. trusted configuration source;
3. integrity of required policy;
4. storage availability and integrity;
5. key availability;
6. administrative authority;
7. schema compatibility;
8. required resource controls;
9. recovery state.

The first trusted configuration cannot simply authorize itself without a defined bootstrap root.

Bootstrap is a special trust-establishment process, not an exception to governance.

## 22. Administration and Emergency Authority

Administrative operations are ordinary Kernel operations with elevated but explicit authority.

An administrator cannot bypass evidence requirements simply by being an administrator.

Emergency authority may exist for availability or safety-critical situations, but it must have:

- explicit activation;
- identity;
- scope;
- expiration;
- reason;
- evidence;
- post-event review data;
- clearly defined powers.

Emergency authority cannot silently rewrite past authorization.

A recovery operator may resolve UNKNOWN conditions only within a defined authority scope and must record the evidence supporting the resolution.

## 23. Failure Semantics

Kernel distinguishes four fundamentally different conditions:

DENIED: the requested action is known to be unauthorized.

FAILED: an attempted operation did not achieve its intended result.

UNKNOWN: the system cannot establish whether the effect occurred or what the authoritative outcome is.

INTERRUPTED: execution or lifecycle processing stopped before a definitive result was recorded.

These states are not interchangeable.

Retry is allowed only when the operation's authorization, resource limits, failure semantics, and idempotency model permit retry.

A failed authorization evaluation is not equivalent to policy denial.

A missing event is not equivalent to no execution.

A process crash is not equivalent to external failure.

A timeout is not equivalent to remote non-execution.

This distinction is central to honest recovery.

## 24. Recovery and Reconciliation

Recovery starts from durable evidence.

On startup or failure detection, Kernel reconstructs:

- authoritative configuration;
- identities and authority state;
- event history;
- materialized state;
- in-flight tasks;
- resource ownership;
- execution attempts;
- unresolved uncertainty;
- recovery checkpoints.

For each interrupted operation, Kernel asks:

1. Was authorization valid?
2. Was execution attempted?
3. Is the effect known to have occurred?
4. Is the effect known not to have occurred?
5. Can the external system establish the answer?
6. Is retry authorized?
7. Is compensation possible and authorized?
8. Does the operation require human resolution?

If evidence does not support a definitive answer, the state remains UNKNOWN or RECONCILING.

Recovery cannot manufacture success from absence of failure evidence.

Recovery cannot grant new authority merely because the original path failed.

Recovery actions are themselves attributable, authorized, and durable.

## 25. Concurrency and Transactions

Kernel treats concurrency as an authority problem as well as a data problem.

Two requests may independently be authorized and still conflict over the same resource.

The system therefore defines:

- authorization freshness;
- resource version checks;
- optimistic or pessimistic concurrency controls;
- reservation semantics;
- transaction boundaries;
- duplicate detection;
- event ordering;
- state materialization ordering.

A lock prevents races. A lock does not grant permission.

An authorization decision must not become invalid simply because a different process acquired a database lock, nor may a database transaction be mistaken for an external-world transaction.

Where an effect and evidence cannot be made atomically durable, the architecture uses explicit uncertainty and reconciliation rather than pretending atomicity exists.

## 26. Time

Kernel uses time as governed data.

The design distinguishes monotonic time for durations and deadlines from wall-clock time for human and external timestamps.

Expiration rules specify which clock is authoritative.

Timestamps from external systems are evidence about those systems' clocks, not automatically Kernel truth.

Clock rollback, clock drift, unavailable time sources, and inconsistent timestamps are explicit failure conditions when they affect security or correctness.

Event ordering cannot depend solely on wall-clock timestamps.

## 27. Determinism and Reproducibility

Kernel does not require every operation to be perfectly deterministic.

It requires enough information to explain relevant nondeterminism.

For important execution paths, the system records versions and inputs necessary to reconstruct the decision environment where practical:

- Kernel version;
- policy version;
- schema version;
- principal identity;
- model/runtime identity when involved;
- adapter version;
- configuration version;
- relevant resource constraints;
- randomization source or seed when appropriate;
- external operation identifiers;
- relevant context provenance.

Reproducibility is bounded by external reality. The goal is not to replay the universe, but to reconstruct why Kernel reached a decision and what it knew at the time.

## 28. Plugin and Extension Model

Extensions are untrusted by default.

An extension declares identity, version, interfaces, requested capabilities, resource requirements, dependencies, and integrity information.

Installation, activation, upgrade, revocation, and removal are governed lifecycle operations.

An extension receives only the capabilities explicitly granted to it.

Extension discovery cannot grant permission.

A plugin may propose an action but cannot authorize itself.

If an extension is compromised, the intended blast radius is limited to its granted authority and resources.

Extensions that require trusted computing base privileges must be explicitly classified as trusted components and subject to the same verification standards as Kernel core.

## 29. Interfaces

External interfaces expose requests, status, observations, administration, and controlled operations.

Every interface validates:

- caller identity;
- input schema;
- authorization;
- version compatibility;
- replay constraints;
- resource constraints;
- output sensitivity.

Internal APIs are not automatically trusted merely because they are internal.

No public API is permitted to expose a shortcut from proposal to execution.

The interface layer is therefore a boundary, not the authority itself.

## 30. Observation and Audit

Observation tells operators what Kernel believes is happening.

Audit evidence explains what Kernel can prove happened.

Diagnostics help explain why a component behaved as it did.

These are separate concepts.

Observability may include metrics, logs, traces, health status, queue depth, resource usage, and operational telemetry.

Audit includes durable evidence of authority, policy decisions, execution attempts, effects, administrative operations, recovery, configuration changes, and integrity events.

Observation cannot create authority.

A health endpoint cannot declare a task authorized.

A dashboard cannot change task state except through a governed administrative interface.

Sensitive evidence is classified, minimized, redacted where required, and access-controlled.

## 31. Privacy and Data Lifecycle

Kernel minimizes collection of sensitive information while preserving required evidence.

Each retained data class has:

- classification;
- purpose;
- retention rule;
- access rule;
- redaction policy;
- deletion behavior;
- recovery behavior.

Deleting sensitive data must not silently destroy mandatory audit integrity. Where a record must remain for evidence but sensitive payload cannot, the architecture separates protected metadata from the sensitive payload and applies the defined retention policy.

Derived data such as indexes and embeddings follows the authority and deletion rules of its source.

## 32. Backup, Restore, and Migration

Backups are only useful if their validity can be established.

A valid backup must preserve the authoritative information necessary to reconstruct a coherent Kernel state, including required event history, configuration, schemas, and cryptographic dependencies according to the deployment model.

Restore verifies integrity and compatibility before becoming authoritative.

Partial restore is not silently treated as complete restore.

Schema migrations are versioned transformations with explicit compatibility rules.

Upgrades must define:

- old/new schema compatibility;
- event compatibility;
- policy compatibility;
- configuration migration;
- interrupted-upgrade recovery;
- rollback boundaries;
- component replacement;
- data integrity validation.

Rollback must not imply that external effects are rolled back. External effects require their own compensation or reconciliation.

## 33. End-to-End Request Walkthrough

A complete ordinary operation works as follows.

A principal submits a request.

Kernel assigns a request ID and records intake provenance.

Kernel authenticates the principal and establishes the principal's current identity state.

Kernel resolves required context, checking freshness and provenance.

The request is transformed into a proposal. If intelligence such as a model was involved, the model output is retained as provenance but has no authority.

Kernel validates the proposal and binds it to the principal, context, and request.

Governance evaluates the proposal against the applicable policy set.

If governance denies the request, the system records the denial and stops. No execution attempt exists.

If governance allows it, Kernel constructs an authorization containing exact scope, resource constraints, validity, and policy evidence.

The scheduler may queue the authorized task. Queueing does not change authority.

Before execution, Kernel checks authorization freshness, task state, resource availability, concurrency conditions, parameter integrity, and cancellation/deadline status.

Kernel reserves or allocates the required resources.

Kernel creates an execution attempt.

The execution boundary invokes the appropriate adapter with only the authorized operation.

The adapter reports its outcome.

Kernel classifies the outcome as succeeded, failed, partial, unknown, blocked, or not attempted.

Kernel durably records the execution outcome and relevant evidence.

State is materialized from the event history.

Observation surfaces the resulting state.

If any point crashes, recovery reconstructs the last durable evidence and determines whether the task is complete, failed, interrupted, or unknown.

If external effect uncertainty remains, reconciliation is performed only under explicit authority.

At no point does a model, scheduler, plugin, adapter, UI, or database get to invent authority.

## 34. End-to-End Denial

A request can be structurally valid, authenticated, and technically executable while still being denied.

Example:

A principal proposes modifying resource X.

Identity is valid.

Context establishes that X exists.

The proposal is valid.

Governance determines that the principal lacks permission to modify X.

Authorization is never issued.

The scheduler never receives executable authority.

No effect adapter is called.

The denial event is durable.

The observed state shows denial.

This is a complete successful Kernel lifecycle even though the requested action did not occur.

## 35. End-to-End Unknown

A request is authorized and dispatched to an external service.

The service receives the request.

The network connection fails before the response reaches Kernel.

Kernel cannot determine whether the remote operation committed.

The execution outcome becomes UNKNOWN.

Kernel does not automatically claim failure.

Kernel does not automatically retry a potentially non-idempotent operation.

A reconciliation task is created.

The external system is queried using the operation identity or other evidence.

If external evidence establishes success, Kernel records reconciled success.

If it establishes non-execution, Kernel records reconciled non-execution and may retry if still authorized.

If evidence remains inconclusive, the operation remains unresolved.

This is intentional behavior, not an error in the architecture.

## 36. Security Model

The principal security objective is:

> No untrusted, compromised, malformed, stale, or merely capable component can cause a consequential effect outside the authority explicitly granted to it.

Threats include malicious model output, compromised applications, forged identities, stale credentials, confused deputies, privilege escalation, replay, duplicate execution, event tampering, state corruption, recovery manipulation, policy corruption, configuration tampering, compromised adapters, malicious plugins, administrator error, dependency compromise, and resource exhaustion.

Security properties include:

- authority non-forgeability;
- scope confinement;
- identity integrity;
- capability/permission separation;
- authorization freshness;
- delegation confinement;
- replay resistance;
- event integrity;
- state/history separation;
- recovery honesty;
- adapter confinement;
- secret isolation;
- configuration integrity;
- administrative accountability;
- observation non-authority;
- resource isolation;
- process containment;
- dependency failure containment;
- provenance preservation;
- fail-closed authority enforcement.

## 37. The Inviolable Rules

The implementation must preserve these rules regardless of language, framework, database, transport, or deployment topology:

1. No ambient authority.
2. Proposal is never authorization.
3. Capability is never permission.
4. Identity is independent of role text.
5. Governance is distinct from execution.
6. Authorization is explicit and bounded.
7. The effect boundary enforces authorization.
8. Model output is untrusted input.
9. Internal components do not gain authority merely by being internal.
10. State is not history.
11. Durable evidence precedes recovery claims.
12. UNKNOWN is not SUCCESS.
13. Recovery cannot invent authority.
14. Retry requires an explicit safety and authorization basis.
15. External systems are separate trust boundaries.
16. Observation cannot authorize action.
17. Administrative authority is itself governed.
18. Configuration that changes authority is itself authority-bearing.
19. Security failures fail closed where continued execution would violate authority.
20. Every consequential effect must be attributable.
21. Every authority-bearing decision must be explainable from durable evidence.
22. Every bypass around the authority boundary is an architectural defect.

## 38. Implementation Shape

The final implementation may be a single process, multiple processes, or a distributed deployment. The architecture does not require microservices.

The implementation should begin with the smallest trusted core capable of enforcing:

- identity;
- proposal;
- governance;
- authorization;
- resource control;
- execution boundary;
- event durability;
- state materialization;
- recovery.

Schedulers, model adapters, external adapters, plugins, interfaces, observation systems, and optional integrations should depend on that authority contract rather than redefine it.

The project must resist unnecessary decomposition. Splitting one conceptual authority boundary into many network services does not make the boundary stronger. It merely creates more places for humans to misconfigure it, which is one of our species' more reliable traditions.

## 39. Required Internal Object Relationships

The authoritative relationships are:

Principal owns identity.

Request belongs to principal.

Proposal derives from request.

Context is associated with request/proposal and carries provenance.

Policy evaluation evaluates proposal against policy and context.

Authorization is issued from a successful applicable policy evaluation.

Execution attempt references authorization.

Outcome belongs to execution attempt.

Event records lifecycle facts and evidence.

State materializes from authoritative events.

Observation reads state and evidence.

Recovery operates on evidence and may create new governed operations.

Resource allocation binds resource ownership to authorized task execution.

No object may acquire authority merely by referencing another object.

## 40. Required State Discipline

The primary lifecycle is:

RECEIVED
-> VALIDATED
-> IDENTIFIED
-> PROPOSED
-> EVALUATING
-> EVALUATED
-> AUTHORIZED
-> EXECUTION_READY
-> ATTEMPTED
-> SUCCEEDED | FAILED | PARTIAL | UNKNOWN
-> RECORDED
-> MATERIALIZED

Blocked or denied paths terminate without effect.

Interrupted work enters:

INTERRUPTED
-> RECONCILING
-> RECONCILED

A reconciliation result must specify what evidence established the new state.

Illegal transitions are rejected.

State changes are attributable and evidence-backed.

## 41. Architecture Acceptance Conditions

Kernel is not considered architecturally complete merely because every module has been named.

The complete design is acceptable only when every consequential operation can answer:

Who requested it?

Who is responsible?

What exactly was proposed?

What context was used?

Which policy applied?

What authorization was issued?

What resources were granted?

What exact effect was attempted?

What happened externally?

What evidence proves the result?

What state was derived?

What happens if the process crashes at that exact point?

What happens if the external system lies, disappears, or responds ambiguously?

What happens if authorization expires while queued?

What happens if the same request arrives twice?

What happens if the event store fails?

What happens if state is corrupted?

What happens if the adapter is compromised?

What happens if a model is malicious?

What happens if an administrator makes a mistake?

What happens after restart?

What happens after restore?

What happens after upgrade?

If any consequential path cannot answer these questions without inventing behavior, that path is not architecturally complete.

## 42. Verification Strategy

Verification proceeds from architecture to implementation rather than from code to hope.

Every invariant receives:

- an implementation target;
- a positive test;
- a negative test;
- an adversarial test where applicable;
- a failure-injection test where applicable;
- a durability/recovery test where applicable;
- a regression test.

The most important tests attempt to violate authority:

- model directly executes;
- proposal self-authorizes;
- capability is mistaken for permission;
- stale authorization executes;
- revoked authorization executes;
- child task escapes parent scope;
- plugin accesses forbidden resource;
- adapter widens parameters;
- duplicate request causes duplicate effect;
- event history is tampered with;
- state claims success without evidence;
- recovery invents completion;
- observation endpoint changes authority;
- administrator bypasses required evidence;
- resource exhaustion causes scope escalation.

The system passes only when these paths are prevented or explicitly represented as external trust failures.

## 43. Technology Decision Boundary

Technology choices remain subordinate to the design.

The following require explicit ADRs before implementation becomes irreversible:

- implementation language/runtime;
- storage engine;
- event serialization;
- cryptographic primitives and key management;
- identity protocol;
- policy language/engine;
- authorization representation;
- delegation/revocation mechanism;
- transaction strategy;
- IPC/transport;
- execution adapter API;
- idempotency mechanism;
- event ordering mechanism;
- recovery/reconciliation mechanism;
- state materialization strategy;
- audit integrity mechanism;
- retention/archival;
- privacy/redaction implementation;
- administrative/emergency authority;
- deployment topology;
- model integration;
- external-effect trust assumptions.

A technology is accepted only when it can satisfy this design without weakening its invariants.

## 44. Complete Construction Target

The implementation target is therefore one coherent system, not a collection of loosely related subsystems.

A conforming Kernel must be able to take an untrusted request from an authenticated principal, establish the relevant identity and context, derive a bounded proposal, evaluate governance, issue explicit authorization, allocate governed resources, schedule and execute through an enforced effect boundary, classify the real outcome, durably record evidence, materialize state, expose observation, survive interruption, reconcile uncertainty, and preserve authority boundaries throughout.

The same system must remain correct when the request is denied, duplicated, malformed, stale, concurrent, cancelled, interrupted, partially completed, externally ambiguous, internally corrupted, or generated by a hostile intelligence component.

The system must be explainable from evidence after the fact.

The system must not rely on the model being honest.

The system must not rely on internal components being harmless.

The system must not confuse technical capability with permission.

The system must not confuse persistence with truth.

The system must not confuse absence of evidence with evidence of absence.

The system must not confuse recovery with authorization.

The system must not confuse successful local execution with successful external effect.

The Kernel is complete when those distinctions are enforced by the actual implementation rather than merely described in documentation.

## 45. Final Architectural Contract

The entire design reduces to one enforceable proposition:

Intelligence may determine what it wants to happen.

A principal may request that it happen.

A proposal may describe how it should happen.

Context may establish the conditions.

Governance may determine whether it is allowed.

Authorization may grant the exact bounded authority.

Resources may constrain what can be consumed.

The scheduler may determine when authorized work runs.

The execution boundary may permit the actual effect.

The external world may accept, reject, partially perform, or ambiguously perform it.

Events must preserve what Kernel knows.

State must represent that evidence.

Observation may expose it.

Recovery may reconcile uncertainty.

None of these steps may silently impersonate another.

That is the Kernel.

**Intelligence proposes. The Kernel authorizes. Evidence remembers. Recovery tells the truth.**
