# Kernel Threat and Adversarial Model

Status: FOUNDATIONAL DESIGN. Threat categories are architectural test targets, not claims that an implementation currently resists them.

## 1. Threat Objective

The principal security question is:

Can an untrusted or compromised intelligence source, caller, component, or data path cause a consequential effect without the authority required by Kernel?

## 2. Threat Sources

Consider:

- malicious model output
- compromised application
- malformed input
- forged identity claims
- stale authorization
- confused deputy behavior
- privilege escalation
- capability misuse
- replay
- duplicate execution
- event tampering
- state corruption
- recovery manipulation
- policy/configuration corruption
- observation-layer deception
- compromised external adapter
- administrator error
- supply-chain compromise

## 3. Attack Classes

### Authority Forgery
Attempt to manufacture authorization through prompts, role text, metadata, fabricated signatures, or model output.

Expected architectural result: rejected unless independently valid.

### Scope Expansion
Attempt to use an authorization for a broader target, operation, principal, or duration.

Expected result: rejected.

### Bypass
Attempt direct execution without governance/authorization.

Expected result: impossible or explicitly denied at the enforced boundary.

### Replay
Reuse a previously valid authorization or operation request.

Expected result: controlled by validity, uniqueness, nonce/idempotency, or operation-specific rules.

### Confused Deputy
Cause a component with authority to perform an action on behalf of an unauthorized requester.

Expected result: principal and delegation remain attributable and bounded.

### Recovery Forgery
Cause recovery to convert uncertainty into success.

Expected result: uncertainty preserved unless evidence resolves it.

### Evidence Tampering
Alter or remove records so that reconstruction becomes misleading.

Expected result: integrity controls detect or prevent the defined classes of tampering.

## 4. Security Properties to Verify

The eventual implementation should test:

- authority non-forgeability
- scope confinement
- authorization freshness
- identity integrity
- delegation confinement
- replay resistance where required
- event integrity
- recovery correctness
- audit reconstruction
- failure containment

Exact guarantees require implementation-specific threat modeling.

## 5. Trust Assumptions

The implementation must explicitly document assumptions about:

- host operating system
- local administrators
- process isolation
- storage
- cryptographic keys
- external services
- model provider
- network
- supply chain

Security guarantees cannot exceed these assumptions.

## 6. Threat Model Boundary

This document does not claim that Kernel alone solves model safety, host compromise, malicious administrators, physical compromise, or every external-system failure.

Those are separate threat domains with explicit interfaces.
