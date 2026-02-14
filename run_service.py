"""
Standalone Service Launcher (No GUI)

Launches a pyWATS client service instance without GUI.
Designed to run as an independent background process.

Features:
- No GUI dependencies (headless operation)
- Lock file tracking (PID, start time, status)
- Survives configurator crashes
- Can be managed via CLI or GUI

Lock File Location:
- Windows: C:/ProgramData/pyWATS/instances/{instance_id}/service.lock
- Linux: /var/lib/pywats/instances/{instance_id}/service.lock

Usage:
    python run_service.py [instance_id]
    
Examples:
    python run_service.py                # Launch "default" instance
    python run_service.py default        # Launch "default" instance
    python run_service.py client_b       # Launch "client_b" instance
"""

import sys
import os
import logging
import json
import asyncio
import signal
from pathlib import Path
from datetime import datetime
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


class ServiceLockFile:
    """Manage service lock file for process tracking."""
    
    def __init__(self, instance_dir: Path):
        self.lock_path = instance_dir / "service.lock"
        self.instance_dir = instance_dir
        self._pid = os.getpid()
    
    def write(self, instance_id: str, config_data: dict) -> None:
        """Write lock file with service metadata."""
        try:
            lock_data = {
                "pid": self._pid,
                "instance_id": instance_id,
                "instance_name": config_data.get("instance_name", instance_id),
                "started_at": datetime.now().isoformat(),
                "service_url": config_data.get("service_address", ""),
                "config_path": str(self.instance_dir / "client_config.json"),
            }
            
            with open(self.lock_path, 'w') as f:
                json.dump(lock_data, f, indent=2)
            
            logger.info(f"Lock file created: {self.lock_path} (PID: {self._pid})")
            
        except Exception as e:
            logger.error(f"Failed to write lock file: {e}")
    
    def delete(self) -> None:
        """Delete lock file on service shutdown."""
        try:
            if self.lock_path.exists():
                self.lock_path.unlink()
                logger.info(f"Lock file deleted: {self.lock_path}")
        except Exception as e:
            logger.error(f"Failed to delete lock file: {e}")
    
    @staticmethod
    def read(instance_dir: Path) -> Optional[dict]:
        """Read lock file and return service metadata (None if not running)."""
        lock_path = instance_dir / "service.lock"
        if not lock_path.exists():
            return None
        
        try:
            with open(lock_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read lock file {lock_path}: {e}")
            return None
    
    @staticmethod
    def is_process_running(pid: int) -> bool:
        """Check if process with given PID is running (cross-platform)."""
        try:
            # Send signal 0 to check if process exists (doesn't kill it)
            if os.name == 'nt':
                # Windows: Use tasklist
                import subprocess
                result = subprocess.run(
                    ['tasklist', '/FI', f'PID eq {pid}'],
                    capture_output=True,
                    text=True
                )
                return str(pid) in result.stdout
            else:
                # Linux/Mac: Send signal 0
                os.kill(pid, 0)
                return True
        except (OSError, ProcessLookupError):
            return False


async def run_service(instance_id: str, config_path: Path, instance_dir: Path) -> int:
    """Run the service with proper lifecycle management."""
    
    service = None
    lock_file = ServiceLockFile(instance_dir)
    
    try:
        from pywats_client.core.config import ClientConfig
        from pywats_client.service.async_client_service import AsyncClientService
        
        # Load configuration
        if config_path.exists():
            config = ClientConfig.load(config_path)
            logger.info(f"Loaded config from: {config_path}")
        else:
            logger.error(f"Config not found: {config_path}")
            logger.error("Please run the configurator to create a config first")
            return 1
        
        # Write lock file
        config_data = {
            "instance_name": config.instance_name,
            "service_address": config.service_address,
        }
        lock_file.write(instance_id, config_data)
        
        # Create and start service
        logger.info("=" * 80)
        logger.info(f"Starting pyWATS Service: {instance_id}")
        logger.info(f"Instance Name: {config.instance_name}")
        logger.info(f"Service URL: {config.service_address or 'Not configured'}")
        logger.info("=" * 80)
        
        service = AsyncClientService(instance_id)
        
        # Setup signal handlers for graceful shutdown
        shutdown_event = asyncio.Event()
        
        def signal_handler(sig, frame):
            logger.info(f"Received signal {sig}, shutting down...")
            shutdown_event.set()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start service in background
        service_task = asyncio.create_task(service.start())
        
        logger.info("Service started successfully (Ctrl+C to stop)")
        logger.info("=" * 80)
        
        # Wait for shutdown signal
        await shutdown_event.wait()
        
        # Stop service
        logger.info("Stopping service...")
        await service.stop()
        
        # Cancel service task
        if not service_task.done():
            service_task.cancel()
            try:
                await service_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Service stopped successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Service error: {e}", exc_info=True)
        return 1
        
    finally:
        # Always delete lock file on exit
        lock_file.delete()


def main():
    """Main entry point."""
    
    # Get instance_id from command line (default: "default")
    instance_id = sys.argv[1] if len(sys.argv) > 1 else "default"
    
    # Get system-wide instance directory
    if os.name == 'nt':
        base_path = Path(os.environ.get('PROGRAMDATA', 'C:\\ProgramData')) / 'pyWATS' / 'instances'
    else:
        base_path = Path('/var/lib/pywats/instances')
    
    instance_dir = base_path / instance_id
    config_path = instance_dir / "client_config.json"
    
    # Check if instance exists
    if not instance_dir.exists():
        logger.error(f"Instance directory not found: {instance_dir}")
        logger.error("Available instances:")
        if base_path.exists():
            for item in base_path.iterdir():
                if item.is_dir():
                    logger.error(f"  - {item.name}")
        else:
            logger.error(f"  (none - base path does not exist: {base_path})")
        return 1
    
    # Check for existing lock file
    existing_lock = ServiceLockFile.read(instance_dir)
    if existing_lock:
        pid = existing_lock.get('pid')
        if ServiceLockFile.is_process_running(pid):
            logger.error(f"Service already running (PID: {pid})")
            logger.error(f"Lock file: {instance_dir / 'service.lock'}")
            logger.error("Stop the existing service first or delete stale lock file")
            return 1
        else:
            logger.warning(f"Stale lock file found (PID {pid} not running)")
            logger.warning(f"Removing stale lock: {instance_dir / 'service.lock'}")
            (instance_dir / "service.lock").unlink()
    
    # Run service
    try:
        return asyncio.run(run_service(instance_id, config_path, instance_dir))
    except KeyboardInterrupt:
        logger.info("Service interrupted by user")
        return 0


if __name__ == "__main__":
    sys.exit(main())
