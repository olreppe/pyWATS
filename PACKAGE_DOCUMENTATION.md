# PyWATS Package Documentation Structure

This document describes what documentation is included in the PyPI package vs what stays in the repository.

## Included in PyPI Package

### Official Documentation
**Location**: `docs/`

The following files are included in every pip install:

- `docs/INDEX.md` - Documentation index and navigation
- `docs/PRODUCT.md` - Product domain API reference  
- `docs/ASSET.md` - Asset domain API reference
- `docs/PRODUCTION.md` - Production domain API reference
- `docs/REPORT.md` - Report domain API reference
- `docs/ANALYTICS.md` - Analytics domain API reference
- `docs/SOFTWARE.md` - Software domain API reference
- `docs/ROOTCAUSE.md` - RootCause domain API reference
- `docs/PROCESS.md` - Process domain API reference

### Client Documentation
**Location**: `src/pywats_client/`

User-facing client documentation:

- `src/pywats_client/GUI_CONFIGURATION.md` - GUI configuration guide
- `src/pywats_client/control/HEADLESS_GUIDE.md` - Headless operation guide

### Examples
**Location**: `examples/`

Practical code examples for all domains:

- `examples/README.md` - Examples overview
- `examples/getting_started/` - Basic setup and connection
- `examples/product/` - Product management examples
- `examples/asset/` - Asset management examples
- `examples/production/` - Production tracking examples
- `examples/report/` - Test report examples
- `examples/analytics/` - Analytics and yield examples
- `examples/software/` - Software package examples
- `examples/rootcause/` - Ticket management examples
- `examples/process/` - Process operation examples

### Root Files
Always included:

- `README.md` - Package overview and quick start
- `CHANGELOG.md` - Version history
- `LICENSE` - MIT license

## Excluded from PyPI Package

### Internal Documentation
**Location**: `docs/` (excluded)

Development and internal documentation:

- `docs/ARCHITECTURE.md` - Internal architecture details
- `docs/WATS_DOMAIN_KNOWLEDGE.md` - Domain knowledge for AI agents
- `docs/CONNECTION_ARCHITECTURE.md` - Connection layer details
- `docs/CONVERTER_ARCHITECTURE.md` - Converter system design
- `docs/STATION_ARCHITECTURE.md` - Station implementation
- `docs/STEP_GRAPH_MODEL.md` - Step graph data model
- `docs/REST_API_INSTRUCTION.md` - Internal API instructions
- `docs/FRONTEND_COPILOT_MIGRATION.md` - Migration notes
- `docs/README.md` - Internal documentation index
- `docs/archive/` - Archived working notes
- `docs/api_specs/` - OpenAPI specifications
- `docs/examples/` - Internal example code
- `docs/usage/` - Legacy usage guides
- `docs/DOMAIN_STATUS/` - Development status tracking

### Internal Client Documentation
**Location**: `src/pywats_client/` (excluded)

- `src/pywats_client/GUI_REDESIGN.md` - Internal redesign notes

### Root-Level Internal Docs
Development and release documentation:

- `RELEASE.md` - Release process (internal)
- `RELEASE_CHECKLIST.md` - Release checklist
- `QUICK_REFERENCE.md` - Developer quick reference
- `ENVIRONMENT_SETUP_GUIDE.md` - Development setup
- `DIALOG_BUGS_FIXED.md` - Bug tracking
- `PYPI_INSTALLATION.md` - PyPI publishing instructions

### Development Folders
**Excluded entirely:**

- `tests/` - Unit tests
- `api-tests/` - Integration tests
- `scripts/` - Development scripts
- `converters/` - User converter templates (available in GitHub)
- `.github/` - GitHub workflows and actions
- `packages/` - Separate packages (pywats-langchain, etc.)

## Rationale

### What Users Need (Included)

Users who `pip install pywats-api` need:

1. **Domain API Documentation** - How to use each domain
2. **Client Guides** - How to configure and run the client
3. **Examples** - Working code they can copy/modify
4. **README/CHANGELOG** - Package info and version history

### What Users Don't Need (Excluded)

Internal documentation that only benefits:

- **Developers** contributing to pyWATS
- **AI Agents** with repository access (WATS_DOMAIN_KNOWLEDGE.md)
- **Maintainers** releasing versions
- **Architects** understanding internal design

This separation keeps the pip package clean while maintaining full documentation in the GitHub repository.

## Verification

To verify what's included in a build:

```powershell
# Build source distribution
python -m build --sdist

# Extract and examine
tar -tzf dist/pywats-api-*.tar.gz | Select-String "\.md$"
```

Expected markdown files in distribution:
```
pywats-api-0.1.0b24/README.md
pywats-api-0.1.0b24/CHANGELOG.md
pywats-api-0.1.0b24/docs/INDEX.md
pywats-api-0.1.0b24/docs/PRODUCT.md
pywats-api-0.1.0b24/docs/ASSET.md
pywats-api-0.1.0b24/docs/PRODUCTION.md
pywats-api-0.1.0b24/docs/REPORT.md
pywats-api-0.1.0b24/docs/ANALYTICS.md
pywats-api-0.1.0b24/docs/SOFTWARE.md
pywats-api-0.1.0b24/docs/ROOTCAUSE.md
pywats-api-0.1.0b24/docs/PROCESS.md
pywats-api-0.1.0b24/src/pywats_client/GUI_CONFIGURATION.md
pywats-api-0.1.0b24/src/pywats_client/control/HEADLESS_GUIDE.md
pywats-api-0.1.0b24/examples/README.md
pywats-api-0.1.0b24/examples/**/*.md
```

## Configuration Files

The packaging is controlled by:

- **`MANIFEST.in`** - Explicitly includes/excludes files from source distribution
- **`pyproject.toml`** - Package metadata and build configuration

Both files are kept in sync to ensure consistent packaging.
