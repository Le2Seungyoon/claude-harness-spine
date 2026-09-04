---
name: init
description: Scaffold THIS plugin's harness skeleton (CLAUDE.md + .claude/rules + enforcement hooks) into a repo that has none. Use when the user asks to "init the harness", "set up claude rules", or "scaffold the harness" — not for writing a CLAUDE.md from scratch (that is the built-in /init), and not for a repo that already has the harness (that is the update skill).
---

# init — bootstrap the harness into a project

Scaffolds a project-agnostic Claude Code harness (instruction files + rules + enforcement hooks)
into the current repository, fills what it can **detect**, **interviews** for the rest, and
**reports** the `<!-- FILL -->` markers left for the human.

The files to copy live in the plugin's shared skeleton home, `${CLAUDE_PLUGIN_ROOT}/skeleton/` —
shared with the `update` skill, so **neither skill keeps its own copy**. **Never invent harness
content — copy from `skeleton/` and substitute.**

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
- **"What gets built N times in this project?"** — screens? endpoints? pipeline nodes? reports?
  Whatever they name is what will be copied instead of shared, and later defines the signature a
  counting check would have to match. Record the answer in `coding-patterns.md` → canonical analogs.
- **"Where does a shared one live?"** — for each kind they named, the directory/module it gets
  promoted to. Fills `architecture.md` → Shared homes. A kind with no home is the one that gets
  copied; if they don't have an answer yet, leave the row with an explicit "no home yet".

### 4. Copy + fill
- Copy everything under `skeleton/` into the project root, preserving paths (`CLAUDE.md`,
  `.claude/rules/*.md` — including `enforcement.md` —, `.claude/settings.json`,
  `.claude/hooks/check_rules_size.py` **and its `test_check_rules_size.py`**,
  `.claude/scripts/check_rule_links.py` **and its `test_check_rule_links.py`**).
- Substitute all `{{VARS}}` with detected/interviewed values across the copied files.
- **PR-gate hook variant** (`settings.json` + the `git-workflow.md` prose):
  - The shipped default gates **`git push`** (works for any host). Keep it for Bitbucket / GitLab /
    when `gh` is absent.
  - If host is GitHub **and** `gh` is installed **and** the user prefers CLI PRs: swap the gate to
    **`gh pr create`** — change the grep to `gh pr create`, the `if` to `Bash(gh pr create:*)`, and
    the statusMessage/reason wording to "before PR" (reason template in the design doc).
  - If the default branch isn't `main`, replace `main` in the hook command accordingly.
- **Permissions — leave `allow` empty by default.** Claude Code already allows the common
  read-only commands, so most hand-written entries are dead weight: in a measured audit, 104 of 144
  accumulated rules had never matched anything. Add an `allow` entry only for a command the user is
  actually being prompted for repeatedly, and prefer the shape the parser can read — prompts come
  from constructs it cannot statically parse (`for` loops, `$var`, `$( )`), which no allow-list
  entry can pre-approve anyway.
- **`deny` shapes that don't work**: `Write(<path>)` is accepted but never matches — file-write
  denials must be written as `Edit(<path>)`. Verify any deny you add by triggering it once; an
  entry that never fires is worse than none, because it reads as protection.
- **enabledPlugins**: declare team-mandatory plugins in `settings.json` `enabledPlugins` ONLY from
  official/default-known marketplaces (teammates get an auto-install prompt on open). Never put
  personal-marketplace plugins — including this harness plugin itself — into project settings:
  teammates without that marketplace only get "unknown marketplace" warnings.

### 5. Verify
- `python3 -c "import json; json.load(open('.claude/settings.json'))"` — valid JSON.
- `python3 .claude/hooks/test_check_rules_size.py` — all checks pass. It covers both halves
  (must-block *and* must-pass); a hook test with only the must-block half cannot catch false positives.
- `python3 .claude/scripts/test_check_rule_links.py` — all checks pass. Then run
  `python3 .claude/scripts/check_rule_links.py` on the filled tree: it must print
  `RULE_LINKS_CLEAN`. Substitution can leave a pointer aimed at a file this project deleted.
- Wire `check_rule_links.py` into the project's own test suite before finishing — as a shipped
  script nothing calls, it is inert (`enforcement.md` -> Four layers).
- Pipe a sample over-budget input through `.claude/hooks/check_rules_size.py` and confirm it nudges;
  pipe a `git push` sample through the PR-gate command and confirm allow/deny behaves; pipe a
  `git commit -m "... Co-Authored-By: ..."` sample through the commit-attribution hook and confirm
  it denies (and that a trailer-free commit passes).
- Grep for leftover `{{...}}` — none should ship raw. Any value you couldn't fill → convert to a
  `<!-- FILL -->` marker instead of leaving a bare `{{VAR}}`.

### 6. Report
- List every remaining FILL marker (file + line) as a checklist for the human. **Grep both forms**
  — `grep -rn -e '<!-- FILL' -e '# FILL' CLAUDE.md .claude/` — because markers in a `.py` file
  carry the comment form and a `<!-- FILL -->`-only grep silently misses them.
- Especially: the ② stub rules (`coding-patterns.md`, `architecture.md`, `testing.md`) whose deep
  project rules only the human / a later session can write; `self-review.md` ① — an unfilled
  gates table leaves half that checklist inert; and `check_rule_links.py` -> `SEARCH_DIRS` — if
  this project's source is not at the repo root, an unfilled slot makes that checker report real
  files as broken pointers, which is how a check gets deleted rather than fixed.
- Remind: add topic/tool rules files (a service integration, a framework) as the project grows;
  keep each under the ~150-line budget (the `check_rules_size.py` hook nudges when crossed).
- **State plainly what was not installed: there is no counting layer.** The harness ships the
  convention ("extract on the second occurrence") and the place to put it (Shared homes), but
  nothing that counts occurrences — that detector has to be defined against this project's own
  material (a markup string? an AST shape? a query?) and cannot be inherited.
- **Warn before anyone builds one**: measure its false-positive rate over the existing tree first,
  and gate one occurrence later than the convention asks. A candidate signature measured elsewhere
  ran at 12.5% / 25% / 75% false positives depending on the shape chosen — promoting such a check
  straight to `permissions.deny` is how a hook gets switched off for good. See `enforcement.md` →
  Before promoting a check to deny.

## Notes
- The harness is intentionally minimal — ① meta-process kept, ② stubbed, ③ tool-specific rules
  dropped. Grow it per-project via Capturing Learnings, not by bloating the template.
- Everything is prose + hooks; there is no runtime state.
- **`init` is for a repo with no harness.** Once a repo has one, reconciling it against a newer
  skeleton is the `update` skill's job — it matches section by section and never overwrites rules
  the project has since written. If step 1 finds an existing harness, offer `update` instead.
