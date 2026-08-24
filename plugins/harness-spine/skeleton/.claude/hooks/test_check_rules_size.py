#!/usr/bin/env python3
"""Tests for check_rules_size.py — run: python3 test_check_rules_size.py

A hook is code, so it ships with a test (`enforcement.md` -> Hook contracts). Both halves
matter: the must-block half proves the check fires, the must-pass half is what keeps false
positives from creeping in. A test that only ever asserts "it blocked" cannot notice the day
the hook starts blocking everything.

Stdlib only, no test runner: the hook must be verifiable in a freshly scaffolded repo that
has no dev dependencies installed yet.
"""
import json
import os
import subprocess
import sys
import tempfile

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_rules_size.py")
BUDGET = 150

failures = []


def run(payload, cwd):
    """Feed the hook a payload; return (stdout, returncode)."""
    proc = subprocess.run(
        [sys.executable, HOOK],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=10,  # stays below the hook's own timeout in settings.json
    )
    return proc.stdout.strip(), proc.returncode


def context(stdout):
    """The advisory text the hook emitted, or '' if it stayed silent."""
    if not stdout:
        return ""
    return json.loads(stdout)["hookSpecificOutput"]["additionalContext"]


def check(name, condition, detail=""):
    print(("PASS  " if condition else "FAIL  ") + name + (f"  ({detail})" if detail and not condition else ""))
    if not condition:
        failures.append(name)


def write(root, relpath, n_lines):
    path = os.path.join(root, relpath.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("line\n" * n_lines)
    return relpath


def main():
    with tempfile.TemporaryDirectory() as root:
        over = write(root, ".claude/rules/over.md", BUDGET + 50)
        under = write(root, ".claude/rules/under.md", BUDGET - 50)
        edge = write(root, ".claude/rules/edge.md", BUDGET)  # exactly at budget: still passing
        claude_md = write(root, "CLAUDE.md", BUDGET + 1)
        source = write(root, "src/big_module.py", BUDGET + 500)
        doc = write(root, "docs/2026-01-01-notes.md", BUDGET + 500)

        def payload(path, tool="Write"):
            return {
                "hook_event_name": "PostToolUse",
                "tool_name": tool,
                "tool_input": {"file_path": path},
            }

        # --- must-block half: the nudge has to fire, and say something usable ---
        out, rc = run(payload(over), root)
        msg = context(out)
        check("over-budget rules file nudges", bool(msg), "silent")
        check("nudge reports the real line count", str(BUDGET + 50) in msg, msg[:60])
        check("nudge names the four options", all(w in msg for w in ("RELOCATE", "SPLIT", "ABSTRACT", "COMPRESS")), msg[:60])
        check("nudge cites the rule file it enforces", "workflow.md" in msg, msg[:60])
        check("advisory: exit code stays 0", rc == 0, f"rc={rc}")

        check("over-budget CLAUDE.md nudges", bool(context(run(payload(claude_md), root)[0])))
        for tool in ("Edit", "MultiEdit"):
            # MultiEdit was missing from the settings.json matcher; the payload shape is identical
            check(f"{tool} payload nudges", bool(context(run(payload(over, tool), root)[0])))

        # --- must-pass half: everything below is legitimate work and must stay silent ---
        check("under-budget rules file is silent", context(run(payload(under), root)[0]) == "")
        check("exactly at budget is silent", context(run(payload(edge), root)[0]) == "")
        check("huge source file is not governed", context(run(payload(source), root)[0]) == "")
        check("huge doc file is not governed", context(run(payload(doc), root)[0]) == "")
        check("payload with no file_path is silent", context(run({"hook_event_name": "PostToolUse", "tool_input": {}}, root)[0]) == "")
        check("windows-style path is governed", bool(context(run(payload(over.replace("/", "\\")), root)[0])))

        # --- silence must mean exactly one thing: checked and passing ---
        out, rc = run(payload(".claude/rules/does_not_exist.md"), root)
        msg = context(out)
        check("unreadable file says so instead of passing quietly", "NOT checked" in msg, msg[:60] or "silent")
        check("unreadable file still exits 0", rc == 0, f"rc={rc}")

        proc = subprocess.run([sys.executable, HOOK], input="not json at all", capture_output=True, text=True, timeout=10)
        check("broken payload says so", "NOT checked" in context(proc.stdout.strip()))
        check("broken payload exits 0", proc.returncode == 0, f"rc={proc.returncode}")

    print()
    if failures:
        print(f"{len(failures)} FAILED: " + ", ".join(failures))
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
