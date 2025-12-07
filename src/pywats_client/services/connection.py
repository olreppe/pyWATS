"""
Connection Service

Manages connection to WATS server and monitors connectivity status.
"""

import asyncio
import logging
from enum import Enum
from typing import Optional, Callable, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from ..core.config import ProxyConfig

logger = logging.getLogger(__name__)


class ConnectionStatus(Enum):
    """Connection status states"""
    DISCONNECTED = "Disconnected"
    CONNECTING = "Connecting"
    ONLINE = "Online"
    OFFLINE = "Offline"
    ERROR = "Error"


class ConnectionService:
    """
    Manages connection to WATS server.
    
    Features:
    - Connection state management
    - Automatic reconnection
    - Connection health monitoring
    - Proxy support
    """
    
    def __init__(
        self,
        service_address: str,
        api_token: str,
        proxy_config: Optional['ProxyConfig'] = None,
        check_interval: int = 30
    ):
        self.service_address = service_address.rstrip('/')
        self.api_token = api_token
        self.proxy_config = proxy_config
        self.check_interval = check_interval
        
        self._status = ConnectionStatus.DISCONNECTED
        self._status_callbacks: List[Callable[[ConnectionStatus], None]] = []
        self._pywats_client = None
        self._check_task: Optional[asyncio.Task] = None
        self._last_check: Optional[datetime] = None
        self._last_error: Optional[str] = None
    
    @property
    def status(self) -> ConnectionStatus:
        """Get current connection status"""
        return self._status
    
    @status.setter
    def status(self, value: ConnectionStatus) -> None:
        """Set status and notify callbacks"""
        if self._status != value:
            old_status = self._status
            self._status = value
            logger.info(f"Connection status changed: {old_status.value} -> {value.value}")
            for callback in self._status_callbacks:
                try:
                    callback(value)
                except Exception as e:
                    logger.error(f"Error in status callback: {e}")
    
    @property
    def last_error(self) -> Optional[str]:
        """Get last error message"""
        return self._last_error
    
    def on_status_change(self, callback: Callable[[ConnectionStatus], None]) -> None:
        """Register callback for status changes"""
        self._status_callbacks.append(callback)
    
    async def connect(self) -> bool:
        """
        Establish connection to WATS server.
        
        Returns True if connection successful.
        """
        if not self.service_address or not self.api_token:
            logger.error("Service address and API token are required")
            self.status = ConnectionStatus.ERROR
            self._last_error = "Service address and API token are required"
            return False
        
        self.status = ConnectionStatus.CONNECTING
        
        try:
            # Import pyWATS and create client
            from pywats import pyWATS
            
            self._pywats_client = pyWATS(
                base_url=self.service_address,
                token=self.api_token
            )
            
            # Test connection
            if await self.test_connection():
                self.status = ConnectionStatus.ONLINE
                
                # Start health check task
                self._check_task = asyncio.create_task(self._health_check_loop())
                
                return True
            else:
                self.status = ConnectionStatus.OFFLINE
                self._last_error = "Connection test failed"
                return False
                
        except ImportError:
            logger.error("pyWATS package not found")
            self.status = ConnectionStatus.ERROR
            self._last_error = "pyWATS package not installed"
            return False
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.status = ConnectionStatus.ERROR
            self._last_error = str(e)
            return False
    
    async def disconnect(self) -> None:
        """Disconnect from WATS server"""
        # Cancel health check task
        if self._check_task:
            self._check_task.cancel()
            try:
                await self._check_task
            except asyncio.CancelledError:
                pass
            self._check_task = None
        
        self._pywats_client = None
        self.status = ConnectionStatus.DISCONNECTED
    
    async def test_connection(self) -> bool:
        """
        Test connection to WATS server.
        
        Returns True if server is reachable and credentials are valid.
        """
        if not self._pywats_client:
            return False
        
        try:
            # Try to get version info as a simple connection test
            version = self._pywats_client.app.get_version()
            self._last_check = datetime.now()
            return version is not None
        except Exception as e:
            logger.debug(f"Connection test failed: {e}")
            self._last_error = str(e)
            return False
    
    async def _health_check_loop(self) -> None:
        """Background task to monitor connection health"""
        while True:
            try:
                await asyncio.sleep(self.check_interval)
                
                if await self.test_connection():
                    if self.status != ConnectionStatus.ONLINE:
                        self.status = ConnectionStatus.ONLINE
                        logger.info("Connection restored")
                else:
                    if self.status == ConnectionStatus.ONLINE:
                        self.status = ConnectionStatus.OFFLINE
                        logger.warning("Connection lost")
                        
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check error: {e}")
    
    def get_client(self):
        """
        Get the pyWATS client instance.
        
        Returns None if not connected.
        """
        return self._pywats_client
    
    def get_status_info(self) -> dict:
        """Get detailed status information"""
        return {
            "status": self.status.value,
            "service_address": self.service_address,
            "last_check": self._last_check.isoformat() if self._last_check else None,
            "last_error": self._last_error,
        }
