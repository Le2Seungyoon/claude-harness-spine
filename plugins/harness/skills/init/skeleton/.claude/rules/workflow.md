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

## Task Completion

- Don't mark done without proving behavior.
- Bugs: reproduce → fix → confirm it's gone.
- After a structural change, compare behavior against the previous state (tests + a real run).

## Capturing Learnings

At the end of every task, before declaring done: **did anything reusable/recurring emerge this
session?** If so, don't leave it in chat — capture it.

Route first — **team rule vs personal/environment vs deterministic enforcement**:
- Applies to anyone touching this repo (convention · contract · gotcha) → a committed
  `.claude/rules/` file.
- Specific to this machine/session/environment (local path, personal taste, one-off setup) →
  auto memory (not a shared rule).
- Absolute and deterministically enforceable in every context → `settings.json` /
  `permissions.deny` (not prose). Prose is for context-dependent advice (boundary:
  `git-workflow.md` → Protected Commands).

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
Detection is deterministic. When the nudge fires, **review the whole file — never just shave the
line you added.** Then pick from **four options, in this order**:

- **① Relocate — you decide.** If a section belongs to another existing rules file's topic, move it
  to its owner file and leave a one-line pointer. Content ownership beats file convenience.
  <!-- FILL: record precedents as they happen ("<section> moved <fileA> → <fileB>"). -->
- **② Split — you decide (the plugin can't).** If the overflow is a distinct sub-topic a `paths:`
  glob can gate, move it into its own path-scoped rules file (front-matter `paths:`) and
  cross-reference from the parent. Don't split just to hit the number; a tight single-topic file
  slightly over is fine.
- **③ Abstract — you decide (highest leverage).** If several concrete entries are instances of one
  generative principle, state the principle and delete the examples it now regenerates — losing
  specifics is acceptable when the principle reliably reproduces them (e.g. "find the nearest
  existing analog", "1:1 correspondence"). Keep an example only if it carries a non-derivable why
  (a gotcha).
- **④ Compress / dedupe / currency — delegate to the plugin.** For tightening prose, removing
  redundancy, and stale-content trimming: `AskUserQuestion` whether to clean up, then invoke the
  `claude-md-management:claude-md-improver` skill via `Skill`, naming the over-budget file (its
  default discovery only scans `CLAUDE.md`, so point it at the `.claude/rules/*.md` file).
  Note the plugin only compresses wording — ①②③ are judgment calls it does not make.

## Rule Conflicts & Harness Improvement

The harness (CLAUDE.md · `.claude/rules/` · settings) is not a static document — it's a device
that keeps growing and getting corrected.

- **Rule ↔ request conflict**: if a user request contradicts the rules — don't silently follow the
  rule and ignore the request, and don't silently break the rule. **Surface the conflict**: name
  which item in which file it conflicts with and why, and confirm which takes precedence. User
  instructions override rules, but present the rationale so the reason the rule exists isn't lost.
- **Rule wrong or stale**: if during work a rule doesn't match reality (code · server · convention),
  fixing that rule is part of the task. Propose/apply the update immediately and tell the user.
- **Improving the harness itself**: if you spot a harness defect — a missing trigger, a dead rule
  (code/config already blocks it), a wrong path-gate, a bloated CLAUDE.md — refine the harness
  alongside Capturing Learnings.

## Verification Commands

```bash
{{TEST_COMMAND}}      # must pass before declaring done
```
<!-- FILL: project verification commands (test / build / e2e / lint). -->
