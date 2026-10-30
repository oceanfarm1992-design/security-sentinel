# Asset Inventory

What this application is built from. Triage depends on this file being accurate:
a vulnerability can only be ruled in or out against what is listed here.
Keep `inventory.json` (machine-readable, used by the KEV checker) in sync.

Last reviewed: <YYYY-MM-DD> · Reviewed by: <name / agent>

Write `Unknown — ask owner` rather than guessing.

## Application

| Item | Value |
|---|---|
| Name / URL | |
| Purpose | |
| Users (who logs in) | |
| Most sensitive data held | |

## Stack

| Layer | Technology | Version (exact) | Where it runs | Exposed to internet? |
|---|---|---|---|---|
| Programming languages | | | | |
| Frontend framework | | | | |
| Backend framework / API | | | | |
| Database | | | | |
| Authentication provider | | | | |
| Storage (files) | | | | |
| Hosting / deployment | | | | |
| CDN / WAF | | | | |
| CI/CD | | | | |
| Package manager + lockfile | | | | |

## External APIs and services

| Service | Used for | Key type (public/secret) | Where the key lives |
|---|---|---|---|
| | | | |

## AI models and agents

| Model / agent / library | What it can read | What it can change | Human approval required for |
|---|---|---|---|
| | | | |

## Secrets inventory (names only — never values)

| Secret name | Purpose | Stored in | Last rotated |
|---|---|---|---|
| | | | |

## Critical dependencies

List the dependencies whose compromise would hurt most (auth, DB clients, AI
gateways, payment SDKs), with pinned versions.

| Package | Version | Why critical |
|---|---|---|
| | | |
