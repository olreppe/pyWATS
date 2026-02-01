# Type Stub Generation for pyWATS

## Overview

The pyWATS library provides both asynchronous (`AsyncWATS`) and synchronous (`pyWATS`) APIs. The synchronous API uses a dynamic wrapper (`SyncServiceWrapper`) which prevents type checkers from inferring proper return types.

To solve this, we auto-generate **type stub files** (`.pyi`) that provide full type information for IDE autocomplete and type checking.

## What This Provides

✅ **Full autocomplete** in VS Code/PyCharm  
✅ **Type checking** with mypy/Pylance  
✅ **IDE hints** for method signatures and return types  
✅ **Refactoring safety** - catch errors before runtime

## How It Works

The stub generator (`scripts/generate_type_stubs.py`):
1. Parses all async service classes (e.g., `AsyncReportService`)
2. Extracts method signatures with full type annotations
3. Generates corresponding sync wrapper stubs (e.g., `SyncReportService`)
4. Creates a main `pywats.pyi` stub file

**Generated files:**
- `src/pywats/pywats.pyi` - Main API type stubs
- `src/pywats/domains/*/service.pyi` - Per-service type stubs (9 services, 256 methods)

## Usage

### For Developers

**When to regenerate stubs:**
- After adding/modifying methods in async services
- After changing method signatures or return types
- Before creating a release

**How to regenerate:**
```powershell
# Generate all stub files
python scripts/generate_type_stubs.py

# Generate with verbose output
python scripts/generate_type_stubs.py --verbose

# Check if stubs are up-to-date
python scripts/generate_type_stubs.py --check
```

### For Users

Stub files are included in the package distribution. Just install pyWATS and enjoy full type hints:

```python
from pywats import pyWATS

api = pyWATS(base_url="https://your-server.com", api_key="...")

# Full autocomplete! Type: List[ReportHeader]
headers = api.report.get_headers_by_serial("SN123")

# IDE knows all available fields
for header in headers:
    print(header.serial_number)  # ✅ Autocomplete works
    print(header.result)          # ✅ Type checking works
```

## CI/CD Integration

The pre-release check script validates that stubs are up-to-date:

```powershell
.\scripts\pre_release_check.ps1
```

This runs `generate_type_stubs.py --check` to ensure you haven't forgotten to regenerate stubs after modifying async services.

## Technical Details

**Why `.pyi` files?**
- Standard Python approach for type stubs
- Separate from implementation (no code duplication)
- Automatically used by type checkers (Pylance, mypy, Pyright)
- No runtime overhead (only used during static analysis)

**What gets generated?**

For each async method like:
```python
# In AsyncReportService
async def get_headers_by_serial(
    self, 
    serial_number: str, 
    report_type: Union[ReportType, str] = ReportType.UUT,
    top: Optional[int] = None
) -> List[ReportHeader]:
    ...
```

We generate:
```python
# In SyncReportService stub
def get_headers_by_serial(
    self,
    serial_number: str,
    report_type: Union[ReportType, str] = ReportType.UUT,
    top: Optional[int] = None
) -> List[ReportHeader]: ...
```

## Maintenance

✅ **Checked into git** - Other developers get type hints immediately  
✅ **Validated in CI** - Pre-release checks catch outdated stubs  
✅ **Zero runtime cost** - Stubs only used for static analysis  
✅ **Auto-generated** - No manual maintenance required

## Architecture

```
src/pywats/
├── pywats.py                           # Sync API implementation
├── pywats.pyi                          # ✨ Sync API type stubs
├── domains/
│   ├── report/
│   │   ├── async_service.py           # Source of truth for types
│   │   └── service.pyi                # ✨ Generated sync stubs
│   ├── product/
│   │   ├── async_service.py
│   │   └── service.pyi                # ✨ Generated sync stubs
│   └── ... (7 more services)

scripts/
└── generate_type_stubs.py             # Stub generator script
```

## Troubleshooting

**VS Code not showing autocomplete?**
1. Reload VS Code window: `Ctrl+Shift+P` → "Developer: Reload Window"
2. Check Pylance is installed and enabled
3. Verify `.pyi` files exist in `src/pywats/`

**"Type stubs are outdated" error in CI?**
```powershell
python scripts/generate_type_stubs.py
git add src/pywats/**/*.pyi
git commit -m "chore: regenerate type stubs"
```

**Want to see what changed?**
```powershell
python scripts/generate_type_stubs.py --verbose
```
