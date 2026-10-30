# Security Baseline

The controls that exist **today**. Future changes must never weaken anything
listed here. The agent may add or strengthen entries; loosening one requires the
owner's written approval recorded in `SECURITY_CHANGELOG.md`.

Last updated: <YYYY-MM-DD>

## Authentication & authorization

| Control | Status | Evidence (file / setting) |
|---|---|---|
| All non-public routes require a session | | |
| Server-side authorization on every write | | |
| Admin area protected server-side | | |
| MFA available / enforced for admins | | |

## Database & storage

| Table / bucket | RLS / rules enabled | Policy summary | Evidence |
|---|---|---|---|
| | | | |

## Secrets

| Control | Status | Evidence |
|---|---|---|
| No secrets in repo or history (gitleaks clean) | | |
| Service-role / admin keys server-side only | | |
| `.env*` ignored by git | | |

## Web protections

| Control | Status | Evidence |
|---|---|---|
| HTTPS + HSTS | | |
| Content-Security-Policy | | |
| X-Content-Type-Options / frame-ancestors | | |
| Rate limiting on auth + AI endpoints | | |
| Server-side input validation | | |

## Supply chain & CI

| Control | Status | Evidence |
|---|---|---|
| Lockfile committed | | |
| Dependency scanning (osv-scanner) in CI | | |
| Secret scanning (gitleaks) in CI | | |
| Branch protection on default branch | | |

## AI agents

| Agent | Least-privilege tools | Human approval for destructive actions | Evidence |
|---|---|---|---|
| | | | |
