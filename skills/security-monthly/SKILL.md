---
name: security-monthly
description: Run the monthly security posture review — threat model, auth and authorization, database policies, AI agent permissions, dependencies and infrastructure, obsolete controls — and produce a prioritized improvement roadmap in security/reports/monthly/YYYY-MM-DD.md. Use when the user asks for a monthly security review, security audit, or roadmap.
---

# Monthly security posture review

Follow the `security-intelligence` skill's rules throughout.

1. **Inventory refresh** — re-derive `ASSET_INVENTORY.md` and
   `inventory.json` from the code; note what changed since last month.

2. **Threat model** — update `THREAT_MODEL.md`: new features, new data, new
   integrations, new entry points. Re-rank the top risks.

3. **Review, area by area** (use
   `security-intelligence/references/vibe-coded-app-checks.md`):
   - Authentication and session handling
   - Authorization on every route / server action / function
   - Database policies (RLS / rules) and storage buckets
   - Secrets handling and history
   - Input validation and output encoding
   - Security headers, CORS, rate limiting
   - AI agents and LLM features: permissions, tool access, prompt-injection exposure
   - Dependencies (age, maintenance, known issues) and CI/CD supply chain
   - Infrastructure and provider settings (hosting, DB, auth, DNS)

4. **Obsolete controls** — find rules, scanners, or docs that no longer match the
   app and propose updates (never silently remove a control).

5. **Roadmap** — produce a prioritized table: item, severity, effort (S/M/L),
   owner action needed, proposed branch. Top three items first.

6. Update `SECURITY_BASELINE.md` only with **added or strengthened** controls.
   Any proposal that would loosen a control goes to the owner as a question.

7. Write `security/reports/monthly/YYYY-MM-DD.md` and append a summary line to
   `SECURITY_CHANGELOG.md`.
