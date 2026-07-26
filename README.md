# claude-harness-spine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A reusable, project-agnostic **Claude Code harness** — `CLAUDE.md` + `.claude/rules/*` +
enforcement hooks — distributed as a Claude Code plugin and scaffolded into any repo by one command.

## Features

- **Self-growing rules** — gotchas and conventions discovered mid-task get written into
  `.claude/rules/*` at the end of every task, instead of staying lost in chat.
- **Auto file-size enforcement** — a hook nudges the moment a rules file crosses ~150 lines,
  triggering a relocate / split / abstract / compress pass (in that priority order) before it
  turns into noise.
- **Self-correcting** — a rule that's gone stale or wrong gets fixed as part of the task that
  exposed it, not left to rot.
- **Active edits, not append-only** — updates land in the matching section of the existing file,
  pruning anything now-dead in the same pass.
- **Convention-following by default** — before writing new code, find the nearest existing analog
  and mirror it (naming, layout, imports, return shape) instead of inventing a new pattern.

## Built on the Claude Code Ecosystem

`claude-harness-spine` is a harness that orchestrates Claude Code plugins:

- **[superpowers](https://claude.com/plugins/superpowers)** — the scaffolded `workflow.md` calls
  its `brainstorming` / `test-driven-development` / `verification-before-completion` skills before
  any new feature or 3+ file change. Optional: `init` drops the section if superpowers isn't installed.
- **[claude-md-management](https://claude.com/plugins/claude-md-management)** — once a rules file
  crosses the ~150-line budget, cleanup is delegated to its `claude-md-improver` skill rather than
  hand-trimmed prose.

## Plugins in This Marketplace

| Name | Description | Contents |
|------|-------------|----------|
| [harness](plugins/harness/) | Scaffold a project-agnostic Claude Code harness into any repo | **Skill:** `init` — detect/interview/copy/fill/verify workflow<br>**Skeleton:** `CLAUDE.md`, `.claude/rules/*`, `.claude/settings.json`, `.claude/hooks/check_rules_size.py` |

## What you get

Running `/harness:init` in a project scaffolds:

- `CLAUDE.md` — router skeleton (optional Stack table / Commands / Configuration / Rules /
  Enforcement hooks summary / References).
- `.claude/rules/` — the meta-process spine (`workflow.md`, `git-workflow.md`) plus stubbed
  tech-stack rules (`coding-patterns.md`, `architecture.md`, `testing.md`) to fill per project.
- `.claude/settings.json` — a **PR-gate** hook (blocks push/PR until the default branch is merged),
  a **commit-attribution** hook (denies `git commit` carrying AI-signature trailers), and a
  **file-size-budget** hook (nudges when an instruction file exceeds ~150 lines).
- `.claude/hooks/check_rules_size.py` — the file-size nudge (project-agnostic).

## Install

```
/plugin marketplace add Le2Seungyoon/claude-harness-spine
/plugin install harness@claude-harness-spine
```

## Use

In any project:

```
/harness:init
```

## Layout

```
├── .claude-plugin/marketplace.json          # declares this repo's plugins
└── plugins/
    └── harness/
        ├── .claude-plugin/plugin.json        # plugin manifest
        ├── README.md                         # plugin usage doc
        └── skills/
            └── init/
                ├── SKILL.md                  # the bootstrap skill (detect/interview/copy/fill/verify)
                └── skeleton/                 # files copied into the target project
                    ├── CLAUDE.md              # router skeleton (Stack/Commands/Configuration/Rules/Enforcement hooks/References)
                    └── .claude/
                        ├── settings.json      # PR-gate + commit-attribution + file-size-budget hooks
                        ├── hooks/
                        │   └── check_rules_size.py   # the file-size nudge hook
                        └── rules/
                            ├── workflow.md          # planning, bug fixing, capturing learnings, file-size budget
                            ├── git-workflow.md      # branch-first, protected commands, syncing main, PR conventions
                            ├── coding-patterns.md   # stub: style/convention rules to fill per project
                            ├── architecture.md      # stub: layers/boundaries rules to fill per project
                            └── testing.md           # stub: test conventions to fill per project
```
