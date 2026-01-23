# Async Implementation Strategy

> **Status**: ✅ COMPLETE - All 9 domains have async support

## Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| AsyncHttpClient | ✅ Complete | `pywats/core/async_client.py` |
| AsyncWATS client | ✅ Complete | `pywats/async_wats.py` |
| SyncWATS wrapper | ✅ Complete | `pywats/sync.py` with `run_sync()` |
| Async repositories (9) | ✅ Complete | All domains have `async_repository.py` |
| Async services (9) | ✅ Complete | All domains have `async_service.py` |
| Sync services (9) | ✅ Complete | Thin wrappers using `run_sync()` |
| GUI AsyncTaskRunner | ✅ Complete | Alternative to qasync |
| GUI Pages async | ✅ Complete | 4 pages converted |

## 1. Executive Summary
This document outlines the strategy to transition the entire `pyWATS` API and Client from a synchronous (blocking) architecture to a fully asynchronous (non-blocking) architecture. This is critical for the GUI application to remain responsive while performing network operations.

## 2. Risk Assessment

### 2.1 Technical Risks
*   **"Function Coloring" / viral Async**: Converting the Core `HttpClient` to async requires every calling function up the stack (Repositories -> Services -> GUI Event Handlers) to effectively become async. Ideally, we want to expose *only* async to the future-proof the library, but this breaks all existing synchronous scripts.
*   **Complexity in GUI Integration**: `asyncio` and Qt (PySide6) both have their own event loops. Integrating them incorrectly yields "Event loop is already running" errors or freezes the GUI.
*   **Debugging Difficulty**: Async stack traces can be harder to read, and un-awaited coroutines result in silent failures.

### 2.2 Migration Risks
*   **Breaking Changes**: This is a complete rewrite of the public API signature. `api.product.get()` becomes `await api.product.get()`.
*   **Race Conditions**: With non-blocking calls, the user might click a button twice before the first operation completes. The GUI must manage state (disable buttons) during `await` periods.

## 3. Implementation Strategy: The "Modern Async" Stack

We will migrate to `httpx.AsyncClient` and strictly usage of `async/await` throughout the logic layers. For the GUI, we will use `qasync` to bridge the Qt and asyncio event loops.

### 3.1 Core Layer (`pywats.core`)
Refactor `HttpClient` to use `httpx.AsyncClient`.

**Before:**
```python
def get(self, endpoint, ...):
    resp = self.client.get(...)
    return resp 
```

**After:**
```python
async def get(self, endpoint, ...):
    # Context manager for the client session is preferred
    resp = await self.client.get(...)
    return resp
```

### 3.2 Domain Layer (Repositories & Services)
All domain methods become coroutines.

**Example `ProductionService`:**
```python
class ProductionService:
    def __init__(self, repository):
        self._repo = repository

    async def get_unit(self, sn: str, pn: str) -> Unit:
        # We await the repository, which awaits the http client
        return await self._repo.get_unit(sn, pn)
```

### 3.3 GUI Integration (`pywats_client`)

#### Strategy: `qasync` (The "Lenient" Way)
We need the UI to "wait" for data (so we continue logic flow linearly) without "freezing" the window. `qasync` allows us to run the `asyncio` loop *inside* the Qt main loop.

**Dependency:** Add `qasync` to requirements.

**Main Entry Point (`app.py`):**
```python
import sys
import asyncio
from qasync import QEventLoop
from PySide6.QtWidgets import QApplication

def run_gui():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    main_window = MainWindow()
    main_window.show()
    
    with loop:
        loop.run_forever()
```

**Event Handlers (`production.py`):**
We use the `@asyncSlot()` decorator (provided by `qasync`) to allow buttons to trigger async functions.

```python
from qasync import asyncSlot

class ProductionPage(BasePage):
    
    @asyncSlot()
    async def _on_refresh_clicked(self):
        # 1. UI State: Busy
        self.show_loading_spinner()
        self.refresh_btn.setEnabled(False)
        
        try:
            # 2. Await the response - UI remains responsive (repaints, handles events)
            #    but execution of THIS function pauses here.
            phases = await self.facade.production_service.get_phases()
            
            # 3. Update UI with data
            self._update_phase_dropdown(phases)
            
        except Exception as e:
            self.show_error(e)
            
        finally:
            # 4. UI State: Idle
            self.refresh_btn.setEnabled(True)
            self.hide_loading_spinner()
```

## 4. Migration Steps
1.  ✅ **Core**: Rewrite `HttpClient` to support `async with` context manager and `async` methods.
2.  ✅ **Domains**: Systematically update one domain at a time (Product first, then Production, etc.) to `async def`.
3.  ✅ **GUI**: Using `AsyncTaskRunner` instead of `qasync` for better control.
4.  ✅ **Pages**: Convert button handlers using `run_async()` pattern.

## 5. Actual Implementation (2026-01-23)

Instead of `qasync`, we implemented `AsyncTaskRunner` which provides:
- Runs coroutines in a background thread pool
- Delivers results via Qt signals (thread-safe)
- Loading indicators and task management
- Task cancellation support

**Pattern used in pages:**
```python
def _on_refresh(self) -> None:
    self.run_async(
        self._fetch_data(),
        name="Loading data...",
        on_complete=self._on_data_loaded,
        on_error=self._on_data_error
    )

async def _fetch_data(self) -> List[Dict]:
    client = self._get_api_client()
    return await client.domain.get_items()

def _on_data_loaded(self, result: TaskResult) -> None:
    if result.is_success:
        self._populate_table(result.result)
```

**Sync service wrappers** use `run_sync()` for scripts that don't need async:
```python
from pywats.core.sync_runner import run_sync

class ProductService:
    def __init__(self, async_service: AsyncProductService):
        self._async = async_service
    
    def get_product(self, part_number: str) -> Optional[Product]:
        return run_sync(self._async.get_product(part_number))
```
