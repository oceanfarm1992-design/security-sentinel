#!/usr/bin/env python3
"""Match the CISA Known Exploited Vulnerabilities (KEV) catalog against a project.

Reads:
  * security/inventory.json   (products/services you declare: vendor, product, version)
  * package.json, requirements.txt, pyproject.toml, composer.json (dependency names)

Writes a Markdown report of KEV entries whose vendor/product matches something the
project uses. Matches are *candidates*: a human or the agent must still confirm the
affected version and exposure (see the security-intelligence skill).

Standard library only. Never executes anything it downloads.

Exit codes: 0 = ran, no matches · 3 = matches found (with --fail-on-match) ·
            1 = error (e.g. catalog unreachable).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.request
from pathlib import Path

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

# Package name -> names a KEV entry may use for the same product.
ALIASES: dict[str, list[str]] = {
    "next": ["next.js", "nextjs"],
    "react": ["react"],
    "react-dom": ["react"],
    "express": ["express"],
    "node": ["node.js", "nodejs"],
    "@supabase/supabase-js": ["supabase"],
    "firebase": ["firebase"],
    "firebase-admin": ["firebase"],
    "vite": ["vite"],
    "axios": ["axios"],
    "lodash": ["lodash"],
    "jsonwebtoken": ["jsonwebtoken"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "litellm": ["litellm"],
    "langchain": ["langchain"],
    "laravel/framework": ["laravel"],
    "wordpress": ["wordpress"],
    "php": ["php"],
}

# Product names too generic to match on their own (would cause noise).
STOPWORDS = {"core", "server", "client", "app", "api", "web", "framework", "sdk", "cli", "types"}


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        raise SystemExit(f"error: {path} is not valid JSON: {e}")


def project_terms(project: Path) -> dict[str, str]:
    """Return {normalized term: human-readable origin}."""
    terms: dict[str, str] = {}

    def add(name: str, origin: str) -> None:
        key = norm(name)
        if key and key not in STOPWORDS and len(key) >= 3:
            terms.setdefault(key, origin)

    inv = load_json(project / "security" / "inventory.json") or {}
    for item in inv.get("products", []):
        product = item.get("product", "")
        vendor = item.get("vendor", "")
        version = item.get("version", "")
        origin = f"inventory: {vendor} {product} {version}".strip()
        add(product, origin)
        if vendor and product:
            add(f"{vendor} {product}", origin)
    for kw in inv.get("keywords", []):
        add(kw, f"inventory keyword: {kw}")

    pkg = load_json(project / "package.json") or {}
    for section in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies"):
        for name, ver in (pkg.get(section) or {}).items():
            origin = f"package.json {section}: {name}@{ver}"
            for alias in ALIASES.get(name, []):
                add(alias, origin)
            add(name.split("/")[-1], origin)
    engines = (pkg.get("engines") or {}).get("node")
    if engines:
        add("node.js", f"package.json engines.node {engines}")

    req = project / "requirements.txt"
    if req.exists():
        for line in req.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.split("#", 1)[0].strip()
            if not line or line.startswith("-"):
                continue
            name = re.split(r"[<>=!~\[; ]", line, maxsplit=1)[0]
            for alias in ALIASES.get(name.lower(), []):
                add(alias, f"requirements.txt: {line}")
            add(name, f"requirements.txt: {line}")

    pyproject = project / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(encoding="utf-8", errors="ignore")
        for name in re.findall(r'^\s*"?([A-Za-z0-9_.-]+)\s*[<>=~!]', text, flags=re.M):
            add(name, f"pyproject.toml: {name}")

    composer = load_json(project / "composer.json") or {}
    for name, ver in (composer.get("require") or {}).items():
        origin = f"composer.json: {name}@{ver}"
        if name == "php":
            add("php", origin)
        for alias in ALIASES.get(name, []):
            add(alias, origin)
        add(name.split("/")[-1], origin)
    return terms


def fetch_kev(kev_file: str | None) -> dict:
    if kev_file:
        data = load_json(Path(kev_file))
        if data is None:
            raise SystemExit(f"error: KEV file not found: {kev_file}")
        return data
    req = urllib.request.Request(KEV_URL, headers={"User-Agent": "security-sentinel/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"error: could not download KEV catalog: {e}\n")
        sys.exit(1)


def match(kev: dict, terms: dict[str, str], days: int, today: dt.date) -> list[dict]:
    cutoff = today - dt.timedelta(days=days) if days > 0 else None
    hits = []
    for v in kev.get("vulnerabilities", []):
        added = v.get("dateAdded", "")
        try:
            added_d = dt.date.fromisoformat(added)
        except ValueError:
            added_d = None
        if cutoff and (added_d is None or added_d < cutoff):
            continue
        product = norm(v.get("product", ""))
        vendor_product = norm(f"{v.get('vendorProject', '')} {v.get('product', '')}")
        origin = terms.get(product) or terms.get(vendor_product)
        if origin:
            hits.append({**v, "_matched_on": origin})
    hits.sort(key=lambda x: x.get("dateAdded", ""), reverse=True)
    return hits


def render(hits: list[dict], terms: dict[str, str], days: int, kev: dict, today: dt.date) -> str:
    window = f"added in the last {days} days" if days > 0 else "entire catalog"
    lines = [
        f"# CISA KEV check — {today.isoformat()}",
        "",
        f"Catalog version: {kev.get('catalogVersion', 'unknown')} · "
        f"Entries scanned: {len(kev.get('vulnerabilities', []))} ({window}) · "
        f"Project terms: {len(terms)}",
        "",
    ]
    if not hits:
        lines += ["**No KEV entries matched this project.**", ""]
    else:
        lines += [
            f"**{len(hits)} candidate match(es).** Each is *known to be exploited in the wild*. "
            "Confirm the affected version and whether the component is exposed, then triage "
            "with the seven questions. A confirmed match on an exposed component is CRITICAL.",
            "",
        ]
        for h in hits:
            cve = h.get("cveID", "?")
            lines += [
                f"## {cve} — {h.get('vendorProject', '')} {h.get('product', '')}",
                "",
                f"- **Name:** {h.get('vulnerabilityName', '')}",
                f"- **Added to KEV:** {h.get('dateAdded', '')} · **CISA due date:** {h.get('dueDate', '')}",
                f"- **Ransomware use:** {h.get('knownRansomwareCampaignUse', 'Unknown')}",
                f"- **Matched on:** {h['_matched_on']}",
                f"- **Required action (CISA):** {h.get('requiredAction', '')}",
                f"- **Description:** {h.get('shortDescription', '')}",
                f"- **Sources:** https://nvd.nist.gov/vuln/detail/{cve} · "
                "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
                "- **Verification status:** Unverified (version and exposure not yet confirmed)",
                "",
            ]
    lines += [
        "---",
        "Matching is by product name only. It can miss products named differently and can "
        "flag products you use in an unaffected version. Keep `security/inventory.json` accurate.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", default=".", help="project root (default: .)")
    ap.add_argument("--days", type=int, default=0, help="only KEV entries added in the last N days (0 = all)")
    ap.add_argument("--kev-file", help="use a local KEV JSON file instead of downloading")
    ap.add_argument("--out", help="write the Markdown report here (default: stdout)")
    ap.add_argument("--json", help="also write matches as JSON here")
    ap.add_argument("--fail-on-match", action="store_true", help="exit 3 if any match is found")
    ap.add_argument("--today", help=argparse.SUPPRESS)  # for tests
    args = ap.parse_args(argv)

    project = Path(args.project).resolve()
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    terms = project_terms(project)
    kev = fetch_kev(args.kev_file)
    hits = match(kev, terms, args.days, today)
    report = render(hits, terms, args.days, kev, today)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"KEV check: {len(hits)} match(es). Report: {out}")
    else:
        print(report)
    if args.json:
        Path(args.json).write_text(json.dumps(hits, indent=2), encoding="utf-8")
    return 3 if (hits and args.fail_on_match) else 0


if __name__ == "__main__":
    sys.exit(main())
