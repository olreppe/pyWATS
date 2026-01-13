# GUI-Application Coupling Analysis

## Executive Summary

The current pyWATS Client has **significant coupling issues** between the GUI layer and the application/API layer. GUI pages directly access internal application state through a chain like `self._main_window.app.wats_client`, violating architectural principles outlined in ARCHITECTURE_REVIEW.md.

**Key finding**: The architecture review document already identified this issue in section 1.3:
> "GUI must interact only with **facade-level services** - No direct access to internal state of queues, converters, or connection internals - Prefer **events/signals** over state polling"

---

## Current Architecture Problems

### 1. Deep Coupling Chain

GUI pages currently access the API through a deep coupling chain:

```
Page → MainWindow → pyWATSApplication → pyWATS (API client)
```

Example from `asset.py:349`:
```python
client = self._main_window.app.wats_client
assets = client.asset.get_assets()
```

**Problems:**
- Pages depend on MainWindow's internal structure
- Pages know about pyWATSApplication internals
- No abstraction between GUI and API
- Hard to test pages in isolation
- If app structure changes, all pages break

### 2. Repeated Connection Checks

Every page that needs API access has duplicate boilerplate:

```python
if self._main_window and self._main_window.app.wats_client:
    client = self._main_window.app.wats_client
    # ... do something
else:
    QMessageBox.warning(self, "Not Connected", "...")
```

This pattern appears **20+ times** across pages.

### 3. No Event System for State Changes

Pages need to react to:
- Connection state changes (Online → Offline)
- API client initialization
- Service start/stop
- Configuration updates

Currently, MainWindow manually updates pages:
```python
# main_window.py line 627
if "Connection" in self._pages:
    connection_page = self._pages["Connection"]
    if isinstance(connection_page, ConnectionPage):
        connection_page.update_status(status)
```

**Problems:**
- MainWindow knows about page internals
- New pages require MainWindow modifications
- No way for pages to subscribe to events they care about

### 4. Mixed Concerns in Pages

Pages mix:
- UI logic (Qt widgets)
- Data fetching (API calls)
- Data transformation (model to dict)
- Error handling (QMessageBox)

Example from `asset.py`:
```python
def _load_assets(self) -> None:
    try:
        self._status_label.setText("Loading assets...")  # UI
        if self._main_window and self._main_window.app.wats_client:  # Coupling
            client = self._main_window.app.wats_client  # Direct access
            self._asset_types = client.asset.get_asset_types() or []  # API call
            assets = client.asset.get_assets()  # API call
            self._assets = [self._asset_to_dict(a) for a in assets]  # Transform
            self._populate_table()  # UI
    except Exception as e:  # Error handling
        QMessageBox.warning(self, "Error", f"...")
```

---

## Recommended Solution: Event Bus + Facade Pattern

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         GUI Layer                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │
│  │AssetPage│  │SoftPage │  │ProdPage │  │ Other Pages...  │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────────┬────────┘ │
│       │            │            │                 │          │
│       └────────────┴────────────┴─────────────────┘          │
│                           │                                  │
│                    ┌──────▼──────┐                          │
│                    │  EventBus   │  ← Qt Signals-based      │
│                    └──────┬──────┘                          │
└───────────────────────────┼──────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────┐
│                    ┌──────▼──────┐                           │
│                    │ AppFacade   │  ← Single access point    │
│                    └──────┬──────┘                           │
│                           │                                  │
│  ┌────────────────────────┼────────────────────────────┐    │
│  │                 pyWATSApplication                    │    │
│  │  ┌───────────┐  ┌──────────┐  ┌────────────────┐   │    │
│  │  │Connection │  │ProcessSync│  │ConverterMgr   │   │    │
│  │  │ Service   │  │ Service   │  │               │   │    │
│  │  └───────────┘  └──────────┘  └────────────────┘   │    │
│  └─────────────────────────┼────────────────────────────┘   │
│                            │                                 │
│                     ┌──────▼──────┐                         │
│                     │   pyWATS    │  ← API Library          │
│                     │   (API)     │                         │
│                     └─────────────┘                         │
│                      Service Layer                           │
└──────────────────────────────────────────────────────────────┘
```

### Implementation Plan

#### 1. Create EventBus (Qt Signal-based)

```python
# src/pywats_client/core/event_bus.py
"""
Application Event Bus

Provides decoupled communication between GUI and application layers
using Qt Signals for thread-safe event delivery.
"""
from enum import Enum, auto
from typing import Optional, Any, Dict
from PySide6.QtCore import QObject, Signal


