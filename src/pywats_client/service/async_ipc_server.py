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
from pywats.core.logging import get_logger
import sys
import hashlib
from pathlib import Path
from typing import Optional, TYPE_CHECKING, Any, Union, Callable, Dict

from ..core.security import load_secret, validate_token, RateLimiter
from .ipc_protocol import (
    PROTOCOL_VERSION,
    HelloMessage,
    IPCResponse,
    ServerCapability,
    is_version_compatible,
    MIN_CLIENT_VERSION,
)

if TYPE_CHECKING:
    from .client_service import ClientService
    from .async_client_service import AsyncClientService

logger = get_logger(__name__)


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
    
    H6 Fix: Includes timeout handling to prevent hung/slow clients from blocking server.
    
    Usage:
        server = AsyncIPCServer(instance_id, service)
        await server.start()
        # ... server runs until stopped
        await server.stop()
    """
    
    # H6: Timeout configuration (in seconds)
    CONNECTION_TIMEOUT = 30.0   # Max time to establish connection and send hello
    READ_TIMEOUT = 30.0         # Max time to read a request from client
    WRITE_TIMEOUT = 10.0        # Max time to write response to client
    REQUEST_TIMEOUT = 60.0      # Max time to process a request
    
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
        
        # Security: per-connection auth state and rate limiting
        self._authenticated_clients: set[asyncio.StreamWriter] = set()
        self._rate_limiter = RateLimiter(requests_per_minute=100, burst_size=20)
        self._secret: Optional[str] = None
        
        # Protocol versioning
        self._protocol_version = PROTOCOL_VERSION
        self._server_version = self._get_server_version()
        self._capabilities = self._get_capabilities()
    
    def _get_server_version(self) -> str:
        """Get pyWATS version string"""
        try:
            from .. import __version__
            return __version__
        except ImportError:
            return "unknown"
    
    def _get_capabilities(self) -> list[str]:
        """Get list of server capabilities"""
        caps = [
            ServerCapability.RATE_LIMIT.value,
            ServerCapability.CONFIG.value,
        ]
        # Auth capability depends on whether secret is configured (checked at start)
        # Converter capability depends on service
        if hasattr(self.service, 'converter_pool'):
            caps.append(ServerCapability.CONVERTERS.value)
        if hasattr(self.service, 'queue'):
            caps.append(ServerCapability.QUEUE.value)
        if hasattr(self.service, 'sync_now'):
            caps.append(ServerCapability.SYNC.value)
        return caps
    
    async def start(self) -> bool:
        """
        Start IPC server.
        
        Returns:
            True if started successfully
        """
        try:
            # Load shared secret for authentication
            self._secret = load_secret(self.instance_id)
            if self._secret:
                logger.info(f"Loaded IPC authentication secret for instance '{self.instance_id}'")
                # Add auth capability
                if ServerCapability.AUTH.value not in self._capabilities:
                    self._capabilities.append(ServerCapability.AUTH.value)
            else:
                logger.warning(f"No IPC secret found for instance '{self.instance_id}' - auth disabled")
            
            # Clean up stale socket on Unix
            if self._is_unix:
                socket_path = Path(self._address)
                if socket_path.exists():
                    try:
                        socket_path.unlink()
                        logger.debug(f"Removed stale socket: {socket_path}")
                    except OSError as e:
                        logger.warning(f"Failed to remove stale socket: {e}", exc_info=True)
            
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
            logger.exception(f"Failed to start async IPC server: {e}")
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
    
    async def _send_hello(self, writer: asyncio.StreamWriter) -> None:
        """
        Send hello message to newly connected client with timeout (H6 fix).
        
        Contains protocol version, capabilities, and auth requirements.
        """
        hello = HelloMessage(
            protocol_version=self._protocol_version,
            server_version=self._server_version,
            instance_id=self.instance_id,
            requires_auth=self._secret is not None,
            capabilities=self._capabilities
        )
        
        hello_bytes = json.dumps(hello.to_dict()).encode('utf-8')
        hello_length = len(hello_bytes).to_bytes(4, 'big')
        
        # H6: Add timeout to hello send
        try:
            writer.write(hello_length + hello_bytes)
            await asyncio.wait_for(writer.drain(), timeout=self.WRITE_TIMEOUT)
            logger.debug(f"Sent hello: protocol={self._protocol_version}, auth_required={self._secret is not None}")
        except asyncio.TimeoutError:
            logger.warning(f"Timeout sending hello message after {self.WRITE_TIMEOUT}s", exc_info=True)
            raise

    async def _handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ) -> None:
        """Handle a client connection with timeouts (H6 fix)"""
        self._clients.append(writer)
        peer = writer.get_extra_info('peername') or 'unknown'
        logger.debug(f"IPC client connected: {peer}")
        
        try:
            # H6: Send hello message with timeout
            try:
                await asyncio.wait_for(
                    self._send_hello(writer),
                    timeout=self.CONNECTION_TIMEOUT
                )
            except asyncio.TimeoutError:
                logger.warning(f"Connection timeout for client {peer} during hello", exc_info=True)
                return
            
            while self._running:
                # H6: Read message length with timeout
                try:
                    length_bytes = await asyncio.wait_for(
                        reader.read(4),
                        timeout=self.READ_TIMEOUT
                    )
                except asyncio.TimeoutError:
                    logger.warning(f"Read timeout for client {peer} (no data after {self.READ_TIMEOUT}s)", exc_info=True)
                    break
                
                if not length_bytes:
                    break
                
                if len(length_bytes) < 4:
                    logger.warning("Incomplete length header")
                    break
                
                msg_length = int.from_bytes(length_bytes, 'big')
                if msg_length > 1024 * 1024:  # 1MB limit
                    logger.warning(f"Message too large: {msg_length}")
                    break
                
                # H6: Read message body with timeout
                try:
                    data = await asyncio.wait_for(
                        reader.read(msg_length),
                        timeout=self.READ_TIMEOUT
                    )
                except asyncio.TimeoutError:
                    logger.warning(f"Read timeout for client {peer} (message body)", exc_info=True)
                    break
                
                if len(data) < msg_length:
                    logger.warning("Incomplete message body")
                    break
                
                # Process request with timeout
                try:
                    request = json.loads(data.decode('utf-8'))
                    # H6: Add timeout to request processing
                    response = await asyncio.wait_for(
                        self._process_request(request, writer),
                        timeout=self.REQUEST_TIMEOUT
                    )
                except asyncio.TimeoutError:
                    logger.warning(f"Request processing timeout for client {peer} after {self.REQUEST_TIMEOUT}s", exc_info=True)
                    response = {
                        "success": False,
                        "error": f"Request processing timeout after {self.REQUEST_TIMEOUT}s",
                        "data": None
                    }
                except json.JSONDecodeError as e:
                    response = {
                        "success": False,
                        "error": f"Invalid JSON: {e}",
                        "data": None
                    }
                
                # H6: Send response with timeout
                try:
                    response_bytes = json.dumps(response).encode('utf-8')
                    response_length = len(response_bytes).to_bytes(4, 'big')
                    writer.write(response_length + response_bytes)
                    await asyncio.wait_for(writer.drain(), timeout=self.WRITE_TIMEOUT)
                except asyncio.TimeoutError:
                    logger.warning(f"Write timeout for client {peer} after {self.WRITE_TIMEOUT}s", exc_info=True)
                    break
                
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
            logger.exception(f"Error handling client {peer}: {e}")
        finally:
            if writer in self._clients:
                self._clients.remove(writer)
            # Clean up auth state
            self._authenticated_clients.discard(writer)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            logger.debug(f"IPC client disconnected: {peer}")
    
    async def _process_request(
        self,
        request: Dict[str, Any],
        writer: asyncio.StreamWriter
    ) -> Dict[str, Any]:
        """
        Process IPC request with authentication and rate limiting.
        
        Args:
            request: Request dict with 'command' and optional 'args'
            writer: Client connection for tracking auth state
            
        Returns:
            Response dict with 'success', 'data', and optional 'error'
        """
        command = request.get("command", "")
        args = request.get("args", {})
        request_id = request.get("request_id", "")
        client_version = request.get("protocol_version", "1.0")
        
        # Check protocol version compatibility
        if not is_version_compatible(client_version, MIN_CLIENT_VERSION):
            logger.warning(f"Client version {client_version} incompatible (min: {MIN_CLIENT_VERSION})")
            return {
                "success": False,
                "error": f"Protocol version {client_version} not supported. Minimum: {MIN_CLIENT_VERSION}",
                "data": None,
                "request_id": request_id,
                "protocol_version": self._protocol_version
            }
        
        # Get client ID for rate limiting (peer address or connection hash)
        peer = writer.get_extra_info('peername')
        client_id = str(peer) if peer else str(id(writer))
        
        # Rate limiting check (applies to all requests)
        if not self._rate_limiter.check_rate_limit(client_id):
            logger.warning(f"Rate limit exceeded for client {client_id}")
            return {
                "success": False,
                "error": "Rate limit exceeded. Try again later.",
                "data": None,
                "request_id": request_id,
                "protocol_version": self._protocol_version
            }
        
        try:
            # Handle auth command (always allowed)
            if command == "auth":
                return await self._handle_auth(args, writer, request_id)
            
            # Ping is allowed without auth (for connection testing)
            if command == "ping":
                data = {"pong": True, "authenticated": writer in self._authenticated_clients}
                return {
                    "success": True,
                    "data": data,
                    "error": None,
                    "request_id": request_id,
                    "protocol_version": self._protocol_version
                }
            
            # All other commands require authentication (if secret is configured)
            if self._secret and writer not in self._authenticated_clients:
                logger.warning(f"Unauthenticated request for command: {command}")
                return {
                    "success": False,
                    "error": "Authentication required",
                    "data": None,
                    "request_id": request_id,
                    "protocol_version": self._protocol_version
                }
            
            # Process authenticated commands
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
                    "request_id": request_id,
                    "protocol_version": self._protocol_version
                }
            
            return {
                "success": True,
                "data": data,
                "error": None,
                "request_id": request_id,
                "protocol_version": self._protocol_version
            }
            
        except Exception as e:
            logger.exception(f"Error processing command {command}: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": None,
                "request_id": request_id,
                "protocol_version": self._protocol_version
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
    
    async def _handle_auth(
        self,
        args: Dict[str, Any],
        writer: asyncio.StreamWriter,
        request_id: str
    ) -> Dict[str, Any]:
        """
        Handle authentication request.
        
        Args:
            args: Should contain 'token' key
            writer: Client connection to mark as authenticated
            request_id: Request ID for response
            
        Returns:
            Response indicating auth success/failure
        """
        # If no secret configured, auth is a no-op success
        if not self._secret:
            self._authenticated_clients.add(writer)
            logger.debug("Auth successful (no secret configured)")
            return {
                "success": True,
                "data": {"authenticated": True, "message": "Auth not required"},
                "error": None,
                "request_id": request_id,
                "protocol_version": self._protocol_version
            }
        
        token = args.get("token", "")
        if not token:
            logger.warning("Auth attempt with no token")
            return {
                "success": False,
                "error": "Token required",
                "data": {"authenticated": False},
                "request_id": request_id,
                "protocol_version": self._protocol_version
            }
        
        # Validate token using timing-safe comparison
        if validate_token(token, self._secret):
            self._authenticated_clients.add(writer)
            logger.info("Client authenticated successfully")
            return {
                "success": True,
                "data": {"authenticated": True},
                "error": None,
                "request_id": request_id,
                "protocol_version": self._protocol_version
            }
        else:
            logger.warning("Auth failed: invalid token")
            return {
                "success": False,
                "error": "Invalid token",
                "data": {"authenticated": False},
                "request_id": request_id,
                "protocol_version": self._protocol_version
            }


# For backward compatibility
ServiceAsyncIPCServer = AsyncIPCServer
