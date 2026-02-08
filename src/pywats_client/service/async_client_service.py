"""
Async Client Service - Main Async Service Controller

Async-first implementation of the WATS Client Service.
Uses AsyncWATS for true async I/O and asyncio event loop for concurrency.

Benefits over sync ClientService:
- Non-blocking API calls
- Efficient concurrent I/O with single thread
- Better resource utilization
- Responsive GUI integration via qasync

See CLIENT_ASYNC_ARCHITECTURE.md for design details.
"""

import asyncio
import logging
from pywats.core.logging import get_logger
import os
import signal
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List

from pywats import AsyncWATS
from pywats.core.exceptions import PyWATSError

from ..core.config import ClientConfig

logger = get_logger(__name__)


class AsyncServiceStatus(Enum):
    """Service status states"""
    STOPPED = "Stopped"
    START_PENDING = "StartPending"
    RUNNING = "Running"
    STOP_PENDING = "StopPending"
    PAUSED = "Paused"
    ERROR = "Error"


class AsyncClientService:
    """
    Async-first WATS Client Service Controller.
    
    Uses AsyncWATS with asyncio event loop for efficient concurrent I/O.
    All timers, watchers, and background tasks run as asyncio.Tasks.
    
    Key differences from sync ClientService:
    - Uses AsyncWATS instead of sync pyWATS
    - All components use async/await
    - Single event loop thread instead of multiple threads
    - Better scalability and resource usage
    
    Usage:
        # Standalone (service mode)
        service = AsyncClientService(instance_id="default")
        asyncio.run(service.run())
        
        # With Qt (GUI mode) using qasync
        import qasync
        app = QApplication(sys.argv)
        loop = qasync.QEventLoop(app)
        asyncio.set_event_loop(loop)
        
        service = AsyncClientService()
        with loop:
            loop.run_until_complete(service.run())
    """
    
    # Timer intervals (in seconds)
    WATCHDOG_INTERVAL = 60.0
    PING_INTERVAL = 300.0  # 5 minutes
    REGISTER_INTERVAL = 3600.0  # 1 hour
    
    def __init__(self, instance_id: str = "default") -> None:
        """
        Initialize async service.
        
        Args:
            instance_id: Instance identifier for multi-instance support
        """
        self.instance_id = instance_id
        self.config = ClientConfig.load_for_instance(instance_id)
        
        # Service state
        self._status = AsyncServiceStatus.STOPPED
        self._shutdown_event = asyncio.Event()
        self._stopping = False  # Flag for graceful shutdown
        self._graceful_shutdown_timeout = 60.0  # Seconds to wait for operations to complete
        self._force_shutdown_timeout = 120.0  # Additional seconds before hard kill
        
        # API client (AsyncWATS with auto-discovery)
        self.api: Optional[AsyncWATS] = None
        
        # Async components (created on start)
        self._converter_pool: Optional['AsyncConverterPool'] = None
        self._pending_queue: Optional['AsyncPendingQueue'] = None
        
        # Metrics collector (optional - created if enabled in config)
        self._metrics_collector: Optional['MetricsCollector'] = None
        
        # Background tasks
        self._tasks: List[asyncio.Task] = []
        self._task_restart_counts: Dict[str, int] = {}  # Track task restarts
        self._task_last_restart: Dict[str, datetime] = {}  # Track restart times
        
        # IPC server for GUI communication
        self._ipc_server: Optional[Any] = None
        
        # Health server for Docker/K8s
        self._health_port = int(os.environ.get('PYWATS_HEALTH_PORT', '8080'))
        self._health_server: Optional[Any] = None
        
        # Statistics
        self._stats: Dict[str, Any] = {
            "start_time": None,
            "reports_submitted": 0,
            "conversions_completed": 0,
            "errors": 0,
            "last_ping": None,
            "api_status": "Offline"
        }
        
        logger.info(f"AsyncClientService initialized [instance: {instance_id}]")
    
    @property
    def status(self) -> AsyncServiceStatus:
        """Get current service status"""
        return self._status
    
    @property
    def is_running(self) -> bool:
        """Check if service is running"""
        return self._status == AsyncServiceStatus.RUNNING
    
    @property
    def api_status(self) -> str:
        """Get API connection status"""
        return self._stats.get("api_status", "Offline")
    
    @property
    def stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        return self._stats.copy()
    
    # =========================================================================
    # Lifecycle
    # =========================================================================
    
    async def run(self) -> None:
        """
        Start and run the service (main entry point).
        
        Blocks until shutdown is signaled. For GUI integration, use with qasync.
        """
        if self._status != AsyncServiceStatus.STOPPED:
            logger.warning(f"Service already in state: {self._status.value}")
            return
        
        try:
            await self.start()
            
            # Wait for shutdown signal
            await self._shutdown_event.wait()
            
        except asyncio.CancelledError:
            logger.info("Service cancelled")
        except Exception as e:
            logger.error(f"Service error: {e}", exc_info=True)
            self._status = AsyncServiceStatus.ERROR
        finally:
            await self.stop()
    
    async def start(self) -> None:
        """
        Start the service components.
        
        Order of initialization (matching C# ClientSvc.OnStart):
        1. Initialize and connect API
        2. Start watchdog timer
        3. Start ping timer
        4. Start registration timer
        5. Initialize PendingQueue (async)
        6. Initialize ConverterPool (async)
        7. Setup config watcher
        8. Setup IPC server
        9. Start health server
        """
        logger.info(f"AsyncClientService starting @{datetime.now().isoformat()}")
        self._set_status(AsyncServiceStatus.START_PENDING)
        self._stats["start_time"] = datetime.now().isoformat()
        
        try:
            # 1. Initialize API (with auto-discovery if available)
            await self._initialize_api()
            
            # 2-4. Start timers as async tasks (wrapped for safety)
            self._tasks.append(
                asyncio.create_task(
                    self._safe_task(self._watchdog_loop(), "watchdog"),
                    name="watchdog"
                )
            )
            logger.info("Watchdog timer started (60s)")
            
            self._tasks.append(
                asyncio.create_task(
                    self._safe_task(self._ping_loop(), "ping"),
                    name="ping"
                )
            )
            logger.info("Ping timer started (5min)")
            
            self._tasks.append(
                asyncio.create_task(
                    self._safe_task(self._register_loop(), "register"),
                    name="register"
                )
            )
            logger.info("Registration timer started (1hr)")
            
            # 5. Initialize async pending queue
            from .async_pending_queue import AsyncPendingQueue
            self._pending_queue = AsyncPendingQueue(
                api=self.api,
                reports_dir=self.config.get_reports_path(),
                max_concurrent=self.config.max_concurrent_uploads,
                max_queue_size=self.config.max_queue_size
            )
            self._tasks.append(
                asyncio.create_task(
                    self._safe_task(self._pending_queue.run(), "pending_queue"),
                    name="pending_queue"
                )
            )
            logger.info("AsyncPendingQueue started")
            
            # 6. Initialize async converter pool
            from .async_converter_pool import AsyncConverterPool
            self._converter_pool = AsyncConverterPool(
                config=self.config,
                api=self.api,
                max_concurrent=10
            )
            self._tasks.append(
                asyncio.create_task(
                    self._safe_task(self._converter_pool.run(), "converter_pool"),
                    name="converter_pool"
                )
            )
            logger.info("AsyncConverterPool started")
            
            # 7. Setup config watcher (wrapped for safety)
            self._tasks.append(
                asyncio.create_task(
                    self._safe_task(self._config_watch_loop(), "config_watcher"),
                    name="config_watcher"
                )
            )
            logger.info("Config watcher started")
            
            # 8. Start task monitor (wrapped for safety)
            self._tasks.append(
                asyncio.create_task(
                    self._safe_task(self._monitor_tasks(), "task_monitor"),
                    name="task_monitor"
                )
            )
            logger.info("Task monitor started")
            
            # 9. Setup IPC server
            await self._setup_ipc_server()
            
            # 10. Start health server
            await self._start_health_server()
            
            self._set_status(AsyncServiceStatus.RUNNING)
            logger.info("AsyncClientService started successfully")
            
        except Exception as e:
            logger.error(f"Service startup failed: {e}", exc_info=True)
            self._set_status(AsyncServiceStatus.ERROR)
            raise
    
    async def stop(self) -> None:
        """
        Stop the service gracefully with two-phase shutdown.
        
        Phase 1: Stop accepting new work, wait for in-flight operations (60s)
        Phase 2: Force cancel remaining tasks (120s total)
        Phase 3: Hard cleanup
        
        This prevents data loss by allowing operations to checkpoint before shutdown.
        """
        if self._status == AsyncServiceStatus.STOPPED:
            return
        
        logger.info("Stopping AsyncClientService (two-phase shutdown)...")
        self._set_status(AsyncServiceStatus.STOP_PENDING)
        
        # Signal shutdown
        self._shutdown_event.set()
        self._stopping = True
        
        # PHASE 1: Stop accepting new work, wait for completion (60s)
        logger.info("Phase 1: Stopping new work acceptance, waiting for in-flight operations...")
        try:
            # Stop components from accepting new work
            if self._pending_queue:
                logger.info("Pausing pending queue...")
                await self._pending_queue.pause()
            
            if self._converter_pool:
                logger.info("Stopping converter pool from accepting new work...")
                await self._converter_pool.stop_accepting()
            
            # Wait for in-flight operations to complete
            await asyncio.wait_for(
                self._wait_for_completion(),
                timeout=self._graceful_shutdown_timeout
            )
            logger.info("Phase 1 complete: All operations completed gracefully")
            
        except asyncio.TimeoutError:
            logger.warning(
                f"Phase 1 timeout ({self._graceful_shutdown_timeout}s): "
                "Some operations did not complete, proceeding to Phase 2..."
            )
        
        # PHASE 2: Force cancel remaining tasks (additional 60s)
        logger.info("Phase 2: Force cancelling remaining tasks...")
        try:
            await asyncio.wait_for(
                self._force_cancel_tasks(),
                timeout=self._force_shutdown_timeout - self._graceful_shutdown_timeout
            )
            logger.info("Phase 2 complete: All tasks cancelled")
            
        except asyncio.TimeoutError:
            logger.exception(
                f"Phase 2 timeout ({self._force_shutdown_timeout}s total): "
                "Hard killing remaining tasks"
            )
        
        # PHASE 3: Hard cleanup
        logger.info("Phase 3: Final cleanup...")
        
        # Verify pending queue status
        if self._pending_queue:
            pending_count = await self._pending_queue.get_pending_count()
            if pending_count > 0:
                logger.warning(
                    f"{pending_count} operations still pending - will retry on next start"
                )
            await self._pending_queue.stop()
            self._pending_queue = None
        
        if self._converter_pool:
            await self._converter_pool.stop()
            self._converter_pool = None
        
        # Clear task list
        self._tasks.clear()
        
        # Stop IPC server
        if self._ipc_server:
            await self._stop_ipc_server()
        
        # Stop health server
        if self._health_server:
            await self._stop_health_server()
        
        # Close API connection properly via context manager exit
        if self.api:
            try:
                await self.api.__aexit__(None, None, None)
            except Exception as e:
                logger.warning(f"API cleanup error (non-fatal): {e}", exc_info=True)
            self.api = None
        
        self._set_status(AsyncServiceStatus.STOPPED)
        logger.info("AsyncClientService stopped successfully")
    
    async def _wait_for_completion(self) -> None:
        """
        Wait for all in-flight operations to complete.
        
        Checks:
        - Pending queue has no active uploads
        - Converter pool has no active conversions
        - All operations have checkpointed
        """
        logger.info("Waiting for in-flight operations to complete...")
        
        while True:
            # Check pending queue
            pending_active = 0
            if self._pending_queue:
                pending_active = await self._pending_queue.get_active_count()
            
            # Check converter pool
            converter_active = 0
            if self._converter_pool:
                converter_active = await self._converter_pool.get_active_count()
            
            total_active = pending_active + converter_active
            
            if total_active == 0:
                logger.info("All in-flight operations completed")
                break
            
            logger.debug(
                f"Waiting for {total_active} operations "
                f"(pending: {pending_active}, converters: {converter_active})"
            )
            await asyncio.sleep(1.0)
    
    async def _force_cancel_tasks(self) -> None:
        """
        Force cancel all remaining background tasks.
        
        Tasks that haven't completed after graceful period are cancelled.
        """
        logger.info(f"Force cancelling {len(self._tasks)} background tasks...")
        
        # Cancel all tasks
        for task in self._tasks:
            if not task.done():
                task.cancel()
                logger.debug(f"Cancelling task: {task.get_name()}")
        
        # Wait for cancellations to complete
        if self._tasks:
            results = await asyncio.gather(*self._tasks, return_exceptions=True)
            
            # Log any unexpected exceptions (not CancelledError)
            for i, result in enumerate(results):
                if isinstance(result, Exception) and not isinstance(result, asyncio.CancelledError):
                    task_name = self._tasks[i].get_name() if i < len(self._tasks) else "unknown"
                    logger.error(f"Task {task_name} raised exception: {result}")
    
    def request_shutdown(self) -> None:
        """Request graceful shutdown (can be called from sync code)"""
        self._shutdown_event.set()
    
    # =========================================================================
    # Task Safety & Monitoring
    # =========================================================================
    
    async def _safe_task(self, coro, task_name: str) -> None:
        """
        Wrap coroutine with exception handling.
        
        Prevents silent failures by catching and logging all exceptions
        except CancelledError (which is used for graceful shutdown).
        
        Args:
            coro: Coroutine to execute
            task_name: Name for logging
        """
        try:
            await coro
        except asyncio.CancelledError:
            # Allow proper cancellation during shutdown
            logger.debug(f"Task {task_name} cancelled")
            raise
        except Exception as e:
            # Log exception with full traceback
            logger.error(
                f"Background task '{task_name}' failed with exception: {e}",
                exc_info=True
            )
            self._stats["errors"] += 1
            
            # Update service status if critical task fails
            if task_name in ["pending_queue", "converter_pool"]:
                logger.critical(f"CRITICAL TASK FAILED: {task_name}")
                self._set_status(AsyncServiceStatus.ERROR)
    
    async def _monitor_tasks(self) -> None:
        """
        Monitor background tasks for unexpected death.
        
        Checks task status every 30s and detects:
        - Tasks that completed when they shouldn't have
        - Tasks that died with exceptions
        - Tasks that need restart
        """
        try:
            while not self._shutdown_event.is_set():
                try:
                    await asyncio.sleep(30.0)
                    
                    # Check each task
                    for task in self._tasks:
                        task_name = task.get_name()
                        
                        # If task is done but not cancelled, something went wrong
                        if task.done() and not task.cancelled():
                            exc = task.exception()
                            if exc:
                                logger.error(
                                    f"Detected dead task: {task_name} - Exception: {exc}"
                                )
                                self._stats["errors"] += 1
                                
                                # Update status if critical task died
                                if task_name in ["pending_queue", "converter_pool"]:
                                    logger.critical(
                                        f"Critical task {task_name} died unexpectedly!"
                                    )
                                    self._set_status(AsyncServiceStatus.ERROR)
                            else:
                                logger.warning(
                                    f"Task {task_name} completed unexpectedly "
                                    "(should run until shutdown)"
                                )
                
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    logger.error(f"Task monitor error: {e}", exc_info=True)
        
        except asyncio.CancelledError:
            logger.debug("Task monitor cancelled")
            raise
    
    # =========================================================================
    # API Initialization
    # =========================================================================
    
    async def _initialize_api(self) -> None:
        """
        Initialize AsyncWATS API with credentials.
        
        Supports:
        - Explicit credentials from config
        - Auto-discovery from running service
        - Optional metrics collection
        - Optional HTTP caching
        """
        logger.info("Initializing async API...")
        
        try:
            # Initialize metrics collector if enabled
            if self.config.enable_metrics:
                from pywats.core.metrics import MetricsCollector
                self._metrics_collector = MetricsCollector(
                    instance_id=self.instance_id,
                    enabled=True
                )
                logger.info("Metrics collection enabled")
            
            # Get runtime credentials
            service_address, api_token = self.config.get_runtime_credentials()
            
            # Create async API client with cache and metrics configuration
            self.api = AsyncWATS(
                base_url=service_address,
                token=api_token,
                instance_id=self.instance_id,
                enable_cache=self.config.enable_cache,
                cache_ttl=self.config.cache_ttl_seconds,
                cache_max_size=self.config.cache_max_size
            )
            
            # Enter async context
            await self.api.__aenter__()
            
            # Verify connection
            version = await self.api.get_version()
            logger.info(f"Connected to WATS server: {version}")
            
            self._stats["api_status"] = "Online"
            
        except Exception as e:
            logger.exception(f"API initialization failed: {e}")
            self._stats["api_status"] = "Error"
            # Continue in degraded mode (like C# implementation)
    
    # =========================================================================
    # Timer Loops (replace threading.Timer)
    # =========================================================================
    
    async def _watchdog_loop(self) -> None:
        """
        Watchdog timer loop - health checks every 60s.
        
        Checks:
        - Service is responsive
        - API connection is alive
        - Components are healthy
        """
        try:
            await asyncio.sleep(self.WATCHDOG_INTERVAL)  # Initial delay
            
            while not self._shutdown_event.is_set():
                try:
                    await self._on_watchdog_elapsed()
                except asyncio.CancelledError:
                    raise  # Always re-raise CancelledError
                except Exception as e:
                    logger.exception(f"Watchdog error: {e}")
                    self._stats["errors"] += 1
                
                try:
                    await asyncio.wait_for(
                        self._shutdown_event.wait(),
                        timeout=self.WATCHDOG_INTERVAL
                    )
                    break  # Shutdown requested
                except asyncio.TimeoutError:
                    pass  # Continue loop
        except asyncio.CancelledError:
            logger.debug("Watchdog loop cancelled")
            raise
    
    async def _on_watchdog_elapsed(self) -> None:
        """Handle watchdog timer tick"""
        logger.debug("Watchdog check")
        
        # Check API health
        if self.api:
            try:
                await asyncio.wait_for(
                    self.api.get_version(),
                    timeout=10.0
                )
                self._stats["api_status"] = "Online"
            except Exception:
                self._stats["api_status"] = "Offline"
        
        # Check pending queue health
        if self._pending_queue:
            queue_stats = self._pending_queue.stats
            if queue_stats.get("stuck_files", 0) > 0:
                logger.warning(f"Found {queue_stats['stuck_files']} stuck files in queue")
    
    async def _ping_loop(self) -> None:
        """
        Ping timer loop - connectivity check every 5 minutes.
        
        Verifies server is reachable and updates status.
        """
        try:
            await asyncio.sleep(self.PING_INTERVAL)  # Initial delay
            
            while not self._shutdown_event.is_set():
                try:
                    await self._on_ping_elapsed()
                except asyncio.CancelledError:
                    raise  # Always re-raise CancelledError
                except Exception as e:
                    logger.exception(f"Ping error: {e}")
                
                try:
                    await asyncio.wait_for(
                        self._shutdown_event.wait(),
                        timeout=self.PING_INTERVAL
                    )
                    break
                except asyncio.TimeoutError:
                    pass
        except asyncio.CancelledError:
            logger.debug("Ping loop cancelled")
            raise
    
    async def _on_ping_elapsed(self) -> None:
        """Handle ping timer tick"""
        if self.api:
            try:
                await self.api.get_version()
                self._stats["last_ping"] = datetime.now().isoformat()
                logger.debug("Ping successful")
            except Exception as e:
                logger.warning(f"Ping failed: {e}", exc_info=True)
    
    async def _register_loop(self) -> None:
        """
        Registration timer loop - status update every hour.
        
        Registers/updates client status with server.
        """
        try:
            await asyncio.sleep(60)  # Initial delay (1 minute)
            
            while not self._shutdown_event.is_set():
                try:
                    await self._on_register_elapsed()
                except asyncio.CancelledError:
                    raise  # Always re-raise CancelledError
                except Exception as e:
                    logger.exception(f"Registration error: {e}")
                
                try:
                    await asyncio.wait_for(
                        self._shutdown_event.wait(),
                        timeout=self.REGISTER_INTERVAL
                    )
                    break
                except asyncio.TimeoutError:
                    pass
        except asyncio.CancelledError:
            logger.debug("Register loop cancelled")
            raise
    
    async def _on_register_elapsed(self) -> None:
        """Handle registration timer tick"""
        # TODO: Implement client registration with server
        logger.debug("Registration update")
    
    async def _config_watch_loop(self) -> None:
        """
        Config file watcher loop.
        
        Watches for configuration changes and hot-reloads.
        """
        config_path = self.config.config_path
        last_mtime = config_path.stat().st_mtime if config_path.exists() else 0
        
        try:
            while not self._shutdown_event.is_set():
                try:
                    if config_path.exists():
                        current_mtime = config_path.stat().st_mtime
                        if current_mtime > last_mtime:
                            logger.info("Config file changed, reloading...")
                            await self._reload_config()
                            last_mtime = current_mtime
                except asyncio.CancelledError:
                    raise  # Always re-raise CancelledError
                except Exception as e:
                    logger.exception(f"Config watch error: {e}")
                
                try:
                    await asyncio.wait_for(
                        self._shutdown_event.wait(),
                        timeout=5.0  # Check every 5 seconds
                    )
                    break
                except asyncio.TimeoutError:
                    pass
        except asyncio.CancelledError:
            logger.debug("Config watch loop cancelled")
            raise
    
    async def _reload_config(self) -> None:
        """Reload configuration from file"""
        try:
            self.config = ClientConfig.load_for_instance(self.instance_id)
            
            # Update components with new config
            if self._converter_pool:
                await self._converter_pool.reload_config(self.config)
            
            logger.info("Configuration reloaded")
        except Exception as e:
            logger.exception(f"Config reload failed: {e}")
    
    # =========================================================================
    # IPC Server (for GUI communication)
    # =========================================================================
    
    async def _setup_ipc_server(self) -> None:
        """Setup IPC server for GUI communication (pure asyncio, no Qt)"""
        try:
            from .async_ipc_server import AsyncIPCServer
            self._ipc_server = AsyncIPCServer(self.instance_id, self)
            if await self._ipc_server.start():
                logger.info(f"Async IPC server started [instance: {self.instance_id}]")
            else:
                logger.warning("Async IPC server failed to start")
        except Exception as e:
            logger.exception(f"Async IPC server setup failed: {e}")
    
    async def _stop_ipc_server(self) -> None:
        """Stop IPC server"""
        if self._ipc_server:
            try:
                await self._ipc_server.stop()
            except Exception as e:
                logger.exception(f"IPC server stop failed: {e}")
            self._ipc_server = None
    
    # =========================================================================
    # Health Server (for Docker/K8s)
    # =========================================================================
    
    async def _start_health_server(self) -> None:
        """Start health check server with metrics and component wiring"""
        try:
            from .health_server import HealthServer
            self._health_server = HealthServer(port=self._health_port)
            self._health_server.set_health_check(self._get_health_status)
            
            # Wire components for /metrics endpoint
            if self._metrics_collector:
                self._health_server._metrics_collector = self._metrics_collector
                logger.debug("Wired MetricsCollector to health server")
            
            if self.api and hasattr(self.api, '_http_client'):
                self._health_server._http_client = self.api._http_client
                logger.debug("Wired HTTP client to health server for cache stats")
            
            if self._converter_pool:
                self._health_server._converter_pool = self._converter_pool
                logger.debug("Wired converter pool to health server for queue stats")
            
            self._health_server.start()
            logger.info(f"Health server started on port {self._health_port}")
        except Exception as e:
            logger.warning(f"Health server not started: {e}", exc_info=True)
        except Exception as e:
            logger.warning(f"Health server not started: {e}", exc_info=True)
    
    async def _stop_health_server(self) -> None:
        """Stop health server"""
        if self._health_server:
            try:
                self._health_server.stop()
            except Exception as e:
                logger.exception(f"Health server stop failed: {e}")
            self._health_server = None
    
    def _get_health_status(self) -> 'HealthStatus':
        """Get health status for health endpoint"""
        from .health_server import HealthStatus
        return HealthStatus(
            healthy=self.is_running,
            status="running" if self.is_running else "stopped",
            details={
                "service_status": self._status.value,
                "api_status": self._stats.get("api_status", "Unknown"),
                "uptime_seconds": self._get_uptime_seconds(),
                "instance_id": self.instance_id
            }
        )
    
    def _get_uptime_seconds(self) -> float:
        """Calculate uptime in seconds"""
        start_time = self._stats.get("start_time")
        if start_time:
            start = datetime.fromisoformat(start_time)
            return (datetime.now() - start).total_seconds()
        return 0
    
    # =========================================================================
    # IPC Command Handlers
    # =========================================================================
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get service status for IPC"""
        return {
            "status": self._status.value,
            "api_status": self._stats.get("api_status", "Offline"),
            "start_time": self._stats.get("start_time"),
            "reports_submitted": self._stats.get("reports_submitted", 0),
            "conversions_completed": self._stats.get("conversions_completed", 0),
            "errors": self._stats.get("errors", 0),
            "pending_queue": self._pending_queue.stats if self._pending_queue else {},
            "converter_pool": self._converter_pool.stats if self._converter_pool else {}
        }
    
    async def get_status_async(self) -> Dict[str, Any]:
        """Get service status for async IPC (same as get_service_status)"""
        return self.get_service_status()
    
    def get_status(self) -> Dict[str, Any]:
        """Alias for get_service_status (used by IPC server)"""
        return self.get_service_status()
    
    def get_credentials(self) -> Optional[Dict[str, str]]:
        """Get API credentials for auto-discovery"""
        try:
            service_address, api_token = self.config.get_runtime_credentials()
            return {
                "base_url": service_address,
                "token": api_token
            }
        except Exception:
            return None
    
    # =========================================================================
    # Internal
    # =========================================================================
    
    def _set_status(self, status: AsyncServiceStatus) -> None:
        """Update service status"""
        old_status = self._status
        self._status = status
        logger.info(f"Service status: {old_status.value} -> {status.value}")


# =========================================================================
# Entry Points
# =========================================================================

def run_async_service(instance_id: str = "default") -> None:
    """
    Run async service as standalone (non-GUI) mode.
    
    Args:
        instance_id: Instance identifier
    """
    service = AsyncClientService(instance_id)
    
    # Setup signal handlers
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}, shutting down...")
        service.request_shutdown()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the service
    asyncio.run(service.run())


def run_async_service_with_qt(instance_id: str = "default") -> None:
    """
    Run async service with Qt integration (GUI mode).
    
    Uses qasync to integrate asyncio with Qt event loop.
    
    Args:
        instance_id: Instance identifier
    """
    try:
        import qasync
        from PySide6.QtWidgets import QApplication
    except ImportError:
        logger.exception("qasync and PySide6 required for Qt mode")
        raise
    
    app = QApplication.instance() or QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    service = AsyncClientService(instance_id)
    
    with loop:
        loop.run_until_complete(service.run())
