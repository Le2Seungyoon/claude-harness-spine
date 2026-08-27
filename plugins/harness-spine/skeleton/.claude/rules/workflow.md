# Workflow

## Planning

- Use plan mode for work that changes module/layer boundaries or affects 3+ files.
- If you hit an unexpected blocker mid-implementation, stop and redesign — don't force it through.
- Before a non-trivial change, ask once "is there a more elegant way?". If it's hacky, do it properly.
- In pre-finalized stages (config values still undecided), only make values easy to change via
  config — don't hard-couple logic to a specific value.

## Superpowers (High-Impact Tasks)

For a **new feature** or a **3+ file patch**, before writing code use `AskUserQuestion` to ask
whether to apply a superpowers workflow: `brainstorming` (lock intent/design) /
`test-driven-development` (failing test first) / `verification-before-completion` (gather evidence
before done). If selected, actually invoke it with the `Skill` tool. Skip for trivial edits /
1–2 lines / doc-only changes.
<!-- FILL: remove this section if the superpowers plugin is not installed for this project. -->

## Bug Fixing

- Investigate → fix → verify. Reproduce first; point at logs/errors directly rather than
  guessing from symptoms.
- If a fix feels hacky, implement the proper solution instead. Skip this for simple, obvious
  one-liners.

## Task Completion

- Don't mark done without proving behavior.
- Bugs: reproduce → fix → confirm it's gone.
- After a structural change, compare behavior against the previous state (tests + a real run).
- Type checks and test suites verify code correctness, not feature correctness. When the change
  has a runtime surface (a UI, a CLI, an endpoint, a running service), exercise it directly — start
  it and drive the actual path — before declaring done, not just its automated tests.
- **A quiet checker is not evidence.** A hook or linter can be silent because it passed, or because
  it never ran, or because the last instance fell below its threshold. Confirm by searching the
  source (`enforcement.md` → An empty result is not proof).

## Self-review

At the end of every task, before declaring done: work `self-review.md` — ① this project's
gates, and ② the judgments no gate can make (escape hatches, allowlist lines, re-invented
equivalents, both halves of a mirror). Write the answers where the task is reported.

## Capturing Learnings

At the end of every task, before declaring done: **did anything reusable/recurring emerge this
session?** If so, don't leave it in chat — capture it.

Route first — the layer decides whether the rule ever runs (`enforcement.md` → Four layers):
- Anyone touching this repo (convention · contract · gotcha) → a committed `.claude/rules/` file.
- This machine/session only (local path, personal taste, one-off setup) → auto memory.
- Deterministic, and checkable on this session's edits → a **hook** (+ its test).
- Must hold on every authoring path (IDE · teammate · another agent) → a **test/CI invariant**;
  absolute in every context → `permissions.deny`. Contracts and gate promotion: `enforcement.md`.

Qualifies for a rules file:
- A new convention/pattern decided this time (naming, structure, defaults).
- Non-obvious design rationale.
- A contract (an interface/protocol other modules depend on) or a change to one.
- A gotcha/footgun that bit us and will bite again.
- A missing step in an existing "how to add …" checklist.

Do not capture: one-off facts specific to this task (already in code/tests/commit), or anything
code/git already makes self-evident.

Format:
- Write instruction files (CLAUDE.md, `.claude/rules/*`) in **English** — clarity + tokens.
- Pick the file by topic; **read the target file first** and match its existing style/format —
  update the relevant section, don't blindly append a duplicate.
- Keep it terse and actionable — rules, not prose narrative. Stage it with the code change.
- **Prune as you add**: when adding a rule, check whether an existing item is now dead —
  absorbed into a default, or promoted to enforcement (test / `settings.json` / `permissions.deny`)
  — and delete it in the same change. A gotcha that code/config already blocks is noise.

## File size budget (keep each instruction file dense)

Gotchas accumulate; a bloated rules file loads in full every session and dilutes signal. Soft
budget: **~150 lines per file** (CLAUDE.md and each `.claude/rules/*.md`). A PostToolUse hook
(`.claude/hooks/check_rules_size.py`, wired in `settings.json`) nudges when an edit crosses it.
Detection is deterministic; the response is a **four-option judgment, in priority order** — review
the whole file, never just shave the line you added:

- **① Relocate — you decide.** If a section is really another rules file's topic (e.g. an
  architectural invariant sitting in `coding-patterns.md`), move it to the file that owns it and
  leave a one-line pointer behind. Content ownership beats file convenience. Do this first.
  <!-- FILL: record precedents as they happen ("<section> moved <fileA> → <fileB>"). -->
- **② Split — you decide (the plugin can't).** If the overflow is a distinct sub-topic a `paths:`
  glob can gate, move it into its own path-scoped rules file (front-matter `paths:`) and
  cross-reference from the parent. Don't split just to hit the number.
- **③ Abstract — you decide (highest leverage).** If several concrete items are instances of one
  generative principle, state the principle and delete the examples it regenerates. Keep only
  examples with a non-derivable why (a gotcha).
- **④ Compress / dedupe / currency — delegate to the plugin.** `AskUserQuestion` whether to clean
  up, then invoke `claude-md-management:claude-md-improver` via `Skill`, **naming the over-budget
  file** (its discovery only scans `CLAUDE.md`). It audits conciseness / duplication / currency.

**A generated file takes none of the four.** Hand-edits and compression skills are both discarded
by the next regeneration; the only lever is the generator — narrow its scope, or cap the entries
and have it state how many were truncated (`enforcement.md` → Keeping a generated artifact alive).

A tight single-topic file slightly over budget is fine — these are levers, not a mandate to hit
the number.

## Rule Conflicts & Harness Improvement

The harness (CLAUDE.md · `.claude/rules/` · settings) is not a static document — it's a device
that keeps growing and getting corrected.

- **Rule ↔ request conflict**: if a user request contradicts the rules — don't silently follow the
  rule and ignore the request, and don't silently break the rule. **Surface the conflict**: name
  which item in which file it conflicts with and why, and confirm which takes precedence. User
  instructions override rules, but present the rationale so the reason the rule exists isn't lost.
- **Rule wrong or stale**: if during work a rule doesn't match reality (code · server · convention),
  fixing that rule is part of the task. Propose/apply the update immediately and tell the user.
- **Screen every rule revision with one question**: *was the rule wrong to begin with, or did this
  change just make it inconvenient?* Only the first justifies rewriting it. The second is the rule
  doing its job, and editing it there is how a harness argues itself out of its own constraints.
- **An unsupported claim is an assumption.** If a statement in the harness lives only in the
  sentence that asserts it — no test, no generated artifact, no command that re-checks it — mark it
  as an assumption or delete it. A self-growing harness accumulates its own folklore otherwise.
- **Improving the harness itself**: if you spot a harness defect — a missing trigger, a dead rule
  (code/config already blocks it), a wrong path-gate, a bloated CLAUDE.md — refine the harness
  alongside Capturing Learnings.

## Verification Commands

```bash
{{TEST_COMMAND}}      # must pass before declaring done
```
<!-- FILL: project verification commands (test / build / e2e / lint). -->
