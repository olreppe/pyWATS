# PyWATS API Architecture

## Overview

PyWATS is a Python library for interacting with the WATS server. The library follows a **layered domain-driven architecture** that separates concerns and provides a clean, maintainable codebase.

## Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│                   pyWATS (Facade)                   │
│              Single entry point for API             │
└──────────────────┬──────────────────────────────────┘
                   │
     ┌─────────────┼─────────────┬──────────────┐
     │             │             │              │
┌────▼────┐   ┌───▼────┐   ┌───▼────┐    ┌───▼────┐
│ Product │   │ Asset  │   │ Report │... │  App   │
│ Service │   │Service │   │Service │    │Service │
└────┬────┘   └───┬────┘   └───┬────┘    └───┬────┘
     │             │             │              │
┌────▼────┐   ┌───▼────┐   ┌───▼────┐    ┌───▼────┐
│ Product │   │ Asset  │   │ Report │... │  App   │
│  Repo   │   │  Repo  │   │  Repo  │    │  Repo  │
└────┬────┘   └───┬────┘   └───┬────┘    └───┬────┘
     │             │             │              │
     └─────────────┴─────────────┴──────────────┘
                   │
            ┌──────▼──────┐
            │ HTTP Client │
            │  (Core)     │
            └──────┬──────┘
                   │
            ┌──────▼──────┐
            │ WATS Server │
            └─────────────┘
```

## Layer Responsibilities

### 1. Facade Layer (`pywats.py`)

**Purpose**: Single entry point for the entire API

**Responsibilities**:
- Initialize and manage all domain services
- Provide property-based access to each domain
- Handle authentication configuration
- Manage HTTP client lifecycle

**Example**:
```python
from pywats import pyWATS

api = pyWATS(
    base_url="https://wats.example.com",
    token="base64_encoded_credentials"
)

# Access domains through properties
products = api.product.get_products()
report = api.report.get_report(uuid)
```

### 2. Service Layer (`service.py`)

**Purpose**: Business logic and orchestration

**Responsibilities**:
- Validate business rules beyond basic field validation
- Transform and enrich data
- Orchestrate multiple repository calls
- Provide high-level convenience methods
- Handle complex workflows

**Example**:
```python
class ProductService:
    def __init__(self, repository: ProductRepository):
        self._repo = repository
    
    def get_active_products(self) -> List[Product]:
        """Get only active products"""
        products = self._repo.get_products()
        return [p for p in products if p.state == ProductState.ACTIVE]
```

### 3. Repository Layer (`repository.py`)

**Purpose**: Data access and API communication

**Responsibilities**:
- Make HTTP requests to WATS server
- Parse responses into domain models
- Handle HTTP errors
- No business logic - pure data access

**Example**:
```python
class ProductRepository:
    def __init__(self, client: HttpClient, error_handler: ErrorHandler):
        self._client = client
        self._error_handler = error_handler
    
    def get_product(self, part_number: str) -> Optional[Product]:
        response = self._client.get(f"/api/Product/{part_number}")
        if response.status == 404:
            return self._error_handler.handle_not_found(...)
        return Product.model_validate(response.data)
```

### 4. Model Layer (`models.py`)

**Purpose**: Data structures and validation

**Responsibilities**:
- Define data models using Pydantic
- Field-level validation
- Serialization/deserialization rules
- Type safety
- No business logic, no API calls

**Example**:
```python
class Product(PyWATSModel):
    part_number: str = Field(..., alias="partNumber")
    state: ProductState = Field(default=ProductState.ACTIVE)
    description: Optional[str] = None
