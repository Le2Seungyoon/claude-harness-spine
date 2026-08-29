# harness

Scaffold a project-agnostic Claude Code harness — `CLAUDE.md` + `.claude/rules/*` + enforcement
hooks — into any repo with one command.

## Usage

```
/harness:init
```

`init` detects what your repo already reveals (VCS host, package manager, test command, source
globs), interviews you for the rest, copies the skeleton in, and reports the `<!-- FILL -->`
markers left for you to complete.

## Contents

| Component | Description |
|-----------|--------------|
| `skills/init/SKILL.md` | The bootstrap skill: detect → interview → copy → fill → verify → report |
| `skills/init/skeleton/CLAUDE.md` | Router skeleton (optional Stack table / Commands / Configuration / Rules / Enforcement hooks summary / References) |
| `skills/init/skeleton/.claude/rules/workflow.md`, `git-workflow.md` | Meta-process rules, kept generic |
| `skills/init/skeleton/.claude/rules/coding-patterns.md`, `architecture.md`, `testing.md` | Tech-stack rules, shipped as stubs to fill per project |
| `skills/init/skeleton/.claude/settings.json` | PR-gate + commit-attribution + file-size-budget hooks |
| `skills/init/skeleton/.claude/hooks/check_rules_size.py` | The file-size nudge, project-agnostic |

## Re-running

`init` is idempotent — running it again on an already-scaffolded repo diffs against what's there
(merge / overwrite / skip per file) instead of clobbering it.
