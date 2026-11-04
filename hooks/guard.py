#!/usr/bin/env python3
"""Security Sentinel guard hook (Claude Code PreToolUse).

Enforces the boundaries in security/SECURITY_POLICY.md mechanically, so they do
not depend on the model remembering them:

  * Blocks edits to protected files (the security policy and the security CI
    workflows) unless the owner has unlocked them for this session.
  * Blocks shell commands that pipe remote content into an interpreter.
  * Blocks pushes to the default branch and force pushes.

Exit code 2 blocks the tool call; the message on stderr is shown to Claude.

Owner unlock (deliberate, per session): start Claude Code with
    SECURITY_SENTINEL_UNLOCK=1 claude
The unlock covers protected-file edits only. Remote-script and push rules stay on.
"""
from __future__ import annotations

import json
import os
import re
import sys

PROTECTED_PATTERNS = [
    re.compile(r"(^|/)security/SECURITY_POLICY\.md$", re.IGNORECASE),
    re.compile(r"(^|/)\.github/workflows/security-sentinel-[\w.-]+\.ya?ml$", re.IGNORECASE),
    re.compile(r"(^|/)\.security-sentinel-lock$", re.IGNORECASE),
]

# Shell fragments that write/move/delete a path.
WRITE_VERBS = r"(?:>>?|\btee\b|\brm\b|\bmv\b|\bcp\b|\btruncate\b|\bsed\s+-i|\bperl\s+-pi|\bchmod\b|\bln\b|\bgit\s+(?:rm|mv|checkout\s+--)|\bpython3?\b.*open\()"

REMOTE_EXEC = re.compile(
    r"\b(curl|wget|iwr|Invoke-WebRequest)\b[^|;&]*\|\s*(sudo\s+)?(ba|z|da|k)?sh\b"
    r"|\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(python3?|node|perl|ruby|php)\b"
    r"|\b(ba|z)?sh\s+<\(\s*(curl|wget)\b"
    r"|\biex\s*\(\s*(iwr|Invoke-WebRequest|New-Object\s+Net\.WebClient)",
    re.IGNORECASE,
)

PUSH_DEFAULT = re.compile(
    r"\bgit\s+push\b(?=[^;&|]*\b(main|master|HEAD:main|HEAD:master)\b)", re.IGNORECASE
)
PUSH_FORCE = re.compile(r"\bgit\s+push\b[^;&|]*\s(--force\b|-f\b|--force-with-lease\b)")


def unlocked() -> bool:
    return os.environ.get("SECURITY_SENTINEL_UNLOCK") == "1"


def is_protected(path: str) -> bool:
    if not path:
        return False
    norm = path.replace("\\", "/")
    return any(p.search(norm) for p in PROTECTED_PATTERNS)


def block(msg: str) -> None:
    sys.stderr.write(
        "Security Sentinel blocked this action: "
        + msg
        + " See security/SECURITY_POLICY.md. If the owner explicitly approves, "
        "they can restart Claude Code with SECURITY_SENTINEL_UNLOCK=1 "
        "(protected files only).\n"
    )
    sys.exit(2)


def check_file_tool(tool_input: dict) -> None:
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if is_protected(path) and not unlocked():
        block(f"'{path}' is a protected security file and cannot be modified by the agent.")


def check_bash(command: str) -> None:
    if REMOTE_EXEC.search(command):
        block("piping remote content into an interpreter (e.g. `curl ... | sh`) is not allowed.")
    if PUSH_FORCE.search(command):
        block("force pushes are not allowed.")
    if PUSH_DEFAULT.search(command):
        block("pushing to the default branch is not allowed; push a security/<name> branch and open a PR.")
    if not unlocked():
        for pat in PROTECTED_PATTERNS:
            # Look for a protected path mentioned alongside a write verb.
            for m in re.finditer(
                r"[\w./\\-]*(SECURITY_POLICY\.md|security-sentinel-[\w.-]+\.ya?ml|\.security-sentinel-lock)",
                command,
                re.IGNORECASE,
            ):
                if re.search(WRITE_VERBS, command) and pat.search(m.group(0).replace("\\", "/")):
                    block(f"shell command would modify protected file '{m.group(0)}'.")


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # never break the session on malformed input
    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        check_file_tool(tool_input)
    elif tool == "Bash":
        check_bash(tool_input.get("command", "") or "")
    sys.exit(0)


if __name__ == "__main__":
    main()
