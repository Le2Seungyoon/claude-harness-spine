# Enforcement

Where a rule lives is a design decision, not a formatting one. This file is the routing
function — prose vs hook vs test vs `permissions.deny` — plus the contracts every hook in
this project honors. Route a rule **before** writing it: a rule in the wrong layer is not a
weaker rule, it is a rule that never runs.

## Four layers

| Layer | Use when | How it fails |
|-------|----------|--------------|
| **Prose** (`.claude/rules/*.md`) | context-dependent advice; the *why* behind a ban | quietly ignored under deadline |
| **Hook** (`.claude/hooks/*.py`) | deterministic check, fast feedback, this session's edits | one false positive and it gets switched off |
| **Test / CI invariant** | must hold no matter who authored the code | slow feedback; needs a real assertion |
| **`permissions.deny`** | absolute in every context (person · solo/team · time) | blocks legitimate work with no escape |

## Hooks only see this session's edits

A hook fires on this session's `Write` / `Edit` / `MultiEdit`. Code authored in an IDE, by
another agent, or by a teammate bypasses every hook here. **A rule that must hold on every
authoring path needs a test layer** — the hook is fast feedback, the test is the guarantee.

## Hook contracts

Breaking one of these is how a hook stops being trusted, and an untrusted hook gets removed.

- **PreToolUse may deny; PostToolUse never does.** One script may serve both events (branch on
  `hook_event_name`), but the PostToolUse path only advises.
- **Environment failure exits 0.** Tool missing, timeout, unreadable payload → pass. A hook must
  never block an edit for a reason unrelated to what it checks.
- **Silence means exactly one thing: "checked, and it passes."** If the check could not run,
  emit one line saying so. Otherwise "all clear" and "never looked" are indistinguishable.
- **Timeouts nest**: any subprocess timeout stays below the hook's own `timeout` in
  `settings.json`, so the hook controls its own outcome instead of being killed mid-write.
- **A hook is code — it ships with `test_<name>.py` beside it.** Cover the must-block and the
  must-pass halves; the must-pass half is what keeps false positives from creeping in.
- **A deny message says what to do instead**: why it fired, the canonical alternative, the
  escape hatch, and the rule file it enforces.

## Before promoting a check to deny

- **Measure the false-positive rate first.** Run the candidate rule over the existing tree and
  classify every hit. A rule that blocks legitimate work trains everyone to route around it.
- **Set the gate one occurrence later than the rule asks for.** If the convention says "extract
  on the second copy", gate the third. The gap is deliberate: it is where judgment lives.
- **Every deny needs an escape hatch that costs one sentence** — a marker comment carrying a
  *reason* (`<gate-name>-exempt: <reason>`); an empty or near-empty reason must not pass. The
  goal is not prohibition, it is surfacing: turn a silent copy into an explicit decision a
  reviewer can see.
- **When a hook takes over a rule, delete the prose it replaced.** Keep only what the hook
  cannot check — it blocks the import, but it cannot say why the ban exists.

## Answers, not lookup procedures

A rule that says *"check X first"* makes the reader perform a lookup, and every point where
that lookup fails is an incident. Where the answer is derivable from the tree, **generate it**:

- The generated file carries a `do not edit by hand — regenerate with <cmd>` header and is
  committed, so it is readable without running anything.
- Generate from the **default branch**, not the working tree. A long-lived branch otherwise
  reports "this does not exist yet" about something that was shared while it was away.
- A **freshness test** fails when the committed artifact is stale. Hooks cannot cover this:
  the artifact goes stale through edits they never see.
- A hand-maintained list of the same information rots. Do not keep one beside the generated one.

## An empty result is not proof

A checker that reports nothing has three ways to be lying: the count fell below its threshold
when all but one instance was fixed; a promotion masked an unrelated repetition sharing the
same signature; near-matches were never grouped at all. **Judge completion by searching the
source, not by the checker being quiet** — and remember a detector only sees copies *before*
they drift apart. Green is not "none".

## This project's gates

<!-- FILL: one row per gate as it is added — gate | layer | what it checks | escape hatch.
     Delete this section only if the project has none. -->
