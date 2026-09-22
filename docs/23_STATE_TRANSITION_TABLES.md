# State Transition Tables

## Purpose

This document defines the lifecycle as an explicit transition contract so implementation cannot invent legal transitions inside handlers, callbacks, queues, or database mutations.

## Primary lifecycle

| Current | Allowed next | Required condition | Evidence |
|---|---|---|---|
| RECEIVED | VALIDATED | Intake checks pass | intake event |
| RECEIVED | REJECTED | Request is invalid/out of contract | rejection event |
| VALIDATED | IDENTIFIED | Principal attribution succeeds | identity evidence |
| IDENTIFIED | PROPOSED | Valid proposal exists | proposal event |
| PROPOSED | EVALUATING | Required context and policy inputs exist | evaluation-start event |
| EVALUATING | EVALUATED | Evaluation completes | evaluation event |
| EVALUATING | INDETERMINATE | Required evidence cannot be established | indeterminate event |
| EVALUATING | FAILED | Evaluation mechanism fails | failure event |
| EVALUATED | AUTHORIZED | Explicit authorization contract is satisfied | authorization evidence |
| EVALUATED | DENIED | Governance denies effect | denial event |
| AUTHORIZED | EXECUTION_READY | Authorization remains valid and scope binds exactly | binding evidence |
| AUTHORIZED | EXPIRED | Authorization lifetime ends | expiry evidence |
| AUTHORIZED | REVOKED | Authorization is revoked | revocation evidence |
| EXECUTION_READY | ATTEMPTED | Effect boundary accepts authorized attempt | attempt event |
| EXECUTION_READY | BLOCKED | Preconditions fail | blocked event |
| ATTEMPTED | SUCCEEDED | Success is positively established | outcome event |
| ATTEMPTED | FAILED | Failure is positively established | outcome event |
| ATTEMPTED | PARTIAL | Some effects are established | outcome event |
| ATTEMPTED | UNKNOWN | Effect status cannot be established | uncertainty event |
| SUCCEEDED | RECORDED | Outcome is durably recorded | event evidence |
| FAILED | RECORDED | Failure is durably recorded | event evidence |
| PARTIAL | RECORDED | Partial evidence is durably recorded | event evidence |
| UNKNOWN | RECORDED | Uncertainty is durably recorded | event evidence |
| RECORDED | MATERIALIZED | State is derived from durable evidence | materialization evidence |

## Recovery lifecycle

| Current | Allowed next | Condition |
|---|---|---|
| INTERRUPTED | RECONCILING | Durable evidence indicates incomplete lifecycle |
| RECONCILING | RECONCILED | Evidence permits bounded conclusion |
| RECONCILING | UNKNOWN | Evidence cannot establish effect status |
| RECONCILING | FAILED | Failure is conclusively established |
| RECONCILING | PARTIAL | Partial effect is conclusively established |
| RECONCILED | RECORDED | Reconciliation result is durable |

## Forbidden transitions

- PROPOSED -> AUTHORIZED without governance evidence.
- AUTHORIZED -> SUCCEEDED without an execution attempt and outcome evidence.
- CAPABILITY -> AUTHORIZED.
- MODEL_OUTPUT -> AUTHORIZED.
- FAILED -> SUCCEEDED without a new independently evidenced operation.
- UNKNOWN -> SUCCEEDED merely because a retry was requested.
- State mutation -> historical success without corresponding evidence.
- Recovery -> success without evidence establishing success.
- Observation/UI state -> authority transition.

## Transition requirements

Every authoritative transition MUST define its preconditions, authority requirement, evidence, failure behavior, and concurrency semantics. Consequential transitions MUST be attributable and timestamped.

## Concurrency

Concurrent actors MUST NOT produce conflicting authoritative transitions merely because both observed the same previous state. The implementation must choose and document appropriate serialization, locking, versioning, or transactional semantics.

## Status

This is a pre-implementation lifecycle contract, not an executable state machine.
