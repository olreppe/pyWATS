"""
Shared Client Launcher

Provides a single entry point for launching pyWATS client instances (A, B, or custom).
Eliminates duplication between run_client_a.py and run_client_b.py.

Usage:
    from pywats_client.launcher import launch_client

    # Launch Client A (master)
    launch_client(instance_id="default", instance_name="Client A (Master)")

    # Launch Client B (secondary, with token sharing from A)
    launch_client(instance_id="client_b", instance_name="Client B (Secondary)", share_token_from="default")
"""

from __future__ import annotations

import sys
import os
import json
import asyncio
import logging
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pywats_client.core.config import ClientConfig
    from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
    from pywats_ui.framework.system_tray import SystemTrayIcon

logger = logging.getLogger(__name__)


def get_instance_base_path() -> Path:
    """Get the system-wide base path for instance configs.

    Returns:
        Path to instances directory (e.g. C:/ProgramData/Virinco/pyWATS/instances/)
    """
    if os.name == 'nt':
        return Path(os.environ.get('PROGRAMDATA', 'C:\\ProgramData')) / 'Virinco' / 'pyWATS' / 'instances'
    else:
        return Path('/var/lib/pywats/instances')


def migrate_old_config(old_config_path: Path, new_config: 'ClientConfig', instance_id: str) -> bool:
    """Migrate settings from old GUI config to new instance config if empty.

    Args:
        old_config_path: Path to legacy ~/.pywats/config.json
        new_config: New ClientConfig to populate
        instance_id: Instance identifier (for logging)

    Returns:
        True if migration occurred, False otherwise
    """
    if not old_config_path.exists():
        return False

    # Check if new config is empty (no server/token configured)
    if new_config.service_address or new_config.api_token:
        logger.info("Config already has settings, skipping migration")
        return False

    try:
        with open(old_config_path, 'r') as f:
            old_config = json.load(f)

        logger.info(f"Migrating settings from old config: {old_config_path}")

        # Migrate core connection settings
        if old_config.get('service_address'):
            new_config.service_address = old_config['service_address']
            logger.info(f"  Migrated service_address: {new_config.service_address}")

        if old_config.get('api_token'):
            new_config.api_token = old_config['api_token']
            logger.info("  Migrated api_token: ****")

        # Migrate station settings
        for key in ['station_name', 'location', 'purpose']:
            if old_config.get(key):
                setattr(new_config, key, old_config[key])
                logger.info(f"  Migrated {key}: {old_config[key]}")

        # Migrate converter settings
        if old_config.get('converters') and len(old_config['converters']) > 0:
            from pywats_client.core.config import ConverterConfig
            new_config.converters = [
                ConverterConfig.from_dict(c) if isinstance(c, dict) else c
                for c in old_config['converters']
            ]
            logger.info(f"  Migrated {len(new_config.converters)} converters")

        # Migrate other settings
        for key in ['proxy_mode', 'proxy_host', 'proxy_port', 'log_level',
                     'auto_connect', 'converters_enabled']:
            if key in old_config:
                setattr(new_config, key, old_config[key])

        logger.info("Migration complete!")
        return True

    except Exception as e:
        logger.error(f"Failed to migrate old config: {e}")
        return False


def share_token_from_instance(config: 'ClientConfig', source_instance_id: str = "default") -> bool:
    """Copy API token/URL from another instance if current config has none.

    Uses get_runtime_credentials() to also pick up env-var-based tokens
    (PYWATS_SERVER_URL / PYWATS_API_TOKEN).

    Args:
        config: Target config to populate
        source_instance_id: Instance to copy token from

    Returns:
        True if token was shared, False otherwise
    """
    if config.api_token:
        return False  # Already has a token

    base_path = get_instance_base_path()
    source_config_path = base_path / source_instance_id / "client_config.json"

    if not source_config_path.exists():
        return False

    try:
        from pywats_client.core.config import ClientConfig
        source_config = ClientConfig.load(source_config_path)
        # Use runtime credentials (includes env var fallback)
        source_url, source_token = source_config.get_runtime_credentials()
        if source_token:
            config.api_token = source_token
            config.service_address = source_url
            logger.info(f"Inherited API token from instance '{source_instance_id}'")
            return True
    except Exception as e:
        logger.warning(f"Could not load source config: {e}")

    return False


def load_or_create_config(
    instance_id: str,
    instance_name: str,
    share_token_from: Optional[str] = None
) -> 'ClientConfig':
    """Load existing config or create a new one for the given instance.

    Args:
        instance_id: Instance identifier (e.g. "default", "client_b")
        instance_name: Human-readable name (e.g. "Client A (Master)")
        share_token_from: If set, inherit API token from this instance when creating new config

    Returns:
        Loaded or newly created ClientConfig
    """
    from pywats_client.core.config import ClientConfig

    base_path = get_instance_base_path()
    config_path = base_path / instance_id / "client_config.json"
    old_config_path = Path.home() / ".pywats" / "config.json"

    if config_path.exists():
        config = ClientConfig.load(config_path)
        logger.info(f"Loaded config from: {config_path}")
        # Try migration from legacy config
        migrate_old_config(old_config_path, config, instance_id)
    else:
        logger.info(f"Creating new config for {instance_name}")
        config = ClientConfig(instance_id=instance_id)
        config.instance_name = instance_name
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config._config_path = config_path

        # Try migration from legacy config
        migrate_old_config(old_config_path, config, instance_id)

        # Token sharing from another instance
        if share_token_from:
            share_token_from_instance(config, share_token_from)

        config.save()
        logger.info(f"Config saved to: {config_path}")

    # Ensure instance directories exist
    instance_dir = config_path.parent
    for subdir in ['queue', 'logs', 'reports', 'converters']:
        (instance_dir / subdir).mkdir(exist_ok=True)

    return config


