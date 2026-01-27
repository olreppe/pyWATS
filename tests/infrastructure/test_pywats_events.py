"""
Unit Tests for pywats_events core functionality.

Tests for Event, EventBus, handlers, and policies.
"""

import asyncio
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from uuid import uuid4

from pywats_events import (
    Event,
    EventMetadata,
    EventType,
    EventBus,
    AsyncEventBus,
    BaseHandler,
    HandlerRegistry,
)
from pywats_events.policies.retry_policy import RetryPolicy, RetryConfig
from pywats_events.policies.error_policy import ErrorPolicy, DeadLetterQueue, CircuitBreaker, CircuitState
from pywats_events.transports import MockTransport


# =============================================================================
# Event Tests
# =============================================================================

class TestEvent:
    """Tests for Event model."""
    
    def test_create_event_with_defaults(self):
        """Event should have auto-generated ID and timestamp."""
        event = Event(
            event_type=EventType.TEST_RESULT,
            payload={"result": "passed"},
        )
        
        assert event.event_id is not None
        assert event.timestamp is not None
        assert event.event_type == EventType.TEST_RESULT
        assert event.payload == {"result": "passed"}
    
    def test_create_event_with_metadata(self):
        """Event should accept custom metadata."""
        metadata = EventMetadata(
            correlation_id="corr-123",
            source="test-station",
            trace_id="trace-456",
        )
        
        event = Event(
            event_type=EventType.ASSET_FAULT,
            payload={"fault": "temperature"},
            metadata=metadata,
        )
        
        assert event.metadata.correlation_id == "corr-123"
        assert event.metadata.source == "test-station"
        assert event.metadata.trace_id == "trace-456"
    
    def test_event_to_dict(self):
        """Event should serialize to dict."""
        event = Event(
            event_type=EventType.MATERIAL_INSTALLED,
            payload={"component": "IC123"},
        )
        
        data = event.to_dict()
        
        assert "event_id" in data
        assert "timestamp" in data
        assert data["event_type"] == "material.installed"
        assert data["payload"] == {"component": "IC123"}
    
    def test_event_from_dict(self):
        """Event should deserialize from dict."""
        data = {
            "event_id": str(uuid4()),
            "event_type": "test_result",
            "timestamp": datetime.now().isoformat(),
            "payload": {"test": "data"},
            "metadata": {
                "correlation_id": "abc",
                "source": "test",
            },
        }
        
        event = Event.from_dict(data)
        
        assert event.payload == {"test": "data"}
        assert event.metadata.correlation_id == "abc"


# =============================================================================
# Handler Tests
# =============================================================================

class TestHandlerRegistry:
    """Tests for HandlerRegistry."""
    
    def test_register_handler(self):
        """Should register handlers by event type."""
        registry = HandlerRegistry()
        
        class TestHandler(BaseHandler):
            @property
            def event_types(self) -> list[EventType]:
                return [EventType.TEST_RESULT]
            
            def handle(self, event: Event) -> None:
                pass
        
        handler = TestHandler()
        registry.register(handler)
        
        handlers = registry.get_handlers(EventType.TEST_RESULT)
        assert handler in handlers
    
    def test_get_handlers_returns_empty_for_unknown_type(self):
        """Should return empty list for unknown event type."""
        registry = HandlerRegistry()
        
        handlers = registry.get_handlers(EventType.CUSTOM)
        assert handlers == []
    
    def test_unregister_handler(self):
        """Should unregister handlers."""
        registry = HandlerRegistry()
        
        class TestHandler(BaseHandler):
            @property
            def event_types(self) -> list[EventType]:
                return [EventType.TEST_RESULT]
            
            def handle(self, event: Event) -> None:
                pass
        
        handler = TestHandler()
        registry.register(handler)
        registry.unregister(handler)
        
        handlers = registry.get_handlers(EventType.TEST_RESULT)
        assert handler not in handlers


# =============================================================================
# EventBus Tests
# =============================================================================