```

### 5. Core Layer (`core/`)

**Purpose**: Infrastructure and shared utilities

**Components**:
- `client.py` - HTTP client with authentication
- `exceptions.py` - Custom exception hierarchy

### 6. Shared Layer (`shared/`)

**Purpose**: Cross-cutting concerns

**Components**:
- `base_model.py` - Base Pydantic model configuration
- `common_types.py` - Shared types (e.g., `Setting`)

### 7. Logging (`core/logging.py`)

**Purpose**: Diagnostic and troubleshooting support

**Features**:
- Uses Python's standard `logging` module
- Library never configures handlers (user's responsibility)
- Each module has its own logger under `pywats.*` hierarchy
- Quick debug helper: `enable_debug_logging()`

**Logging Levels**:
- **DEBUG**: Detailed operations (HTTP requests, parameters, response sizes)
- **INFO**: Successful operations with context (counts, IDs)
- **WARNING**: Non-critical issues (empty responses in LENIENT mode)
- **ERROR**: Actual errors with full context

**Example**:
```python
from pywats import enable_debug_logging

# Quick debug mode
enable_debug_logging()

# Or custom configuration
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('pywats.http_client').setLevel(logging.DEBUG)
```

See [LOGGING_STRATEGY.md](../LOGGING_STRATEGY.md) for comprehensive guide.

## Domain Structure

Each domain follows the same structure:

```
domains/
└── {domain}/
    ├── __init__.py          # Public exports
    ├── models.py            # Data models
    ├── enums.py            # Enumerations (optional)
    ├── service.py          # Business logic
    └── repository.py       # API communication
```

### Available Domains

| Domain | Purpose | Key Models |
|--------|---------|------------|
| **product** | Product/part management | Product, ProductRevision, BOM |
| **asset** | Test equipment tracking | Asset, AssetType, AssetLog |
| **production** | Serial number/unit tracking | Unit, UnitChange, SerialNumberType |
| **report** | Test report submission/query | UUTReport, UURReport, WATSFilter |
| **rootcause** | Issue ticketing system | Ticket, TicketUpdate |
| **app** | Statistics and KPIs | YieldData, ProcessInfo |
| **software** | Software distribution | SoftwarePackage |
| **process** | Operation/process data | ProcessType, ProcessDefinition |

## Data Flow

### 1. Reading Data (Query)

```
User Code
   ↓
api.{domain}.get_*()
   ↓
Service (business logic/filtering)
   ↓
Repository (HTTP GET)
   ↓
HttpClient (authentication/request)
   ↓
WATS Server
   ↓
Response → Model (validation)
   ↓
User Code
```

### 2. Writing Data (Command)

```
User Code (creates model)
   ↓
api.{domain}.create_*() or send_*()
   ↓
Service (validation/enrichment)
   ↓
Repository (HTTP POST/PUT)
   ↓
HttpClient (authentication/request)
   ↓
WATS Server
   ↓
Response → Model
   ↓
User Code
```

## Authentication & Configuration

### Basic Authentication

```python
import base64

credentials = base64.b64encode(b"username:password").decode()
api = pyWATS(
    base_url="https://wats.example.com",
    token=credentials
)
```

### Error Modes

```python
from pywats.core.exceptions import ErrorMode

# STRICT mode (default) - raises exceptions
api = pyWATS(..., error_mode=ErrorMode.STRICT)

# LENIENT mode - returns None for 404s
api = pyWATS(..., error_mode=ErrorMode.LENIENT)
```

### Timeouts

```python
# 60 second timeout
api = pyWATS(..., timeout=60)
```

## Best Practices

### 1. Use Domain Properties

```python
# ✓ Good
products = api.product.get_products()

# ✗ Avoid
from pywats.domains.product import ProductService
service = ProductService(...)  # Don't instantiate directly
```

### 2. Import Models from Top-Level

```python
# ✓ Good - common models
from pywats import Product, Asset, Unit

# ✓ Good - report models
from pywats.models import UUTReport, UURReport

# ✓ Good - domain-specific
from pywats.domains.report import ReportType  # For UUT/UUR queries
from pywats.domains.report import WATSFilter  # For analytics API (not report queries)
```

### 3. Use Service Methods, Not Direct API

```python
# ✓ Good - uses service methods
report = api.report.get_report_by_serial("SN-001")

