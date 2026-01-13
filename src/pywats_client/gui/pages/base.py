"""
Base Page Widget

Base class for all configuration pages.

Supports both legacy (config-only) and new (facade-based) initialization patterns
to allow gradual migration of existing pages.
"""

from typing import Callable, Dict, Any, List, Optional, TYPE_CHECKING
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Signal

from ...core.config import ClientConfig
from ...core.event_bus import AppEvent, event_bus

if TYPE_CHECKING:
    from ...core.app_facade import AppFacade


class BasePage(QWidget):
    """
    Base class for configuration pages.
    
    Provides common functionality for all pages:
    - Title display
    - Config change signal
    - Save/load config methods
    - Optional AppFacade integration for decoupled event-driven updates
    
    Two initialization patterns are supported:
    
    1. Legacy pattern (for backward compatibility):
        page = MyPage(config, parent)
        
    2. Facade pattern (recommended for new pages):
        page = MyPage(config, parent, facade=app_facade)
        # Or set later:
        page.set_facade(app_facade)
    
    Pages using the facade pattern can:
    - Subscribe to application events via EventBus
    - Access API client safely via facade.api
    - Use domain shortcuts (facade.asset, facade.product, etc.)
    """
    
    # Emitted when configuration is changed
    config_changed = Signal()
    
    def __init__(
        self, 
        config: ClientConfig, 
        parent: Optional[QWidget] = None,
        *,
        facade: Optional["AppFacade"] = None
    ):
        super().__init__(parent)
        self.config = config
        self._facade: Optional["AppFacade"] = facade
        self._event_subscriptions: List[tuple[AppEvent, Callable]] = []
        self._setup_base_ui()
    
    def _setup_base_ui(self) -> None:
        """Setup base UI layout"""
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(15)
        
        # Title
        self._title_label = QLabel(self.page_title)
        self._title_label.setObjectName("titleLabel")
        self._layout.addWidget(self._title_label)
        
        # Separator
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFixedHeight(1)
        self._layout.addWidget(separator)
    
    @property
    def page_title(self) -> str:
        """Override in subclass to set page title"""
        return "Page"
    
    # =========================================================================
    # Facade Integration
    # =========================================================================
    
    @property
    def facade(self) -> Optional["AppFacade"]:
        """
        Get the application facade.
        
        Returns:
            AppFacade if set, None otherwise
        """
        return self._facade
    
    def set_facade(self, facade: "AppFacade") -> None:
        """
        Set the application facade.
        
        This can be called after construction to enable facade features
        on pages that were created with the legacy pattern.
        
        Args:
            facade: The AppFacade instance to use
        """
        self._facade = facade
        self._on_facade_ready()
    
    def _on_facade_ready(self) -> None:
        """
        Called when facade becomes available.
        
        Override in subclasses to perform initialization that requires
        the facade (e.g., subscribing to events, loading initial data).
        """
        pass
    
    # =========================================================================
    # Event Subscription Helpers
    # =========================================================================
    
    def subscribe_event(
        self, 
        event: AppEvent, 
        callback: Callable[[Dict[str, Any]], None]
    ) -> None:
        """
        Subscribe to an application event.
        
        Events are automatically unsubscribed when the page is destroyed.
        
        Args:
            event: The event type to subscribe to
            callback: Function to call when event occurs
        """
        event_bus.subscribe(event, callback)
        self._event_subscriptions.append((event, callback))
    
    def unsubscribe_event(
        self, 
        event: AppEvent, 
        callback: Callable[[Dict[str, Any]], None]
    ) -> None:
        """
        Unsubscribe from an application event.
        
        Args:
            event: The event type to unsubscribe from
            callback: The callback function to remove
        """
        event_bus.unsubscribe(event, callback)
        try:
            self._event_subscriptions.remove((event, callback))
        except ValueError:
            pass  # Not in list
    
    def unsubscribe_all_events(self) -> None:
        """
        Unsubscribe from all events this page subscribed to.
        
        Called automatically during cleanup.
        """
        for event, callback in self._event_subscriptions:
            event_bus.unsubscribe(event, callback)
        self._event_subscriptions.clear()
    
    # =========================================================================
    # Qt Lifecycle
    # =========================================================================
    
    def closeEvent(self, event) -> None:
        """Clean up event subscriptions when page is closed."""
        self.unsubscribe_all_events()
        super().closeEvent(event)
    
    def deleteLater(self) -> None:
        """Clean up event subscriptions before deletion."""
        self.unsubscribe_all_events()
        super().deleteLater()
    
    # =========================================================================
    # Configuration Methods
    # =========================================================================
    
    def save_config(self) -> None:
        """Override in subclass to save configuration"""
        pass
    
    def load_config(self) -> None:
        """Override in subclass to load configuration"""
        pass
    
    def _emit_changed(self) -> None:
        """Emit config changed signal"""
        self.config_changed.emit()
