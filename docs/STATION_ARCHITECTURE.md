# Station Architecture Analysis & Design

## Overview

This document analyzes the current implementation of station-related concepts in pyWATS and proposes improvements to support:
1. Clear distinction between **Client Name** and **Station Name**
2. A core **Station** concept in the API layer
3. **Multi-station support** from a single client (hub mode)
4. Configurable defaults at multiple levels

---

## Current Architecture Analysis

### Key Concepts

| Concept | Description | Current Location |
|---------|-------------|------------------|
| **Client Name** | The pyWATS client installation identity | `ClientConfig.instance_name` |
| **Station Name** | The test station identity in reports (`machineName`) | `ClientConfig.station_name` |
| **Location** | Physical/logical location of station | `ClientConfig.location` |
| **Purpose** | Testing purpose (Production, Debug, etc.) | `ClientConfig.purpose` |

### Current Implementation

#### 1. Client Layer (`pywats_client/core/config.py`)

```python
@dataclass
class ClientConfig:
    instance_id: str               # Unique client instance ID
    instance_name: str             # Client display name
    station_name: str              # Station name for reports
    location: str                  # Location string
    purpose: str                   # Purpose string
    include_station_in_reports: bool = True
```

**Problem**: Station properties are flat fields mixed with client configuration.

#### 2. API Layer (`pywats/domains/report/service.py`)

```python
def create_uut_report(
    self,
    operator: str,
    part_number: str,
    ...
    station_name: Optional[str] = None,  # ← Optional, often "Unknown"
    location: Optional[str] = None,
    purpose: Optional[str] = None
) -> UUTReport:
```

**Problem**: No station concept - values passed as individual optional parameters.

#### 3. Report Model (`pywats/domains/report/report_models/report.py`)

```python
class Report(WATSBase):
    station_name: str = Field(..., validation_alias="machineName", serialization_alias="machineName")
    location: str = Field(...)
    purpose: str = Field(...)
```

**Problem**: Required fields with no defaults - users must always specify.

#### 4. GUI Setup Page (`pywats_client/gui/pages/setup.py`)

- Computer name: Read from `socket.gethostname()` (read-only)
- Location: User editable
- Purpose: User editable

**Problem**: No distinction between client name and station name in UI.

---

## Proposed Architecture

### 1. Core Station Concept

Create a `Station` dataclass in the core API that represents the test station identity:

```
src/pywats/
└── core/
    └── station.py       # NEW: Station concept
```

#### Station Model

```python
@dataclass
class Station:
    """
    Represents a test station identity.
    
    A Station encapsulates the identity information that appears in test reports:
    - name: The station/machine name (appears as machineName in reports)
    - location: Physical or logical location
    - purpose: Testing purpose (Production, Debug, Development, etc.)
    
    Usage:
        # Create a station with defaults
        station = Station.from_hostname()
        
        # Create a custom station
        station = Station(
            name="TEST-STATION-01",
            location="Building A, Floor 2",
            purpose="Production"
        )
        
        # Apply to reports
        report.apply_station(station)
    """
    name: str
    location: str = ""
    purpose: str = "Development"
    description: str = ""  # Optional station description
    
    @classmethod
    def from_hostname(cls, location: str = "", purpose: str = "Development") -> "Station":
        """Create station using computer hostname as name."""
        import socket
        return cls(
            name=socket.gethostname().upper(),
            location=location,
            purpose=purpose
        )
    
    @classmethod  
    def from_config(cls, config: Dict[str, Any]) -> "Station":
        """Create station from configuration dictionary."""
        return cls(
            name=config.get("name", ""),
            location=config.get("location", ""),
            purpose=config.get("purpose", "Development"),
            description=config.get("description", "")
        )
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "location": self.location,
            "purpose": self.purpose,
            "description": self.description
        }
```

### 2. Station Registry for Multi-Station Support

```python
class StationRegistry:
    """
    Manages multiple station configurations.
    
    Enables a single client to act as a hub for multiple stations:
    - Database converters that import data from multiple test systems
    - Centralized upload clients that receive reports from various stations
    - Test cells with multiple fixtures/positions
    
    Usage:
        registry = StationRegistry()
        
        # Add stations
        registry.add("STATION-A", Station("STATION-A", "Lab 1", "Production"))
        registry.add("STATION-B", Station("STATION-B", "Lab 2", "Debug"))
        
        # Set active station
        registry.set_active("STATION-A")
        
        # Get active station
        station = registry.active
    """
    
    def __init__(self):
        self._stations: Dict[str, Station] = {}
        self._active_key: Optional[str] = None
        self._default: Optional[Station] = None
    
    def add(self, key: str, station: Station) -> None:
        """Add a station to the registry."""
        self._stations[key] = station
        if self._active_key is None:
            self._active_key = key
    
    def remove(self, key: str) -> None:
        """Remove a station from the registry."""
        if key in self._stations:
            del self._stations[key]
            if self._active_key == key:
                self._active_key = next(iter(self._stations), None)
    
    def get(self, key: str) -> Optional[Station]:
        """Get a station by key."""
        return self._stations.get(key)
    
    def set_active(self, key: str) -> None:
        """Set the active station."""
        if key not in self._stations:
            raise ValueError(f"Station '{key}' not found in registry")
        self._active_key = key
    
    def set_default(self, station: Station) -> None:
        """Set the default station (used when no active station)."""
        self._default = station
    
    @property
    def active(self) -> Optional[Station]:
        """Get the currently active station."""
        if self._active_key:
            return self._stations.get(self._active_key)
        return self._default
    
    @property
    def all_stations(self) -> Dict[str, Station]:
        """Get all registered stations."""
        return self._stations.copy()
    
    def __len__(self) -> int:
        return len(self._stations)
    
    def __iter__(self):
        return iter(self._stations.values())
```

