---
name: init
description: Scaffold the Claude Code harness (CLAUDE.md + .claude/rules + settings hooks) into the current project. Use when bootstrapping/setting up the harness in a new or existing repo, or when the user asks to "init harness", "set up claude rules", or "scaffold the harness".
---

# init — bootstrap the harness into a project

Scaffolds a project-agnostic Claude Code harness (instruction files + rules + enforcement hooks)
into the current repository, fills what it can **detect**, **interviews** for the rest, and
**reports** the `<!-- FILL -->` markers left for the human.

The files to copy live in `skeleton/` next to this SKILL.md — this skill's base directory
(`${CLAUDE_PLUGIN_ROOT}/skills/init/skeleton/`). **Never invent harness content — copy from
`skeleton/` and substitute.**

## Checklist (create a todo per step)

### 1. Safety / pre-flight
- Confirm the CWD is the project root the user wants to scaffold.
- Check for existing harness files (`CLAUDE.md`, `.claude/rules/`, `.claude/settings.json`). If any
  exist, **STOP and ask** per file: merge / overwrite / skip. Never clobber an existing `CLAUDE.md`.
- `git branch --show-current` and follow the Branch-First convention (offer a branch) — this step
  writes files.

### 2. Detect (fill what the repo already tells you — read, don't ask)
- **VCS host + default branch**: `git remote -v` (github.com / bitbucket.org / gitlab.com / other);
  default branch via `git symbolic-ref refs/remotes/origin/HEAD` (fallback `main`).
- **Package manager + commands**: `uv.lock`/`pyproject.toml` (uv), `package.json` + lockfile
  (npm/pnpm/yarn), `go.mod`, `Cargo.toml`, `poetry.lock`, `requirements.txt`, … → derive
  `{{SETUP_COMMAND}}` and `{{TEST_COMMAND}}`.
- **Source & test globs**: infer `{{SOURCE_GLOB}}` (`src/**`, `include/**`, `app/**`, …) and
  `{{TEST_GLOB}}` (`tests/**`, …) from the tree.

### 3. Interview (ONE question at a time, ONLY for what you couldn't detect)
- `{{PROJECT_NAME}}` (default: repo dir name) and `{{PROJECT_ONE_LINER}}` (domain, 2-3 lines).
- `{{COMMIT_LANGUAGE}}` / commit style (default: English, single-line subject, no AI attribution).
- Configuration-table surfaces: `{{SECRETS_EXAMPLES}}`, `{{TUNABLES_EXAMPLES}}`,
  `{{CONFIG_LOCATION}}`, `{{DEPS_FILES}}`.
- Whether the **superpowers** plugin is installed (keep or delete that `workflow.md` section).
- Confirm the detected package manager / test command.
- Whether `CLAUDE.md` → Stack table is worth keeping (versions to pin, cross-repo sync notes,
  dependency-add bar) — fill it or delete the section.

### 4. Copy + fill
- Copy everything under `skeleton/` into the project root, preserving paths (`CLAUDE.md`,
  `.claude/rules/*.md`, `.claude/settings.json`, `.claude/hooks/check_rules_size.py`).
- Substitute all `{{VARS}}` with detected/interviewed values across the copied files.
- **PR-gate hook variant** (`settings.json` + the `git-workflow.md` prose):
  - The shipped default gates **`git push`** (works for any host). Keep it for Bitbucket / GitLab /
    when `gh` is absent.
  - If host is GitHub **and** `gh` is installed **and** the user prefers CLI PRs: swap the gate to
    **`gh pr create`** — change the grep to `gh pr create`, the `if` to `Bash(gh pr create:*)`, and
    the statusMessage/reason wording to "before PR" (reason template in the design doc).
  - If the default branch isn't `main`, replace `main` in the hook command accordingly.
- **Permissions**: populate `settings.json` `permissions.allow`/`deny` for the detected package
  manager (e.g. uv → allow `Bash(uv sync:*)`, `Bash(uv run:*)`; deny `Bash(uv pip install:*)`,
  `Write(uv.lock)`, `Edit(uv.lock)`). Leave empty if unsure rather than guessing.
- **enabledPlugins**: declare team-mandatory plugins in `settings.json` `enabledPlugins` ONLY from
  official/default-known marketplaces (teammates get an auto-install prompt on open). Never put
  personal-marketplace plugins — including this harness plugin itself — into project settings:
  teammates without that marketplace only get "unknown marketplace" warnings.

### 5. Verify
- `python3 -c "import json; json.load(open('.claude/settings.json'))"` — valid JSON.
- Pipe a sample over-budget input through `.claude/hooks/check_rules_size.py` and confirm it nudges;
  pipe a `git push` sample through the PR-gate command and confirm allow/deny behaves; pipe a
  `git commit -m "... Co-Authored-By: ..."` sample through the commit-attribution hook and confirm
  it denies (and that a trailer-free commit passes).
- Grep for leftover `{{...}}` — none should ship raw. Any value you couldn't fill → convert to a
  `<!-- FILL -->` marker instead of leaving a bare `{{VAR}}`.

### 6. Report
- List every remaining `<!-- FILL: ... -->` marker (file + line) as a checklist for the human —
  especially the ② stub rules (`coding-patterns.md`, `architecture.md`, `testing.md`) whose deep
  project rules only the human / a later session can write.
- Remind: add topic/tool rules files (a service integration, a framework) as the project grows;
  keep each under the ~150-line budget (the `check_rules_size.py` hook nudges when crossed).

## Notes
- The harness is intentionally minimal — ① meta-process kept, ② stubbed, ③ tool-specific rules
  dropped. Grow it per-project via Capturing Learnings, not by bloating the template.
- Everything is prose + hooks; there is no runtime state. Re-running `init` on an initialized repo
  should diff against existing files and offer only additive changes (per step 1).
