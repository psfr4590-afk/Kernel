# Kernel Storage and Recovery Architecture

Status: FOUNDATIONAL CONTRACT. Intended architecture, not implemented behavior.

## 1. Purpose

Storage is part of the authority and durability model because loss or corruption of evidence can change what Kernel can legitimately know.

## 2. Storage Classes

The eventual implementation SHOULD distinguish:

- durable authoritative evidence;
- materialized state;
- cache;
- temporary/in-flight data;
- external references.

## 3. Authoritative Record

For each data class, the architecture MUST define whether it is authoritative and what evidence establishes that status.

## 4. Persistence Failure

Persistence failure MUST be visible.

The system MUST NOT report a durable commitment when the required durability guarantee was not achieved.

## 5. Restart

Restart MUST preserve or recover all state required by the defined durability guarantees.

In-memory state alone MUST NOT be treated as durable unless explicitly backed by a durable mechanism.

## 6. Corruption

The recovery system must detect or surface corruption according to the integrity guarantees.

Unknown or corrupted evidence MUST NOT be silently reconstructed as authoritative.

## 7. Rebuild

A materialized state MAY be rebuilt from authoritative evidence when the event/state model permits.

Rebuild procedures MUST be deterministic enough to support defined consistency guarantees.

## 8. Backup

Backups are not automatically authoritative.

The implementation must define backup integrity, freshness, provenance, restoration authority, and conflict handling.

## 9. Recovery Ordering

Recovery SHOULD establish:

1. storage availability;
2. integrity status;
3. event/evidence availability;
4. interrupted-operation inventory;
5. state reconstruction;
6. reconciliation;
7. readiness.

## 10. Open Decisions

Storage engine, WAL/journaling, backups, snapshots, archival, encryption at rest, corruption detection, restore procedure, recovery authority, and consistency model remain UNKNOWN.
