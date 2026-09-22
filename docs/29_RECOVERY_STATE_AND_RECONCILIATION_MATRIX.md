# Recovery State and Reconciliation Matrix

Recovery is a governed continuation of the lifecycle, not a cleanup shortcut.

| Situation | Evidence | Permitted conclusion | Action |
|---|---|---|---|
| Crash before execution acceptance | pre-execution evidence | NOT ATTEMPTED | record interruption |
| Attempt created, invocation uncertain | incomplete invocation evidence | UNKNOWN unless impossible to have invoked | reconcile |
| Remote request sent, response lost | submission evidence | UNKNOWN | reconcile remote state |
| Remote success authenticated | authoritative remote evidence | SUCCEEDED | record |
| Remote failure authenticated | authoritative remote evidence | FAILED | record |
| Partial remote completion | authoritative evidence | PARTIAL | record scope |
| Event persisted, state missing | complete history | reconstructible | rematerialize |
| State persisted, event missing | incomplete history | insufficient historical proof | preserve gap |
| Authorization expired | current authority invalid | no automatic renewal | inspect only or reauthorize |
| Authorization revoked | revocation evidence | no automatic continuation | block effect |
| Conflicting evidence | competing authoritative evidence | UNKNOWN/CONFLICT | governed escalation |
| External system unavailable | no new evidence | preserve uncertainty | reconcile later |

## Recovery rules

1. Identify the interrupted operation.
2. Preserve the original principal and scope.
3. Never expand authorization during recovery.
4. Never manufacture success.
5. Distinguish reconciliation from retry.
6. Record reconciliation evidence.
7. Keep recovery auditable.
8. Administrative recovery requires its own authority.
9. If evidence is insufficient, UNKNOWN is valid.

## Reconciliation versus retry

Reconciliation asks whether the effect already happened. Retry asks whether a new attempt should occur. They are different operations.

## Recovery authority

Recovery may inspect evidence without necessarily retaining permission to create new effects. Expired or revoked authority cannot be silently revived.

## State repair

Derived state can be rebuilt from authoritative evidence. Repair MUST NOT rewrite history to make the result appear complete.

## Completion

Recovery is complete only when effect status is established or UNKNOWN is durably recorded, required evidence is preserved, state is reconciled, ambiguity is explicit, and no hidden privilege escalation occurred.