class AppEvent(Enum):
    """Application event types"""
    # Connection events
    CONNECTION_CHANGED = auto()      # status: ConnectionStatus
    CONNECTION_ERROR = auto()        # error: str
    
    # Application lifecycle
    APP_STARTING = auto()
    APP_STARTED = auto()
    APP_STOPPING = auto()
    APP_STOPPED = auto()
    APP_ERROR = auto()               # error: str
    
    # API client events
    API_CLIENT_READY = auto()        # client: pyWATS
    API_CLIENT_DISCONNECTED = auto()
    
    # Data events (for cache invalidation)
    ASSETS_CHANGED = auto()
    PRODUCTS_CHANGED = auto()
    SOFTWARE_CHANGED = auto()
    PROCESSES_REFRESHED = auto()
    
    # Queue events
    QUEUE_ITEM_ADDED = auto()
    QUEUE_ITEM_PROCESSED = auto()
    QUEUE_EMPTY = auto()


class EventBus(QObject):
    """
    Central event bus for application-wide communication.
    
    Uses Qt Signals for thread-safe delivery to GUI components.
    
    Usage:
        # Subscribe to events
        event_bus.subscribe(AppEvent.CONNECTION_CHANGED, self._on_connection)
        
        # Publish events
        event_bus.publish(AppEvent.CONNECTION_CHANGED, status="Online")
    """
    
    # Generic signal for all events
    event_occurred = Signal(AppEvent, dict)
    
    # Typed signals for common events (for direct connection)
    connection_changed = Signal(str)      # status string
    api_client_ready = Signal(object)     # pyWATS instance
    app_status_changed = Signal(str)      # status string
    
    _instance: Optional['EventBus'] = None
    
    def __new__(cls) -> 'EventBus':
        """Singleton pattern for global event bus"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        super().__init__()
        self._initialized = True
        self._subscribers: Dict[AppEvent, list] = {}
    
    def publish(self, event: AppEvent, **data) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event: Event type to publish
            **data: Event data as keyword arguments
        """
        # Emit generic signal
        self.event_occurred.emit(event, data)
        
        # Emit typed signals for convenience
        if event == AppEvent.CONNECTION_CHANGED:
            self.connection_changed.emit(data.get('status', ''))
        elif event == AppEvent.API_CLIENT_READY:
            self.api_client_ready.emit(data.get('client'))
        elif event in (AppEvent.APP_STARTING, AppEvent.APP_STARTED, 
                       AppEvent.APP_STOPPING, AppEvent.APP_STOPPED):
            self.app_status_changed.emit(event.name)
    
    def subscribe(self, event: AppEvent, callback) -> None:
        """
        Subscribe to a specific event type.
        
        Args:
            event: Event type to subscribe to
            callback: Function to call when event occurs
        """
        if event not in self._subscribers:
            self._subscribers[event] = []
        self._subscribers[event].append(callback)
        
        # Connect to generic signal and filter
        def filtered_handler(evt, data):
            if evt == event:
                callback(data)
        
        self.event_occurred.connect(filtered_handler)
    
    def unsubscribe(self, event: AppEvent, callback) -> None:
        """Remove a subscription"""
        if event in self._subscribers:
            self._subscribers[event] = [
                cb for cb in self._subscribers[event] if cb != callback
            ]


# Global instance
event_bus = EventBus()
```

#### 2. Create Application Facade

```python
# src/pywats_client/core/app_facade.py
"""
Application Facade

Provides a clean interface between GUI and application internals.
All GUI components should access application functionality through this facade.
"""
from typing import Optional, List, Any, TYPE_CHECKING
from .event_bus import event_bus, AppEvent

if TYPE_CHECKING:
    from pywats import pyWATS
    from ..app import pyWATSApplication


