from __future__ import annotations

from typing import Any

from tools._shared import terms


def rank_sources(
    query: str = "",
    items: list[dict[str, Any]] | None = None,
    top_k: int = 5,
) -> dict[str, Any]:
    """Re-rank research items by lexical overlap with the query (no embeddings)."""
    query_terms = terms(query or "")
    if not query_terms:
        return {
            "tool": "rank_sources",
            "error": "ValueError",
            "message": "query must contain at least one meaningful term",
        }

    if items is None:
        items = []
    if not isinstance(items, list):
        return {
            "tool": "rank_sources",
            "error": "TypeError",
            "message": "items must be a list",
        }

    try:
        k = int(top_k)
    except (TypeError, ValueError):
        return {
            "tool": "rank_sources",
            "error": "ValueError",
            "message": f"top_k must be an integer, got {top_k!r}",
        }
    k = max(1, min(k, 20))

    ranked_with_index: list[tuple[int, int, dict[str, Any]]] = []
    for index, raw in enumerate(items):
        if not isinstance(raw, dict):
            return {
                "tool": "rank_sources",
                "error": "TypeError",
                "message": "each item must be an object",
            }
        blob = " ".join(
            str(raw.get(field) or "")
            for field in ("title", "summary", "source", "url")
        )
        matched = sorted(query_terms & terms(blob))
        scored = dict(raw)
        scored["score"] = len(matched)
        scored["matched_terms"] = matched
        ranked_with_index.append((scored["score"], index, scored))

    ranked_with_index.sort(key=lambda row: (-row[0], row[1]))
    out_items = [row[2] for row in ranked_with_index[:k]]

    return {
        "tool": "rank_sources",
        "query": query,
        "items": out_items,
        "item_count": len(out_items),
    }
