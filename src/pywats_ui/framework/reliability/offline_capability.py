"""Offline capability mixin for pages.

Fixes CRITICAL issue C3: No offline mode - GUI unusable without connection
- Enables local editing when disconnected
- Saves changes locally, syncs when connection restored
- Provides visual feedback for offline/online states
- Graceful degradation of features requiring server

User requirement: "Fix weaknesses, ensure reliability"
"""

import logging
from pywats.core.logging import get_logger
from typing import Optional
from enum import Enum

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Signal, Slot

logger = get_logger(__name__)


class OnlineMode(Enum):
    """Online mode states"""
    ONLINE = "online"           # Connected to server, full functionality
    OFFLINE = "offline"         # Not connected, local editing only
    SYNCING = "syncing"         # Connected but syncing local changes


class OfflineCapability:
    """Mixin to add offline capability to pages.
    
    Pages using this mixin can:
    - Edit settings when offline (saves locally)
    - Show visual indicator for offline/online/syncing states
    - Sync local changes when connection restored
    - Gracefully disable features requiring server
    
    Usage:
        class MyPage(BasePage, OfflineCapability):
            def __init__(self, config, parent=None):
                BasePage.__init__(self, config, parent)
                OfflineCapability.__init__(self)
                
                # Connect to connection monitor
                connection_monitor.status_changed.connect(self.set_online_mode)
    
    Required methods to implement:
        - save_config_locally() -> None: Save config to local file
        - sync_config_to_server() -> None: Upload local config to server (async recommended)
        - load_local_config() -> None: Load config from local file
    
    Optional methods to override:
        - on_online_mode_changed(mode: OnlineMode) -> None: Custom behavior on mode change
        - get_offline_message() -> str: Custom offline message
    """
    
    # Signals (will be added to page class)
    online_mode_changed = Signal(object)  # OnlineMode
    
    def __init__(self):
        """Initialize offline capability.
        
        Note: Should be called AFTER parent widget __init__
        """
        self._online_mode = OnlineMode.OFFLINE
        self._offline_banner: Optional[QWidget] = None
        self._has_unsaved_changes = False
        
        logger.debug(f"OfflineCapability initialized for {self.__class__.__name__}")
    
    @property
    def online_mode(self) -> OnlineMode:
        """Get current online mode."""
        return self._online_mode
    
    @property
    def is_online(self) -> bool:
        """Check if currently online."""
        return self._online_mode == OnlineMode.ONLINE
    
    @property
    def has_unsaved_changes(self) -> bool:
        """Check if there are unsaved local changes."""
        return self._has_unsaved_changes
    
    @Slot(object)
    def set_online_mode(self, connection_status) -> None:
        """Update online mode based on connection status.
        
        Args:
            connection_status: ConnectionStatus enum from ConnectionMonitor
        """
        from .connection_monitor import ConnectionStatus
        
        if connection_status == ConnectionStatus.CONNECTED:
            # Just connected - sync if have unsaved changes
            if self._has_unsaved_changes:
                self._set_mode(OnlineMode.SYNCING)
                self._sync_local_changes()
            else:
                self._set_mode(OnlineMode.ONLINE)
        else:
            self._set_mode(OnlineMode.OFFLINE)
    
    def _set_mode(self, mode: OnlineMode) -> None:
        """Update mode and emit signal."""
        if mode != self._online_mode:
            old_mode = self._online_mode
            self._online_mode = mode
            
            logger.info(f"{self.__class__.__name__} mode: {old_mode.value} → {mode.value}")
            self.online_mode_changed.emit(mode)
            
            # Update UI
            self._update_offline_banner()
            
            # Call custom handler if implemented
            if hasattr(self, 'on_online_mode_changed'):
                self.on_online_mode_changed(mode)
    
    def _update_offline_banner(self) -> None:
        """Show/hide offline mode banner."""
        if not isinstance(self, QWidget):
            return
        
        # Create banner if needed
        if self._offline_banner is None:
            self._offline_banner = QLabel(self)
            self._offline_banner.setObjectName("offlineBanner")
            self._offline_banner.setStyleSheet("""
                QLabel#offlineBanner {
                    background-color: #856404;
                    color: #fff;
                    padding: 8px;
                    font-weight: bold;
                    border-radius: 4px;
                }
            """)
            self._offline_banner.hide()
            
            # Insert at top of layout
            if hasattr(self, 'layout') and self.layout():
                self.layout().insertWidget(0, self._offline_banner)
        
        # Update banner based on mode
        if self._online_mode == OnlineMode.OFFLINE:
            message = self.get_offline_message() if hasattr(self, 'get_offline_message') else \
                      "⚠️ Offline Mode - Changes saved locally, will sync when connected"
            self._offline_banner.setText(message)
            self._offline_banner.show()
            
        elif self._online_mode == OnlineMode.SYNCING:
            self._offline_banner.setText("🔄 Syncing local changes to server...")
            self._offline_banner.setStyleSheet("""
                QLabel#offlineBanner {
                    background-color: #0c5460;
                    color: #fff;
                    padding: 8px;
                    font-weight: bold;
                    border-radius: 4px;
                }
            """)
            self._offline_banner.show()
            
        else:  # ONLINE
            self._offline_banner.hide()
    
    def save_config_offline(self) -> None:
        """Save config locally (works offline).
        
        Delegates to save_config_locally() which must be implemented by page.
        """
        if not hasattr(self, 'save_config_locally'):
            logger.error(f"{self.__class__.__name__} must implement save_config_locally()")
            return
        
        try:
            self.save_config_locally()
            self._has_unsaved_changes = True
            logger.info(f"Config saved locally (offline mode)")
            
            # If online, sync immediately
            if self._online_mode == OnlineMode.ONLINE:
                self._sync_local_changes()
                
        except Exception as e:
            logger.exception(f"Failed to save config locally: {e}")
            # Show error dialog if page has error handling
            if hasattr(self, 'handle_error'):
                self.handle_error(e, "Failed to save configuration locally")
    
    def _sync_local_changes(self) -> None:
        """Sync local changes to server."""
        if not hasattr(self, 'sync_config_to_server'):
            logger.warning(f"{self.__class__.__name__} doesn't implement sync_config_to_server()")
            self._has_unsaved_changes = False
            self._set_mode(OnlineMode.ONLINE)
            return
        
        try:
            logger.info("Syncing local changes to server...")
            result = self.sync_config_to_server()
            
            # Handle async sync
            import asyncio
            if asyncio.iscoroutine(result):
                asyncio.create_task(self._async_sync(result))
            else:
                self._sync_complete(success=True)
                
        except Exception as e:
            logger.exception(f"Failed to sync config to server: {e}")
            self._sync_complete(success=False, error=str(e))
    
    async def _async_sync(self, coro) -> None:
        """Handle async sync operation."""
        try:
            await coro
            self._sync_complete(success=True)
        except Exception as e:
            logger.exception(f"Async sync failed: {e}")
            self._sync_complete(success=False, error=str(e))
    
    def _sync_complete(self, success: bool, error: Optional[str] = None) -> None:
        """Handle sync completion."""
        if success:
            self._has_unsaved_changes = False
            self._set_mode(OnlineMode.ONLINE)
            logger.info("Local changes synced successfully")
        else:
            logger.error(f"Sync failed: {error}")
            # Stay in offline mode, keep unsaved flag
            self._set_mode(OnlineMode.OFFLINE)
            
            if hasattr(self, 'handle_error'):
                self.handle_error(Exception(error), "Failed to sync changes to server")
    
    def enable_server_features(self, enabled: bool) -> None:
        """Enable/disable features requiring server connection.
        
        Override this method to customize which widgets are disabled offline.
        Default implementation does nothing (all features work offline).
        
        Args:
            enabled: True if server is available, False if offline
        """
        pass
