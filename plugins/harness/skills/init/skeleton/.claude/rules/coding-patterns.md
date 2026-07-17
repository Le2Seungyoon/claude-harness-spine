---
paths:
  - {{SOURCE_GLOB}}
---
# Coding Patterns

## Before writing new code (the rule that generates the rest)

**Find the nearest existing analog and copy its conventions** — file naming, layout, import order,
config loading, return shape. Most rules below are just instances of this. When unsure, don't
invent — read a sibling file. Canonical analogs:

<!-- FILL: list 2-4 canonical files new code should mirror. Shape:
- New <layer> module → the signature pattern of `<path/to/module>` (`<fn>(...)`).
- <External service> access code → `<path/to/client>`.
- Reading config → `<config loader call>`.
- Tests → `tests/<module>/test_*.py` (see `testing.md`).
-->

Prefer a proven library over a hand-rolled implementation. Don't borrow a library's metric/API name
for a different custom implementation.

## Style & configuration

- **Secrets** → environment variables (e.g. `.env` + `os.getenv()` or the language's equivalent).
  Never hardcode or commit secrets.
- **Tunable values** (thresholds · windows · hyperparameters · feature flags) → config, not code.
  No hardcoding.
- Imports/ordering: stdlib → third-party → local, blank-line separated. Type hints on signatures.
  <!-- FILL: adjust to this project's language / style conventions. -->
- Don't couple logic to specific value names/counts — behave off the config lists / thresholds.

## Gotchas (non-obvious — mirroring won't catch these)

<!-- FILL: record project footguns as they bite (capture the "why", not just the "what"). Shape:
- **<config auto-load behavior>** — <what surprises, why it's done this way>.
- **<dependency-management rule>** — <the one correct command; what breaks otherwise>.
- **<a subtle default that flips behavior>** — <the trap + the regression test that pins it>.
-->

> For tests, see `testing.md`. Add topic-scoped rules files (a service/tool rule) as the project
> grows; keep each file under the ~150-line budget (see `workflow.md` → File size budget).
