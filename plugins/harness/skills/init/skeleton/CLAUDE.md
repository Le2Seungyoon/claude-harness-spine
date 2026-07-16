# {{PROJECT_NAME}}

{{PROJECT_ONE_LINER}}
<!-- FILL: 2-3 lines on what this project does and its domain. -->

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

## Rules

Read the relevant rule in `.claude/rules/` before writing code:

| File | When to read |
|------|--------------|
| `git-workflow.md` | before any task that changes files |
| `workflow.md` | when planning a feature or a patch touching 3+ files |
| `coding-patterns.md` | when touching source (`{{SOURCE_GLOB}}`) |
| `architecture.md` | when working on new modules / layer boundaries |
| `testing.md` | when writing/editing tests |
<!-- FILL: add rows for topic/tool rules files you create (e.g. a service integration). -->

When reusable knowledge emerges (a new convention, checklist, design decision, contract, or
recurring gotcha), record it in the matching `.claude/rules/` file — not in personal memory.

**At the end of every task, before declaring done**: scan for anything reusable/recurring from
this session and record it in the right rules file. See `workflow.md` → Capturing Learnings.

If a rule conflicts with a request, or a rule is out of sync with reality, don't silently paper
over it — surface it to the user (see `workflow.md` → Rule Conflicts & Harness Improvement).

## References

<!-- FILL: pointers to design docs / specs / dashboards, or delete this section. -->
