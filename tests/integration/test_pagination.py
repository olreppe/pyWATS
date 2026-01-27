"""Unit tests for pagination utilities.

Tests the pagination utilities in pywats.core.pagination.
"""
import pytest
from unittest.mock import Mock, MagicMock

from pywats.core.pagination import (
    paginate,
    paginate_all,
    Paginator,
    PaginationConfig,
)


class MockResponse:
    """Mock paginated response."""
    def __init__(self, items, total=None):
        self.items = items
        self.total = total


class TestPaginate:
    """Tests for paginate function."""

    def test_empty_first_page_returns_nothing(self):
        """Empty first page yields no items."""
        def fetch_page(start, count):
            return MockResponse(items=[])

        result = list(paginate(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
        ))
        assert result == []

    def test_single_page_all_items(self):
        """Single page returns all items."""
        def fetch_page(start, count):
            return MockResponse(items=["a", "b", "c"], total=3)

        result = list(paginate(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
            get_total=lambda r: r.total,
            page_size=10,
        ))
        assert result == ["a", "b", "c"]

    def test_multiple_pages(self):
        """Multiple pages are fetched correctly."""
        pages = {
            1: ["a", "b"],
            3: ["c", "d"],
            5: ["e"],
        }

        def fetch_page(start, count):
            return MockResponse(items=pages.get(start, []), total=5)

        result = list(paginate(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
            get_total=lambda r: r.total,
            page_size=2,
            start_index=1,
        ))
        assert result == ["a", "b", "c", "d", "e"]

    def test_max_items_limits_results(self):
        """max_items stops iteration early."""
        def fetch_page(start, count):
            return MockResponse(items=list(range(start, start + count)), total=1000)

        result = list(paginate(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
            page_size=10,
            start_index=0,
            max_items=15,
        ))
        assert len(result) == 15

    def test_partial_last_page_stops(self):
        """Partial last page indicates end of data."""
        pages = {
            1: ["a", "b", "c"],  # Full page (3)
            4: ["d"],  # Partial page (1 < 3)
        }

        def fetch_page(start, count):
            return MockResponse(items=pages.get(start, []))

        result = list(paginate(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
            page_size=3,
            start_index=1,
        ))
        assert result == ["a", "b", "c", "d"]

    def test_on_page_callback_called(self):
        """on_page callback is invoked for each page."""
        callbacks = []

        def fetch_page(start, count):
            items = ["x"] * count if start < 5 else []
            return MockResponse(items=items, total=4)

        def on_page(page_num, items_so_far, total):
            callbacks.append((page_num, items_so_far, total))

        list(paginate(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
            get_total=lambda r: r.total,
            page_size=2,
            start_index=1,
            on_page=on_page,
        ))
        
        assert len(callbacks) == 2
        assert callbacks[0] == (1, 2, 4)
        assert callbacks[1] == (2, 4, 4)

    def test_early_break_works(self):
        """Breaking iteration stops fetching pages."""
        fetch_count = 0

        def fetch_page(start, count):
            nonlocal fetch_count
            fetch_count += 1
            return MockResponse(items=["item"] * count, total=100)

        for i, item in enumerate(paginate(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
            page_size=5,
            start_index=1,
        )):
            if i >= 3:
                break
        
        # Should only fetch first page
        assert fetch_count == 1


class TestPaginateAll:
    """Tests for paginate_all function."""

    def test_returns_list(self):
        """paginate_all returns a list."""
        def fetch_page(start, count):
            return MockResponse(items=["a", "b"] if start == 1 else [])

        result = paginate_all(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
            page_size=10,
            start_index=1,
        )
        assert isinstance(result, list)
        assert result == ["a", "b"]


class TestPaginator:
    """Tests for Paginator class."""

    def test_iterate_returns_iterator(self):
        """iterate() returns an iterator."""
        def fetch_page(start, count):
            return MockResponse(items=["x"] if start == 1 else [])

        paginator = Paginator(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
        )
        
        result = list(paginator.iterate())
        assert result == ["x"]

    def test_all_returns_list(self):
        """all() returns a list."""
        def fetch_page(start, count):
            return MockResponse(items=["a", "b"] if start == 1 else [])

        paginator = Paginator(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
        )
        
        result = paginator.all()
        assert result == ["a", "b"]

    def test_count_returns_total(self):
        """count() returns total without fetching all."""
        def fetch_page(start, count):
            return MockResponse(items=["x"], total=42)

        paginator = Paginator(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
            get_total=lambda r: r.total,
        )
        
        assert paginator.count() == 42

    def test_count_without_get_total_returns_none(self):
        """count() returns None if no get_total function."""
        paginator = Paginator(
            fetch_page=lambda s, c: MockResponse(items=[]),
            get_items=lambda r: r.items,
        )
        
        assert paginator.count() is None

    def test_reusable_for_multiple_iterations(self):
        """Paginator can be used for multiple iterations."""
        call_count = 0

        def fetch_page(start, count):
            nonlocal call_count
            call_count += 1
            return MockResponse(items=["item"] if start == 1 else [])

        paginator = Paginator(
            fetch_page=fetch_page,
            get_items=lambda r: r.items,
        )
        
        # First iteration
        list(paginator.iterate())
        # Second iteration
        list(paginator.iterate())
        
        assert call_count >= 2  # Should fetch for each iteration


class TestPaginationConfig:
    """Tests for PaginationConfig."""

    def test_default_values(self):
        """Default config values are sensible."""
        config = PaginationConfig()
        assert config.page_size == 100
        assert config.max_items is None
        assert config.start_index == 1

    def test_invalid_page_size_raises(self):
        """page_size < 1 raises ValueError."""
        with pytest.raises(ValueError):
            PaginationConfig(page_size=0)

    def test_high_page_size_warns(self, caplog):
        """High page_size logs warning."""
        import logging
        with caplog.at_level(logging.WARNING):
            PaginationConfig(page_size=5000)
        assert "slow" in caplog.text.lower()
