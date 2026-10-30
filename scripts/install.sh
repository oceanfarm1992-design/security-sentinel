#!/usr/bin/env bash
# Security Sentinel — project installer.
# Copies the security/ knowledge base and (optionally) the scheduled GitHub
# workflows into a project. Never overwrites an existing file.
#
# Usage:
#   bash scripts/install.sh --project /path/to/app            # knowledge base + workflows
#   bash scripts/install.sh --project . --no-workflows        # knowledge base only
#   bash scripts/install.sh --project . --workflows-only      # workflows only
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT="."
DO_KB=1
DO_WF=1

while [ $# -gt 0 ]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2 ;;
    --no-workflows) DO_WF=0; shift ;;
    --workflows-only) DO_KB=0; shift ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

PROJECT="$(cd "$PROJECT" && pwd)"
created=0; skipped=0

copy_new() { # src dest
  local src="$1" dest="$2"
  if [ -e "$dest" ]; then
    echo "  keep   ${dest#$PROJECT/}  (already exists)"; skipped=$((skipped+1))
  else
    mkdir -p "$(dirname "$dest")"
    cp "$src" "$dest"
    echo "  create ${dest#$PROJECT/}"; created=$((created+1))
  fi
}

echo "Security Sentinel -> $PROJECT"

if [ "$DO_KB" = 1 ]; then
  echo "Knowledge base:"
  (cd "$HERE/templates" && find security -type f) | sort | while read -r f; do
    copy_new "$HERE/templates/$f" "$PROJECT/$f"
  done
  # Project-local copy of the operating procedure, so other AI coding tools
  # (not only Claude Code) can follow it too.
  copy_new "$HERE/skills/security-intelligence/SKILL.md" "$PROJECT/security/SKILL.md"
  copy_new "$HERE/skills/security-intelligence/references/alert-template.md" "$PROJECT/security/references/alert-template.md"
  copy_new "$HERE/skills/security-intelligence/references/vibe-coded-app-checks.md" "$PROJECT/security/references/vibe-coded-app-checks.md"
fi

if [ "$DO_WF" = 1 ]; then
  echo "Scheduled checks (GitHub Actions):"
  copy_new "$HERE/templates/.github/workflows/security-sentinel-daily.yml" "$PROJECT/.github/workflows/security-sentinel-daily.yml"
  copy_new "$HERE/templates/.github/workflows/security-sentinel-weekly.yml" "$PROJECT/.github/workflows/security-sentinel-weekly.yml"
  copy_new "$HERE/scripts/kev_check.py" "$PROJECT/security/tools/kev_check.py"
fi

echo
echo "Done. Next: open the project in Claude Code and ask:"
echo "  \"Run security-init to fill in the asset inventory and baseline.\""
