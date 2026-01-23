"""
Inter-Process Communication for pyWATS Client

Provides IPC between service instances and GUI using Qt Local Sockets.

Components:
- ServiceIPCServer: Runs in service mode, handles GUI requests
- ServiceIPCClient: Used by GUI to communicate with service
- ServiceDiscovery: Discovers all running service instances

Protocol: JSON messages over QLocalSocket
"""

import json
import logging
from typing import Optional, Dict, Any, List, Callable
from pathlib import Path
from dataclasses import dataclass, asdict

from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtCore import QObject, Signal, QByteArray

logger = logging.getLogger(__name__)


@dataclass
class InstanceInfo:
    """Information about a discovered service instance"""
    instance_id: str
    socket_name: str
    status: str = "unknown"  # unknown, online, offline
    connection_state: str = "unknown"
    config_file: Optional[str] = None
    uptime: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class ServiceIPCServer(QObject):
    """
    IPC Server for service mode.
    
    Listens for connections from GUI clients and responds to commands.
    Runs in service process.
    
    Usage:
        server = ServiceIPCServer(instance_id="station1", app=my_app)
        server.start()
        # Server runs, handling GUI requests
        server.stop()
    """
    
    # Signals
    config_update_requested = Signal(dict)  # Emitted when GUI requests config change
    command_received = Signal(str)  # Emitted when GUI sends command (restart, stop, etc.)
    
    def __init__(self, instance_id: str, app: Any, parent: Optional[QObject] = None):
        """
        Initialize IPC server.
        
        Args:
            instance_id: Unique instance identifier
            app: pyWATSApplication instance (for status queries)
            parent: Qt parent object
        """
        super().__init__(parent)
        self.instance_id = instance_id
        self.app = app
        self.socket_name = f"pyWATS_Service_{instance_id}"
        
        self._server: Optional[QLocalServer] = None
        self._clients: List[QLocalSocket] = []
        
    def start(self) -> bool:
        """
        Start the IPC server.
        
        Returns:
            True if started successfully
        """
        # Remove any stale server
        QLocalServer.removeServer(self.socket_name)
        
        # Create server
        self._server = QLocalServer(self)
        self._server.newConnection.connect(self._on_new_connection)
        
        if not self._server.listen(self.socket_name):
            logger.error(f"Failed to start IPC server: {self._server.errorString()}")
            return False
        
        logger.info(f"IPC server started: {self.socket_name}")
        return True
    
    def stop(self) -> None:
        """Stop the IPC server"""
        if self._server:
            self._server.close()
            logger.info(f"IPC server stopped: {self.socket_name}")
        
        # Disconnect all clients
        for client in self._clients:
            client.disconnectFromServer()
        self._clients.clear()
    
    def _on_new_connection(self) -> None:
        """Handle new client connection"""
        if not self._server:
            return
        
        client = self._server.nextPendingConnection()
        if not client:
            return
        
        logger.debug(f"New IPC client connected")
        
        client.readyRead.connect(lambda: self._on_client_data(client))
        client.disconnected.connect(lambda: self._on_client_disconnected(client))
        
        self._clients.append(client)
    
    def _on_client_data(self, client: QLocalSocket) -> None:
        """Handle data from client"""
        try:
            data = bytes(client.readAll()).decode('utf-8')
            if not data:
                return
            
            # Parse JSON command
            try:
                message = json.loads(data)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from client: {e}")
                self._send_error(client, "Invalid JSON")
                return
            
            command = message.get("command")
            if not command:
                self._send_error(client, "Missing 'command' field")
                return
            
            logger.debug(f"IPC command received: {command}")
            
            # Handle command
            if command == "get_status":
                self._handle_get_status(client)
            elif command == "get_config":
                self._handle_get_config(client)
            elif command == "update_config":
                self._handle_update_config(client, message.get("config", {}))
            elif command == "ping":
                self._handle_ping(client)
            elif command == "restart":
                self.command_received.emit("restart")
                self._send_response(client, {"status": "ok", "message": "Restart initiated"})
            elif command == "stop":
                self.command_received.emit("stop")
                self._send_response(client, {"status": "ok", "message": "Stop initiated"})
            else:
                self._send_error(client, f"Unknown command: {command}")
        
        except Exception as e:
            logger.error(f"Error handling client data: {e}", exc_info=True)
            self._send_error(client, f"Server error: {str(e)}")
    
    def _handle_get_status(self, client: QLocalSocket) -> None:
        """Handle get_status command"""
        try:
            # Get status from application
            status_info = {
                "status": self.app.status.value if hasattr(self.app, 'status') else "unknown",
                "instance_id": self.instance_id,
                "config_file": str(self.app.config.config_path) if hasattr(self.app.config, 'config_path') else None,
                "services": {},
                "stats": {}
            }
            
            # Get service statuses
            if hasattr(self.app, '_connection') and self.app._connection:
                status_info["services"]["connection"] = str(self.app._connection.status.value) if hasattr(self.app._connection, 'status') else "unknown"
                status_info["connection_state"] = str(self.app._connection.status.value) if hasattr(self.app._connection, 'status') else "unknown"
            
            if hasattr(self.app, '_process_sync') and self.app._process_sync:
                status_info["services"]["process_sync"] = "running"
            
            if hasattr(self.app, '_report_queue') and self.app._report_queue:
                status_info["services"]["report_queue"] = "running"
                # Get queue size if available
                if hasattr(self.app._report_queue, 'queue_size'):
                    status_info["stats"]["queue_size"] = self.app._report_queue.queue_size()
            
            if hasattr(self.app, '_converter_manager') and self.app._converter_manager:
                status_info["services"]["converter_manager"] = "running"
            
            self._send_response(client, status_info)
        
        except Exception as e:
            logger.error(f"Error getting status: {e}", exc_info=True)
            self._send_error(client, f"Failed to get status: {str(e)}")
    
    def _handle_get_config(self, client: QLocalSocket) -> None:
        """Handle get_config command"""
        try:
            # Convert config to dict
            config_dict = self.app.config.to_dict() if hasattr(self.app.config, 'to_dict') else {}
            self._send_response(client, {"config": config_dict})
        
        except Exception as e:
            logger.error(f"Error getting config: {e}", exc_info=True)
            self._send_error(client, f"Failed to get config: {str(e)}")
    
    def _handle_update_config(self, client: QLocalSocket, config_updates: Dict[str, Any]) -> None:
        """Handle update_config command"""
        try:
            # Emit signal for application to handle
            self.config_update_requested.emit(config_updates)
            self._send_response(client, {"status": "ok", "message": "Config update requested"})
        
        except Exception as e:
            logger.error(f"Error updating config: {e}", exc_info=True)
            self._send_error(client, f"Failed to update config: {str(e)}")
    
    def _handle_ping(self, client: QLocalSocket) -> None:
        """Handle ping command"""
        self._send_response(client, {"status": "ok", "message": "pong"})
    
    def _send_response(self, client: QLocalSocket, data: Dict[str, Any]) -> None:
        """Send JSON response to client"""
        try:
            response = json.dumps(data)
            client.write(response.encode('utf-8'))
            client.flush()
        except Exception as e:
            logger.error(f"Error sending response: {e}")
    
    def _send_error(self, client: QLocalSocket, error_message: str) -> None:
        """Send error response to client"""
        self._send_response(client, {"error": error_message})
    
    def _on_client_disconnected(self, client: QLocalSocket) -> None:
        """Handle client disconnection"""
        logger.debug("IPC client disconnected")
        if client in self._clients:
            self._clients.remove(client)
        client.deleteLater()


