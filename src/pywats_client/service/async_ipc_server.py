"""
Async IPC Server (Pure Python)

Cross-platform IPC server using asyncio streams.
No Qt dependency - enables true headless operation.

Platform support:
- Linux/macOS: Unix domain sockets
- Windows: TCP localhost (with port derived from socket name)
"""

import asyncio
import json
import logging
import sys
import hashlib
from pathlib import Path
from typing import Optional, TYPE_CHECKING, Any, Union, Callable, Dict

if TYPE_CHECKING:
    from .client_service import ClientService
    from .async_client_service import AsyncClientService

logger = logging.getLogger(__name__)


def get_socket_address(socket_name: str) -> tuple:
    """
    Get platform-appropriate socket address.
    
    Args:
        socket_name: Logical socket name (e.g., 'pyWATS_Service_default')
        
    Returns:
        Tuple of (is_unix, address) where address is:
        - Unix: socket path string
        - Windows: ('127.0.0.1', port) tuple
    """
    if sys.platform == 'win32':
        # Windows: use TCP localhost with deterministic port
        # Hash the name to get a consistent port in range 50000-59999
        port_hash = int(hashlib.md5(socket_name.encode()).hexdigest()[:8], 16)
        port = 50000 + (port_hash % 10000)
        return (False, ('127.0.0.1', port))
    else:
        # Unix: use domain socket in /tmp
        socket_path = f"/tmp/{socket_name}.sock"
        return (True, socket_path)


