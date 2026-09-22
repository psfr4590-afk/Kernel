# Kernel Observability and Audit Model

Status: FOUNDATIONAL DESIGN. Intended contract, not implemented behavior.

## 1. Purpose

Observability exists to make system behavior inspectable without becoming a source of invented authority.

## 2. Three Questions

Operational observability asks: what is happening?

Audit evidence asks: what happened, under what authority, and what evidence supports that conclusion?

Diagnostics asks: why did the system behave this way?

These concerns may share data but must not be conceptually conflated.

## 3. Minimum Trace

A consequential operation SHOULD expose a trace from:

principal
→ proposal
→ context
→ policy evaluation
→ authorization
→ execution
→ outcome
→ event
→ state

## 4. Evidence Classes

Evidence should be distinguishable as:

- authoritative durable record
- derived/materialized record
- external evidence
- diagnostic observation
- unverified assertion
- unknown/missing evidence

## 5. Audit Integrity

Audit output MUST NOT be considered authoritative merely because it looks complete.

Audit reconstruction must identify missing, conflicting, or uncertain evidence.

## 6. Sensitive Data

Logs and audit records may contain secrets, credentials, personal data, model prompts, or other sensitive material.

The implementation must define minimization, redaction, access control, retention, and encryption rules.

Exact policy is UNKNOWN.

## 7. Monitoring

Metrics and health checks SHOULD distinguish availability from correctness.

A healthy process does not prove an authorized or correct outcome.

## 8. Tamper Evidence

Where audit integrity matters, the system must define protections against unauthorized alteration or deletion.

The mechanism is unresolved.

## 9. Incident Reconstruction

The audit model should support reconstruction without requiring the same process instance, UI state, or in-memory objects that existed when the event occurred.

## 10. Open Decisions

Telemetry format, storage, access controls, retention, redaction, integrity mechanism, export format, and query interface remain unresolved.
