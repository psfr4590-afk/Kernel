# ADR-002: SQLite as the Initial Kernel Durable Storage Engine

Status: ACCEPTED
Date: 2026-09-22
Decision owner: Project architecture

## Context

Kernel requires durable event history, state materialization, identity records, configuration, policy/evidence records, recovery information, and transactional boundaries while remaining local-first.

The first implementation should minimize infrastructure while still providing transactional durability and recovery semantics. A separate database service would introduce deployment, networking, authentication, availability, and operational failure domains that are not required to prove the initial Kernel authority/evidence model.

SQLite is an embedded transactional database designed for local application storage. Python's standard library provides the `sqlite3` module, so the initial storage layer does not require an additional database server or ORM merely to establish durable Kernel behavior.

## Decision

Kernel will use **SQLite as its initial authoritative durable storage engine**.

The database file is local to the Kernel deployment. The storage implementation will be behind a Kernel-defined persistence contract so that storage technology does not redefine Kernel semantics.

SQLite is a storage mechanism, not the source of architectural authority. Kernel contracts define what records mean, which transitions are valid, and what evidence is authoritative.

## Initial authoritative storage responsibilities

The first storage implementation will support, as required by the vertical slice:

- durable events;
- authoritative request/proposal/authorization evidence needed for reconstruction;
- state materialization;
- transaction boundaries;
- uniqueness/idempotency constraints where required;
- schema versioning/migrations;
- integrity/error detection;
- restart and recovery behavior.

The exact physical schema remains an implementation task governed by the existing formal object schemas and state-transition documents.

## Architectural consequences

Positive:

- Local-first and self-contained.
- No database server dependency for the initial Kernel.
- Transactional semantics suitable for coordinating related local records.
- Mature and widely deployed embedded database technology.
- Straightforward backup/restore at the database-file level, subject to Kernel's consistency and recovery requirements.
- Python standard-library integration reduces dependency surface.

Constraints:

- SQLite transactions cannot make external-world effects atomic with local database commits.
- Concurrent write behavior and locking must be explicitly designed and tested.
- Database durability settings and filesystem behavior must be verified rather than assumed.
- A SQLite database file does not by itself provide the complete audit, integrity, provenance, or recovery guarantees defined by Kernel.
- Multi-host/distributed storage is outside the first implementation unless later requirements justify it.

## Alternatives considered

### PostgreSQL or another server database

Provides strong multi-client/server capabilities, but introduces an unnecessary service and operational boundary for the first local Kernel slice. It may become justified by future deployment requirements.

### In-memory storage

Rejected because durable evidence and restart reconstruction are fundamental Kernel requirements.

### Flat files / JSON / ad-hoc event logs

Rejected as the primary authoritative store because the first slice requires transactional coordination, structured constraints, durable state, and recovery semantics that should not be recreated informally.

## Invariant impact

SQLite does not change Kernel's invariants.

The implementation must preserve:

- events/history distinct from materialized state;
- durable evidence before recovery claims;
- explicit transaction boundaries;
- no authority derived from storage access;
- no state transition that lacks required evidence;
- honest UNKNOWN outcomes when durable evidence cannot establish completion.

## Reversal conditions

Reconsider SQLite if executable evidence demonstrates that the required deployment topology, concurrency, durability, performance, storage scale, or recovery guarantees cannot be satisfied without a different engine.

A future replacement must preserve the Kernel persistence contract and be introduced through a new ADR plus migration/recovery evidence.

## Verification

The storage implementation must include reproducible tests for transaction atomicity, restart recovery, persistence failure, corruption handling, concurrent access, schema migration, duplicate handling, and event/state reconstruction as applicable to the implemented slice.