### 3. Integration with pyWATS API

Extend the main `pyWATS` class to support station configuration:

```python
class pyWATS:
    def __init__(
        self,
        base_url: str,
        token: str,
        station: Optional[Station] = None,  # NEW: Default station
        timeout: int = 30,
        ...
    ):
        self._station = station
        self._station_registry = StationRegistry()
        if station:
            self._station_registry.set_default(station)
    
    @property
    def station(self) -> Optional[Station]:
        """Get the currently active station."""
        return self._station_registry.active or self._station
    
    @station.setter
    def station(self, station: Station) -> None:
        """Set the default station."""
        self._station = station
        self._station_registry.set_default(station)
    
    @property
    def stations(self) -> StationRegistry:
        """Access the station registry for multi-station support."""
        return self._station_registry
```

### 4. Enhanced Report Creation

Update `ReportService` to use station configuration:

```python
class ReportService:
    def create_uut_report(
        self,
        operator: str,
        part_number: str,
        revision: str,
        serial_number: str,
        operation_type: int,
        station: Optional[Station] = None,    # NEW: Station object
        station_name: Optional[str] = None,   # Legacy support
        location: Optional[str] = None,       # Legacy support
        purpose: Optional[str] = None         # Legacy support
    ) -> UUTReport:
        """
        Create a new UUT report.
        
        Station information priority:
        1. Explicit station parameter
        2. Legacy station_name/location/purpose parameters
        3. API's default station (from pyWATS instance)
        4. Fallback to "Unknown" values
        """
        # Resolve station
        effective_station = self._resolve_station(
            station, station_name, location, purpose
        )
        
        report = UUTReport(
            ...
            station_name=effective_station.name,
            location=effective_station.location,
            purpose=effective_station.purpose,
        )
        return report
    
    def _resolve_station(
        self,
        station: Optional[Station],
        station_name: Optional[str],
        location: Optional[str],
        purpose: Optional[str]
    ) -> Station:
        """Resolve station from various sources."""
        if station:
            return station
        
        if station_name:
            return Station(
                name=station_name,
                location=location or "",
                purpose=purpose or "Development"
            )
        
        # Get from API default
        api_station = self._get_api_station()
        if api_station:
            return api_station
        
        # Fallback
        return Station(name="Unknown", location="Unknown", purpose="Development")
```

### 5. Client Configuration Updates

Update `ClientConfig` to support multi-station:

```python
@dataclass
class ClientConfig:
    # Client identification (the client installation itself)
    instance_id: str
    instance_name: str  # "pyWATS Client - Production Hub"
    
    # Default station (single-station mode)
    station_name: str = ""       # Default station name
    location: str = ""           # Default location
    purpose: str = ""            # Default purpose
    
    # Multi-station support
    stations: List[StationConfig] = field(default_factory=list)
    active_station_key: str = ""  # Key of active station
    
    # Station behavior
    use_hostname_as_station: bool = True     # Use computer hostname as station name
    station_name_source: str = "hostname"    # "hostname", "config", "manual"
    allow_station_override: bool = True      # Allow per-report station override
    
    # ... existing fields ...

@dataclass
class StationConfig:
    """Configuration for a saved station preset."""
    key: str                    # Unique identifier
    name: str                   # Station name
    location: str = ""
    purpose: str = ""
    description: str = ""
    is_default: bool = False
```

### 6. GUI Updates

#### Setup Page Enhancements

```
┌─────────────────────────────────────────────────────────────┐
│ Setup                                                       │
├─────────────────────────────────────────────────────────────┤
│ Client Name         [pyWATS Production Hub        ]         │
│ Client ID           abc12345-...                            │
│                                                             │
│ ─── Station Configuration ───────────────────────────────── │
│                                                             │
│ Station Name        [TEST-STATION-01              ] [▼]     │
│   □ Use computer hostname as station name                   │
│                                                             │
│ Location            [Building A, Floor 2          ]         │
│ Purpose             [Production                   ] [▼]     │
│                                                             │
│ ─── Multi-Station Mode ──────────────────────────────────── │
│                                                             │
│ □ Enable multi-station mode (hub)                           │
│                                                             │
│ Stations:           [Manage Stations...]                    │
│   • STATION-A (Building A) ← Active                         │
│   • STATION-B (Building B)                                  │
│   • STATION-C (Building C)                                  │
│                                                             │
│ ─── Connection ──────────────────────────────────────────── │
│ Account / Server    https://company.wats.com/               │
│ Token               ••••••••••••••••                        │
│                                                             │
│ [Connect]  [Disconnect]  [New customer]                     │
└─────────────────────────────────────────────────────────────┘
```