def launch_client(
    instance_id: str = "default",
    instance_name: str = "Client A (Master)",
    share_token_from: Optional[str] = None,
    enable_tray: bool = False
) -> int:
    """Launch a pyWATS client GUI instance.

    Args:
        instance_id: Instance identifier
        instance_name: Human-readable display name
        share_token_from: If set, inherit API token from this instance
        enable_tray: If True, create a persistent system tray icon

    Returns:
        Application exit code
    """
    try:
        import qasync
    except ImportError:
        qasync = None
        logger.warning("qasync not installed - async operations may not work correctly")

    logger.info("=" * 80)
    logger.info(f"pyWATS {instance_name}")
    logger.info("=" * 80)
    logger.info(f"Instance ID: {instance_id}")
    logger.info("=" * 80)

    try:
        # Set Windows AppUserModelID BEFORE creating QApplication
        # so the taskbar shows our icon instead of the default Python icon
        if os.name == 'nt':
            try:
                import ctypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    f"Virinco.pyWATS.Client.{instance_id}"
                )
            except Exception:
                pass  # Non-critical, continue without custom taskbar grouping

        from PySide6.QtWidgets import QApplication, QSystemTrayIcon
        from PySide6.QtGui import QIcon
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
        from pywats_ui.framework.system_tray import SystemTrayIcon, create_default_icon

        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName(f"pyWATS {instance_name}")
        app.setOrganizationName("pyWATS")

        if enable_tray:
            app.setQuitOnLastWindowClosed(False)  # Keep running even if window is hidden

        # Set application icon
        icon_path = Path(__file__).parent.parent / "pywats_ui" / "apps" / "resources" / "favicon.ico"
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))

        # Load or create config
        config = load_or_create_config(instance_id, instance_name, share_token_from)

        # Create main window
        window = ConfiguratorMainWindow(config=config)

        # Setup tray icon if requested
        tray_icon: Optional[SystemTrayIcon] = None
        if enable_tray and QSystemTrayIcon.isSystemTrayAvailable():
            tray_icon = _setup_tray_for_window(window, instance_name)
            window.set_tray_icon(tray_icon)

        window.show()

        # Auto-start background service if configured
        if config.get("service_auto_start", False):
            from pywats_client.core import service_manager
            svc_status = service_manager.get_service_status(instance_id)
            if not svc_status.is_running:
                logger.info("Auto-starting background service...")
                if service_manager.start_service(instance_id, wait=False):
                    logger.info("Background service started successfully")
                else:
                    logger.warning("Failed to auto-start background service")
            else:
                logger.info(f"Service already running (PID: {svc_status.pid})")

        logger.info(f"{instance_name} launched successfully")
        if tray_icon:
            logger.info("System tray icon active")
        logger.info("=" * 80)

        # Run with qasync event loop for async operations
        if qasync:
            logger.info("Using qasync event loop for async operations")
            loop = qasync.QEventLoop(app)
            asyncio.set_event_loop(loop)
            with loop:
                return loop.run_forever()
        else:
            logger.warning("Running without qasync - async operations may fail")
            return app.exec()

    except Exception as e:
        logger.error(f"Failed to launch {instance_name}: {e}", exc_info=True)
        return 1


def _setup_tray_for_window(
    window: 'ConfiguratorMainWindow',
    instance_name: str
) -> 'SystemTrayIcon':
    """Create a system tray icon integrated with the main window.

    Args:
        window: Main configurator window
        instance_name: Instance display name for tooltip

    Returns:
        Configured SystemTrayIcon
    """
    from pywats_ui.framework.system_tray import SystemTrayIcon
    from PySide6.QtGui import QIcon
    from pathlib import Path

    # Use favicon.ico if available
    icon_path = Path(__file__).parent.parent / "pywats_ui" / "apps" / "resources" / "favicon.ico"
    icon = QIcon(str(icon_path)) if icon_path.exists() else None

    tray = SystemTrayIcon(icon=icon)
    tray.setToolTip(f"pyWATS - {instance_name}")

    tray.add_application("Show Window", lambda: _show_window(window))
    tray.add_separator()
    tray.add_application("Restart Service", lambda: _restart_service_from_tray(window))
    tray.add_separator()
    tray.add_application("Quit", lambda: _quit_with_tray(window, tray))
    tray.show()

    return tray


def _show_window(window: 'ConfiguratorMainWindow') -> None:
    """Restore and bring window to front."""
    window.show()
    window.showNormal()
    window.activateWindow()
    window.raise_()


def _restart_service_from_tray(window: 'ConfiguratorMainWindow') -> None:
    """Restart service from system tray menu."""
    # Delegate to main window's restart handler
    if hasattr(window, '_on_restart_service'):
        window._on_restart_service()


def _quit_with_tray(window: 'ConfiguratorMainWindow', tray: 'SystemTrayIcon') -> None:
    """Clean up tray icon and close window."""
    tray.hide()
    window.quit_application()  # Use quit_application instead of close

    from PySide6.QtWidgets import QApplication
    QApplication.quit()
