# Threat Model

Last reviewed: <YYYY-MM-DD>

## 1. What are we protecting?

| Asset | Sensitivity (High/Med/Low) | Why it matters |
|---|---|---|
| | | |

## 2. Who might attack, and how capable are they?

Assume automated, AI-assisted scanners that find exposed apps without needing to
know they exist. Small apps are in scope.

| Actor | Goal | Likely method |
|---|---|---|
| Automated internet scanners | Data, credentials, compute | Open DB rules, leaked keys, known CVEs |
| Malicious user of the app | Other users' data, free usage | Broken authorization, missing rate limits |
| Supply-chain attacker | Secrets from build/CI | Poisoned package release |
| Prompt-injection via content | Make the AI agent misuse its tools | Instructions hidden in documents/pages |

## 3. Entry points and trust boundaries

| Entry point | Auth required? | Trust boundary crossed | Notes |
|---|---|---|---|
| | | | |

## 4. Top risks (ranked)

| # | Risk | Likelihood | Impact | Current control | Gap |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

## 5. Changes since last review

-
