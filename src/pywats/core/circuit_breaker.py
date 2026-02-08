"""Circuit Breaker Pattern Implementation

Prevents cascading failures by failing fast when a service is down.
Circuit breaker has three states:

- CLOSED: Normal operation, requests pass through
- OPEN: Service is down, requests fail immediately  
- HALF_OPEN: Testing if service has recovered

State transitions:
- CLOSED → OPEN: After failure_threshold consecutive failures
- OPEN → HALF_OPEN: After timeout_seconds elapsed
- HALF_OPEN → CLOSED: After success_threshold consecutive successes
- HALF_OPEN → OPEN: On any failure

This prevents retry storms and provides faster failure feedback.
"""

import time
import logging
from pywats.core.logging import get_logger
from enum import Enum
from typing import Optional, Callable, TypeVar, Any
from dataclasses import dataclass
import threading

logger = get_logger(__name__)

T = TypeVar('T')


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"       # Normal operation
    OPEN = "open"          # Failing fast
    HALF_OPEN = "half_open"  # Testing recovery


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open and request is blocked."""
    
    def __init__(self, message: str = "Circuit breaker is OPEN"):
        self.message = message
        super().__init__(self.message)


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    
    failure_threshold: int = 5
    """Number of consecutive failures before opening circuit."""
    
    success_threshold: int = 2
    """Number of consecutive successes to close circuit from half-open."""
    
    timeout_seconds: float = 60.0
    """Seconds to wait before attempting recovery (OPEN → HALF_OPEN)."""
    
    excluded_exceptions: tuple = ()
    """Exception types that don't count as failures (e.g., validation errors)."""


class CircuitBreaker:
    """
    Circuit breaker to prevent cascading failures.
    
    Fails fast when a service is degraded, preventing retry storms
    and providing faster feedback to callers.
    
    Thread-safe for concurrent access.
    
    Example:
        >>> config = CircuitBreakerConfig(
        ...     failure_threshold=5,
        ...     timeout_seconds=60
        ... )
        >>> breaker = CircuitBreaker("api-service", config)
        >>> 
        >>> try:
        ...     result = breaker.call(lambda: api_request())
        ... except CircuitBreakerOpenError:
        ...     logger.error("Service is down, failing fast")
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None
    ):
        """
        Initialize circuit breaker.
        
        Args:
            name: Name for logging and identification
            config: Configuration (uses defaults if None)
        """
        self.name = name
        self.config = config or CircuitBreakerConfig()
        
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: Optional[float] = None
        self._lock = threading.Lock()
        
        logger.debug(
            f"Circuit breaker '{name}' initialized: "
            f"failure_threshold={self.config.failure_threshold}, "
            f"timeout={self.config.timeout_seconds}s"
        )
    
    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        with self._lock:
            return self._state
    
    @property
    def is_open(self) -> bool:
        """Check if circuit is open (failing fast)."""
        return self.state == CircuitState.OPEN
    
    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed (normal operation)."""
        return self.state == CircuitState.CLOSED
    
    @property
    def is_half_open(self) -> bool:
        """Check if circuit is half-open (testing recovery)."""
        return self.state == CircuitState.HALF_OPEN
    
    def call(self, func: Callable[[], T]) -> T:
        """
        Execute function with circuit breaker protection.
        
        Args:
            func: Function to execute
            
        Returns:
            Result from function
            
        Raises:
            CircuitBreakerOpenError: If circuit is open
            Any exception from func execution
        """
        with self._lock:
            if self._state == CircuitState.OPEN:
                # Check if we should attempt recovery
                if self._should_attempt_reset():
                    logger.info(
                        f"Circuit breaker '{self.name}': "
                        f"Timeout elapsed, entering HALF_OPEN state"
                    )
                    self._state = CircuitState.HALF_OPEN
                    self._success_count = 0
                else:
                    # Still open, fail fast
                    raise CircuitBreakerOpenError(
                        f"Circuit breaker '{self.name}' is OPEN "
                        f"(failing fast to prevent cascade)"
                    )
        
        # Execute function
        try:
            result = func()
            self._on_success()
            return result
        except Exception as e:
            # Check if this exception should be excluded
            if isinstance(e, self.config.excluded_exceptions):
                # Don't count as failure
                raise
            
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has elapsed to attempt recovery."""
        if self._last_failure_time is None:
            return True
        
        elapsed = time.time() - self._last_failure_time
        return elapsed >= self.config.timeout_seconds
    
    def _on_success(self) -> None:
        """Handle successful call."""
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                
                if self._success_count >= self.config.success_threshold:
                    logger.info(
                        f"Circuit breaker '{self.name}': "
                        f"Service recovered, entering CLOSED state"
                    )
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
                    self._success_count = 0
                    self._last_failure_time = None
            
            elif self._state == CircuitState.CLOSED:
                # Reset failure count on success
                self._failure_count = 0
    
    def _on_failure(self) -> None:
        """Handle failed call."""
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            
            if self._state == CircuitState.HALF_OPEN:
                # Any failure in half-open reopens circuit
                logger.warning(
                    f"Circuit breaker '{self.name}': "
                    f"Recovery attempt failed, returning to OPEN state"
                )
                self._state = CircuitState.OPEN
                self._success_count = 0
            
            elif self._state == CircuitState.CLOSED:
                # Check if we've hit failure threshold
                if self._failure_count >= self.config.failure_threshold:
                    logger.error(
                        f"Circuit breaker '{self.name}': "
                        f"Failure threshold reached ({self.config.failure_threshold}), "
                        f"entering OPEN state"
                    )
                    self._state = CircuitState.OPEN
                    self._success_count = 0
    
    def reset(self) -> None:
        """Manually reset circuit breaker to CLOSED state."""
        with self._lock:
            logger.info(f"Circuit breaker '{self.name}': Manual reset to CLOSED")
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._last_failure_time = None
    
    def get_metrics(self) -> dict[str, Any]:
        """
        Get current circuit breaker metrics.
        
        Returns:
            Dictionary with state, counts, and timing info
        """
        with self._lock:
            return {
                "name": self.name,
                "state": self._state.value,
                "failure_count": self._failure_count,
                "success_count": self._success_count,
                "last_failure_time": self._last_failure_time,
                "config": {
                    "failure_threshold": self.config.failure_threshold,
                    "success_threshold": self.config.success_threshold,
                    "timeout_seconds": self.config.timeout_seconds,
                }
            }
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"CircuitBreaker(name='{self.name}', "
            f"state={self._state.value}, "
            f"failures={self._failure_count})"
        )
