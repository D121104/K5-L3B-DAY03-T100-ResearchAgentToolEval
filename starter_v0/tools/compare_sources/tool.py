
from __future__ import annotations

from typing import Any

from tools._shared import err


def compare_sources(sources: list[dict] | None = None) -> dict[str, Any]:
    try:
        if not isinstance(sources, list) or len(sources) < 2:
            raise ValueError("At least 2 sources are required")

        fields = set().union(
            *(source["facts"].keys() for source in sources)
        )

        comparisons = []

        for field in sorted(fields):
            values = {
                source["title"]: source["facts"].get(field)
                for source in sources
            }

            present = [v for v in values.values() if v is not None]

            if len(present) < len(sources):
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
                "consistent": sum(x["status"] == "consistent" for x in comparisons),
                "different": sum(x["status"] == "different" for x in comparisons),
                "missing": sum(x["status"] == "missing" for x in comparisons),
            },
        }

    except Exception as exc:
        return err("compare_sources", exc)
