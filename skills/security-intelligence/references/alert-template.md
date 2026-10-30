# Alert template

Copy this block for each finding (reports and `VULNERABILITY_REGISTER.md`).

```markdown
### [SEVERITY] <short title>  — ID: SS-YYYY-NNN

| Field | Value |
|---|---|
| Date discovered | YYYY-MM-DD |
| Original source | <URL of vendor advisory / CVE / KEV entry> |
| Second source | <URL> (required for CRITICAL/HIGH) |
| Vulnerability / threat | CVE-XXXX-XXXXX — one-line description |
| Affected component | <package@version / service / file> |
| Application-specific exposure | <is it reachable? from where? by whom?> |
| Exploitation status | In CISA KEV: yes/no · Vendor reports exploitation: yes/no |
| Severity | CRITICAL / HIGH / MEDIUM / LOW — and why |
| Recommended action | <exact upgrade target / config change / mitigation> |
| Patch availability | Fixed in <version> / Mitigation only / None yet |
| Verification status | Confirmed / Likely / Unverified |
| Status | Open / In progress (branch `security/…`) / Resolved YYYY-MM-DD / Not affected / Accepted risk (owner, date) |

**Triage answers**
1. Stack affected?
2. Package/service used?
3. Affected version used?
4. Exposed?
5. Exploited?
6. Patch/mitigation?
7. Actual risk to us:
```