# ✗ Avoid - bypassing service layer
response = api._http_client.get("/api/Report/...")  # Don't access private
```

### 4. Model Validation is Automatic

```python
# Models validate automatically
product = Product(
    part_number="PART-001",
    state=ProductState.ACTIVE  # Enum validated
)
# Pydantic raises ValidationError if invalid
```

## Testing Architecture

The layered architecture enables easy testing:

### Unit Testing Services

```python
from unittest.mock import Mock

def test_get_active_products():
    mock_repo = Mock()
    mock_repo.get_products.return_value = [
        Product(part_number="P1", state=ProductState.ACTIVE),
        Product(part_number="P2", state=ProductState.OBSOLETE),
    ]
    
    service = ProductService(mock_repo)
    active = service.get_active_products()
    
    assert len(active) == 1
    assert active[0].part_number == "P1"
```

### Integration Testing

```python
def test_product_roundtrip(wats_client):
    # Uses real pyWATS instance with test server
    product = wats_client.product.get_product("TEST-001")
    assert product.part_number == "TEST-001"
```

## Extension Points

### Adding Internal APIs

Some domains have `_internal` files for undocumented APIs. These are accessed
through the main domain accessor (unified API pattern):

```python
# Public API
api.product.get_product("PART-001")

# Internal API (accessed same way, marked in docstring)
api.product.get_box_build_template("PART-001")  # ⚠️ INTERNAL API warning in docstring
```

Create `service_internal.py` and `repository_internal.py` for implementation.
Main service wraps internal service methods - see `docs/internal/API_DESIGN_CONVENTIONS.md`.

### Custom Validation

Extend service layer for custom business rules:

```python
class CustomProductService(ProductService):
    def create_product(self, **kwargs):
        # Add custom validation
        if kwargs['part_number'].startswith('TEST'):
            raise ValueError("Test parts not allowed in production")
        return super().create_product(**kwargs)
```

## Error Handling

### Exception Hierarchy

```
PyWATSError (base)
├── AuthenticationError (401)
├── NotFoundError (404)
├── ValidationError (400)
├── ServerError (500)
└── ConnectionError (network)
```

### Usage

```python
from pywats import NotFoundError

try:
    product = api.product.get_product("INVALID")
except NotFoundError:
    print("Product not found")
```

## Performance Considerations

### 1. Connection Pooling

The HTTP client uses connection pooling automatically.

### 2. Batch Operations

Use batch methods when available:

```python
# ✓ Good - single request
units = api.production.get_units([sn1, sn2, sn3])

# ✗ Avoid - multiple requests
units = [api.production.get_unit(sn) for sn in [sn1, sn2, sn3]]
```

### 3. Filtering Server-Side

```python
# ✓ Good - filter on server using OData
headers = api.report.query_uut_headers(
    odata_filter="partNumber eq 'PART-001'"
)

# ✓ Good - use helper methods
headers = api.report.get_headers_by_part_number("PART-001")

# ✗ Avoid - fetch all, filter locally
headers = api.report.query_uut_headers()
filtered = [h for h in headers if h.part_number == "PART-001"]
```

## Version Compatibility

The API is designed for forward compatibility:

- **Adding fields**: New optional fields won't break existing code
- **Deprecation**: Old methods maintained with warnings
- **Breaking changes**: Only in major versions (e.g., 2.0 → 3.0)

## Further Reading

See module-specific documentation in `docs/usage/`:
- [Report Module](usage/REPORT_MODULE.md) - Test reports and factory methods
- [Product Module](usage/PRODUCT_MODULE.md) - Product/BOM management
- [Production Module](usage/PRODUCTION_MODULE.md) - Serial number tracking
- [Asset Module](usage/ASSET_MODULE.md) - Equipment management

---

## pyWATS Client Architecture

The pyWATS Client (`pywats_client`) provides a complete application layer on top of the pyWATS API. It supports both GUI and headless operation modes.

### Client Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                   User Interface Layer                       │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Qt GUI        │   CLI           │   HTTP Control API      │
│   (PySide6)     │   (argparse)    │   (stdlib http.server)  │
│   Desktop only  │   Headless      │   Remote management     │
│   gui/          │   control/cli   │   control/http_api      │
└────────┬────────┴────────┬────────┴────────┬────────────────┘
         │                 │                 │
         └─────────────────┴─────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         │      pyWATSApplication (app.py)    │
         │      Core application - No GUI     │
         │      Service lifecycle management  │
         └─────────────────┬─────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         │          Services Layer            │
         │  services/                         │
         │  ├── connection.py                 │
         │  ├── process_sync.py               │
         │  ├── report_queue.py               │
         │  ├── converter_manager.py          │
         │  └── settings_manager.py           │
         └─────────────────┬─────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         │           pyWATS API               │
         │           (pywats/)                │
         └───────────────────────────────────┘
```

