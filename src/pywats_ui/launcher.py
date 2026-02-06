"""pyWATS Application Launcher - System tray application manager.

This module provides a centralized launcher that sits in the system tray
and provides quick access to all pyWATS GUI applications.
"""

import sys
from typing import Optional, Dict
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
from pywats_ui.framework.system_tray import SystemTrayIcon


class AppLauncher:
    """Centralized launcher for pyWATS applications.
    
    Manages system tray icon and launches applications on demand.
    """
    
    def __init__(self):
        """Initialize the application launcher."""
        self._windows: Dict[str, Optional[QMainWindow]] = {
            "configurator": None,
            "yield_monitor": None,
            "package_manager": None,
            "client_monitor": None,
        }
    
    def launch_configurator(self):
        """Launch the Client Configurator application."""
        if self._windows["configurator"] is None or not self._windows["configurator"].isVisible():
            from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
            from pywats_client.core.config import ClientConfig
            from pathlib import Path
            
            # Load default instance config
            config_dir = Path.home() / ".pywats" / "instances" / "default"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_path = config_dir / "client_config.json"
            
            if config_path.exists():
                config = ClientConfig.load(config_path)
            else:
                config = ClientConfig(instance_id="default")
                config.instance_name = "Instance: default"
                config._config_path = config_path
                config.save()
            
            self._windows["configurator"] = ConfiguratorMainWindow(config)
        
        self._windows["configurator"].show()
        self._windows["configurator"].raise_()
        self._windows["configurator"].activateWindow()
    
    def launch_yield_monitor(self):
        """Launch the Yield Monitor application."""
        if self._windows["yield_monitor"] is None or not self._windows["yield_monitor"].isVisible():
            from pywats_ui.apps.yield_monitor.main_window import YieldMonitorWindow
            self._windows["yield_monitor"] = YieldMonitorWindow()
        
        self._windows["yield_monitor"].show()
        self._windows["yield_monitor"].raise_()
        self._windows["yield_monitor"].activateWindow()
    
    def launch_package_manager(self):
        """Launch the Package Manager application."""
        if self._windows["package_manager"] is None or not self._windows["package_manager"].isVisible():
            from pywats_ui.apps.package_manager.main_window import PackageManagerWindow
            self._windows["package_manager"] = PackageManagerWindow()
        
        self._windows["package_manager"].show()
        self._windows["package_manager"].raise_()
        self._windows["package_manager"].activateWindow()
    
    def launch_client_monitor(self):
        """Launch the Client Monitor application."""
        if self._windows["client_monitor"] is None or not self._windows["client_monitor"].isVisible():
            from pywats_ui.apps.client_monitor.main_window import ClientMonitorWindow
            self._windows["client_monitor"] = ClientMonitorWindow()
        
        self._windows["client_monitor"].show()
        self._windows["client_monitor"].raise_()
        self._windows["client_monitor"].activateWindow()


def main():
    """Main entry point for the pyWATS application launcher."""
    # Create application
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running when windows close
    app.setApplicationName("pyWATS Application Launcher")
    app.setApplicationVersion("0.3.0")
    
    # Set up logging
    from pywats.core.logging import configure_logging
    configure_logging(
        level="INFO",
        file_path="pywats_launcher.log"
    )
    
    # Create launcher instance
    launcher = AppLauncher()
    
    # Create system tray icon
    tray = SystemTrayIcon()
    tray.add_application("🔧 Client Configurator", launcher.launch_configurator)
    tray.add_application("📊 Yield Monitor", launcher.launch_yield_monitor)
    tray.add_application("📦 Package Manager", launcher.launch_package_manager)
    tray.add_application("🖥️ Client Monitor", launcher.launch_client_monitor)
    tray.add_quit_action()
    
    tray.show()
    tray.showMessage(
        "pyWATS Applications",
        "Click the tray icon to launch applications",
        SystemTrayIcon.MessageIcon.Information,
        2000
    )
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
