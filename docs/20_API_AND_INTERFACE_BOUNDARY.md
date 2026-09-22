# Kernel API and Interface Boundary

Status: FOUNDATIONAL CONTRACT. Exact transport and API technology remain unresolved.

## 1. Purpose

Interfaces are authority boundaries. An API is not merely a convenience wrapper around internal functions.

## 2. External Interface Rule

Every externally reachable consequential operation MUST enter through a governed interface that establishes identity, validates input, applies governance, enforces authorization, and records required evidence.

## 3. Internal Interface Rule

Internal calls MUST NOT be presumed trusted solely because they occur inside the process.

A privileged internal interface must have an explicitly defined trust and authority model.

## 4. Input Boundary

Input handling SHOULD distinguish:

- transport validity;
- authentication;
- authorization;
- schema validation;
- semantic validation;
- governance evaluation.

These are separate stages.

## 5. Output Boundary

Responses SHOULD distinguish:

- accepted request;
- authorized operation;
- execution outcome;
- durable commitment;
- uncertain outcome.

A successful HTTP/RPC response is not proof that a consequential operation succeeded.

## 6. Replay and Idempotency

Interfaces must define request identifiers and duplicate semantics where necessary.

## 7. Versioning

Externally observable contracts SHOULD be versioned.

Breaking changes MUST NOT silently alter authority semantics.

## 8. Error Model

Errors SHOULD identify the failed architectural stage without leaking unnecessary sensitive information.

At minimum distinguish:

authentication failure;
authorization denial;
policy evaluation failure;
validation failure;
execution failure;
persistence failure;
recovery uncertainty.

## 9. Interface Bypass

Direct invocation of an implementation function MUST NOT create a second authority path.

Tests and controlled maintenance interfaces are exceptions only when explicitly governed.

## 10. Open Decisions

Transport, API style, serialization, authentication protocol, rate limiting, quotas, streaming, IPC, versioning, and error format remain UNKNOWN.
