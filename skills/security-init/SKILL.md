---
name: security-init
description: Set up Security Sentinel in the current project — create the security/ knowledge base, build the asset inventory from the real code, and optionally add the scheduled scanning workflows. Use when the user says "set up security", "initialize security sentinel", or when another security skill finds no security/ folder.
---

# Initialize Security Sentinel for this project

1. **Check first.** If `security/` already exists, do not overwrite anything.
   Tell the user what exists and offer to fill only the missing files.

2. **Copy the templates** (without overwriting):
   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/install.sh" --project . --no-workflows
   ```

3. **Build `security/ASSET_INVENTORY.md` from evidence, not guesses.** Inspect:
   `package.json` + lockfile, `requirements.txt`/`pyproject.toml`, `composer.json`,
   `Dockerfile`, `vercel.json`, `next.config.*`, `supabase/`, `.env.example`,
   CI files, and imports of SDKs (Supabase, Firebase, Stripe, OpenAI, Anthropic,
   LiteLLM, etc.). Fill every section; write `Unknown — ask owner` where you
   cannot tell. Also fill the machine-readable `security/inventory.json`
   (vendor/product keywords used by the KEV checker).

4. **Write a first `THREAT_MODEL.md`**: what data the app holds, who its users
   are, entry points, trust boundaries, and the top five risks.

5. **Record the baseline** in `SECURITY_BASELINE.md`: which controls exist today
   (RLS on/off per table, auth on each route, headers, rate limits, scanners).
   This is what future changes must never weaken.

6. **Ask the owner** before adding CI workflows:
   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/install.sh" --project . --workflows-only
   ```
   Explain that the workflows run daily/weekly on GitHub, upload reports as
   artifacts, and open an issue for CRITICAL findings. They never deploy or
   merge.

7. Run the **security-daily** skill once to produce the first report.

8. Summarise for the owner: files created, top risks found, and what still needs
   their input (marked `Unknown — ask owner`).
