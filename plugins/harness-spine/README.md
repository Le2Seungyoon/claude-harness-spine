# harness-spine

Scaffold a project-agnostic Claude Code harness — `CLAUDE.md` + `.claude/rules/*` + enforcement
hooks — into any repo, and reconcile it later as this plugin's skeleton evolves.

## Usage

```
/harness-spine:init      # repo has no harness yet
/harness-spine:update    # repo has one; pull in what the skeleton has since gained
```

`init` detects what your repo already reveals (VCS host, package manager, test command, source
globs), interviews you for the rest, copies the skeleton in, and reports the `<!-- FILL -->`
markers left for you to complete.

`update` takes the repo's harness **as it is** — no version stamp needed — classifies every skeleton
file as *missing / pristine / diverged / project-only*, and proposes the difference section by
section. Rules you have since written are never overwritten; conflicts are reported, not resolved.

## Contents

| Component | Description |
|-----------|--------------|
| `skills/init/SKILL.md` | Scaffold: detect → interview → copy → fill → verify → report |
| `skills/update/SKILL.md` | Reconcile: classify → section-level proposals → budget check → verify → report |
| `skeleton/CLAUDE.md` | Router skeleton (optional Stack table / Commands / Configuration / Rules / Enforcement hooks summary / References) |
| `skeleton/.claude/rules/workflow.md`, `git-workflow.md` | Meta-process rules, kept generic |
| `skeleton/.claude/rules/enforcement.md` | Routing (prose / hook / test / deny), hook contracts, what to measure before a deny |
| `skeleton/.claude/rules/coding-patterns.md`, `architecture.md`, `testing.md` | Tech-stack rules, shipped as stubs to fill per project |
| `skeleton/.claude/rules/self-review.md` | End-of-task checklist — the gates to run, and the judgments no gate can make |
| `skeleton/.claude/settings.json` | PR-gate + commit-attribution + file-size-budget hooks |
| `skeleton/.claude/hooks/check_rules_size.py` | The file-size nudge, project-agnostic — the contract template for later hooks |
| `skeleton/.claude/hooks/test_check_rules_size.py` | Its test: a hook is code, and ships with must-block + must-pass halves |
| `skeleton/.claude/scripts/check_rule_links.py` | Scanner: every file a rules file points at must exist — the test-layer half hooks cannot cover |
| `skeleton/.claude/scripts/test_check_rule_links.py` | Its test, weighted toward must-pass: the scanner reads prose |

`skeleton/` sits at the plugin root, not inside a skill: both skills read it and neither owns a
second copy.

## Which skill

`init` refuses to clobber an existing harness and hands off to `update`; `update` refuses a repo
with no harness and hands back to `init`. Neither is the built-in `/init`, which writes a
`CLAUDE.md` from a codebase scan and knows nothing about this skeleton.
