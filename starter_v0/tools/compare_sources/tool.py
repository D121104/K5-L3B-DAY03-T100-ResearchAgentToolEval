from __future__ import annotations

from typing import Any

from tools._shared import err


def compare_sources(sources: list[dict] | None = None) -> dict[str, Any]:
    try:
        if not isinstance(sources, list) or len(sources) < 2:
            raise ValueError("At least 2 sources are required")

        normalized: list[dict[str, Any]] = []
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                raise ValueError(f"Source at index {index} must be an object")
            if "title" not in source or "facts" not in source:
                raise ValueError("Each source requires title and facts")
            if not isinstance(source["facts"], dict):
                raise TypeError("facts must be an object")
            normalized.append(source)

        fields = set().union(*(source["facts"].keys() for source in normalized))
        comparisons = []

        for field in sorted(fields):
            values = {
                source["title"]: source["facts"].get(field)
                for source in normalized
            }
            present = [value for value in values.values() if value is not None]

            if len(present) < len(normalized):
                status = "missing"
            elif len(set(map(str, present))) == 1:
                status = "consistent"
            else:
                status = "different"

            comparisons.append({
                "field": field,
                "status": status,
                "values": values,
            })

        return {
            "tool": "compare_sources",
            "comparisons": comparisons,
            "summary": {
                "consistent": sum(item["status"] == "consistent" for item in comparisons),
                "different": sum(item["status"] == "different" for item in comparisons),
                "missing": sum(item["status"] == "missing" for item in comparisons),
            },
        }

    except Exception as exc:
        return err("compare_sources", exc)