class TestEventBus:
    """Tests for synchronous EventBus."""
    
    def test_publish_event_to_handler(self):
        """Published events should reach registered handlers."""
        bus = EventBus()
        received_events = []
        
        class TestHandler(BaseHandler):
            @property
            def event_types(self) -> list[EventType]:
                return [EventType.TEST_RESULT]
            
            def handle(self, event: Event) -> None:
                received_events.append(event)
        
        bus.register_handler(TestHandler())
        
        event = Event(
            event_type=EventType.TEST_RESULT,
            payload={"passed": True},
        )
        bus.publish(event)
        
        # Give worker thread time to process
        import time
        time.sleep(0.1)
        
        assert len(received_events) == 1
        assert received_events[0].payload == {"passed": True}
    
    def test_handler_filtering_by_event_type(self):
        """Handlers should only receive their registered event types."""
        bus = EventBus()
        test_events = []
        fault_events = []
        
        class TestHandler(BaseHandler):
            @property
            def event_types(self) -> list[EventType]:
                return [EventType.TEST_RESULT]
            
            def handle(self, event: Event) -> None:
                test_events.append(event)
        
        bus.register_handler(TestHandler())
        
        class FaultHandler(BaseHandler):
            @property
            def event_types(self) -> list[EventType]:
                return [EventType.ASSET_FAULT]
            
            def handle(self, event: Event) -> None:
                fault_events.append(event)
        
        bus.register_handler(FaultHandler())
        
        bus.publish(Event(event_type=EventType.TEST_RESULT, payload={}))
        bus.publish(Event(event_type=EventType.ASSET_FAULT, payload={}))
        
        import time
        time.sleep(0.1)
        
        assert len(test_events) == 1
        assert len(fault_events) == 1
    
    def test_start_stop_lifecycle(self):
        """Bus should support start/stop lifecycle."""
        bus = EventBus()
        
        bus.start()
        assert bus._running
        
        bus.stop()
        assert not bus._running


# =============================================================================
# Async EventBus Tests
# =============================================================================

class TestAsyncEventBus:
    """Tests for AsyncEventBus."""
    
    @pytest.mark.asyncio
    async def test_async_publish(self):
        """Should publish events asynchronously."""
        bus = AsyncEventBus()
        received = []
        
        class AsyncHandler(BaseHandler):
            @property
            def event_types(self) -> list[EventType]:
                return [EventType.TEST_RESULT]
            
            async def handle(self, event: Event) -> None:
                received.append(event)
        
        bus.register_handler(AsyncHandler())
        await bus.start()
        
        event = Event(event_type=EventType.TEST_RESULT, payload={"async": True})
        await bus.publish(event)
        
        await asyncio.sleep(0.1)
        await bus.stop()
        
        assert len(received) == 1
    
    @pytest.mark.asyncio
    async def test_concurrent_handlers(self):
        """Should handle events concurrently."""
        bus = AsyncEventBus(max_concurrent=5)
        call_times = []
        
        class SlowHandler(BaseHandler):
            @property
            def event_types(self) -> list[EventType]:
                return [EventType.TEST_RESULT]
            
            async def handle(self, event: Event) -> None:
                call_times.append(datetime.now())
                await asyncio.sleep(0.05)
        
        bus.register_handler(SlowHandler())
        await bus.start()
        
        # Publish multiple events
        for i in range(5):
            await bus.publish(Event(event_type=EventType.TEST_RESULT, payload={"i": i}))
        
        await asyncio.sleep(0.2)
        await bus.stop()
        
        assert len(call_times) == 5


# =============================================================================
# RetryPolicy Tests
# =============================================================================

class TestRetryPolicy:
    """Tests for RetryPolicy."""
    
    def test_default_config(self):
        """Should have sensible defaults."""
        policy = RetryPolicy()
        
        assert policy.config.max_retries == 3
        assert policy.config.initial_delay > 0
    
    def test_should_retry_within_limit(self):
        """Should allow retry when within retry limit."""
        policy = RetryPolicy(max_retries=3)
        
        event = Event(event_type=EventType.TEST_RESULT, payload={})
        error = ValueError("Temporary error")
        
        assert policy.should_retry(event, error) is True
    
    def test_should_not_retry_after_max_retries(self):
        """Should not retry after max retries exceeded."""
        policy = RetryPolicy(max_retries=2)
        
        event = Event(event_type=EventType.TEST_RESULT, payload={})
        # Simulate event that has already been retried 2 times
        event.metadata.retry_count = 2
        error = ValueError("Temporary error")
        
        assert policy.should_retry(event, error) is False
    
    def test_get_delay_increases_exponentially(self):
        """Should calculate exponential backoff delay."""
        policy = RetryPolicy(initial_delay=1.0, exponential_base=2.0, jitter=False)
        
        event = Event(event_type=EventType.TEST_RESULT, payload={})
        delay1 = policy.get_delay(event)
        
        event.metadata.retry_count = 1
        delay2 = policy.get_delay(event)
        
        # Second delay should be larger due to exponential backoff
        assert delay2 > delay1


# =============================================================================
# ErrorPolicy Tests
# =============================================================================

