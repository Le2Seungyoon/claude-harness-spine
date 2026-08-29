---
paths:
  - {{SOURCE_GLOB}}
---
# Architecture

## Layers & dependency direction

```
<!-- FILL: layer diagram, e.g.  config → data/io → domain → interface -->
```

- **Lower layers never import higher ones.** State the dependency arrows explicitly.
<!-- FILL: how modules are accessed (package import? path?), and the entry points. -->

## Module boundary contracts

<!-- FILL: for each boundary that must NOT be crossed by a direct import, name the contract that
replaces it (a registry, a queue, a shared config, an interface). Shape:
- `<producer>` and `<consumer>` never import each other — `<the contract>` is the only touchpoint.
-->

## Idempotency (if applicable)

- If writes must be safe to re-run (retries / backfills), make them UPSERT-by-key so the same input
  yields the same result. <!-- FILL: state the actual write path + keys, or delete if N/A. -->

## CLI / logic separation

- Keep logic functions free of argument parsing; put the CLI (argparse / click / …) in a thin
  wrapper so the same function is callable from a notebook · CLI · scheduler without rewriting.
  <!-- FILL: adjust or delete to match this project. -->
