---
paths:
  - {{TEST_GLOB}}
---
# Testing

- Location & convention: `tests/<module>/test_*.py` (or this project's equivalent — match the
  existing tree). <!-- FILL: test layout + the run command. -->
- Deterministic, **no network access** in unit tests. Isolate external state (DB / services /
  tracking servers) in tmp dirs or fakes so no artifacts leak into the repo root.
  <!-- FILL: the project's isolation pattern + a reference test to copy. -->
- **No weak asserts**: checking only "within range" lets a wrong implementation pass. Verify exact
  values and relationships (distributions, invariants), not just bounds.
- Regression tests reproducing a gotcha come **with rationale** — a comment naming the bug they pin,
  so the assert isn't "mysteriously specific" to a future reader.
