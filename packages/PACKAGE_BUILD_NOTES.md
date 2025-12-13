# Package Build Notes

## Package Separation Strategy

The pyWATS codebase is organized into 4 separate packages, all built from the same source tree:

### Source Tree Structure
```
src/
├── pyWATS/              # Core API library
│   └── (all API code)
└── pywats_client/       # Client code
    ├── core/            # Client core (included in all client packages)
    ├── services/        # Services (included in all client packages)
    ├── converters/      # Converters (included in all client packages)
    ├── gui/             # GUI code (only in GUI package)
    └── control/         # CLI/API code (only in headless package)
```

### Package Inclusion/Exclusion

#### pywats (Core API)
- **Includes**: `src/pyWATS/*`
- **Excludes**: Everything else
- **Note**: Standalone package, no client code

#### pywats-client-service (Client Framework)
- **Includes**: `src/pywats_client/*` (core, services, converters, app.py)
- **Excludes**: `pywats_client.gui.*`, `pywats_client.control.*`
- **Note**: Base package for both headless and GUI clients

#### pywats-client-headless (Headless Client)
- **Includes**: `src/pywats_client/*` (everything except GUI)
- **Excludes**: `pywats_client.gui.*`
- **Note**: Includes control module for CLI/HTTP API

#### pywats-client-gui (GUI Client)
- **Includes**: `src/pywats_client/*` (everything)
- **Excludes**: Nothing
- **Note**: Full client including GUI components

## Build Process

All packages are built from the `packages/*/` directories using:
```bash
cd packages/pywats
python -m build
```

The `pyproject.toml` in each package directory:
1. Points to the shared source tree: `where = ["../../src"]`
2. Uses include/exclude patterns to select appropriate modules
3. References the shared LICENSE file: `license = {file = "../../LICENSE"}`

## Important Considerations

### 1. No Source Code Duplication
- Source code lives only in `src/`
- Packages reference the same source tree
- Include/exclude patterns control what goes in each package

### 2. License File
- Single LICENSE file at repository root
- All packages reference it with relative paths
- Setuptools resolves paths correctly during build

### 3. Package Dependencies
- pywats-client-service depends on pywats
- pywats-client-headless depends on pywats + pywats-client-service
- pywats-client-gui depends on pywats + pywats-client-service
- Circular dependencies are avoided

### 4. MANIFEST.in Files
- Each package has its own MANIFEST.in
- Controls additional files (README, CHANGELOG, docs)
- Excludes __pycache__ and .pyc files

## Avoiding Package Conflicts

### Problem
If include/exclude patterns are wrong, packages might:
- Include wrong modules
- Conflict with each other when installed together
- Have missing dependencies

### Solution
Carefully designed patterns ensure:
- No overlap between packages (except base dependencies)
- Each package is self-contained for its purpose
- Proper dependency chain (pywats → client-service → headless/GUI)

## Testing Package Separation

### Test 1: Install Core Only
```bash
pip install packages/pywats/dist/*.whl
python -c "import pywats; from pywats_client import core"  # Should FAIL
```

### Test 2: Install Headless (Should Include Service)
```bash
pip install packages/pywats-client-headless/dist/*.whl
python -c "from pywats_client.control import cli"  # Should work
python -c "from pywats_client.gui import app"  # Should FAIL
```

### Test 3: Install GUI (Should Include Everything)
```bash
pip install packages/pywats-client-gui/dist/*.whl
python -c "from pywats_client.gui import app"  # Should work
python -c "from pywats_client.control import cli"  # Should work
```

## Build Directory Structure

After building, each package directory will have:
```
packages/pywats/
├── build/           # Build artifacts (gitignored)
├── dist/            # Distribution files (gitignored)
│   ├── pywats-2.0.0-py3-none-any.whl
│   └── pywats-2.0.0.tar.gz
├── *.egg-info/      # Egg metadata (gitignored)
├── pyproject.toml   # Package configuration
├── README.md        # Package documentation
├── CHANGELOG.md     # Version history
└── MANIFEST.in      # Distribution manifest
```

## Common Issues and Solutions

### Issue: "Module not found" after installation
**Cause**: Include/exclude patterns are wrong  
**Solution**: Check pyproject.toml patterns, rebuild

### Issue: Package too large
**Cause**: Including too much or not excluding properly  
**Solution**: Check MANIFEST.in and pyproject.toml excludes

### Issue: Missing dependencies
**Cause**: Dependencies not specified in pyproject.toml  
**Solution**: Add to dependencies list

### Issue: LICENSE file not included
**Cause**: Path resolution or MANIFEST.in issue  
**Solution**: Verify LICENSE path and MANIFEST.in includes

## Version Synchronization

All 4 packages should use the same version number:
- Makes it clear which versions work together
- Simplifies dependency management
- Reduces confusion for users

Example: Version 2.0.0
- pywats 2.0.0
- pywats-client-service 2.0.0
- pywats-client-headless 2.0.0
- pywats-client-gui 2.0.0

## Build Script

The build script (`scripts/build_all_packages.sh`) handles:
1. Cleaning old build artifacts
2. Building all packages in dependency order
3. Verifying builds succeeded
4. Showing summary of built packages

Run it from repository root:
```bash
bash scripts/build_all_packages.sh
```
