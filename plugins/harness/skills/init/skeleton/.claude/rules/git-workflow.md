# Git Workflow

> Remote: `{{GIT_REMOTE_URL}}` — host `{{GIT_HOST}}` (default branch `{{DEFAULT_BRANCH}}`).
> `.gitignore` is in place.
<!-- FILL: confirm remote host + auth model — the PR gate below depends on the host. -->
<!-- FILL: if README has a human-facing contribution section, add: "README §N mirrors this file — when changing either, sync the other." -->

## Branch-First Rule

For any request that changes files, **before writing the first file**:

1. `git branch --show-current`
2. Ask the user: "You're on `<branch>`. Continue here? / new branch name? / update
   `{{DEFAULT_BRANCH}}` first?"

Don't skip this even for "small" changes or doc edits.

## Branch Naming

- New feature: `feature/<name>` · bug fix: `fix/<name>`

## Protected Commands

Do not run without explicit confirmation: `git checkout`/`switch`, `git pull`/`push`, branch
creation (`checkout -b`, `branch`), `git reset`/`rebase`.

**Why prose and not `permissions.deny`**: this is a collaboration convention that protects a shared
repo — it doesn't hold in every context. A solo admin who authorizes direct git on their own
credentials for one session overrides this list, and that authorization wins. `permissions.deny` is
only for things absolute across every context (person · solo/team · time) — e.g. "never commit
secrets", "never force-push `{{DEFAULT_BRANCH}}`". Context-dependent conventions stay here as prose.

## Commits

- Message style: **{{COMMIT_LANGUAGE}}**, **single-line subject** with the core change only — no
  bullet body, no verbose explanation. Goal: the change is **scannable at a glance** in history.
  <!-- FILL: commit message language & style convention for this project. -->
- **No AI attribution** in commit messages — do NOT append `Co-Authored-By: …` or
  `🤖 Generated with …` trailers. This **overrides** the harness default. (Delete this line if the
  project wants attribution.)
- Default: **stage + diff only, the developer runs `git commit`**. Exception: in a solo session
  where the admin has explicitly authorized direct git, Claude may commit during that session.

## Pull Requests

- **PR title/description: concise, no AI attribution**, no lengthy narrative — same reason as
  commits (scan the diff, not prose). A short summary + key changes + how it was verified is enough.

Before opening a PR, **always incorporate the latest `{{DEFAULT_BRANCH}}`**: `git fetch origin
{{DEFAULT_BRANCH}} && git merge origin/{{DEFAULT_BRANCH}}`. Resolve conflicts locally first, not at
PR time.

**PR-gate hook (host-dependent — `init` wires the matching variant into `settings.json`):**
- **GitHub + `gh` CLI**: the PR is created from the CLI, so the gate blocks `gh pr create` when
  `origin/{{DEFAULT_BRANCH}}` isn't merged into the current branch.
- **Bitbucket / GitLab / no `gh`**: the PR is opened in the web UI, so the CLI gate lives on
  `git push` instead (blocks push when `origin/{{DEFAULT_BRANCH}}` isn't merged). The shipped
  `settings.json` ships this **`git push` variant by default** (works for any host; a
  `{{DEFAULT_BRANCH}}` push passes since it's its own ancestor).

The hook fetches first, is a no-op before git init, and can't gate a web-UI PR — so keep "merge
`{{DEFAULT_BRANCH}}` first" as a **convention** too. (merge-before-PR is a context-independent
invariant, so it's enforced at the CLI gate rather than left as prose — see `Protected Commands`
"why prose".)
