# Intelligence Sources

Primary sources can be cited for findings. Secondary sources are leads only and
must be confirmed against a primary source. Add sources with a date and reason;
never remove a source silently — mark it `Retired` with the reason.

## Primary — vulnerability intelligence

| Source | URL | Use for |
|---|---|---|
| CISA Known Exploited Vulnerabilities | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | Is it exploited in the wild? |
| CISA KEV JSON feed | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | Automated checks |
| OSV.dev | https://osv.dev/ | Package-level advisories (npm, PyPI, Go, …) |
| GitHub Advisory Database | https://github.com/advisories | Package advisories, fixed versions |
| NVD | https://nvd.nist.gov/ | CVE details, CVSS |
| CISA advisories | https://www.cisa.gov/news-events/cybersecurity-advisories | Government alerts |

## Primary — standards & guidance

| Source | URL |
|---|---|
| OWASP Cheat Sheet Series | https://github.com/OWASP/CheatSheetSeries |
| OWASP ASVS | https://github.com/OWASP/ASVS |
| OWASP WSTG | https://github.com/OWASP/wstg |
| OWASP API Security | https://github.com/OWASP/API-Security |
| OWASP Top 10 for LLM Applications | https://genai.owasp.org/ |
| NIST cybersecurity publications | https://csrc.nist.gov/publications |

## Tools

| Tool | URL | Purpose |
|---|---|---|
| gitleaks | https://github.com/gitleaks/gitleaks | Secret scanning |
| osv-scanner | https://github.com/google/osv-scanner | Dependency vulnerabilities |
| semgrep | https://github.com/semgrep/semgrep | Static analysis |
| trivy | https://github.com/aquasecurity/trivy | Containers, IaC, filesystem |

## Our providers' security pages (fill in for this app)

| Provider | Security advisories URL |
|---|---|
| Hosting (e.g. Vercel) | |
| Database (e.g. Supabase) | |
| Auth provider | |
| Framework (e.g. Next.js) | |
| AI / LLM provider | |

## Secondary — leads only

| Source | URL | Notes |
|---|---|---|
| GitHub Security Blog | https://github.blog/security/ | |
| Security news | | Confirm before recording |

## Change log for this file

| Date | Change | Reason |
|---|---|---|
| | | |