class TestDeadLetterQueue:
    """Tests for DeadLetterQueue."""
    
    def test_add_failed_event(self):
        """Should store failed events."""
        dlq = DeadLetterQueue()
        
        event = Event(event_type=EventType.TEST_RESULT, payload={})
        error = ValueError("Test error")
        
        dlq.add(event, error)
        
        assert dlq.size == 1
        
        items = dlq.get_entries()
        assert items[0].event == event
        assert "Test error" in str(items[0].error)
    
    def test_max_size_limit(self):
        """Should respect max size limit."""
        dlq = DeadLetterQueue(max_size=3)
        
        for i in range(5):
            event = Event(event_type=EventType.TEST_RESULT, payload={"i": i})
            dlq.add(event, ValueError(f"Error {i}"))
        
        assert dlq.size == 3


class TestCircuitBreaker:
    """Tests for CircuitBreaker."""
    
    def test_starts_closed(self):
        """Circuit should start in closed state."""
        cb = CircuitBreaker()
        assert cb.is_closed
    
    def test_opens_after_failures(self):
        """Circuit should open after failure threshold."""
        cb = CircuitBreaker(failure_threshold=2, reset_timeout=1.0)
        
        cb.record_failure()
        assert cb.is_closed
        
        cb.record_failure()
        assert cb.is_open
    
    def test_allows_call_when_closed(self):
        """Should allow calls when closed."""
        cb = CircuitBreaker()
        assert cb.can_proceed()
    
    def test_blocks_call_when_open(self):
        """Should block calls when open."""
        cb = CircuitBreaker(failure_threshold=1)
        
        cb.record_failure()
        assert not cb.can_proceed()
    
    def test_transitions_to_half_open(self):
        """Should transition to half-open after timeout."""
        cb = CircuitBreaker(failure_threshold=1, reset_timeout=0.05)
        
        cb.record_failure()
        assert cb.is_open
        
        import time
        time.sleep(0.1)
        
        # After timeout, state should allow requests (half-open)
        assert cb.state == CircuitState.HALF_OPEN
        assert cb.can_proceed()  # Single test request allowed
    
    def test_closes_on_success_from_half_open(self):
        """Should close on success from half-open state."""
        # success_threshold defaults to 2, so we need to set it to 1
        cb = CircuitBreaker(failure_threshold=1, success_threshold=1, reset_timeout=0.01)
        
        cb.record_failure()
        import time
        time.sleep(0.02)
        
        # Access state to trigger the transition to HALF_OPEN
        assert cb.state == CircuitState.HALF_OPEN
        
        # Now in half-open state, record success to close
        cb.record_success()
        assert cb.is_closed


# =============================================================================
# MockTransport Tests
# =============================================================================

class TestMockTransport:
    """Tests for MockTransport."""
    
    def test_start_stop_lifecycle(self):
        """Should support start/stop lifecycle."""
        transport = MockTransport()
        
        transport.start()
        assert transport._state.value == "connected"
        
        transport.stop()
        assert transport._state.value == "disconnected"
    
    def test_inject_event_publishes_to_bus(self):
        """Injected events should be recorded and published."""
        transport = MockTransport()
        transport.start()
        
        event = Event(event_type=EventType.TEST_RESULT, payload={})
        transport.inject_event(event)
        
        assert len(transport.injected_events) == 1
        assert transport.injected_events[0] == event
    
    def test_published_events_are_recorded(self):
        """Published events should be recorded."""
        transport = MockTransport()
        transport.start()
        
        event = Event(event_type=EventType.TEST_RESULT, payload={"test": 1})
        transport.inject_event(event)
        
        assert len(transport.published_events) == 1
        assert transport.published_events[0] == event
    
    def test_not_connected_raises(self):
        """Should raise when injecting without connection."""
        transport = MockTransport(auto_connect=False)
        transport.start()  # Will be in CONNECTING state
        
        event = Event(event_type=EventType.TEST_RESULT, payload={})
        with pytest.raises(RuntimeError, match="not connected"):
            transport.inject_event(event)


# =============================================================================
# Integration Tests
# =============================================================================

class TestEventBusWithTransport:
    """Integration tests for EventBus with MockTransport."""
    
    @pytest.mark.asyncio
    async def test_transport_events_reach_handlers(self):
        """Events from transport should reach handlers via event bus."""
        bus = AsyncEventBus()
        received = []
        
        class TestHandler(BaseHandler):
            @property
            def event_types(self) -> list[EventType]:
                return [EventType.TEST_RESULT]
            
            async def handle(self, event: Event) -> None:
                received.append(event)
        
        bus.register_handler(TestHandler())
        
        # Register transport with event bus
        transport = MockTransport()
        bus.register_transport(transport)
        
        await bus.start()
        await bus.start_transport(transport)
        
        # Inject event through transport
        event = Event(event_type=EventType.TEST_RESULT, payload={"from": "transport"})
        transport.inject_event(event)
        
        await asyncio.sleep(0.1)
        await bus.stop()
        
        assert len(received) == 1
        assert received[0].payload["from"] == "transport"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