class ServiceIPCClient(QObject):
    """
    IPC Client for GUI mode.
    
    Connects to a service instance and sends commands/queries.
    Runs in GUI process.
    
    Usage:
        client = ServiceIPCClient(instance_id="station1")
        if client.connect():
            status = client.get_status()
            client.disconnect()
    """
    
    # Signals
    connected = Signal()
    disconnected = Signal()
    error_occurred = Signal(str)
    
    def __init__(self, instance_id: str, parent: Optional[QObject] = None):
        """
        Initialize IPC client.
        
        Args:
            instance_id: Instance ID to connect to
            parent: Qt parent object
        """
        super().__init__(parent)
        self.instance_id = instance_id
        self.socket_name = f"pyWATS_Service_{instance_id}"
        
        self._socket: Optional[QLocalSocket] = None
        self._response_data: Optional[str] = None
    
    def connect_to_service(self, timeout_ms: int = 1000) -> bool:
        """
        Connect to service instance.
        
        Args:
            timeout_ms: Connection timeout in milliseconds
            
        Returns:
            True if connected successfully
        """
        self._socket = QLocalSocket(self)
        self._socket.connectToServer(self.socket_name)
        
        if not self._socket.waitForConnected(timeout_ms):
            error = self._socket.errorString()
            logger.debug(f"Failed to connect to {self.socket_name}: {error}")
            self._socket.deleteLater()
            self._socket = None
            return False
        
        logger.debug(f"Connected to service: {self.socket_name}")
        self.connected.emit()
        return True
    
    def disconnect_from_service(self) -> None:
        """Disconnect from service"""
        if self._socket:
            self._socket.disconnectFromServer()
            self._socket.deleteLater()
            self._socket = None
            self.disconnected.emit()
    
    def is_connected(self) -> bool:
        """Check if connected to service"""
        return self._socket is not None and self._socket.state() == QLocalSocket.ConnectedState
    
    def _send_command(self, command: str, data: Optional[Dict[str, Any]] = None, timeout_ms: int = 2000) -> Optional[Dict[str, Any]]:
        """
        Send command and wait for response.
        
        Args:
            command: Command name
            data: Additional data to send
            timeout_ms: Response timeout in milliseconds
            
        Returns:
            Response dict or None on error
        """
        if not self.is_connected():
            logger.error("Not connected to service")
            return None
        
        try:
            # Build message
            message = {"command": command}
            if data:
                message.update(data)
            
            # Send message
            payload = json.dumps(message).encode('utf-8')
            self._socket.write(payload)
            self._socket.flush()
            
            # Wait for response
            if not self._socket.waitForReadyRead(timeout_ms):
                logger.error(f"Timeout waiting for response to {command}")
                return None
            
            # Read response
            response_data = bytes(self._socket.readAll()).decode('utf-8')
            response = json.loads(response_data)
            
            # Check for error
            if "error" in response:
                logger.error(f"Service error: {response['error']}")
                self.error_occurred.emit(response['error'])
                return None
            
            return response
        
        except Exception as e:
            logger.error(f"Error sending command {command}: {e}", exc_info=True)
            self.error_occurred.emit(str(e))
            return None
    
    def ping(self) -> bool:
        """
        Ping service to check if alive.
        
        Returns:
            True if service responded
        """
        response = self._send_command("ping")
        return response is not None and response.get("status") == "ok"
    
    def get_status(self) -> Optional[Dict[str, Any]]:
        """
        Get service status.
        
        Returns:
            Status dict or None on error
        """
        return self._send_command("get_status")
    
    def get_config(self) -> Optional[Dict[str, Any]]:
        """
        Get service configuration.
        
        Returns:
            Config dict or None on error
        """
        response = self._send_command("get_config")
        return response.get("config") if response else None
    
    def update_config(self, config_updates: Dict[str, Any]) -> bool:
        """
        Request config update.
        
        Args:
            config_updates: Config changes to apply
            
        Returns:
            True if request accepted
        """
        response = self._send_command("update_config", {"config": config_updates})
        return response is not None and response.get("status") == "ok"
    
    def send_restart(self) -> bool:
        """
        Request service restart.
        
        Returns:
            True if request accepted
        """
        response = self._send_command("restart")
        return response is not None and response.get("status") == "ok"
    
    def send_stop(self) -> bool:
        """
        Request service stop.
        
        Returns:
            True if request accepted
        """
        response = self._send_command("stop")
        return response is not None and response.get("status") == "ok"


