# Security Property Catalog

Security requirements are properties to verify, not merely products or configuration switches.

| ID | Property | Definition | Verification |
|---|---|---|---|
| SEC-001 | Authority non-forgeability | Untrusted input cannot manufacture authority | forged-data tests |
| SEC-002 | Scope confinement | Effects cannot exceed authorized scope | boundary tests |
| SEC-003 | Identity integrity | Attribution cannot be replaced by claims | identity tests |
| SEC-004 | Capability separation | Capability does not imply permission | abuse tests |
| SEC-005 | Authorization freshness | Expired/revoked authority cannot authorize effects | time/revocation tests |
| SEC-006 | Delegation confinement | Delegates cannot exceed delegated scope | delegation tests |
| SEC-007 | Replay resistance | Replayed evidence cannot create unauthorized duplicates | replay tests |
| SEC-008 | Event integrity | Historical evidence cannot be silently altered | tamper tests |
| SEC-009 | State/history separation | Derived state cannot rewrite history | rebuild tests |
| SEC-010 | Recovery honesty | Recovery cannot turn uncertainty into unsupported success | fault injection |
| SEC-011 | Adapter confinement | Adapters cannot bypass authority | direct-adapter tests |
| SEC-012 | Secret isolation | Secrets do not cross unauthorized boundaries | isolation tests |
| SEC-013 | Configuration integrity | Unauthorized changes cannot redefine authority | config tests |
| SEC-014 | Administrative accountability | Admin actions are attributable and governed | admin tests |
| SEC-015 | Observation non-authority | Telemetry cannot grant/mutate authority | observation tests |
| SEC-016 | Resource isolation | Workloads stay within resource contracts | sandbox tests |
| SEC-017 | Process containment | Terminated workloads cannot retain unintended authority | lifecycle tests |
| SEC-018 | Dependency failure containment | Dependency failures cannot broaden authority | fault tests |
| SEC-019 | Provenance preservation | Transformations retain source lineage | lineage tests |
| SEC-020 | Integrity fail-closed | Invalid authority/evidence is rejected | corruption tests |

## Security assumptions

The architecture permits untrusted intelligence, adapters, callers, data, and dependencies. Trust must be explicit at boundaries.

## Non-goals

These properties do not guarantee honest external systems, uncompromised hosts, perfect telemetry, morally correct policy, or usefulness.

## Verification rule

A security mechanism is not evidence that a security property holds. The property requires adversarial verification.
