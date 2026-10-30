---
name: security-weekly
description: Run the weekly security intelligence review — upstream OWASP and scanner changes, new attack techniques and research, scanner runs, and whether current controls are still adequate — and write security/reports/weekly/YYYY-MM-DD.md. Use when the user asks for a weekly security review.
---

# Weekly security intelligence review

Follow the `security-intelligence` skill's rules throughout.

1. Summarise the week's daily reports and any open register items.

2. **Upstream changes** (last 7 days) — check releases/commits of:
   OWASP CheatSheetSeries, ASVS, WSTG, API-Security, LLM Top 10; semgrep, trivy,
   gitleaks, osv-scanner. Note only changes that matter for this stack.

3. **New techniques & research** — search for newly published attack techniques
   and incident reports relevant to the inventory (framework, host, database,
   auth, AI/LLM usage). Confirm with primary sources before recording.

4. **Run the scanners that are installed** (do not install new ones without
   approval): `gitleaks detect --redact`, `osv-scanner scan source -r .`,
   `semgrep scan --config auto`. Summarise findings; triage real ones.

5. **Control adequacy** — compare the code against `SECURITY_BASELINE.md`. Has
   any control regressed (RLS disabled, route lost its auth check, header removed,
   scanner removed from CI)? A regression is at least HIGH.

6. **Sources** — add any new reputable source to `INTELLIGENCE_SOURCES.md` with
   the date and reason.

7. Write `security/reports/weekly/YYYY-MM-DD.md` with: summary, findings,
   regressions, proposed improvements (each following the 10-step safe
   improvement workflow), and questions for the owner.
