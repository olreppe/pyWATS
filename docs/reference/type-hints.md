# Type Hints & IDE Support

**Why this matters:** Get full autocomplete and type checking in your IDE when using pyWATS.

---

## TL;DR

✅ pyWATS includes type stub files (`.pyi`) for **full IDE autocomplete**  
✅ Works out-of-the-box with VS Code, PyCharm, and other modern Python IDEs  
✅ If autocomplete isn't working → [Troubleshooting](#troubleshooting)

---

## What You Get

```python
from pywats import pyWATS

api = pyWATS(base_url="https://your-server.com", api_key="...")

# ✅ Full autocomplete as you type!
headers = api.report.get_headers_by_serial("SN123")
#            ↑ IDE suggests: report, product, asset, analytics, etc.

# ✅ Type checker knows the return type
for header in headers:  # Type: List[ReportHeader]
    print(header.serial_number)  # ✅ Autocomplete for all fields
    print(header.result)          # ✅ Catches typos before running
```

---

## Why This Works

The **synchronous API** (`pyWATS`) uses a dynamic wrapper that prevents Python type checkers from seeing return types. To solve this, we include **type stub files** (`.pyi`) that tell your IDE exactly what types each method returns.

**AsyncWATS** has native type hints and doesn't need stubs:
```python
from pywats import AsyncWATS

async with AsyncWATS(base_url="...") as api:
    headers = await api.report.get_headers_by_serial("SN123")
    # ✅ Native type hints - perfect autocomplete!
```

---

## Troubleshooting

### VS Code not showing autocomplete?

**1. Reload VS Code window**
- Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
- Type "Developer: Reload Window"
- Press Enter

**2. Verify Pylance is installed**
- Open Extensions (`Ctrl+Shift+X`)
- Search for "Pylance"
- Install if not already installed
- Ensure it's enabled

**3. Check Python interpreter**
- Click Python version in bottom-left corner
- Select the interpreter where pyWATS is installed
- Should show your virtual environment

**4. Verify type stubs exist**

Type stubs are in your installed package:
```powershell
python -c "import pywats; print(pywats.__file__)"
# Should show path ending in: pywats/__init__.py
# Type stubs are in: pywats/pywats.pyi (same folder)
```

**5. Still not working?**

Check if stubs are included in your installation:
```python
from pathlib import Path
import pywats

package_dir = Path(pywats.__file__).parent
stub_file = package_dir / "pywats.pyi"

if stub_file.exists():
    print("✅ Type stubs found!")
else:
    print("❌ Type stubs missing - try reinstalling pyWATS")
```

If missing, reinstall pyWATS:
```bash
pip install --force-reinstall pywats
```

---

## PyCharm

PyCharm automatically uses type stubs. If autocomplete isn't working:

1. **Invalidate caches:**
   - File → Invalidate Caches...
   - Check "Clear file system cache and Local History"
   - Click "Invalidate and Restart"

2. **Check interpreter:**
   - File → Settings → Project → Python Interpreter
   - Ensure pyWATS is listed in packages

---

## Other IDEs

**mypy** (command-line type checker):
```bash
mypy your_script.py
# Automatically uses .pyi stub files
```

**Pyright** (Microsoft's type checker):
```bash
pyright your_script.py
# Automatically uses .pyi stub files
```

**Visual Studio**:
- Uses Pylance (same as VS Code)
- Same troubleshooting steps apply

---

## Technical Details

**What are type stubs?**
- Files ending in `.pyi` (Python Interface)
- Contain only type signatures, no implementation
- Standard Python approach (PEP 484)
- Used by IDEs and type checkers

**Why needed for sync API?**
- Sync API uses `__getattr__` for dynamic method wrapping
- Python type checkers can't infer through dynamic attributes
- Type stubs provide explicit signatures

**Coverage:**
- 9 domain services (report, product, asset, production, software, analytics, rootcause, scim, process)
- 256 methods with full type signatures
- All return types explicitly declared

---

## See Also

- [Quick Reference](quick-reference.md) - Common API patterns
- [Getting Started](../getting-started.md) - Installation and first steps
- [Error Catalog](error-catalog.md) - Common errors and solutions

---

**Note for Contributors:** If you're adding new methods to the async services, see `docs/internal_documentation/TYPE_STUBS.md` for how to regenerate stub files.