#### New Station Manager Dialog

```
┌─────────────────────────────────────────────────────────────┐
│ Station Manager                                      [X]    │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌────────────────────────────────────┐ │
│ │ Stations        │  │ Station Details                    │ │
│ │                 │  │                                    │ │
│ │ ► STATION-A     │  │ Key:      STATION-A                │ │
│ │   STATION-B     │  │ Name:     [TEST-STATION-A      ]   │ │
│ │   STATION-C     │  │ Location: [Building A, Floor 2]   │ │
│ │                 │  │ Purpose:  [Production      ] [▼]   │ │
│ │ [+] [-] [↑] [↓] │  │ Description:                      │ │
│ │                 │  │ [Main production line test...  ]   │ │
│ │                 │  │                                    │ │
│ │                 │  │ □ Set as default station           │ │
│ └─────────────────┘  └────────────────────────────────────┘ │
│                                                             │
│                              [Cancel]  [Apply]  [OK]        │
└─────────────────────────────────────────────────────────────┘
```

---

## Use Cases

### Use Case 1: Simple Single Station

The most common case - one client represents one test station.

```python
# API usage
api = pyWATS(
    base_url="https://company.wats.com",
    token="...",
    station=Station.from_hostname(location="Lab 1", purpose="Production")
)

# Reports automatically use station info
report = api.report.create_uut_report(
    operator="John",
    part_number="PN-001",
    revision="A",
    serial_number="SN-001",
    operation_type=100
)
# report.station_name = "HOSTNAME"
# report.location = "Lab 1"
# report.purpose = "Production"
```

### Use Case 2: Hub Client with Multiple Stations

Client acts as a hub, processing reports from multiple stations.

```python
# Configure multiple stations
api = pyWATS(base_url="...", token="...")

api.stations.add("line-1", Station("PROD-LINE-1", "Building A", "Production"))
api.stations.add("line-2", Station("PROD-LINE-2", "Building A", "Production"))
api.stations.add("debug", Station("DEBUG-STATION", "Engineering", "Debug"))

# Switch active station
api.stations.set_active("line-1")

# Create report using active station
report1 = api.report.create_uut_report(...)  # Uses PROD-LINE-1

# Or specify station explicitly
report2 = api.report.create_uut_report(
    ...,
    station=api.stations.get("debug")
)
```

### Use Case 3: Database Converter

Converting historical data from a database with multiple source stations.

```python
api = pyWATS(base_url="...", token="...")

# Process records from different stations
for record in database_records:
    station = Station(
        name=record["machine_name"],
        location=record["location"],
        purpose="Production"
    )
    
    report = api.report.create_uut_report(
        ...,
        station=station
    )
    api.report.submit(report)
```

### Use Case 4: Override Station in Report

User wants to adjust station info before sending.

```python
# Create report with default station
report = api.report.create_uut_report(...)

# Override before submission
report.station_name = "OVERRIDE-STATION"
report.location = "New Location"

api.report.submit(report)
```

---

## Implementation Plan

### Phase 1: Core Station Concept
1. Create `Station` dataclass in `pywats/core/station.py`
2. Create `StationRegistry` class for multi-station support
3. Add `station` parameter to `pyWATS.__init__`
4. Add `stations` property to `pyWATS`

### Phase 2: Report Service Integration
1. Update `ReportService.create_uut_report` to accept `Station`
2. Update `ReportService.create_uur_report` to accept `Station`
3. Add `_resolve_station` helper method
4. Maintain backward compatibility with legacy parameters

### Phase 3: Client Configuration
1. Add `StationConfig` dataclass to `ClientConfig`
2. Add multi-station fields to `ClientConfig`
3. Update serialization/deserialization

### Phase 4: GUI Updates
1. Update Setup page with station section
2. Create Station Manager dialog
3. Add station switcher to main window
4. Update test UUT functionality to use current station

### Phase 5: Documentation
1. Update API documentation
2. Add usage examples
3. Update architecture documentation

---

## Backward Compatibility

All changes maintain backward compatibility:

1. **Legacy parameters still work**:
   ```python
   # This still works
   report = api.report.create_uut_report(
       station_name="STATION",
       location="LOC",
       purpose="PROD"
   )
   ```

2. **API without station still works**:
   ```python
   # This still works (falls back to "Unknown")
   api = pyWATS(base_url="...", token="...")
   ```

3. **Existing config files still load**:
   - Old `station_name`, `location`, `purpose` fields still respected
   - New `stations` array is optional

---

## Summary

| Feature | Current | Proposed |
|---------|---------|----------|
| Station concept | None (scattered fields) | Core `Station` class |
| Multi-station | Not supported | `StationRegistry` |
| Default station | Must specify each time | API-level default |
| Client vs Station | Conflated | Clearly separated |
| Hub mode | Not supported | Full support |
| GUI station editing | Setup page only | Station Manager dialog |

This design provides flexibility for all use cases while maintaining simplicity for the common single-station scenario.
