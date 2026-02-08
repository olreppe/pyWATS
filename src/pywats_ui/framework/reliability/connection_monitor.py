"""Connection monitor with auto-reconnect logic.

Fixes CRITICAL issue C2: No auto-reconnect mechanism
- Monitors connection status continuously
- Auto-reconnects with exponential backoff
- Emits status events for UI feedback
- Triggers queue processing on reconnection

User requirement: "Fix weaknesses, ensure reliability"
"""

import asyncio
import logging
from pywats.core.logging import get_logger
from typing import Optional, Callable, Any
from enum import Enum
from datetime import datetime, timedelta

from PySide6.QtCore import QObject, Signal, QTimer

logger = get_logger(__name__)


class ConnectionStatus(Enum):
    """Connection status states"""
    DISCONNECTED = "disconnected"       # Not connected
    CONNECTING = "connecting"           # Attempting to connect
    CONNECTED = "connected"             # Successfully connected
    RECONNECTING = "reconnecting"       # Attempting to reconnect after disconnect


class ConnectionMonitor(QObject):
    """Monitors connection and handles auto-reconnect with exponential backoff.
    
    Signals:
        status_changed(ConnectionStatus): Emitted when connection status changes
        connected(): Emitted when connection established
        disconnected(): Emitted when connection lost
        reconnecting(int, int): Emitted during reconnect (attempt_num, max_delay_seconds)
        reconnect_failed(str): Emitted when reconnect attempt fails (error message)
    """
    
    # Signals
    status_changed = Signal(object)    # ConnectionStatus
    connected = Signal()
    disconnected = Signal()
    reconnecting = Signal(int, int)    # attempt_num, current_delay_seconds
    reconnect_failed = Signal(str)     # error_message
    
    def __init__(
        self,
        connect_callback: Callable[[], Any],  # async or sync function to establish connection
        check_callback: Callable[[], bool],   # sync function to check if connected
        check_interval_ms: int = 5000,        # Check connection every 5s
        initial_retry_delay_ms: int = 1000,   # Start with 1s delay
        max_retry_delay_ms: int = 30000,      # Max 30s delay
        backoff_multiplier: float = 2.0,      # Double delay each attempt
        parent: Optional[QObject] = None
    ):
        """Initialize connection monitor.
        
        Args:
            connect_callback: Async/sync function to establish connection. Should raise on failure.
            check_callback: Sync function that returns True if connected, False otherwise
            check_interval_ms: Interval between connection checks (default 5s)
            initial_retry_delay_ms: Initial retry delay (default 1s)
            max_retry_delay_ms: Maximum retry delay (default 30s)
            backoff_multiplier: Delay multiplier for exponential backoff (default 2.0)
            parent: Parent QObject
        """
        super().__init__(parent)
        
        self.connect_callback = connect_callback
        self.check_callback = check_callback
        self.initial_retry_delay_ms = initial_retry_delay_ms
        self.max_retry_delay_ms = max_retry_delay_ms
        self.backoff_multiplier = backoff_multiplier
        
        # Connection state
        self._status = ConnectionStatus.DISCONNECTED
        self._last_connected: Optional[datetime] = None
        self._reconnect_attempt = 0
        self._current_retry_delay_ms = initial_retry_delay_ms
        self._reconnecting = False
        
        # Status check timer
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self._check_connection)
        self.check_timer.start(check_interval_ms)
        
        # Reconnect timer (one-shot)
        self.reconnect_timer = QTimer(self)
        self.reconnect_timer.setSingleShot(True)
        self.reconnect_timer.timeout.connect(self._attempt_reconnect)
        
        logger.info("ConnectionMonitor initialized")
    
    @property
    def status(self) -> ConnectionStatus:
        """Get current connection status."""
        return self._status
    
    @property
    def is_connected(self) -> bool:
        """Check if currently connected."""
        return self._status == ConnectionStatus.CONNECTED
    
    @property
    def reconnect_attempt(self) -> int:
        """Get current reconnect attempt number."""
        return self._reconnect_attempt
    
    @property
    def current_retry_delay_seconds(self) -> int:
        """Get current retry delay in seconds."""
        return self._current_retry_delay_ms // 1000
    
    def _set_status(self, status: ConnectionStatus) -> None:
        """Update connection status and emit signal."""
        if status != self._status:
            old_status = self._status
            self._status = status
            
            logger.info(f"Connection status: {old_status.value} → {status.value}")
            self.status_changed.emit(status)
            
            # Emit specific signals
            if status == ConnectionStatus.CONNECTED:
                self._last_connected = datetime.now()
                self._reconnect_attempt = 0
                self._current_retry_delay_ms = self.initial_retry_delay_ms
                self._reconnecting = False
                self.connected.emit()
            elif status == ConnectionStatus.DISCONNECTED and old_status == ConnectionStatus.CONNECTED:
                self.disconnected.emit()
    
    def _check_connection(self) -> None:
        """Periodically check connection status."""
        try:
            is_connected = self.check_callback()
            
            if is_connected:
                if self._status != ConnectionStatus.CONNECTED:
                    self._set_status(ConnectionStatus.CONNECTED)
            else:
                if self._status == ConnectionStatus.CONNECTED:
                    # Just lost connection
                    logger.warning("Connection lost")
                    self._set_status(ConnectionStatus.DISCONNECTED)
                    self._start_reconnect()
                elif self._status == ConnectionStatus.DISCONNECTED and not self._reconnecting:
                    # Still disconnected, not yet reconnecting
                    self._start_reconnect()
                    
        except Exception as e:
            logger.exception(f"Error checking connection: {e}")
    
    def _start_reconnect(self) -> None:
        """Start reconnection process with exponential backoff."""
        if self._reconnecting:
            return
        
        self._reconnecting = True
        self._reconnect_attempt = 0
        self._current_retry_delay_ms = self.initial_retry_delay_ms
        
        logger.info("Starting reconnection process")
        self._set_status(ConnectionStatus.RECONNECTING)
        
        # Schedule first reconnect attempt
        self.reconnect_timer.start(self._current_retry_delay_ms)
    
    def _attempt_reconnect(self) -> None:
        """Attempt to reconnect."""
        self._reconnect_attempt += 1
        
        logger.info(f"Reconnect attempt {self._reconnect_attempt} (delay: {self.current_retry_delay_seconds}s)")
        self.reconnecting.emit(self._reconnect_attempt, self.current_retry_delay_seconds)
        
        # Attempt connection
        asyncio.create_task(self._async_reconnect())
    
    async def _async_reconnect(self) -> None:
        """Async reconnection logic."""
        try:
            result = self.connect_callback()
            
            # Handle async callback
            if asyncio.iscoroutine(result):
                await result
            
            # Check if connection succeeded
            if self.check_callback():
                logger.info(f"Reconnected successfully after {self._reconnect_attempt} attempts")
                self._set_status(ConnectionStatus.CONNECTED)
                return
            else:
                raise Exception("Connection check failed after connect")
                
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"Reconnect attempt {self._reconnect_attempt} failed: {error_msg}", exc_info=True)
            self.reconnect_failed.emit(error_msg)
            
            # Schedule next retry with exponential backoff
            self._current_retry_delay_ms = min(
                int(self._current_retry_delay_ms * self.backoff_multiplier),
                self.max_retry_delay_ms
            )
            
            logger.debug(f"Next reconnect in {self.current_retry_delay_seconds}s")
            self.reconnect_timer.start(self._current_retry_delay_ms)
    
    def manual_connect(self) -> None:
        """Manually trigger connection attempt."""
        if self._status == ConnectionStatus.CONNECTED:
            logger.info("Already connected")
            return
        
        logger.info("Manual connection triggered")
        self._set_status(ConnectionStatus.CONNECTING)
        asyncio.create_task(self._async_manual_connect())
    
    async def _async_manual_connect(self) -> None:
        """Async manual connection logic."""
        try:
            result = self.connect_callback()
            
            # Handle async callback
            if asyncio.iscoroutine(result):
                await result
            
            # Check if connection succeeded
            if self.check_callback():
                logger.info("Manual connection successful")
                self._set_status(ConnectionStatus.CONNECTED)
            else:
                raise Exception("Connection check failed after connect")
                
        except Exception as e:
            error_msg = str(e)
            logger.exception(f"Manual connection failed: {error_msg}")
            self._set_status(ConnectionStatus.DISCONNECTED)
            self.reconnect_failed.emit(error_msg)
    
    def stop_reconnecting(self) -> None:
        """Stop reconnection attempts."""
        if self._reconnecting:
            logger.info("Stopping reconnection attempts")
            self._reconnecting = False
            self.reconnect_timer.stop()
            if self._status == ConnectionStatus.RECONNECTING:
                self._set_status(ConnectionStatus.DISCONNECTED)
    
    def cleanup(self) -> None:
        """Stop timers and clean up resources."""
        if self.check_timer.isActive():
            self.check_timer.stop()
        if self.reconnect_timer.isActive():
            self.reconnect_timer.stop()
        
        logger.info("ConnectionMonitor cleanup complete")
