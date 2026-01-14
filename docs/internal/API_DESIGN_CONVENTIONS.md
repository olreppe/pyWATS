# pyWATS API Design Conventions

## Unified API Access Pattern

All pyWATS functionality is accessed through a single, unified interface:

```python
api = pyWATS(url, username, password)

# All methods via domain accessor - no _internal suffix in access path
api.analytics.get_top_failed(...)
api.product.get_box_build_template(...)
api.asset.upload_blob(...)
api.production.get_all_unit_phases()
api.process.get_fail_codes(...)
```

**Key principle**: Users access ALL methods via `api.{domain}.{method}()` - there is 
NO `api.{domain}_internal` accessor.

---

## Code Organization: service.py vs service_internal.py

The separation is for **developer organization**, NOT user experience:

| File | Contains | Backend |
|------|----------|---------|
| `repository.py` | Public API endpoints | `/api/...` |
| `repository_internal.py` | Internal API endpoints | `/api/internal/...` |
| `service.py` | All public methods + wrapper methods | Both |
| `service_internal.py` | Implementation of internal endpoint logic | Internal only |

### Why This Matters

Methods in `service_internal.py` use **undocumented WATS backend endpoints** that may 
change without notice. By keeping them in separate files:

1. **Tracking**: Easy to identify which methods rely on internal endpoints
2. **Migration**: When an endpoint becomes public, move code from `*_internal.py` to main files
3. **User Experience**: Users see ONE unified API regardless of backend implementation

---

## Identifying Internal API Methods

Methods that use internal endpoints are marked in their docstrings:

```python
def get_box_build_template(self, part_number: str, revision: str) -> BoxBuildTemplate:
    """
    Get or create a box build template for a product revision.
    
    ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
    
    ...
    """
```

The `⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️` warning indicates:
- Method uses undocumented backend endpoint
- May change or break without notice
- Should be migrated when public endpoint available

---

## Service Layer Architecture

Each domain service follows this pattern:

```python
class ProductService:
    def __init__(
        self, 
        repository: ProductRepository,
        internal_service: Optional["ProductServiceInternal"] = None
    ):
        self._repository = repository
        self._internal = internal_service
    
    # === Public API Methods ===
    # These use repository.py (public endpoints)
    
    def get_products(self) -> List[ProductView]:
        return self._repository.get_all()
    
    # === Extended Methods (from internal service) ===
    # ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
    
    def _ensure_internal(self) -> "ProductServiceInternal":
        if self._internal is None:
            raise RuntimeError("Internal methods not available")
        return self._internal
    
    def get_box_build_template(self, part_number: str, revision: str):
        """
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        """
        return self._ensure_internal().get_box_build(part_number, revision)
```

---

## Migration Process

When a WATS backend endpoint becomes public:

1. **Move repository method** from `repository_internal.py` to `repository.py`
2. **Move service method** from `service_internal.py` to `service.py`
3. **Remove wrapper** from main service (the method is now direct)
4. **Remove warning** from docstring
5. **Update tests** if endpoint behavior changed

The user-facing API (`api.domain.method()`) remains unchanged.

---

## Current Internal Methods by Domain

### Analytics
- `get_unit_flow()` - Unit flow analysis
- `get_measurement_list()` - Detailed measurements with filters
- `get_step_status_list()` - Step status breakdown
- `get_top_failed_internal()` - Extended TopFailed with POST

### Product
- `get_box_build_template()` - Box build template management
- `get_box_build_subunits()` - Read-only subunit list
- `get_product_categories()` - Product category management
- `save_product_categories()` - Save categories

### Asset
- `upload_blob()` - Upload file to blob storage
- `download_blob()` - Download file from blob storage
- `list_blobs()` - List files in blob storage
- `delete_blobs()` - Delete files from blob storage
- `blob_exists()` - Check if file exists

### Production
- `get_all_unit_phases()` - Full phase details
- `get_phase_by_name()` - Lookup phase by name

### Process
- `get_all_processes()` - Full process details
- `get_process_by_id()` - Lookup by GUID
- `get_all_test_operations()` - Test operations with details
- `get_all_repair_processes()` - Repair processes with details
- `get_process_by_code()` - Lookup by code
- `get_repair_operation_configs()` - Repair configurations
- `get_repair_categories()` - Fail code categories
- `get_fail_codes()` - Flattened fail codes

---

## Summary

| Aspect | Pattern |
|--------|---------|
| User Access | `api.domain.method()` - always |
| Internal Suffix | NO `_internal` in method names or accessors |
| File Organization | `*_internal.py` files for internal code |
| Documentation | `⚠️ INTERNAL API` warning in docstrings |
| Migration | Move code when endpoint becomes public |
