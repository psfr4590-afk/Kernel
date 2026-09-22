# Failure Taxonomy

Failures must be classified consistently because retry, audit, recovery, and security behavior depend on what actually failed.

## Classes

**Intake:** malformed input, unsupported operation, invalid encoding, oversized input.

**Identity:** unknown principal, authentication failure, expired credential, invalid credential, ambiguous attribution.

**Context:** missing, stale, contradictory, or unavailable evidence.

**Proposal:** invalid operation, target, parameters, transformation, or provenance.

**Governance:** policy denial, conflict, evaluation failure, missing policy, invalid version.

**Authorization:** missing, expired, revoked, out of scope, invalid issuer, or invalid delegation.

**Scheduling:** resource exhaustion, deadline expiry, starvation, cancellation, queue failure, priority conflict.

**Execution:** adapter rejection, process failure, timeout, local failure, dependency failure.

**External-effect uncertainty:** response lost, ambiguous acknowledgement, remote state unavailable.

**Persistence:** event write failure, transaction failure, storage outage, corruption, incomplete commit.

**State:** materialization failure, stale state, corrupted snapshot, conflicting version.

**Recovery:** insufficient evidence, reconciliation failure, conflicting evidence, unavailable external system.

**Security/integrity:** tampering, invalid signature, compromised credential, unauthorized mutation, integrity mismatch.

**Observation:** missing telemetry, collector failure, incomplete trace, inconsistent query.

**Configuration:** invalid configuration, unauthorized change, incompatible version, secret failure, policy/config mismatch.

## Failure, denial, and unknown

Denial means governance deliberately disallowed an operation. Failure means the system could not complete or establish it. UNKNOWN means evidence cannot establish the external effect status.

UNKNOWN is not a weaker synonym for FAILED.

## Retry semantics

Retries are potentially consequential. Each retry policy MUST specify idempotency, prior-effect knowledge, duplicate handling, and applicable authority.

## Failure evidence

Consequential failure and uncertainty SHOULD produce durable evidence sufficient for reconstruction, subject to privacy and retention rules.
