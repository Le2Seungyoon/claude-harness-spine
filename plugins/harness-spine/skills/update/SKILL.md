---
name: update
description: Reconcile a repo that already has the harness against this plugin's current skeleton — add what is missing, propose section-level changes for files the project has since rewritten, and never overwrite project-authored rules. Use when the user asks to "update the harness", "sync the rules", or after this plugin itself has changed.
---

# update — reconcile an existing harness against the current skeleton

Reads the target repo's harness **as it actually is**, compares it against
`${CLAUDE_PLUGIN_ROOT}/skeleton/`, and lands only what the project is missing — section by
section, with the human deciding each one.

There is no version stamp to trust and none is required: **the repo's current files are the
baseline.** A repo scaffolded before this skill existed, or hand-edited for months, reconciles
the same way as a fresh one.

## What this skill is not

- **Not `init`.** If the repo has no harness, stop and hand off — scaffolding is that skill's job.
- **Not an audit of the project's own rules.** Rules this project wrote are out of scope; the
  question here is only *"what does the skeleton now have that this repo doesn't."*

## Checklist (create a todo per step)

### 1. Pre-flight
- Confirm a harness exists (`CLAUDE.md` **and** `.claude/rules/`). If not → `init`, not this.
- Branch-First: this step writes files. `git branch --show-current` and offer a branch.
- Read the repo's `CLAUDE.md` Rules table first — it names which rules files the project treats as
  live, which is not always what is on disk.

### 2. Classify every skeleton file — before proposing anything

| Class | Test | Action |
|-------|------|--------|
| **Missing** | skeleton has it, repo doesn't | propose the whole file |
| **Pristine** | the repo's copy is still the shipped stub | whole-file replace is safe |
| **Diverged** | the project filled or rewrote it | **never replace** — section-level proposals only |
| **Project-only** | the repo has it, the skeleton doesn't | leave untouched; never delete |

Classify by **reading both files**, not by timestamps or hashes — a stub with one filled `<!-- FILL -->`
is already Diverged, and a reformatted-but-untouched file is still Pristine.

### 3. Reconcile — by section, not by file
- For **Diverged** files, match on heading text and propose only the skeleton sections with no
  counterpart. Where both sides have the section and disagree, **report the conflict; do not
  resolve it silently** — the project's wording usually encodes a decision this skill can't see.
- Never re-insert a `<!-- FILL -->` marker into a slot the project already filled.
- `settings.json` is not text-mergeable. Compare **key by key** — hook matchers, `permissions`,
  `enabledPlugins` — and name each key-level change on its own.
- Hook and script files: if the repo's copy differs, show the diff and **ask which way it should
  go** — a project may have hardened its copy deliberately, or may simply have drifted. Never
  assume either. Where a project keeps a deliberate divergence, have it say so in that file's
  docstring, so the next reconcile reads intent instead of guessing.
- Ask per proposal: **apply / skip / defer**, and record the reason for every skip.

### 4. Budget check — the update itself can blow the budget
- After applying, `wc -l` every instruction file. The skeleton grows over time, and a project that
  already filled a stub can cross the ~150-line budget the moment new sections land on top of it.
- If one crosses: relocate / split / abstract / compress, in that priority order, **in this pass**.

### 5. Verify
- `python3 -c "import json; json.load(open('.claude/settings.json'))"` — valid JSON.
- Run the tests beside every hook and script (`test_*.py`); for any one this update touched, re-run
  it against both a must-block and a must-pass sample. A check that only ever fires is a
  false-positive factory.
- `python3 .claude/scripts/check_rule_links.py` — `RULE_LINKS_CLEAN`. Relocating a section is the
  most common thing this skill proposes, and it is exactly what orphans a pointer.
- `grep -rn '{{' CLAUDE.md .claude/` — no raw `{{VAR}}` may ship.

### 6. Report
- Table of **applied / skipped (+reason) / deferred**, plus every conflict left for the human.
- **"Nothing to apply" is not proof the harness is current.** Section matching fails by design on a
  file the project rewrote in its own words: the change can be real and simply unmatched. Say that
  in the report instead of issuing a clean bill of health.
- **Divergence is the defect, and only a check that sees both sides finds it.** A shipped file
  edited in one repo and not another leaves both looking internally consistent while the same
  nudge tells two teams different things. List every file whose copy differs from the skeleton,
  even the ones left alone on purpose — an unlisted divergence is one nobody re-decides.
- Any check this update introduced stays advisory until someone **measures its false-positive rate
  against this repo's existing tree**. Do not promote it to `permissions.deny` on the same day.

## Notes
- The skeleton is a **shared home**, not this skill's property: `init` copies it, `update`
  reconciles against it, and neither keeps a second copy.
- Skeleton changes that only *add* (a new rules file, a new hook + its test) are the safe majority.
  The expensive ones are edits to files every project was expected to fill — treat those as
  proposals to a human, always.
