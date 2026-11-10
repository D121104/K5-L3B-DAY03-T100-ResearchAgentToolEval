---
name: rank_sources
track: core
kind: local_formatter
requires_env: []
inputs: [query, items, top_k]
outputs: [items, item_count, query]
side_effect: false
---
# rank_sources

Re-ranks already-collected research items by lexical overlap with a query.
Does not fetch data. Prefer after `lookup` / `fetch` / `social_search` / `papers`
when the user wants the most relevant sources first.
