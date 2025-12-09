# pyWATS Refactoring Plan

## Overview

This document outlines the refactoring strategy to separate business logic from data models in pyWATS by implementing a service/repository layer pattern.

## Goals

1. **Separation of Concerns**: Split models (data), services (business logic), and repositories (data access)
2. **Better Organization**: Group related code by domain (asset, report, product, etc.)
3. **Improved Testability**: Enable easy mocking of repositories for unit testing
4. **Maintainability**: Shorter, focused files instead of large mixed-concern files

---

## Current Structure

```
src/pywats/
├── models/
│   ├── asset.py          # Mixed: data models + some logic
│   ├── product.py
│   ├── report_query.py
│   └── report/           # Complex nested structure
├── modules/
│   ├── asset.py          # API calls + business logic mixed
│   ├── product.py
│   ├── report.py
│   └── ...
└── pywats.py
```

---

## Proposed Structure

```
src/pywats/
├── core/
│   ├── __init__.py
│   ├── client.py              # HTTP client, auth, base requests
│   └── exceptions.py          # Custom exceptions
│
├── domains/
│   ├── __init__.py
│   │
│   ├── asset/
│   │   ├── __init__.py
│   │   ├── models.py          # Pure data models (Asset, AssetType, AssetLog)
│   │   ├── enums.py           # AssetState, AssetLogType
│   │   ├── service.py         # Business logic (validation, transformations)
│   │   └── repository.py      # API calls (CRUD operations)
│   │
│   ├── product/
│   │   ├── __init__.py
│   │   ├── models.py          # Product, ProductInfo
│   │   ├── service.py
│   │   └── repository.py
│   │
│   ├── report/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # Report, ReportInfo
│   │   │   ├── uut.py         # UUTReport, UUTInfo
│   │   │   ├── uur.py         # UURReport, UURInfo
│   │   │   └── steps/         # Step types (keep existing structure)
│   │   ├── enums.py           # ReportType, Purpose, etc.
│   │   ├── service.py         # Report creation, validation
│   │   ├── repository.py      # Submit, query reports
│   │   └── builder.py         # Factory methods (moved from models)
│   │
│   ├── query/
│   │   ├── __init__.py
│   │   ├── models.py          # WATSFilter, DateGrouping
│   │   ├── service.py         # Query building logic
│   │   └── repository.py
│   │
│   └── production/
│       ├── __init__.py
│       ├── models.py
│       ├── service.py
│       └── repository.py
│
├── shared/
│   ├── __init__.py
│   ├── base_model.py          # PyWATSModel, WATSBase
│   ├── common_types.py        # Shared types, Setting
│   └── validators.py          # Reusable validators
│
└── pywats.py                  # Main entry point (facade)
```

---

## Layer Responsibilities

### 1. Models (Pure Data)

- Pydantic models with field definitions only
- Validation via Pydantic Field constraints
- No business methods
- No API calls

```python
# Example: domains/asset/models.py
class Asset(PyWATSModel):
    """Asset data model - validation only, no methods"""
    serial_number: str = Field(..., alias="serialNumber")
    asset_name: Optional[str] = Field(default=None, alias="assetName")
    state: AssetState = Field(default=AssetState.OK)
    # ... fields only, no business methods
```

### 2. Service (Business Logic)

- Validation beyond Pydantic
- Data transformations
- Business rules
- Orchestration of repository calls

```python
# Example: domains/asset/service.py
class AssetService:
    def __init__(self, repository: AssetRepository):
        self._repo = repository
    
    def create_asset(self, serial_number: str, type_id: str, **kwargs) -> Asset:
        """Create and validate a new asset"""
        asset = Asset(serial_number=serial_number, type_id=type_id, **kwargs)
        return self._repo.save(asset)
    
    def get_assets_needing_maintenance(self) -> List[Asset]:
        """Get all assets that need maintenance"""
        assets = self._repo.get_all()
        return [a for a in assets if a.state == AssetState.NEEDS_MAINTENANCE]
```

### 3. Repository (Data Access)

- HTTP API calls
- Response parsing
- Error handling for API errors
- No business logic

```python
# Example: domains/asset/repository.py
class AssetRepository:
    def __init__(self, client: WATSClient):
        self._client = client
    
    def get_by_serial(self, serial_number: str) -> Optional[Asset]:
        response = self._client.get(f"/asset/{serial_number}")
        return Asset.model_validate(response) if response else None
    
    def save(self, asset: Asset) -> Asset:
        data = asset.model_dump(by_alias=True, exclude_none=True)
        response = self._client.post("/asset", json=data)
        return Asset.model_validate(response)
```

### 4. Core (Infrastructure)

- HTTP client with authentication
- Custom exceptions
- Logging configuration

### 5. Shared (Cross-cutting)

- Base model classes
- Common types used across domains
- Reusable validators

---

## Migration Phases

### Phase 1: Create Folder Structure
- [ ] Create `core/` directory with `__init__.py`
- [ ] Create `domains/` directory with subdirectories for each domain
- [ ] Create `shared/` directory

### Phase 2: Migrate Shared Components
- [ ] Move `PyWATSModel` and `WATSBase` to `shared/base_model.py`
- [ ] Move `Setting` and common types to `shared/common_types.py`
- [ ] Update imports throughout codebase

### Phase 3: Migrate Asset Domain (Reference Implementation)
- [ ] Create `domains/asset/enums.py` with `AssetState`, `AssetLogType`
- [ ] Create `domains/asset/models.py` with `Asset`, `AssetType`, `AssetLog`
- [ ] Create `domains/asset/repository.py` with API calls from `modules/asset.py`
- [ ] Create `domains/asset/service.py` with business logic
- [ ] Create `domains/asset/__init__.py` with clean exports
- [ ] Update tests

### Phase 4: Migrate Product Domain
- [ ] Create `domains/product/models.py`
- [ ] Create `domains/product/repository.py`
- [ ] Create `domains/product/service.py`
- [ ] Update tests

### Phase 5: Migrate Query Domain
- [ ] Create `domains/query/models.py` (WATSFilter, DateGrouping, etc.)
- [ ] Create `domains/query/service.py`
- [ ] Create `domains/query/repository.py`
- [ ] Update tests

### Phase 6: Migrate Report Domain
- [ ] Create `domains/report/models/` structure
- [ ] Create `domains/report/builder.py` (factory methods)
- [ ] Create `domains/report/repository.py`
- [ ] Create `domains/report/service.py`
- [ ] Update tests

### Phase 7: Migrate Remaining Domains
- [ ] Production
- [ ] Root cause
- [ ] Any other modules

### Phase 8: Create Core Layer
- [ ] Extract HTTP client to `core/client.py`
- [ ] Create `core/exceptions.py`
- [ ] Update `pywats.py` as facade

### Phase 9: Cleanup
- [ ] Remove old `models/` directory
- [ ] Remove old `modules/` directory
- [ ] Update all imports
- [ ] Update documentation
- [ ] Run full test suite

---

## Benefits Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Testing** | Hard to unit test | Easy to mock repositories |
| **Maintainability** | Mixed concerns | Clear separation |
| **Scalability** | Adding features = longer files | Each domain isolated |
| **Reusability** | Logic tied to API | Services reusable |
| **Onboarding** | Hard to find code | Predictable structure |

---

## Notes

- Keep backward compatibility during migration by maintaining old imports temporarily
- Each phase should result in passing tests before moving to next phase
- The report domain is most complex; save it for later phases
- Consider using abstract base classes for repositories to enable future database support
