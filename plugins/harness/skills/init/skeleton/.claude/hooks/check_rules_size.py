#!/usr/bin/env python3
"""PostToolUse nudge: warn when a governed instruction file exceeds the soft line budget.

Governed files = `.claude/rules/*.md` and any `CLAUDE.md`. Advisory only (never blocks) —
detection is deterministic, the fix (split / dedupe / compress) is judgment. See
`.claude/rules/workflow.md` -> "File size budget".

This file is project-agnostic; it ships verbatim in every project the harness template
scaffolds. Tune BUDGET below if a project wants a different soft cap.
"""
import json
import os
import sys

BUDGET = 150  # soft line budget per instruction file


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return

    fp = (data.get("tool_input") or {}).get("file_path") or ""
    if not fp:
        return

    norm = fp.replace("\\", "/")
    governed = (".claude/rules/" in norm and norm.endswith(".md")) or (
        os.path.basename(norm) == "CLAUDE.md"
    )
    if not governed:
        return

    try:
        with open(fp, "r", encoding="utf-8") as f:
            n_lines = sum(1 for _ in f)
    except OSError:
        return

    if n_lines <= BUDGET:
        return

    name = os.path.basename(norm)
    msg = (
        f"[rules-size] {name} is now {n_lines} lines (soft budget {BUDGET}). "
        "REVIEW THE WHOLE FILE -- never just shave the line you added. Then apply "
        "workflow.md -> 'File size budget' (four options, in this order): "
        "(1) RELOCATE -- a section owned by another rules file's topic moves there "
        "(leave a one-line pointer). (2) SPLIT -- a distinct sub-topic gateable by its "
        "own paths: glob moves to a new path-scoped rules file (e.g. a subsystem's "
        "deep-rules file). (3) ABSTRACT -- if several concrete entries are instances of "
        "one generative principle, state the principle and delete the examples it "
        "regenerates (e.g. 'nearest existing analog', '1:1 correspondence'); keep only "
        "examples carrying a non-derivable why. (4) COMPRESS -- dedupe/tightening only: "
        "AskUserQuestion, then invoke claude-md-management:claude-md-improver on this "
        "file. (1)-(3) are your judgment; (4) is delegated. Advisory: a tight "
        "single-topic file slightly over is fine."
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": msg,
                }
            }
        )
    )


if __name__ == "__main__":
    main()
