# High-yield checks for AI-built apps — how to verify

These are the gaps behind most real breaches of quickly built apps: exposed
secrets, missing authentication, missing input validation, and over-open database
rules. Verify each one; don't assume.

## 1. Database access (Supabase / Firebase)

- Supabase: in SQL, list tables without RLS:
  ```sql
  select schemaname, tablename from pg_tables
  where schemaname = 'public' and rowsecurity = false;
  ```
  Every row returned is a finding. Then review `pg_policies` for policies whose
  `qual` is `true` for `anon` or `authenticated` on sensitive tables.
- Test from outside: using only the public anon key, try `select` on each table.
  If data comes back without login, that is CRITICAL when the data is personal
  or business-sensitive.
- Storage buckets: check which are `public`; check storage policies.
- Firebase: rules must not contain `allow read, write: if true;`.

## 2. Secrets

- Run `gitleaks detect --source . --redact` (current tree **and** history).
- Search the built frontend (`.next/static`, `dist/`) for `service_role`,
  `sk-`, `sk_live`, `AKIA`, `-----BEGIN`, `eyJhbGci` (JWTs).
- `.env*` files must be in `.gitignore`; check `git log --all -- .env`.
- A secret that was ever committed is compromised: recommend rotation to the
  owner (do not rotate it yourself).

## 3. Authentication and authorization

- List every API route / server action / edge function. For each, confirm it
  (a) requires a session where it should and (b) checks the user may access the
  specific record (no trusting `userId` sent from the client).
- Admin pages must be protected server-side, not just hidden in the UI.

## 4. Input validation

- Server-side schema validation (e.g. zod) on every write endpoint.
- No raw SQL string building; no `dangerouslySetInnerHTML` with user data;
  no `eval`/`new Function` on input.

## 5. Headers and transport

- `curl -sI https://<site>` → expect `strict-transport-security`,
  `content-security-policy`, `x-content-type-options: nosniff`, and
  `frame-ancestors` (or `x-frame-options`).

## 6. Abuse controls

- Rate limits on login, signup, reset, OTP, file upload and any LLM endpoint
  (LLM endpoints cost money when abused).

## 7. Dependencies and supply chain

- `osv-scanner scan source -r .` with lockfiles present.
- Prefer pinned exact versions for security-critical and AI-gateway packages.
- Be wary of a release published in the last 24–72 h for a high-value package.

## 8. AI agents and LLM features

- Which tools/keys can the agent use? Remove anything not needed.
- Destructive actions (delete, pay, send, deploy) need human confirmation.
- Treat model output and retrieved documents as untrusted (prompt injection).
- Never put secrets in prompts or system prompts.