class AsyncIPCServer:
    """
    Pure asyncio IPC server for service<->GUI communication.
    
    Runs in service process, handles requests from GUI clients.
    Uses asyncio streams for cross-platform IPC without Qt dependency.
    
    Usage:
        server = AsyncIPCServer(instance_id, service)
        await server.start()
        # ... server runs until stopped
        await server.stop()
    """
    
    def __init__(
        self,
        instance_id: str,
        service: Union['ClientService', 'AsyncClientService']
    ) -> None:
        """
        Initialize async IPC server.
        
        Args:
            instance_id: Instance identifier (e.g., 'default')
            service: The client service to query for status
        """
        self.instance_id = instance_id
        self.service = service
        self.socket_name = f"pyWATS_Service_{instance_id}"
        
        self._server: Optional[asyncio.Server] = None
        self._clients: list[asyncio.StreamWriter] = []
        self._running = False
        
        # Get platform-specific address
        self._is_unix, self._address = get_socket_address(self.socket_name)
    
    async def start(self) -> bool:
        """
        Start IPC server.
        
        Returns:
            True if started successfully
        """
        try:
            # Clean up stale socket on Unix
            if self._is_unix:
                socket_path = Path(self._address)
                if socket_path.exists():
                    try:
                        socket_path.unlink()
                        logger.debug(f"Removed stale socket: {socket_path}")
                    except OSError as e:
                        logger.warning(f"Failed to remove stale socket: {e}")
            
            # Create server
            if self._is_unix:
                self._server = await asyncio.start_unix_server(
                    self._handle_client,
                    path=self._address
                )
                logger.info(f"Async IPC server started: {self._address}")
            else:
                host, port = self._address
                self._server = await asyncio.start_server(
                    self._handle_client,
                    host=host,
                    port=port
                )
                logger.info(f"Async IPC server started: {host}:{port}")
            
            self._running = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to start async IPC server: {e}")
            return False
    
    async def stop(self) -> None:
        """Stop IPC server"""
        self._running = False
        
        # Close all client connections
        for writer in self._clients:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        self._clients.clear()
        
        # Close server
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            self._server = None
            
            # Clean up socket file on Unix
            if self._is_unix:
                socket_path = Path(self._address)
                if socket_path.exists():
                    try:
                        socket_path.unlink()
                    except OSError:
                        pass
        
        logger.info("Async IPC server stopped")
    
    async def _handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ) -> None:
        """Handle a client connection"""
        self._clients.append(writer)
        peer = writer.get_extra_info('peername') or 'unknown'
        logger.debug(f"IPC client connected: {peer}")
        
        try:
            while self._running:
                # Read message length (4 bytes, big-endian)
                length_bytes = await reader.read(4)
                if not length_bytes:
                    break
                
                if len(length_bytes) < 4:
                    logger.warning("Incomplete length header")
                    break
                
                msg_length = int.from_bytes(length_bytes, 'big')
                if msg_length > 1024 * 1024:  # 1MB limit
                    logger.warning(f"Message too large: {msg_length}")
                    break
                
                # Read message body
                data = await reader.read(msg_length)
                if len(data) < msg_length:
                    logger.warning("Incomplete message body")
                    break
                
                # Process request
                try:
                    request = json.loads(data.decode('utf-8'))
                    response = await self._process_request(request)
                except json.JSONDecodeError as e:
                    response = {
                        "success": False,
                        "error": f"Invalid JSON: {e}",
                        "data": None
                    }
                
                # Send response
                response_bytes = json.dumps(response).encode('utf-8')
                response_length = len(response_bytes).to_bytes(4, 'big')
                writer.write(response_length + response_bytes)
                await writer.drain()
                
        except asyncio.CancelledError:
            pass
        except ConnectionResetError:
            logger.debug(f"Client disconnected: {peer}")
        except Exception as e:
            logger.error(f"Error handling client {peer}: {e}")
        finally:
            if writer in self._clients:
                self._clients.remove(writer)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            logger.debug(f"IPC client disconnected: {peer}")
    
    async def _process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process IPC request.
        
        Args:
            request: Request dict with 'command' and optional 'args'
            
        Returns:
            Response dict with 'success', 'data', and optional 'error'
        """
        command = request.get("command", "")
        args = request.get("args", {})
        request_id = request.get("request_id", "")
        
        try:
            if command == "get_status":
                data = await self._get_status()
            elif command == "get_config":
                data = self._get_config()
            elif command == "stop":
                data = await self._stop_service()
            elif command == "restart":
                data = await self._restart_service()
            elif command == "ping":
                data = {"pong": True}
            else:
                return {
                    "success": False,
                    "error": f"Unknown command: {command}",
                    "data": None,
                    "request_id": request_id
                }
            
            return {
                "success": True,
                "data": data,
                "error": None,
                "request_id": request_id
            }
            
        except Exception as e:
            logger.error(f"Error processing command {command}: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": None,
                "request_id": request_id
            }
    
    async def _get_status(self) -> Dict[str, Any]:
        """Get service status"""
        # Check if service has async status method
        if hasattr(self.service, 'get_status_async'):
            status = await self.service.get_status_async()
        elif hasattr(self.service, 'get_status'):
            status = self.service.get_status()
        else:
            status = {"status": "unknown"}
        
        # Convert to dict if it's a dataclass/object
        if hasattr(status, '__dict__'):
            return vars(status)
        elif hasattr(status, '_asdict'):
            return status._asdict()
        return status
    
    def _get_config(self) -> Dict[str, Any]:
        """Get service configuration"""
        if hasattr(self.service, 'config') and self.service.config:
            config = self.service.config
            if hasattr(config, 'to_dict'):
                return config.to_dict()
            elif hasattr(config, '__dict__'):
                return vars(config)
        return {}
    
    async def _stop_service(self) -> Dict[str, Any]:
        """Request service stop"""
        if hasattr(self.service, 'request_stop'):
            self.service.request_stop()
        elif hasattr(self.service, 'stop'):
            if asyncio.iscoroutinefunction(self.service.stop):
                await self.service.stop()
            else:
                self.service.stop()
        return {"requested": True}
    
    async def _restart_service(self) -> Dict[str, Any]:
        """Request service restart"""
        if hasattr(self.service, 'request_restart'):
            self.service.request_restart()
            return {"requested": True}
        return {"requested": False, "error": "Restart not supported"}


# For backward compatibility
ServiceAsyncIPCServer = AsyncIPCServer