class ServiceDiscovery:
    """
    Discovers running service instances.
    
    Scans for IPC sockets matching pattern and tests connectivity.
    
    Usage:
        discovery = ServiceDiscovery()
        instances = discovery.discover_instances()
        for instance in instances:
            print(f"Found: {instance.instance_id} ({instance.status})")
    """
    
    @staticmethod
    def discover_instances(timeout_ms: int = 500) -> List[InstanceInfo]:
        """
        Discover all running service instances.
        
        Args:
            timeout_ms: Connection timeout per instance
            
        Returns:
            List of discovered instances
        """
        instances = []
        
        # Try common instance IDs
        # TODO: Better discovery method - scan temp directory for lock files?
        common_ids = ["default", "station1", "station2", "station3", "station4", "station5"]
        
        for instance_id in common_ids:
            socket_name = f"pyWATS_Service_{instance_id}"
            
            # Try to connect
            client = ServiceIPCClient(instance_id)
            if client.connect_to_service(timeout_ms):
                # Get status
                status_data = client.get_status()
                
                if status_data:
                    instance = InstanceInfo(
                        instance_id=instance_id,
                        socket_name=socket_name,
                        status=status_data.get("status", "online"),
                        connection_state=status_data.get("connection_state", "unknown"),
                        config_file=status_data.get("config_file"),
                        uptime=status_data.get("stats", {}).get("uptime")
                    )
                else:
                    instance = InstanceInfo(
                        instance_id=instance_id,
                        socket_name=socket_name,
                        status="online"
                    )
                
                instances.append(instance)
                client.disconnect_from_service()
        
        logger.info(f"Discovered {len(instances)} service instance(s)")
        return instances
    
    @staticmethod
    def check_instance_running(instance_id: str, timeout_ms: int = 500) -> bool:
        """
        Check if specific instance is running.
        
        Args:
            instance_id: Instance ID to check
            timeout_ms: Connection timeout
            
        Returns:
            True if instance is running
        """
        client = ServiceIPCClient(instance_id)
        if client.connect_to_service(timeout_ms):
            is_alive = client.ping()
            client.disconnect_from_service()
            return is_alive
        return False
