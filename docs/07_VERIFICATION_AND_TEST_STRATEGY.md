# Kernel Verification and Test Strategy

Status: FOUNDATIONAL DESIGN. This defines what must eventually be demonstrated.

## 1. Verification Principle

A documented invariant is not a verified invariant.

Conformance requires evidence from tests, inspection, and controlled failure/adversarial exercises appropriate to the claim.

## 2. Verification Layers

### Structural Verification
Confirm modules, dependencies, interfaces, and authority boundaries match the architecture.

### Contract Verification
Test preconditions, postconditions, failure semantics, and interface contracts.

### Behavioral Verification
Test ordinary workflows and expected state transitions.

### Adversarial Verification
Attempt bypasses, forged authority, scope expansion, replay, confused deputy behavior, tampering, and recovery manipulation.

### Durability Verification
Test interruption, corruption, duplicate delivery, persistence failure, replay, restart, and reconciliation.

### Regression Verification
Ensure fixes do not weaken previously established invariants.

### Evidence Verification
Ensure test claims correspond to what the tests actually establish.

## 3. Invariant Test Matrix

Each K-INV item SHOULD eventually map to:

invariant → test(s) → expected evidence → failure interpretation → regression coverage.

No invariant should remain permanently dependent on human reading of documentation.

## 4. Property Testing

Where practical, use generated inputs to test that authority cannot appear through unexpected representations, malformed data, ordering changes, duplicate requests, or boundary values.

## 5. Fault Injection

The test strategy SHOULD intentionally interrupt:

- before authorization
- after authorization
- before execution
- during execution
- after effect but before event persistence
- after event persistence but before state materialization
- during recovery

## 6. Security Testing

Security tests SHOULD include:

- forged principal
- forged authorization
- stale authorization
- altered scope
- altered resource
- altered operation
- replay
- duplicate request
- malformed policy input
- malicious model output
- compromised adapter behavior
- audit tampering
- recovery ambiguity

## 7. Determinism

Where deterministic behavior is required, tests must define the source of nondeterminism and control or record it.

## 8. Test Evidence

A passing test proves only the behavior covered by that test.

Coverage percentage alone MUST NOT be treated as proof of architectural correctness.

## 9. Failure Classification

Test failures should identify whether they indicate:

- implementation defect
- contract mismatch
- test defect
- environment problem
- unsupported assumption
- unresolved design decision

## 10. Acceptance

A component should not be considered complete merely because its happy-path tests pass. Completion requires its applicable invariants, failure paths, recovery semantics, and authority boundaries to be demonstrated.
