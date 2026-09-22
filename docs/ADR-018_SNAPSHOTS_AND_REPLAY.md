# ADR-018: Snapshots and Replay for State Materialization

Status: ACCEPTED
Date: 2026-09-22
Decision owner: Project architecture

## Context

Kernel state is materialized evidence, not the historical authority itself. Recovery must be able to reconstruct state without rewriting history.

## Decision

Kernel will use **snapshots plus event replay** for state materialization and recovery.

Snapshots provide bounded recovery/rebuild cost. Durable event history remains authoritative for reconstruction. Replay from an appropriate snapshot must produce the same valid state as replay from the beginning of the applicable event history.

A snapshot is derived state and does not replace or rewrite the event history.

If a snapshot is stale, corrupt, incomplete, or incompatible with the applicable event schema, Kernel must be able to reject it and recover through replay or another explicitly governed recovery path.

## Architectural consequences

The system gains a practical recovery path without abandoning durable event evidence.

Snapshot format/version compatibility becomes a migration concern.

## Verification

Tests must cover snapshot creation, restore, corruption, stale snapshots, replay determinism, schema-version changes, interrupted materialization, and full rebuild from durable events.
