"""
Example: pyWATS Async Service Application

This example shows how to use the pyWATS Client async service architecture
to build a service application with:
- AsyncClientService (background processing with asyncio)
- IPC communication via ServiceIPCClient
- File monitoring
- Graceful shutdown
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional

from pywats_client.service import AsyncClientService, ServiceStatus
from pywats_client.service.ipc_client import ServiceIPCClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ServiceApplication:
    """
    Service application using the pyWATS AsyncClientService.
    
    This demonstrates:
    1. Starting the async background service
    2. Communicating with it via IPC
    3. Monitoring status and controlling the service
    
    The AsyncClientService can run as:
    - A Windows Service
    - A systemd service
    - A standalone daemon
    - A foreground console application
    
    The async architecture provides:
    - Non-blocking I/O with AsyncWATS
    - Concurrent uploads (5 simultaneous via AsyncPendingQueue)
    - Concurrent conversions (10 simultaneous via AsyncConverterPool)
    """
    
    def __init__(self, instance_id: str = "default") -> None:
        """
        Initialize service application.
        
        Args:
            instance_id: Instance ID for multi-station support
        """
        self.instance_id = instance_id
        self.service: Optional[AsyncClientService] = None
        self._running = False

    async def start(self) -> None:
        """Start the async service"""
        if self._running:
            logger.warning("Service already running")
            return
        
        logger.info(f"Starting async service application [instance: {self.instance_id}]")
        
        # Create and start the AsyncClientService
        self.service = AsyncClientService()
        self._running = True
        
        try:
            # Run blocks until service stops
            await self.service.run()
        except asyncio.CancelledError:
            logger.info("Service cancelled")
        except Exception as e:
            logger.error(f"Service error: {e}")
        finally:
            self._running = False
    
    async def stop(self) -> None:
        """Stop the service gracefully"""
        if not self._running:
            return
        
        logger.info("Stopping async service application...")
        
        if self.service:
            await self.service.stop()
        
        self._running = False
        logger.info("Service application stopped")
    
    def get_status(self) -> dict:
        """Get service status"""
        if not self.service:
            return {"status": "not_started"}
        
        return {
            "status": self.service.status.value,
            "running": self._running,
            "instance_id": self.instance_id,
        }


class IPCControlExample:
    """
    Example of controlling a running service via IPC.
    
    This shows how to communicate with an already-running AsyncClientService
    from another process (e.g., GUI, CLI, or web interface).
    """
    
    def __init__(self, instance_id: str = "default") -> None:
        """
        Initialize IPC controller.
        
        Args:
            instance_id: Instance ID of the service to control
        """
        self.instance_id = instance_id
        self.client: Optional[ServiceIPCClient] = None
    
    def connect(self) -> bool:
        """Connect to a running service"""
        try:
            self.client = ServiceIPCClient(self.instance_id)
            self.client.connect()
            logger.info(f"Connected to service [instance: {self.instance_id}]")
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect from the service"""
        if self.client:
            self.client.disconnect()
            self.client = None
    
    def get_status(self) -> Optional[dict]:
        """Get status from the running service"""
        if not self.client:
            return None
        
        try:
            return self.client.get_status()
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            return None
    
    def request_shutdown(self) -> bool:
        """Request the service to shut down"""
        if not self.client:
            return False
        
        try:
            self.client.shutdown()
            return True
        except Exception as e:
            logger.error(f"Failed to request shutdown: {e}")
            return False


# ============================================================================
# Entry Points
# ============================================================================

def run_service():
    """Run the async service in foreground"""
    service = ServiceApplication(instance_id="default")
    asyncio.run(service.start())


def control_service():
    """Example of controlling a running service via IPC"""
    controller = IPCControlExample(instance_id="default")
    
    if controller.connect():
        # Get status
        status = controller.get_status()
        if status:
            print(f"Service status: {status}")
        
        # Disconnect
        controller.disconnect()


def main():
    """Main entry point - run the async service"""
    run_service()


if __name__ == "__main__":
    main()
