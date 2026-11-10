---
name: cite
track: core
kind: local_formatter
requires_env: []
inputs: [items, style]
outputs: [citations, item_count, style]
side_effect: false
---
# cite

Formats already-collected items into a citation list (IEEE online shorthand or
simple markdown). Does not fetch data and does not invent authors or years.
Use after search/rank when the user asks for references; do not use instead of
`format` when a full digest is needed.
