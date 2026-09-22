# Kernel Configuration and Administrative Authority Model

Status: FOUNDATIONAL CONTRACT. Intended architecture, not implemented behavior.

## 1. Purpose

Configuration and administration can change the rules under which Kernel operates. They therefore require explicit authority rather than being treated as harmless implementation detail.

## 2. Configuration Classes

Configuration SHOULD be classified at least as:

- non-consequential presentation/configuration;
- operational configuration;
- governance configuration;
- security/identity configuration;
- authority configuration;
- recovery configuration.

The exact taxonomy remains open.

## 3. Governance Configuration

Changes to policy, authorization rules, identity mappings, delegation, execution capabilities, or trust boundaries are consequential.

Such changes MUST be attributable and auditable.

## 4. Configuration Provenance

Consequential configuration SHOULD record:

- actor;
- change;
- previous value/reference;
- new value/reference;
- reason/context where required;
- authorization;
- time;
- resulting configuration version.

## 5. Startup and Bootstrap

Bootstrap mechanisms MUST have explicit authority semantics.

Default configuration MUST NOT silently grant unrestricted consequential authority.

## 6. Administrative Authority

Administrative authority is still authority.

A debug flag, environment variable, local socket, filesystem write, hidden command, or maintenance endpoint MUST NOT be treated as outside the security model merely because it is intended for operators.

## 7. Emergency Controls

Emergency controls MAY exist, but they require:

- explicit identity;
- bounded scope;
- attribution;
- evidence;
- defined activation conditions;
- defined expiration/recovery semantics.

## 8. Configuration Rollback

Rollback MUST preserve evidence that a configuration change occurred.

Restoring a previous value does not erase the historical change.

## 9. Secrets

Secrets MUST be separated from ordinary configuration where their handling requirements differ.

Exact secret-storage and key-management mechanisms remain UNKNOWN.

## 10. Open Decisions

Configuration format, versioning, signing, administrative roles, bootstrap authority, emergency authority, secret storage, and change-approval workflow remain UNKNOWN.
