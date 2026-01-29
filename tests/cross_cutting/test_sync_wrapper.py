"""Tests for synchronous wrapper utilities.

Tests the SyncServiceWrapper and _run_sync function which provide
blocking interfaces for async operations.
"""
import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock

from pywats.sync import _run_sync, SyncServiceWrapper


class TestRunSync:
    """Tests for the _run_sync function."""
    
    def test_run_sync_simple_coroutine(self):
        """Test running a simple async function synchronously."""
        async def simple_coro():
            return "hello"
        
        result = _run_sync(simple_coro())
        assert result == "hello"
    
    def test_run_sync_with_return_value(self):
        """Test that return values are properly passed through."""
        async def coro_with_value():
            return {"key": "value", "number": 42}
        
        result = _run_sync(coro_with_value())
        assert result == {"key": "value", "number": 42}
    
    def test_run_sync_with_await(self):
        """Test coroutine that uses await internally."""
        async def coro_with_await():
            await asyncio.sleep(0.001)
            return "done"
        
        result = _run_sync(coro_with_await())
        assert result == "done"
    
    def test_run_sync_propagates_exception(self):
        """Test that exceptions from the coroutine are propagated."""
        async def coro_with_error():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError, match="Test error"):
            _run_sync(coro_with_error())
    
    def test_run_sync_none_return(self):
        """Test coroutine that returns None."""
        async def coro_none():
            return None
        
        result = _run_sync(coro_none())
        assert result is None
    
    def test_run_sync_with_arguments(self):
        """Test coroutine that receives arguments via closure."""
        async def coro_with_args(a, b, c=10):
            return a + b + c
        
        result = _run_sync(coro_with_args(1, 2, c=3))
        assert result == 6


class TestSyncServiceWrapper:
    """Tests for the SyncServiceWrapper class."""
    
    def test_wrapper_wraps_async_methods(self):
        """Test that async methods are converted to sync methods."""
        class AsyncService:
            async def get_data(self):
                return "data"
            
            async def process(self, value):
                return value * 2
        
        service = AsyncService()
        wrapper = SyncServiceWrapper(service)
        
        # Should work synchronously
        result = wrapper.get_data()
        assert result == "data"
        
        result = wrapper.process(5)
        assert result == 10
    
    def test_wrapper_passes_regular_attributes(self):
        """Test that non-async attributes are passed through unchanged."""
        class AsyncService:
            name = "TestService"
            value = 42
            
            async def get_data(self):
                return "data"
        
        service = AsyncService()
        wrapper = SyncServiceWrapper(service)
        
        assert wrapper.name == "TestService"
        assert wrapper.value == 42
    
    def test_wrapper_passes_regular_methods(self):
        """Test that regular (non-async) methods work correctly."""
        class AsyncService:
            def regular_method(self):
                return "regular"
            
            async def async_method(self):
                return "async"
        
        service = AsyncService()
        wrapper = SyncServiceWrapper(service)
        
        assert wrapper.regular_method() == "regular"
        assert wrapper.async_method() == "async"
    
    def test_wrapper_preserves_method_arguments(self):
        """Test that method arguments are correctly forwarded."""
        class AsyncService:
            async def method_with_args(self, a, b, *args, **kwargs):
                return {"a": a, "b": b, "args": args, "kwargs": kwargs}
        
        service = AsyncService()
        wrapper = SyncServiceWrapper(service)
        
        result = wrapper.method_with_args(1, 2, 3, 4, key="value")
        assert result == {
            "a": 1, 
            "b": 2, 
            "args": (3, 4), 
            "kwargs": {"key": "value"}
        }
    
    def test_wrapper_propagates_exceptions(self):
        """Test that exceptions from wrapped methods are propagated."""
        class AsyncService:
            async def failing_method(self):
                raise RuntimeError("Service error")
        
        service = AsyncService()
        wrapper = SyncServiceWrapper(service)
        
        with pytest.raises(RuntimeError, match="Service error"):
            wrapper.failing_method()
    
    def test_wrapper_accesses_underlying_async_service(self):
        """Test that the underlying async service is accessible."""
        class AsyncService:
            async def method(self):
                return "result"
        
        service = AsyncService()
        wrapper = SyncServiceWrapper(service)
        
        assert wrapper._async is service
    
    def test_wrapper_with_mock_service(self):
        """Test wrapper with mocked async methods."""
        mock_service = MagicMock()
        mock_service.get_items = AsyncMock(return_value=["item1", "item2"])
        mock_service.count = 5
        
        wrapper = SyncServiceWrapper(mock_service)
        
        result = wrapper.get_items()
        assert result == ["item1", "item2"]
        assert wrapper.count == 5
    
    def test_wrapper_with_property(self):
        """Test that properties on the service work correctly."""
        class AsyncService:
            def __init__(self):
                self._data = "initial"
            
            @property
            def data(self):
                return self._data
        
        service = AsyncService()
        wrapper = SyncServiceWrapper(service)
        
        assert wrapper.data == "initial"
    
    def test_wrapper_getattr_caching(self):
        """Test that __getattr__ correctly handles repeated access."""
        call_count = 0
        
        class AsyncService:
            async def method(self):
                nonlocal call_count
                call_count += 1
                return call_count
        
        service = AsyncService()
        wrapper = SyncServiceWrapper(service)
        
        # Each call should work independently
        result1 = wrapper.method()
        result2 = wrapper.method()
        assert result1 == 1
        assert result2 == 2


class TestSyncWrapperIntegration:
    """Integration tests for the sync wrapper pattern."""
    
    def test_nested_async_calls(self):
        """Test service with nested async operations."""
        class AsyncService:
            async def outer(self, value):
                result = await self.inner(value)
                return result + " processed"
            
            async def inner(self, value):
                return f"[{value}]"
        
        service = AsyncService()
        wrapper = SyncServiceWrapper(service)
        
        result = wrapper.outer("test")
        assert result == "[test] processed"
    
    def test_concurrent_sequential_calls(self):
        """Test that sequential sync calls work correctly."""
        class AsyncService:
            def __init__(self):
                self.counter = 0
            
            async def increment(self):
                self.counter += 1
                return self.counter
        
        service = AsyncService()
        wrapper = SyncServiceWrapper(service)
        
        results = [wrapper.increment() for _ in range(5)]
        assert results == [1, 2, 3, 4, 5]
