# Architectural Improvements & Facade Refactoring

> **Status**: ✅ Routes class COMPLETE, Facade refactoring DEFERRED

## Implementation Status

| Item | Status | Notes |
|------|--------|-------|
| Routes class | ✅ Complete | 170 endpoints in `pywats/core/routes.py` |
| All repos use Routes | ✅ Complete | 9/9 async_repository.py migrated |
| Duck typing removal | 🔲 Not started | Use Pydantic validation |
| Domain-specific facades | 🔲 Deferred | Using direct service access for now |

## 1. Problem: Leaky Facade abstraction
Currently, the `AppFacade` exposes the raw `api` object directly (`facade.api`). This leads to high coupling between GUI code and the specific implementation of the API library. It also leads to "Law of Demeter" violations where pages reach deep into the API structure.

**Problematic Code:**
```python
# In a GUI Page
if api := self.facade.api:
    # Page knows about "product", "get_all", and how the API is structured
    products = api.product.get_all() 
```

## 2. Proposed Solution: Domain-Specific Facades

Instead of exposing the entire `pyWATS` API object, the `AppFacade` should provide curated access to domains. This allows us to inject caching, thread management (if not using async), or specific UI-formatted data transformations at the facade level.

### 2.1 Structure

```python
class AppFacade:
    def __init__(self, app):
        self._app = app
    
    @property
    def production(self) -> ProductionController:
        """Access production related features."""
        # Returns a wrapper that manages the async service calls
        return self._app.services.production 

    @property
    def products(self) -> ProductController:
        return self._app.services.products
```

### 2.2 Controller/Service Pattern for Client
The Client app should have its own "Service" layer that wraps the `pyWATS` library. This is where we handle the connection between the GUI needs and the backend.

```python
class ProductionController:
    def __init__(self, api_client_provider):
        self._provider = api_client_provider

    async def get_active_phases(self) -> List[PhaseViewModel]:
        """
        GUI-specific method. 
        Fetch phases -> Transform to ViewModel (for dropdowns).
        Handles the case where API is not connected implicitly.
        """
        api = self._provider.get_connected_api() # Raises error if offline
        phases = await api.production.get_phases()
        return [PhaseViewModel(p) for p in phases]
```

## 3. Configuration & Constants Standardization

### 3.1 Hardcoded Routes
The current repositories have string literals for paths (e.g., `/api/Production/Unit`). This is error-prone.

**Fix:** ✅ IMPLEMENTED - Created `pywats.core.routes.Routes`

```python
class Routes:
    class Production:
        BASE = "/api/Production"
        UNIT = f"{BASE}/Unit"
        VERIFICATION = f"{BASE}/Verification"
        
        @staticmethod
        def unit_detail(sn, pn):
            return f"{Routes.Production.UNIT}/{sn}/{pn}"
```

**Current Implementation**: Routes class has 170 endpoints across 9 domains + App class.
Each domain has a nested `Internal` class for undocumented API endpoints.

### 3.2 Duck Typing in Repositories
Repositories currently "guess" success based on whether the data is a `list` or `dict`.

**Fix:**
With the new **Error Handling Strategy**, this logic is deleted. If the HTTP client returns, the schema is guaranteed by Pydantic validation.
```python
# Explicit validation
try:
    return Unit.model_validate(data)
except ValidationError as e:
    raise DataContractError(f"API changed schema: {e}")
```
