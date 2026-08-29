#!/usr/bin/env python3
"""PostToolUse nudge: warn when a governed instruction file exceeds the soft line budget.

Contract — this hook is the template every other hook in this project follows.
See `.claude/rules/enforcement.md` -> Hook contracts.

  Event     PostToolUse only. It ADVISES and never denies; denial belongs to PreToolUse.
  Governed  `.claude/rules/*.md` and any `CLAUDE.md`. Fires on Write / Edit / MultiEdit — all
            three carry `tool_input.file_path`; the matcher lives in `settings.json`.
  Silence   Means exactly one thing: the file was read and is within budget. Anything that
            stopped the check from running says so in one line instead of passing quietly,
            so "all clear" and "never looked" stay distinguishable.
  Failure   Never blocks, never raises. An unreadable payload or file exits 0 with a note.
  Advisory  Detection is deterministic; the fix (relocate / split / abstract / compress) is
            judgment, so this reports and lets the author choose — see `workflow.md` ->
            File size budget.
  Tests     `test_check_rules_size.py`, beside this file: must-block and must-pass halves.

This file is project-agnostic; it ships verbatim in every project the harness scaffolds.
Tune BUDGET below if a project wants a different soft cap.
"""
import json
import os
import sys

BUDGET = 150  # soft line budget per instruction file


def emit(message: str) -> None:
    """Speak to the session. The only channel this hook has; it never changes the outcome."""
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": message,
                }
            }
        )
    )


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        emit("[rules-size] could not read the hook payload — size budget NOT checked.")
        return

    fp = (data.get("tool_input") or {}).get("file_path") or ""
    if not fp:
        return  # not a file-writing tool call; nothing this hook governs

    norm = fp.replace("\\", "/")
    governed = (".claude/rules/" in norm and norm.endswith(".md")) or (
        os.path.basename(norm) == "CLAUDE.md"
    )
    if not governed:
        return

    try:
        with open(fp, "r", encoding="utf-8") as f:
            n_lines = sum(1 for _ in f)
    except OSError as exc:
        emit(f"[rules-size] could not read {norm} ({exc.strerror}) — size budget NOT checked.")
        return

    if n_lines <= BUDGET:
        return  # checked, and it passes -- the one thing silence is allowed to mean

    name = os.path.basename(norm)
    emit(
        f"[rules-size] {name} is now {n_lines} lines (soft budget {BUDGET}). "
        "REVIEW THE WHOLE FILE -- never just shave the line you added. Apply "
        "workflow.md -> 'File size budget', in order: (1) RELOCATE -- a section that's "
        "really another rules file's topic belongs there; move it and leave a one-line "
        "pointer. (2) SPLIT is your judgment -- if a distinct sub-topic can be gated by a "
        "paths: glob, move it to its own rules file (may drop this file under budget). "
        "(3) ABSTRACT -- if several concrete items are instances of one generative "
        "principle, state the principle and delete the examples it regenerates; keep only "
        "examples with a non-derivable why. (4) COMPRESS/dedupe/currency -- delegate: "
        "AskUserQuestion then invoke the claude-md-management:claude-md-improver skill on "
        "this file. Advisory: a tight single-topic file slightly over is fine."
    )


if __name__ == "__main__":
    main()
