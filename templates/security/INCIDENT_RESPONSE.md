# Incident Response

Use this when something has **already gone wrong**: a leaked key, data exposed,
an account taken over, a CRITICAL vulnerability being exploited.

## Contacts

| Role | Name | How to reach | Backup |
|---|---|---|---|
| Owner / decision maker | | | |
| Hosting provider support | | | |
| Database provider support | | | |
| Organisation IT / security team | | | |
| Regulator / data protection contact (if personal data) | | | |

## First hour (owner actions — the agent only advises)

1. **Contain.** Take the affected feature or site offline if data is leaking
   (maintenance mode, disable the route, pause the project).
2. **Rotate** any exposed secret at the provider (database keys, API keys,
   OAuth secrets). Assume a committed secret is compromised even if deleted.
3. **Preserve evidence.** Export logs (hosting, database, auth) before they
   expire. Don't wipe and redeploy until logs are saved.
4. **Lock down** access: revoke sessions, reset admin passwords, enable MFA.

## Next 24 hours

5. Find the cause (which vulnerability or misconfiguration).
6. Fix on a `security/incident-<date>` branch; review; deploy with owner approval.
7. Check whether personal data was accessed, and what notification duties apply
   in your jurisdiction and organisation.
8. Record in `VULNERABILITY_REGISTER.md` and `SECURITY_CHANGELOG.md`.

## Afterwards

9. Write a short blameless postmortem in `reports/` (what happened, timeline,
   root cause, what we changed).
10. Add a regression test or CI check so it can't silently recur, and add the
    control to `SECURITY_BASELINE.md`.

## Quick reference — where to rotate keys

| Secret | Where to rotate |
|---|---|
| | |