class AppFacade:
    """
    Facade for GUI access to application functionality.
    
    Provides:
    - Safe API client access with connection checks
    - Event subscription shortcuts
    - Common operations with error handling
    
    Usage in pages:
        class AssetPage(BasePage):
            def __init__(self, facade: AppFacade, ...):
                self._facade = facade
                self._facade.on_api_ready(self._load_data)
                
            def _load_data(self, client):
                assets = self._facade.asset.get_assets()
    """
    
    def __init__(self, app: 'pyWATSApplication'):
        self._app = app
        self._setup_event_forwarding()
    
    def _setup_event_forwarding(self) -> None:
        """Forward app events to event bus"""
        self._app.on_status_changed(self._on_app_status)
        # Add connection status forwarding when connection service exists
    
    def _on_app_status(self, status) -> None:
        """Forward app status to event bus"""
        event_bus.publish(AppEvent.APP_STATUS_CHANGED, status=status.value)
        
        if status.value == "Running" and self._app.wats_client:
            event_bus.publish(AppEvent.API_CLIENT_READY, client=self._app.wats_client)
    
    # =========================================================================
    # Connection State
    # =========================================================================
    
    @property
    def is_connected(self) -> bool:
        """Check if API client is available and connected"""
        return self._app.wats_client is not None and self._app.is_online()
    
    @property
    def is_online(self) -> bool:
        """Check if server is reachable"""
        return self._app.is_online()
    
    @property
    def client(self) -> Optional['pyWATS']:
        """
        Get API client if available.
        
        Returns None if not connected - caller should handle gracefully.
        """
        return self._app.wats_client
    
    def require_client(self) -> 'pyWATS':
        """
        Get API client, raising if not available.
        
        Use this when connection is required - will raise clear error.
        """
        if not self._app.wats_client:
            raise ConnectionError("Not connected to WATS server")
        return self._app.wats_client
    
    # =========================================================================
    # Event Shortcuts
    # =========================================================================
    
    def on_api_ready(self, callback) -> None:
        """Subscribe to API client ready event"""
        event_bus.api_client_ready.connect(callback)
    
    def on_connection_changed(self, callback) -> None:
        """Subscribe to connection status changes"""
        event_bus.connection_changed.connect(callback)
    
    def on_app_status(self, callback) -> None:
        """Subscribe to application status changes"""
        event_bus.app_status_changed.connect(callback)
    
    # =========================================================================
    # Domain Shortcuts (with connection check)
    # =========================================================================
    
    @property
    def asset(self):
        """Get asset service (raises if not connected)"""
        return self.require_client().asset
    
    @property
    def product(self):
        """Get product service (raises if not connected)"""
        return self.require_client().product
    
    @property
    def software(self):
        """Get software service (raises if not connected)"""
        return self.require_client().software
    
    @property
    def report(self):
        """Get report service (raises if not connected)"""
        return self.require_client().report
    
    @property
    def analytics(self):
        """Get analytics service (raises if not connected)"""
        return self.require_client().analytics
    
    @property
    def production(self):
        """Get production service (raises if not connected)"""
        return self.require_client().production
    
    @property
    def rootcause(self):
        """Get rootcause service (raises if not connected)"""
        return self.require_client().rootcause
    
    @property
    def process(self):
        """Get process service (raises if not connected)"""
        return self.require_client().process
    
    # =========================================================================
    # Queue Operations
    # =========================================================================
    
    def get_queue_status(self) -> dict:
        """Get offline queue status"""
        return self._app.get_queue_status()
    
    def get_connection_status(self) -> Optional[str]:
        """Get human-readable connection status"""
        return self._app.get_connection_status()
```

#### 3. Update Base Page

```python
# src/pywats_client/gui/pages/base.py (updated)
"""
Base page with facade integration
"""
from typing import Optional, TYPE_CHECKING
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Signal

if TYPE_CHECKING:
    from ...core.app_facade import AppFacade
    from ...core.config import ClientConfig


