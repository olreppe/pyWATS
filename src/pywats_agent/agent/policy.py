from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class ResponsePolicy:
    """Controls how much data is allowed into the LLM context."""

    summary_max_chars: int = 1000
    preview_max_rows: int = 20
    preview_max_chars: int = 8000


def _coerce_row(obj: Any) -> dict[str, Any]:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, Mapping):
        return dict(obj)
    return {"value": obj}


def _truncate_text(text: str, max_chars: int) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    if max_chars <= 0:
        return "", True
    return text[: max_chars - 1] + "…", True


def build_preview(
    value: Any,
    *,
    policy: ResponsePolicy,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    """Build a bounded preview + metrics for arbitrary tool output."""

    metrics: dict[str, Any] = {}

    if value is None:
        return None, metrics

    # List[rows]
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        rows = [_coerce_row(v) for v in value]
        metrics["row_count"] = len(rows)

        preview_rows = rows[: policy.preview_max_rows]
        preview = {"rows": preview_rows}

        # Best-effort schema
        if preview_rows:
            columns: list[str] = []
            for row in preview_rows:
                for k in row.keys():
                    if k not in columns:
                        columns.append(k)
            metrics["columns"] = columns

        # Char cap (rough): serialize-ish
        import json

        preview_json = json.dumps(preview_rows, ensure_ascii=False)
        metrics["preview_size_chars"] = len(preview_json)
        if len(preview_json) > policy.preview_max_chars:
            # shrink rows until within char cap
            shrunk = preview_rows
            while shrunk and len(json.dumps(shrunk, ensure_ascii=False)) > policy.preview_max_chars:
                shrunk = shrunk[:-1]
            preview["rows"] = shrunk
            metrics["preview_truncated"] = True
        return preview, metrics

    # Mapping/object -> one row
    row = _coerce_row(value)
    metrics["row_count"] = 1
    metrics["columns"] = list(row.keys())
    return {"rows": [row]}, metrics


def normalize_summary(summary: str, *, policy: ResponsePolicy) -> tuple[str, bool]:
    return _truncate_text(summary, policy.summary_max_chars)
