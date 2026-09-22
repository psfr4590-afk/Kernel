# Kernel External Effect and Adapter Model

Status: FOUNDATIONAL CONTRACT. Intended architecture, not implemented behavior.

## 1. Purpose

Kernel may govern operations whose actual effects occur outside Kernel. The adapter boundary must prevent external mechanics from becoming an ungoverned authority path.

## 2. Adapter Contract

An adapter receives an authorized operation and performs a defined effect.

The adapter MUST NOT reinterpret authorization to expand scope.

## 3. Resource Binding

Authorization SHOULD identify the resource or resource class affected.

An adapter MUST verify that its actual target corresponds to the authorized target/scope.

## 4. Parameter Integrity

Consequential parameters SHOULD be bound to the authorization or a deterministic derivation from it.

An adapter MUST NOT accept arbitrary replacement parameters from an untrusted caller after authorization.

## 5. External Response

External responses are evidence, not automatically truth.

The adapter SHOULD preserve:

- request identifier;
- remote identifier where available;
- response;
- response time;
- error;
- transport status;
- ambiguity.

## 6. Timeout

Timeout means local certainty ended, not necessarily that the external effect did not occur.

Timeout handling MUST preserve this distinction.

## 7. Remote Acceptance

A remote system may accept an operation while local confirmation is lost.

The resulting state MUST represent the evidence level accurately.

## 8. Compensation

If rollback is possible, compensation is a new operation with its own authority and evidence.

A failed operation does not automatically authorize compensation.

## 9. Adapter Trust

The adapter may be trusted to perform a narrow mechanism, but that trust MUST NOT allow it to redefine governance.

## 10. Open Decisions

Adapter interface, sandboxing, process isolation, network policy, credential injection, remote idempotency, compensation semantics, and adapter trust model remain UNKNOWN.
