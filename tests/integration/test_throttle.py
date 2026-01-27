"""Tests for rate limiting / throttling."""
import time
import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

from pywats.core.throttle import RateLimiter, configure_throttling, get_default_limiter


class TestRateLimiter:
    """Tests for the RateLimiter class."""

    def test_limiter_allows_requests_under_limit(self):
        """Requests under the limit should pass immediately."""
        limiter = RateLimiter(max_requests=10, window_seconds=60)
        
        # Should be able to make 10 requests without blocking
        for _ in range(10):
            assert limiter.acquire(timeout=0.1) is True
        
        assert limiter.current_usage == 10
        assert limiter.available_slots == 0

    def test_limiter_blocks_when_limit_reached(self):
        """Requests over the limit should be blocked."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        
        # Use up all slots
        for _ in range(5):
            limiter.acquire()
        
        # Next request should timeout (not wait forever)
        result = limiter.acquire(timeout=0.1)
        
        # Should return False indicating timeout
        assert result is False
        assert limiter.available_slots == 0

    def test_limiter_releases_slots_after_window(self):
        """Slots should become available after the window expires."""
        limiter = RateLimiter(max_requests=3, window_seconds=0.2)  # 200ms window
        
        # Use up all slots
        for _ in range(3):
            limiter.acquire()
        
        assert limiter.available_slots == 0
        
        # Wait for window to expire
        time.sleep(0.25)
        
        # Should have slots available again
        assert limiter.available_slots == 3
        assert limiter.acquire(timeout=0.1) is True

    def test_limiter_disabled(self):
        """Disabled limiter should allow unlimited requests."""
        limiter = RateLimiter(max_requests=5, window_seconds=60, enabled=False)
        
        # Should be able to make many requests without blocking
        for _ in range(100):
            assert limiter.acquire(timeout=0) is True

    def test_limiter_stats(self):
        """Stats should track usage correctly."""
        limiter = RateLimiter(max_requests=10, window_seconds=60)
        
        for _ in range(5):
            limiter.acquire()
        
        stats = limiter.stats
        assert stats["total_requests"] == 5
        assert stats["current_usage"] == 5
        assert stats["available_slots"] == 5
        assert stats["max_requests"] == 10
        assert stats["enabled"] is True

    def test_limiter_reset(self):
        """Reset should clear all tracked requests."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        
        for _ in range(5):
            limiter.acquire()
        
        assert limiter.available_slots == 0
        
        limiter.reset()
        
        assert limiter.available_slots == 5

    def test_limiter_thread_safety(self):
        """Limiter should be thread-safe."""
        limiter = RateLimiter(max_requests=100, window_seconds=60)
        results = []
        
        def make_request():
            result = limiter.acquire(timeout=1.0)
            results.append(result)
        
        # Run 100 concurrent requests
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request) for _ in range(100)]
            for f in futures:
                f.result()
        
        # All should succeed
        assert all(results)
        assert len(results) == 100
        assert limiter.current_usage == 100

    def test_limiter_repr(self):
        """Repr should show useful info."""
        limiter = RateLimiter(max_requests=500, window_seconds=60)
        repr_str = repr(limiter)
        
        assert "500" in repr_str
        assert "60" in repr_str


class TestConfigureThrottling:
    """Tests for the configure_throttling function."""

    def test_configure_throttling_updates_default(self):
        """configure_throttling should update the default limiter."""
        # Configure with custom settings
        limiter = configure_throttling(max_requests=100, window_seconds=30, enabled=True)
        
        assert limiter.max_requests == 100
        assert limiter.window_seconds == 30
        assert limiter.enabled is True
        
        # get_default_limiter should return the same configuration
        default = get_default_limiter()
        assert default.max_requests == 100
        
        # Reset to default for other tests
        configure_throttling(max_requests=500, window_seconds=60, enabled=True)

    def test_configure_throttling_can_disable(self):
        """configure_throttling can disable throttling."""
        limiter = configure_throttling(enabled=False)
        
        assert limiter.enabled is False
        
        # Reset for other tests
        configure_throttling(max_requests=500, window_seconds=60, enabled=True)


class TestRateLimiterSliding:
    """Tests for sliding window behavior."""

    def test_sliding_window_allows_burst(self):
        """Should allow burst of requests up to the limit."""
        limiter = RateLimiter(max_requests=10, window_seconds=1.0)
        
        # Burst of 10 requests should all succeed
        start = time.monotonic()
        for _ in range(10):
            assert limiter.acquire(timeout=0.1) is True
        elapsed = time.monotonic() - start
        
        # Should be fast (no waiting)
        assert elapsed < 0.5

    def test_sliding_window_gradual_release(self):
        """Slots should be released gradually as they age out."""
        limiter = RateLimiter(max_requests=3, window_seconds=0.3)
        
        # Make 3 requests with slight delays
        limiter.acquire()
        time.sleep(0.1)
        limiter.acquire()
        time.sleep(0.1)
        limiter.acquire()
        
        # All slots used
        assert limiter.available_slots == 0
        
        # Wait for first slot to expire
        time.sleep(0.15)
        
        # Should have 1 slot available now
        assert limiter.available_slots >= 1
