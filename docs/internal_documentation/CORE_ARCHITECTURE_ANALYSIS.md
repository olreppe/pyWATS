# pyWATS Core Architecture Analysis

> **Document Purpose:** Comprehensive analysis of class naming, sync/async patterns, and layer architecture.  
> **Created:** 2026-01-27  
> **Last Updated:** 2026-01-27 (Post-simplification)  
> **Status:** Reference documentation for architecture review

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Main API Entry Points](#2-main-api-entry-points)
3. [Domain Service Pattern](#3-domain-service-pattern)
4. [HTTP Client Layer](#4-http-client-layer)
5. [Sync/Async Bridge](#5-syncasync-bridge)
6. [pywats_client Package](#6-pywats_client-package)
7. [Architecture Diagrams](#7-architecture-diagrams)
8. [Complete Class Inventory](#8-complete-class-inventory)
9. [Naming Conventions](#9-naming-conventions)
10. [Recent Simplifications](#10-recent-simplifications)

---

## 1. Executive Summary

pyWATS uses an **async-first architecture** where:
- All business logic lives in `AsyncXxxService` classes
- Sync wrappers use generic `SyncServiceWrapper` with `__getattr__` to bridge async → sync
- Two entry points exist with feature parity (auto-discovery, settings)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Entry Point Classes                          │
├─────────────────────────────────┬───────────────────────────────┤
│           pyWATS                │          AsyncWATS            │
│         (sync API)              │         (async API)           │
│    auto-discovery, settings     │    auto-discovery, settings   │
└─────────────────────────────────┴───────────────────────────────┘
```

> **Note:** `SyncWATS` was removed as redundant - `pyWATS` provides the same functionality with additional features.

---

## 2. Main API Entry Points

### 2.1 `pyWATS` Class (Primary Entry Point)

**File:** `src/pywats/pywats.py`

```python
class pyWATS:
    """Main entry point - auto-discovery, settings injection, station support."""
    
    def __init__(
        self,
        base_url: str = None,      # Optional - can auto-discover
        token: str = None,         # Optional - can auto-discover  
        timeout: float = 30.0,
        verify_ssl: bool = True,
        settings: Settings = None,
        station: StationInfo = None
    )
```

| Property | Instance Type | Lazy Init |
|----------|---------------|-----------|
| `.product` | `SyncServiceWrapper[AsyncProductService]` | ✓ |
| `.asset` | `SyncServiceWrapper[AsyncAssetService]` | ✓ |
| `.production` | `SyncServiceWrapper[AsyncProductionService]` | ✓ |
| `.report` | `SyncServiceWrapper[AsyncReportService]` | ✓ |
| `.software` | `SyncServiceWrapper[AsyncSoftwareService]` | ✓ |
| `.analytics` | `SyncServiceWrapper[AsyncAnalyticsService]` | ✓ |
| `.rootcause` | `SyncServiceWrapper[AsyncRootCauseService]` | ✓ |
| `.scim` | `SyncServiceWrapper[AsyncScimService]` | ✓ |
| `.process` | `SyncServiceWrapper[AsyncProcessService]` | ✓ |
| `.instances` | `InstanceManager` | ✓ |
| `.station` | `StationInfo` (optional) | - |
| `.config` | `Settings` | - |
| `.url` | `str` | - |
| `.timeout` | `float` | - |
| `.validation_mode` | `ValidationMode` | - |
| `.retry_config` | `RetryConfig` | - |

**Features:**
- Auto-discovers credentials from running pywats_client service
- Injects settings into services
- Context manager support (`with pyWATS() as api:`)
- Station provider for report creation

---

### 2.2 `AsyncWATS` Class (Async Entry Point)

**File:** `src/pywats/async_wats.py`

```python
class AsyncWATS:
    """Async entry point - auto-discovery, settings injection, full async API."""
    
    def __init__(
        self,
        base_url: str = None,      # Optional - can auto-discover
        token: str = None,         # Optional - can auto-discover  
        timeout: float = 30.0,
        verify_ssl: bool = True,
        settings: Settings = None,
        station: StationInfo = None,
        rate_limiter: RateLimiter = None,
        enable_throttling: bool = True,
        retry_config: RetryConfig = None,
        instance_id: str = "default"
    )
```

| Property | Instance Type | Lazy Init |
|----------|---------------|-----------|
| `.product` | `AsyncProductService` | ✓ |
| `.asset` | `AsyncAssetService` | ✓ |
| `.production` | `AsyncProductionService` | ✓ |
| `.report` | `AsyncReportService` | ✓ |
| `.software` | `AsyncSoftwareService` | ✓ |
| `.analytics` | `AsyncAnalyticsService` | ✓ |
| `.rootcause` | `AsyncRootCauseService` | ✓ |
| `.scim` | `AsyncScimService` | ✓ |
| `.process` | `AsyncProcessService` | ✓ |
| `.settings` | `APISettings` | - |
| `.http_client` | `AsyncHttpClient` | - |

**Features (same as pyWATS):**
- Auto-discovers credentials from running pywats_client service
- Injects settings into services
- Async context manager support (`async with AsyncWATS() as api:`)
- Station provider for report creation

**Usage:**
```python
# With explicit credentials
async with AsyncWATS(base_url="...", token="...") as api:
    products = await api.product.get_products()

# With auto-discovery
async with AsyncWATS() as api:  # Discovers from running service
    products = await api.product.get_products()
```

---

## 3. Domain Service Pattern

### 3.1 File Structure Per Domain

```
src/pywats/domains/<domain>/
├── __init__.py              # Public exports
├── async_repository.py      # Async{Domain}Repository
├── async_service.py         # Async{Domain}Service (source of truth)
├── models.py                # Pydantic models
└── enums.py                 # Enumerations
```

> **Note:** Manual `service.py` sync wrappers (`{Domain}Service`) have been removed. 
> The generic `SyncServiceWrapper` provides sync access via `pyWATS`.

### 3.2 Class Naming Pattern

| Layer | Class | Notes |
|-------|-------|-------|
| Repository | `AsyncAnalyticsRepository` | Data access layer |
| Service | `AsyncAnalyticsService` | Business logic (source of truth) |

### 3.3 Repository Class Structure

```python
class AsyncAnalyticsRepository:
    """Data access layer - HTTP calls to WATS API."""
    
    def __init__(
        self,
        http_client: AsyncHttpClient,
        error_handler: ErrorHandler,
        base_url: str = None
    )
    
    # All methods are async
    async def get_processes(self, ...) -> List[ProcessInfo]
    async def get_dynamic_yield(self, ...) -> List[YieldData]
```

### 3.4 Async Service Class Structure

```python
class AsyncAnalyticsService:
    """Business logic layer - source of truth for all logic."""
    
    def __init__(self, repository: AsyncAnalyticsRepository) -> None:
        self._repository = repository
    
    # All methods are async
    async def get_processes(self, ...) -> List[ProcessInfo]:
        return await self._repository.get_processes(...)
```

> **Note:** Manual sync wrapper classes (`AnalyticsService`, `ProductService`, etc.) have been removed.
> Sync access is provided via generic `SyncServiceWrapper` which uses `__getattr__` for dynamic method wrapping.

---

## 4. HTTP Client Layer

### 4.1 Client Classes

| Class | File | Purpose |
|-------|------|---------|
| `AsyncHttpClient` | `core/async_client.py` | Async HTTP via httpx.AsyncClient |
| `HttpClient` | `core/client.py` | Sync HTTP via httpx.Client |

### 4.2 AsyncHttpClient Structure

```python
class AsyncHttpClient:
    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: float = 30.0,
        verify_ssl: bool = True,
        rate_limiter: RateLimiter = None,
        enable_throttling: bool = True,
        retry_config: RetryConfig = None
    ):
        self._client: Optional[httpx.AsyncClient] = None
    
    # Core methods
    async def get(self, endpoint, params=None, **kwargs) -> Response
    async def post(self, endpoint, data=None, json=None, **kwargs) -> Response
    async def put(self, endpoint, data=None, json=None, **kwargs) -> Response
    async def delete(self, endpoint, **kwargs) -> Response
    async def patch(self, endpoint, data=None, json=None, **kwargs) -> Response
```

### 4.3 Response Model

```python
class Response(BaseModel):
    """Standardized HTTP response wrapper."""
    status_code: int
    headers: Dict[str, str]
    content: bytes
    text: str
    json_data: Optional[Any] = None
    
    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300
```

---

## 5. Sync/Async Bridge

### 5.1 `run_sync()` Function

**File:** `core/sync_runner.py`

```python
def run_sync(coro: Coroutine[Any, Any, T]) -> T:
    """Run an async coroutine synchronously.
    
    Strategy:
    1. If no event loop running: use asyncio.run()
    2. If in async context: run in thread pool to avoid deadlock
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running loop - simple case
        return asyncio.run(coro)
    else:
        # Already in async context - use thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result()
```

### 5.2 `SyncServiceWrapper` Class

**File:** `core/sync_wrapper.py`

```python
class SyncServiceWrapper(Generic[T]):
    """Generic wrapper that proxies method calls through run_sync()."""
    
    def __init__(self, async_service: T):
        self._async_service = async_service
    
    def __getattr__(self, name: str):
        attr = getattr(self._async_service, name)
        if asyncio.iscoroutinefunction(attr):
            @functools.wraps(attr)
            def sync_method(*args, **kwargs):
                return run_sync(attr(*args, **kwargs))
            return sync_method
        return attr
```

---

## 6. pywats_client Package

### 6.1 Overview

`pywats_client` is a **separate application package** (not part of the API library):

```
src/pywats_client/
├── __init__.py
├── service/
│   ├── client_service.py      # ClientService
│   └── ipc_server.py          # IPCServer
├── converter/
│   ├── converter_pool.py      # ConverterPool
│   └── base_converter.py      # BaseConverter
├── watcher/
│   └── pending_watcher.py     # PendingWatcher
└── queue/
    └── report_queue.py        # ReportQueue
```

### 6.2 Class Inventory

| Class | Purpose |
|-------|---------|
| `ClientService` | Main service controller (background service) |
| `ConverterPool` | Manages file-to-report converters |
| `BaseConverter` | Abstract base for custom converters |
| `PendingWatcher` | Monitors folder for new files |
| `ReportQueue` | Queues reports for submission |
| `IPCServer` | Inter-process communication with GUI |

### 6.3 Relationship to pyWATS API

```
┌──────────────────────────────────────────────────────────────┐
│                     pywats_client                            │
│                   (Background Service)                       │
│                                                              │
│  ┌────────────────┐    ┌────────────────┐                   │
│  │ ClientService  │    │  IPCServer     │◄── GUI/Tools      │
│  └───────┬────────┘    └────────────────┘                   │
│          │                                                   │
│          │ uses                                              │
│          ▼                                                   │
│  ┌────────────────┐                                         │
│  │    pyWATS      │  ◄── API library instance               │
│  └───────┬────────┘                                         │
└──────────┼───────────────────────────────────────────────────┘
           │
           ▼
    ┌──────────────┐
    │  WATS Server │
    └──────────────┘
```

**Key relationship:**
- `ClientService` creates and uses a `pyWATS` instance internally
- `pyWATS` can **auto-discover** credentials from running `ClientService` via IPC
- They solve different problems: API library vs. file processing service

---

## 7. Architecture Diagrams

### 7.1 Full Stack Layer Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            USER CODE                                     │
│                                                                          │
│   # Sync usage                        # Async usage                      │
│   api = pyWATS()                     async with AsyncWATS() as api:     │
│   products = api.product.get_all()       products = await api.product...│
└─────────────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
         ▼                                         ▼
┌─────────────────────┐                 ┌─────────────────────┐
│       pyWATS        │                 │     AsyncWATS       │
│                     │                 │                     │
│ • Auto-discover     │                 │ • Auto-discover     │
│ • Settings          │                 │ • Settings          │
│ • Station           │                 │ • Station           │
│ • Sync wrapper      │                 │ • Pure async        │
└──────────┬──────────┘                 └──────────┬──────────┘
           │                                       │
           ▼                                       │
┌─────────────────────┐                           │
│ SyncServiceWrapper  │                           │
│     (generic)       │                           │
│                     │                           │
│ Proxies calls       │                           │
│ via run_sync()      │                           │
└──────────┬──────────┘                           │
           │                                       │
           └───────────────────┬───────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       AsyncXxxService                                    │
│                                                                          │
│   • Business logic (SOURCE OF TRUTH)                                    │
│   • Validation, transformation, logging                                  │
│   • Delegates to repository for data access                             │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     AsyncXxxRepository                                   │
│                                                                          │
│   • Data access layer                                                    │
│   • HTTP call construction                                               │
│   • Response parsing                                                     │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       AsyncHttpClient                                    │
│                                                                          │
│   • httpx.AsyncClient wrapper                                           │
│   • Authentication (Bearer token)                                        │
│   • Retry logic, rate limiting, throttling                              │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         WATS REST API                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Domain Module Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        domains/<domain>/                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────┐                                                    │
│  │  __init__.py    │  Exports:                                          │
│  └────────┬────────┘  • AsyncXxxService                                 │
│           │           • AsyncXxxRepository                               │
│           │           • Models, Enums                                    │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        Exports Tree                              │   │
│  │                                                                  │   │
│  │   async_service.py ──► AsyncAnalyticsService                    │   │
│  │                            │                                     │   │
│  │   async_repository.py ► AsyncAnalyticsRepository                │   │
│  │                            │                                     │   │
│  │   models.py ──────────► YieldData, ProcessInfo, ...             │   │
│  │                            │                                     │   │
│  │   enums.py ───────────► YieldDataType, ProcessType, ...         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

> **Note:** Manual sync wrapper classes (`XxxService`) have been removed.

### 7.3 Sync/Async Flow Diagram

```
                    SYNC CALL                           ASYNC CALL
                    ─────────                           ──────────
                        │                                   │
                        ▼                                   ▼
              ┌─────────────────┐                 ┌─────────────────┐
              │    pyWATS       │                 │   AsyncWATS     │
              │   .analytics    │                 │   .analytics    │
              └────────┬────────┘                 └────────┬────────┘
                       │                                   │
                       ▼                                   │
              ┌─────────────────┐                          │
              │SyncServiceWrapper│                         │
              │ .get_processes()│                          │
              └────────┬────────┘                          │
                       │                                   │
                       ▼                                   │
              ┌─────────────────┐                          │
              │   run_sync()    │                          │
              │                 │                          │
              │ Executes coro   │                          │
              │ synchronously   │                          │
              └────────┬────────┘                          │
                       │                                   │
                       └──────────────┬────────────────────┘
                                      │
                                      ▼
                         ┌─────────────────────┐
                         │AsyncAnalyticsService│
                         │  .get_processes()   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │AsyncAnalyticsRepo   │
                         │  .get_processes()   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  AsyncHttpClient    │
                         │     .get(...)       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                              HTTP Request
```

---

## 8. Complete Class Inventory

### 8.1 Entry Point Classes

| Class | File | Constructor Args |
|-------|------|------------------|
| `pyWATS` | `pywats.py` | `base_url?`, `token?`, `timeout`, `verify_ssl`, `settings?`, `station?`, `instance_id` |
| `AsyncWATS` | `async_wats.py` | `base_url?`, `token?`, `timeout`, `verify_ssl`, `settings?`, `station?`, `instance_id` |

> **Note:** `SyncWATS` has been removed as redundant. Use `pyWATS` for sync access.

### 8.2 Domain Services (All 9 Domains)

| Domain | Async Service | Async Repository |
|--------|---------------|------------------|
| Analytics | `AsyncAnalyticsService` | `AsyncAnalyticsRepository` |
| Asset | `AsyncAssetService` | `AsyncAssetRepository` |
| Process | `AsyncProcessService` | `AsyncProcessRepository` |
| Product | `AsyncProductService` | `AsyncProductRepository` |
| Production | `AsyncProductionService` | `AsyncProductionRepository` |
| Report | `AsyncReportService` | `AsyncReportRepository` |
| RootCause | `AsyncRootCauseService` | `AsyncRootCauseRepository` |
| Scim | `AsyncScimService` | `AsyncScimRepository` |
| Software | `AsyncSoftwareService` | `AsyncSoftwareRepository` |

> **Note:** Manual sync service classes (`AnalyticsService`, etc.) have been removed. 
> Sync access is provided via `SyncServiceWrapper` in `pyWATS`.

### 8.3 Core Infrastructure Classes

| Class | File | Purpose |
|-------|------|---------|
| `AsyncHttpClient` | `core/async_client.py` | Async HTTP client |
| `HttpClient` | `core/client.py` | Sync HTTP client |
| `Response` | `core/response.py` | HTTP response model |
| `ErrorHandler` | `core/error_handler.py` | Error translation |
| `RateLimiter` | `core/rate_limiter.py` | Request throttling |
| `RetryConfig` | `core/retry.py` | Retry configuration |
| `SyncServiceWrapper` | `pywats.py` + `sync.py` | Generic sync wrapper |
| `Settings` | `core/settings.py` | Configuration container |
| `InstanceManager` | `core/instances.py` | Multi-instance support |

### 8.4 Client Package Classes

| Class | File | Purpose |
|-------|------|---------|
| `ClientService` | `pywats_client/service/client_service.py` | Background service |
| `IPCServer` | `pywats_client/service/ipc_server.py` | IPC communication |
| `ConverterPool` | `pywats_client/converter/converter_pool.py` | Converter management |
| `BaseConverter` | `pywats_client/converter/base_converter.py` | Converter base class |
| `PendingWatcher` | `pywats_client/watcher/pending_watcher.py` | File monitoring |
| `ReportQueue` | `pywats_client/queue/report_queue.py` | Report queuing |

---

## 9. Naming Conventions

### 9.1 Entry Point Naming ✓

The `pyWATS` naming follows established Python conventions:

| Package | Convention |
|---------|------------|
| `pygame` | py + Game |
| `pytest` | py + Test |
| `pydantic` | py + Pedantic |
| `pytz` | py + TimeZone |
| `pylint` | py + Lint |
| `pytorch` | py + Torch |
| **`pyWATS`** | **py + WATS** ✓ |

The lowercase `py` prefix is the Python standard for packages that "Python-ify" something.

**Current naming:**
| Class | Purpose | Convention |
|-------|---------|------------|
| `pyWATS` | Main sync entry (auto-discovery) | py + brand name ✓ |
| `AsyncWATS` | Async entry (auto-discovery) | Async + brand ✓ |

> **Note:** `SyncWATS` has been removed as `pyWATS` provides the same functionality with additional features.

### 9.2 Service Property Returns

| Entry Point | Property Returns | Rationale |
|-------------|------------------|-----------|
| `pyWATS` | `SyncServiceWrapper[AsyncXxxService]` | Generic wrapping via `__getattr__` |
| `AsyncWATS` | `AsyncXxxService` directly | Pure async, no wrapping needed |

This is intentional - the `SyncServiceWrapper` approach:
- **Avoids code duplication** - no need to maintain separate sync service implementations
- **Single source of truth** - all business logic lives in `AsyncXxxService`
- **Flexible** - users can choose sync or async based on their needs
- **Type-safe** - the wrapper preserves method signatures

---

## 10. Recent Simplifications

### 10.1 Removed Components

The following components were removed to simplify the architecture:

**Removed Entry Point:**
- `SyncWATS` class - Redundant with `pyWATS` which provides sync access plus auto-discovery

**Removed Domain Services (~4,000 lines removed):**
- `AnalyticsService`, `AssetService`, `ProcessService`, `ProductService`
- `ProductionService`, `ReportService`, `RootCauseService`, `ScimService`, `SoftwareService`

These manual sync wrapper classes were replaced by the generic `SyncServiceWrapper` which:
1. Uses `__getattr__` for dynamic method wrapping
2. Automatically wraps any async method to sync
3. Reduces maintenance burden (one implementation vs. nine)

### 10.2 Two Entry Points - Simplified Design

The two entry points now serve distinct use cases with feature parity:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     ENTRY POINT DECISION TREE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  What's your execution model?                                           │
│  ├─ Sync (scripts, tests, simple tools)                                 │
│  │  └─ Use pyWATS()                                                     │
│  │      • Blocking calls, simple usage                                  │
│  │      • Auto-discovers credentials from running service               │
│  │      • Can also provide explicit credentials                         │
│  │                                                                       │
│  └─ Async (GUI, web, high-concurrency)                                  │
│     └─ Use AsyncWATS()                                                  │
│         • Pure async, maximum performance                               │
│         • Auto-discovers credentials from running service               │
│         • Can also provide explicit credentials                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Both entry points now support:**
- Auto-discovery from running pywats_client service
- Settings injection
- Station configuration
- Explicit credential override

### 10.3 Async-First with Generic Sync Wrapper

The architecture follows an **async-first** pattern:

```
AsyncXxxService  ←── Source of Truth (all business logic)
      │
      ├── Used directly by AsyncWATS
      │
      └── Wrapped by SyncServiceWrapper for pyWATS
              │
              └── run_sync() bridges async → sync
```

**Benefits of generic `SyncServiceWrapper`:**
1. **No code duplication** - Business logic written once in async services
2. **Consistency** - Sync and async APIs have identical behavior
3. **Maintainability** - Changes only need to be made in one place
4. **Flexibility** - Users choose their preferred execution model
5. **Future-proof** - Async is the direction Python is heading
6. **~4,000 fewer lines** - Removed manual sync wrapper classes

---

## Appendix: Quick Reference

### Import Patterns

```python
# Main API - Sync (recommended for scripts)
from pywats import pyWATS

api = pyWATS()  # Auto-discovers from client service
api = pyWATS(base_url="https://...", token="...")  # Explicit

products = api.product.get_products()  # Sync calls

# Async API (recommended for GUI/web/concurrency)
from pywats import AsyncWATS

async with AsyncWATS() as api:  # Auto-discovers
    products = await api.product.get_products()

# Or with explicit credentials
async with AsyncWATS(base_url="...", token="...") as api:
    products = await api.product.get_products()

# Direct async service access (for testing)
from pywats.domains.analytics import AsyncAnalyticsService
```

### Type Hints

```python
from pywats import pyWATS
from pywats.domains.product import ProductView
from typing import List

def get_active_products(api: pyWATS) -> List[ProductView]:
    return api.product.get_products()
```
