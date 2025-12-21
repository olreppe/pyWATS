from pywats_agent.agent.policy import ResponsePolicy, build_preview


def test_build_preview_truncates_large_mapping_payload() -> None:
    policy = ResponsePolicy(preview_max_chars=300, preview_max_rows=10)

    big = {
        "a": "x" * 1000,
        "b": ["y" * 200] * 50,
        "c": {str(i): "z" * 200 for i in range(200)},
    }

    preview, metrics = build_preview(big, policy=policy)

    assert preview is not None
    assert metrics.get("row_count") == 1
    assert metrics.get("preview_truncated") is True
    # Keys-only fallback should be stable
    row = preview["rows"][0]
    assert row.get("_truncated") is True
    assert "keys" in row


def test_build_preview_limits_rows_and_bounds_row_values() -> None:
    policy = ResponsePolicy(preview_max_rows=3, preview_max_chars=2000)

    rows = [
        {"id": i, "msg": "hello" * 200, "items": list(range(100))}
        for i in range(10)
    ]

    preview, metrics = build_preview(rows, policy=policy)

    assert preview is not None
    assert metrics.get("row_count") == 10
    assert len(preview["rows"]) <= 3

    # Bounded values should not keep the full 100-length list
    first = preview["rows"][0]
    assert isinstance(first["items"], list)
    assert len(first["items"]) <= 6  # 5 items + truncation marker
