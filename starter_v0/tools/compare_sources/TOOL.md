---
name: compare_sources
track: bonus
kind: local_formatter
requires_env: []
inputs: [sources]
outputs: [comparisons, summary]
side_effect: false
---
# compare_sources

Compares field values across at least two sources that already have structured
`facts`. Returns per-field status: `consistent`, `different`, or `missing`.
Does not search the web or decide which source is correct.