### Installation Profiles

| Profile | Command | Qt Required | Use Case |
|---------|---------|-------------|----------|
| API Only | `pip install pywats-api` | No | Python scripts, integrations |
| Full Client | `pip install pywats-api[client]` | Yes | Desktop workstations |
| Headless | `pip install pywats-api[client-headless]` | No | Raspberry Pi, servers, Docker |

### GUI Mode (Desktop)

The Qt GUI (`gui/`) provides a full desktop application:

```bash
python -m pywats_client
# or
pywats-client  # (without arguments defaults to GUI)
```

Components:
- `gui/app.py` - Application entry point
- `gui/main_window.py` - Main window with navigation
- `gui/login_window.py` - Authentication
- `gui/settings_dialog.py` - Configuration UI
- `gui/pages/` - Feature pages (converters, queue, log)

### Headless Mode (CLI/API)

The control module (`control/`) enables headless operation:

```bash
# CLI commands
pywats-client config show
pywats-client status
pywats-client start --api --api-port 8765

# Run as daemon (Linux)
pywats-client start --daemon
```

Components:
- `control/cli.py` - Command-line interface
- `control/http_api.py` - REST API server (stdlib, no dependencies)
- `control/service.py` - Daemon/service runner

### Control Interfaces Comparison

| Interface | Port | Use Case | Dependency |
|-----------|------|----------|------------|
| CLI | - | Local management, scripting | None |
| HTTP API | 8765 | Remote management, monitoring | None |
| GUI | - | Interactive desktop use | PySide6 |

### HTTP API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/status` | Service status |
| GET | `/config` | Get configuration |
| POST | `/config` | Update configuration |
| GET | `/converters` | List converters |
| POST | `/start` | Start services |
| POST | `/stop` | Stop services |
| POST | `/restart` | Restart services |

### Deployment Patterns

#### Desktop Workstation
```bash
pip install pywats-api[client]
python -m pywats_client  # GUI
```

#### Raspberry Pi / Embedded
```bash
pip install pywats-api[client-headless]
pywats-client config init --server-url https://wats.example.com
pywats-client start --api  # With remote management
```

#### Linux Server (systemd)
```bash
pip install pywats-api[client-headless]
sudo cp pywats-client.service /etc/systemd/system/
sudo systemctl enable pywats-client
sudo systemctl start pywats-client
```

#### Docker Container
```dockerfile
FROM python:3.11-slim
RUN pip install pywats-api[client-headless]
CMD ["pywats-client", "start", "--api", "--api-host", "0.0.0.0"]
```

### Service Layer Details

All services are GUI-independent and can run headless:

| Service | Purpose | Key Features |
|---------|---------|--------------|
| `ConnectionService` | Server connectivity | Auto-reconnect, status monitoring |
| `ProcessSyncService` | Process data sync | Incremental sync, offline cache |
| `ReportQueueService` | Report upload queue | Retry logic, persistent storage |
| `ConverterManager` | File conversion | File watching, plugin loading |
| `SettingsManager` | Configuration | JSON persistence, validation |

See [Headless Operation Guide](../src/pywats_client/control/HEADLESS_GUIDE.md) for complete setup instructions.
