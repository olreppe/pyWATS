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
from pywats_events.policies.error_policy import ErrorPolicy, DeadLetterQueue, CircuitBreaker
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
        assert data["event_type"] == "test_result"  # or similar
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
        
        bus.subscribe(TestHandler())
        
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
        
        class FaultHandler(BaseHandler):
            @property
            def event_types(self) -> list[EventType]:
                return [EventType.ASSET_FAULT]
            
            def handle(self, event: Event) -> None:
                fault_events.append(event)
        
        bus.subscribe(TestHandler())
        bus.subscribe(FaultHandler())
        
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
        
        bus.subscribe(AsyncHandler())
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
        
        bus.subscribe(SlowHandler())
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
    
    def test_execute_success_no_retry(self):
        """Successful operation should not retry."""
        policy = RetryPolicy()
        call_count = 0
        
        def operation():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = policy.execute(operation)
        
        assert result == "success"
        assert call_count == 1
    
    def test_execute_retries_on_failure(self):
        """Should retry on failure."""
        config = RetryConfig(max_retries=3, initial_delay=0.01, max_delay=0.1)
        policy = RetryPolicy(config)
        call_count = 0
        
        def operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary error")
            return "success"
        
        result = policy.execute(operation)
        
        assert result == "success"
        assert call_count == 3
    
    def test_execute_raises_after_max_retries(self):
        """Should raise after max retries exceeded."""
        config = RetryConfig(max_retries=2, initial_delay=0.01, max_delay=0.1)
        policy = RetryPolicy(config)
        
        def operation():
            raise ValueError("Permanent error")
        
        with pytest.raises(ValueError):
            policy.execute(operation)


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
        
        assert dlq.size() == 1
        
        items = dlq.get_all()
        assert items[0].event == event
        assert "Test error" in str(items[0].error)
    
    def test_max_size_limit(self):
        """Should respect max size limit."""
        dlq = DeadLetterQueue(max_size=3)
        
        for i in range(5):
            event = Event(event_type=EventType.TEST_RESULT, payload={"i": i})
            dlq.add(event, ValueError(f"Error {i}"))
        
        assert dlq.size() == 3


class TestCircuitBreaker:
    """Tests for CircuitBreaker."""
    
    def test_starts_closed(self):
        """Circuit should start in closed state."""
        cb = CircuitBreaker()
        assert cb.is_closed()
    
    def test_opens_after_failures(self):
        """Circuit should open after failure threshold."""
        cb = CircuitBreaker(failure_threshold=2, reset_timeout=1.0)
        
        cb.record_failure()
        assert cb.is_closed()
        
        cb.record_failure()
        assert cb.is_open()
    
    def test_allows_call_when_closed(self):
        """Should allow calls when closed."""
        cb = CircuitBreaker()
        assert cb.allow_request()
    
    def test_blocks_call_when_open(self):
        """Should block calls when open."""
        cb = CircuitBreaker(failure_threshold=1)
        
        cb.record_failure()
        assert not cb.allow_request()
    
    def test_transitions_to_half_open(self):
        """Should transition to half-open after timeout."""
        cb = CircuitBreaker(failure_threshold=1, reset_timeout=0.05)
        
        cb.record_failure()
        assert cb.is_open()
        
        import time
        time.sleep(0.1)
        
        assert cb.is_half_open()
        assert cb.allow_request()  # Single test request allowed
    
    def test_closes_on_success_from_half_open(self):
        """Should close on success from half-open state."""
        cb = CircuitBreaker(failure_threshold=1, reset_timeout=0.01)
        
        cb.record_failure()
        import time
        time.sleep(0.02)
        
        cb.record_success()
        assert cb.is_closed()


# =============================================================================
# MockTransport Tests
# =============================================================================

class TestMockTransport:
    """Tests for MockTransport."""
    
    @pytest.mark.asyncio
    async def test_connect_disconnect(self):
        """Should support connect/disconnect lifecycle."""
        transport = MockTransport()
        
        await transport.connect()
        assert transport._state.value == "connected"
        
        await transport.disconnect()
        assert transport._state.value == "disconnected"
    
    @pytest.mark.asyncio
    async def test_inject_event_triggers_callback(self):
        """Injected events should trigger callback."""
        received = []
        
        def on_event(event):
            received.append(event)
        
        transport = MockTransport(on_event=on_event)
        await transport.connect()
        
        event = Event(event_type=EventType.TEST_RESULT, payload={})
        transport.inject_event(event)
        
        assert len(received) == 1
        assert received[0] == event
    
    @pytest.mark.asyncio
    async def test_sent_events_are_recorded(self):
        """Sent events should be recorded."""
        transport = MockTransport()
        await transport.connect()
        
        event = Event(event_type=EventType.TEST_RESULT, payload={"test": 1})
        await transport.send(event)
        
        assert len(transport.sent_events) == 1
        assert transport.sent_events[0] == event
    
    @pytest.mark.asyncio
    async def test_simulate_disconnect(self):
        """Should simulate disconnect."""
        transport = MockTransport()
        await transport.connect()
        
        transport.simulate_disconnect()
        
        assert transport._state.value == "disconnected"


# =============================================================================
# Integration Tests
# =============================================================================

class TestEventBusWithTransport:
    """Integration tests for EventBus with MockTransport."""
    
    @pytest.mark.asyncio
    async def test_transport_events_reach_handlers(self):
        """Events from transport should reach handlers."""
        bus = AsyncEventBus()
        received = []
        
        class TestHandler(BaseHandler):
            @property
            def event_types(self) -> list[EventType]:
                return [EventType.TEST_RESULT]
            
            async def handle(self, event: Event) -> None:
                received.append(event)
        
        bus.subscribe(TestHandler())
        
        transport = MockTransport(on_event=lambda e: asyncio.create_task(bus.publish(e)))
        await transport.connect()
        await bus.start()
        
        # Inject event through transport
        event = Event(event_type=EventType.TEST_RESULT, payload={"from": "transport"})
        transport.inject_event(event)
        
        await asyncio.sleep(0.1)
        await bus.stop()
        
        assert len(received) == 1
        assert received[0].payload["from"] == "transport"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
