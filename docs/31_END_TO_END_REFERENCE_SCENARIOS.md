# End-to-End Reference Scenarios

These are design test cases, not claims of implementation.

## Scenario set

1. **Benign proposal:** request -> identity -> context -> proposal -> governance -> authorization -> execution -> outcome -> event -> state.
2. **Denied proposal:** governance denies; no execution occurs.
3. **Self-authorization attempt:** intelligence returns authority-shaped output; it remains untrusted data.
4. **Stale authorization:** execution boundary blocks expired authority.
5. **Scope escalation:** modified target/parameters fail authorization binding.
6. **Execution timeout:** status remains UNKNOWN unless stronger evidence establishes outcome.
7. **Effect succeeds, event write fails:** success and durability gap are both recorded for recovery.
8. **Event persists, state materialization fails:** state is rebuilt from evidence.
9. **Duplicate request:** idempotency contract prevents accidental duplicate effects.
10. **Crash during execution:** interruption enters reconciliation.
11. **Administrative change:** actor, authority, before/after state, effective time, and evidence are recorded.
12. **Compromised adapter:** effect boundary prevents or detects unauthorized invocation.
13. **State corruption:** authoritative evidence wins; derived state is rebuilt/quarantined.
14. **Conflicting external evidence:** conflict remains explicit rather than being arbitrarily resolved.
15. **Recovery after revocation:** inspection may continue, new effect cannot use revoked authority.
16. **Resource exhaustion:** scheduler/resource boundary enforces allocation.
17. **Untrusted plugin:** technical capability does not imply permission.
18. **Observation compromise:** monitoring output cannot establish authoritative success.
19. **Configuration tampering:** integrity controls detect or quarantine unauthorized changes.
20. **Shutdown/restart:** durable evidence determines what can resume, reconcile, or remain unknown.

## Required scenario evidence

Each future integration test should identify request, principal, proposal, policy/evaluation, authorization, execution attempt, outcome, events, state, and recovery evidence as applicable.

The scenarios should be run across normal, adversarial, concurrent, failure-injected, and restart conditions.
