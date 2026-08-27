# {{PROJECT_NAME}}

{{PROJECT_ONE_LINER}}
<!-- FILL: 2-3 lines on what this project does and its domain. -->

## Stack

<!-- FILL (optional — delete this section if a version table doesn't earn its keep here):
runtime/framework + major versions the project pins to, one line each. Note any cross-repo
version sync this project must respect and the bar for adding a new dependency (e.g. "requires
PR justification"). -->

## Commands

```bash
{{SETUP_COMMAND}}          # reproduce env / install deps
{{TEST_COMMAND}}           # tests (must pass before declaring done)
```
<!-- FILL: key build / run / deploy commands, copy-paste ready. -->

## Configuration

| What | Where |
|------|-------|
| Secrets ({{SECRETS_EXAMPLES}}) | `.env` (copy `.env.template`) |
| Tunable values ({{TUNABLES_EXAMPLES}}) | {{CONFIG_LOCATION}} |
| Dependencies | {{DEPS_FILES}} |
<!-- FILL: rows for this project's real config surfaces. -->

IMPORTANT: Don't hardcode tunable values; put them in config.
<!-- FILL: dependency-management rule (the one correct command) if the project has one. -->

## Docs convention

- **User-facing docs** — `docs/`, written in the team's language, filename `YYYY-MM-DD-<name>.md`
  (the date prefix keeps the project timeline scannable).
  <!-- FILL: set the language / location / naming for this team, or delete if N/A. -->
- **The date prefix encodes how the file is maintained.** Dated = a snapshot of one moment, never
  rewritten. **Undated = a living document, overwritten in place** — and inside one, the three
  parts age differently: current state is *overwritten*, traps and prerequisites *accumulate*, and
  decisions belong in whatever ledger records decisions, not here.
- **Claude-facing instruction files** (this file, `.claude/**/*.md`) — written in **English**.
  Domain string literals (menu labels, error constants, column names) stay in their original
  language — they are data, not prose.

## Rules

Read the relevant rule in `.claude/rules/` before writing code:

| File | When to read |
|------|--------------|
| `git-workflow.md` | before any task that changes files |
| `workflow.md` | when planning a feature or a patch touching 3+ files |
| `coding-patterns.md` | when touching source (`{{SOURCE_GLOB}}`) |
| `architecture.md` | when working on new modules / layer boundaries |
| `testing.md` | when writing/editing tests |
| `self-review.md` | at the end of every task, before declaring done or pushing |
| `enforcement.md` | before adding a rule, a hook, or a deny — it decides which layer it goes in |
<!-- FILL: add rows for topic/tool rules files you create (e.g. a service integration). Mark any
generated file as `<name> (generated — regenerate with <cmd>)`; never hand-edit one. -->

**Write FILL entries as pointers, not inventories.** A hand-copied list ("the components are A, B,
C") is stale by the next commit — name the file or command that *is* the current answer instead.

When reusable knowledge emerges (a new convention, checklist, design decision, contract, or
recurring gotcha), record it in the matching `.claude/rules/` file — not in personal memory.

**At the end of every task, before declaring done**: scan for anything reusable/recurring from
this session and record it in the right rules file. See `workflow.md` → Capturing Learnings.

If a rule conflicts with a request, or a rule is out of sync with reality, don't silently paper
over it — surface it to the user (see `workflow.md` → Rule Conflicts & Harness Improvement).

## Enforcement hooks

`.claude/settings.json` wires: a PR-gate hook (blocks push/PR when `{{DEFAULT_BRANCH}}` isn't
merged in), a commit-attribution deny hook, and a PostToolUse hook nudging on oversized
instruction files. See `git-workflow.md` and `workflow.md` → File size budget for the rationale.
Generators and repo-wide scanners live in `.claude/scripts/`, not `.claude/hooks/` — both ship
with their tests (`enforcement.md` → Where harness code lives).

**Hooks only see this session's edits** — code written in an IDE, by a teammate, or by another
agent passes none of them, and a silent hook is not proof a check ran. Rules that must hold on
every authoring path need a test instead; see `enforcement.md`.

## References

<!-- FILL: pointers to design docs / specs / dashboards, or delete this section. -->
