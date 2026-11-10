from __future__ import annotations

from typing import Any

from tools._shared import domain


def _title_of(item: dict[str, Any]) -> str:
    title = str(item.get("title") or "").strip()
    if title:
        return title
    url = str(item.get("url") or "").strip()
    source = str(item.get("source") or "").strip() or domain(url)
    return source or url or "Untitled"


def _source_of(item: dict[str, Any]) -> str:
    source = str(item.get("source") or "").strip()
    if source:
        return source
    url = str(item.get("url") or "").strip()
    return domain(url) or "Unknown"


def _format_ieee(index: int, item: dict[str, Any]) -> str:
    title = _title_of(item)
    source = _source_of(item)
    url = str(item.get("url") or "").strip()
    line = f'[{index}] "{title}," {source}.'
    if url:
        line += f" [Online]. Available: {url}"
    return line


def _format_markdown(index: int, item: dict[str, Any]) -> str:
    title = _title_of(item)
    source = _source_of(item)
    url = str(item.get("url") or "").strip()
    if url:
        return f"[{index}] {title} — {source} ({url})"
    return f"[{index}] {title} — {source}"


def cite(
    items: list[dict[str, Any]] | None = None,
    style: str = "ieee",
) -> dict[str, Any]:
    """Format research items as citations (deterministic; no LLM)."""
    if items is None:
        items = []
    if not isinstance(items, list):
        return {
            "tool": "cite",
            "error": "TypeError",
            "message": "items must be a list",
        }

    style_norm = (style or "ieee").strip().lower()
    if style_norm not in {"ieee", "markdown"}:
        return {
            "tool": "cite",
            "error": "ValueError",
            "message": f"style must be 'ieee' or 'markdown', got {style!r}",
        }

    lines: list[str] = []
    for index, raw in enumerate(items, start=1):
        if not isinstance(raw, dict):
            return {
                "tool": "cite",
                "error": "TypeError",
                "message": "each item must be an object",
            }
        if style_norm == "ieee":
            lines.append(_format_ieee(index, raw))
        else:
            lines.append(_format_markdown(index, raw))

    return {
        "tool": "cite",
        "style": style_norm,
        "citations": "\n".join(lines),
        "item_count": len(items),
    }