class BasePage(QWidget):
    """
    Base class for all GUI pages.
    
    Provides:
    - Standard layout with title
    - Facade access for API operations
    - Event subscription helpers
    - Standard error handling
    """
    
    config_changed = Signal()
    
    def __init__(
        self, 
        config: 'ClientConfig',
        facade: Optional['AppFacade'] = None,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self.config = config
        self._facade = facade
        self._setup_base_ui()
        
        # Auto-subscribe to API ready if facade provided
        if self._facade:
            self._facade.on_api_ready(self._on_api_ready)
            self._facade.on_connection_changed(self._on_connection_changed)
    
    def _setup_base_ui(self) -> None:
        """Setup base UI elements"""
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_label = QLabel(self.page_title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self._layout.addWidget(title_label)
    
    @property
    def page_title(self) -> str:
        """Override in subclasses"""
        return "Page"
    
    @property
    def facade(self) -> Optional['AppFacade']:
        """Get application facade"""
        return self._facade
    
    # =========================================================================
    # Event Handlers (override in subclasses)
    # =========================================================================
    
    def _on_api_ready(self, client) -> None:
        """
        Called when API client becomes available.
        Override to load initial data.
        """
        pass
    
    def _on_connection_changed(self, status: str) -> None:
        """
        Called when connection status changes.
        Override to update UI state.
        """
        pass
    
    # =========================================================================
    # Helper Methods
    # =========================================================================
    
    def api_operation(self, operation_name: str):
        """
        Decorator/context for API operations with standard error handling.
        
        Usage:
            with self.api_operation("load assets"):
                assets = self.facade.asset.get_assets()
        """
        return ApiOperationContext(self, operation_name)
    
    def require_connection(self) -> bool:
        """
        Check connection and show message if not connected.
        
        Returns True if connected, False otherwise.
        """
        if not self._facade or not self._facade.is_connected:
            QMessageBox.warning(
                self, 
                "Not Connected", 
                "Please connect to WATS server first."
            )
            return False
        return True
    
    def _emit_changed(self) -> None:
        """Emit config changed signal"""
        self.config_changed.emit()
    
    def save_config(self) -> None:
        """Override to save page config"""
        pass
    
    def load_config(self) -> None:
        """Override to load page config"""
        pass


class ApiOperationContext:
    """Context manager for API operations with error handling"""
    
    def __init__(self, page: BasePage, operation: str):
        self.page = page
        self.operation = operation
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if exc_type == ConnectionError:
                QMessageBox.warning(
                    self.page,
                    "Not Connected",
                    "Please connect to WATS server first."
                )
            else:
                QMessageBox.warning(
                    self.page,
                    f"Error: {self.operation}",
                    f"Operation failed: {exc_val}"
                )
            return True  # Suppress exception
        return False
```

#### 4. Example Refactored Page

```python
# Example: asset.py refactored
class AssetPage(BasePage):
    """Asset Management page - refactored with facade"""
    
    def __init__(
        self, 
        config: ClientConfig, 
        facade: AppFacade,
        parent: Optional[QWidget] = None
    ):
        super().__init__(config, facade, parent)
        self._assets: List[Asset] = []
        self._setup_ui()
    
    def _on_api_ready(self, client) -> None:
        """Auto-load assets when API becomes available"""
        self._load_assets()
    
    def _on_connection_changed(self, status: str) -> None:
        """Update UI based on connection status"""
        connected = status == "Online"
        self._refresh_btn.setEnabled(connected)
        self._add_btn.setEnabled(connected)
        
        if not connected:
            self._status_label.setText("Offline - cached data shown")
    
    def _load_assets(self) -> None:
        """Load assets from server"""
        if not self.require_connection():
            return
        
        with self.api_operation("load assets"):
            self._status_label.setText("Loading assets...")
            self._assets = self.facade.asset.get_assets() or []
            self._populate_table()
            self._status_label.setText(f"Loaded {len(self._assets)} assets")
    
    def _on_refresh(self) -> None:
        """Refresh button clicked"""
        self._load_assets()
```

---

## Migration Plan

### Phase 1: Foundation (Non-breaking)
1. Create `EventBus` class
2. Create `AppFacade` class  
3. Update `pyWATSApplication` to emit events
4. Keep existing page code working

### Phase 2: Update Base Page
1. Add facade support to `BasePage`
2. Add event subscription helpers
3. Add `ApiOperationContext` for error handling
4. Maintain backward compatibility

### Phase 3: Migrate Pages (One at a time)
1. Start with simplest page (e.g., AboutPage)
2. Move to data-fetching pages (AssetPage, SoftwarePage)
3. Update complex pages (ConvertersPage, SetupPage)
4. Remove `_main_window` references

### Phase 4: Cleanup
1. Remove direct `app.wats_client` access from MainWindow
2. Remove page update methods from MainWindow
3. Update MainWindow to create and inject Facade
4. Remove backward compatibility code

---

## Benefits

| Current | With Event Bus + Facade |
|---------|------------------------|
| Pages know about MainWindow internals | Pages only know about Facade interface |
| MainWindow knows about page update methods | MainWindow just creates pages with Facade |
| Connection checks duplicated 20+ times | Single `require_connection()` helper |
| Hard to test pages | Pages can be tested with mock Facade |
| State polling in timer | Event-driven updates |
| Manual error handling each call | Centralized error handling |

---

## Files to Create/Modify

### New Files
- `src/pywats_client/core/event_bus.py`
- `src/pywats_client/core/app_facade.py`

### Modify
- `src/pywats_client/app.py` - Add event publishing
- `src/pywats_client/gui/pages/base.py` - Add facade support
- `src/pywats_client/gui/main_window.py` - Create and inject facade
- All page files in `src/pywats_client/gui/pages/` - Use facade instead of `_main_window.app`

---

## Estimated Effort

| Phase | Effort | Risk |
|-------|--------|------|
| Phase 1: Foundation | 2-3 hours | Low (additive) |
| Phase 2: Base Page | 1-2 hours | Low (backward compatible) |
| Phase 3: Migrate Pages | 4-6 hours | Medium (per-page testing) |
| Phase 4: Cleanup | 1-2 hours | Low (remove old code) |
| **Total** | **8-13 hours** | **Medium** |

---

## Conclusion

The current GUI-Application coupling violates the architectural principles already identified in ARCHITECTURE_REVIEW.md. The recommended solution uses:

1. **Event Bus** - Qt Signal-based for thread-safe, decoupled communication
2. **App Facade** - Clean interface hiding application internals
3. **Enhanced Base Page** - Standard helpers and event subscriptions

This approach:
- Follows established patterns in the codebase (Qt Signals)
- Is backward compatible during migration
- Significantly improves testability and maintainability
- Addresses all coupling issues identified in the review
