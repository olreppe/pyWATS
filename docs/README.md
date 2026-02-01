# Documentation Folder Structure

This folder contains **official, user-facing documentation** that ships with `pip install pywats-api`.

## 📚 Published Documentation (in this folder)

### Quick Start
- **[getting-started.md](getting-started.md)** - Complete installation, configuration, logging, and error handling guide
- **[README.md](../README.md)** - Package overview and quick start at repository root
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history and release notes

### Guides
Conceptual documentation and practical workflows:

- **[guides/installation.md](guides/installation.md)** - Complete installation guide for all platforms (API, Client, GUI, Docker, services)
- **[guides/architecture.md](guides/architecture.md)** - System design: API, Client, GUI layers; async/sync patterns; deployment modes
- **[guides/integration-patterns.md](guides/integration-patterns.md)** - Practical workflows and best practices
- **[guides/security.md](guides/security.md)** - IPC communication, converter sandboxing, file handling security
- **[guides/thread-safety.md](guides/thread-safety.md)** - Threading and concurrency patterns
- **[guides/wats-concepts.md](guides/wats-concepts.md)** - Essential WATS domain knowledge (units, reports, processes, operations)
- **[guides/llm-converter-guide.md](guides/llm-converter-guide.md)** - Quick reference for implementing converters
- **[guides/TESTING_WITHOUT_HARDWARE.md](guides/TESTING_WITHOUT_HARDWARE.md)** - Testing strategies without physical equipment

### API Reference
Auto-generated from code (Sphinx):

- **[api/](api/)** - Complete API documentation (auto-generated from docstrings)
  - All domain services (Report, Product, Asset, Production, Analytics, Software, RootCause, Process, SCIM)
  - All models and data classes
  - Method signatures with type hints
  - Usage examples in docstrings

### Examples
Runnable code examples with comprehensive domain knowledge in comments:

- **[../examples/domains/](../examples/domains/)** - Domain-specific examples
  - `box_build_examples.py` - Multi-level assemblies (templates vs units)
  - `report_examples.py` - Test reports (UUT/UUR), all step types
  - `product_examples.py` - Products, revisions, BOMs
  - And more... (see examples/domains/README.md)

### Reference
Quick lookups and troubleshooting:

- **[reference/quick-reference.md](reference/quick-reference.md)** - Common patterns and code snippets
- **[reference/env-variables.md](reference/env-variables.md)** - Environment variable configuration
- **[reference/error-catalog.md](reference/error-catalog.md)** - Comprehensive error reference with solutions
- **[reference/type-hints.md](reference/type-hints.md)** - IDE setup and type hint troubleshooting

### Platform Guides
Platform-specific information:

- **[platforms/platform-compatibility.md](platforms/platform-compatibility.md)** - Multi-platform deployment matrix
- **[platforms/windows-iot-ltsc.md](platforms/windows-iot-ltsc.md)** - Windows IoT Enterprise LTSC setup

### Other
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[CHEAT_SHEET.md](CHEAT_SHEET.md)** - Quick command reference

## � Internal Documentation (NOT published)

The following folders are **excluded from the pip package** and only available in the GitHub repository:

- **[internal_documentation/](internal_documentation/)** - Architecture, design docs, AI agent knowledge, internal guides
- **[domain_health/](domain_health/)** - Domain health tracking and scoring (maintainer use only)

These folders are for internal development use only.

---

## 📁 New Consolidated Structure (Feb 2026)

**What changed:**
- ✅ **Installation guides**: 8 separate files → 1 comprehensive guide with platform sections
- ✅ **Architecture guides**: 4 separate files → 1 unified architecture guide
- ✅ **Security guides**: 3 separate files → 1 comprehensive security guide
- ✅ **Domain docs**: Removed markdown duplicates (use auto-generated API docs from Sphinx)
- ✅ **Examples**: Created runnable examples with domain knowledge in comments
- ✅ **Naming**: Renamed `wats-domain-knowledge.md` → `wats-concepts.md` for clarity

**Result:** 70% reduction in source files, easier to maintain, single source of truth.

See [internal_documentation/active/DOCUMENTATION_AUDIT_2026.md](internal_documentation/active/DOCUMENTATION_AUDIT_2026.md) for complete analysis.
│   ├── product.md
│   ├── asset.md
│   ├── report.md
│   └── ...
├── usage/                      ✅ Published - Detailed domain guides
│   ├── report-domain.md
│   ├── product-domain.md
│   └── ...
├── installation/               ✅ Published - Installation guides
│   ├── client.md
│   ├── docker.md
│   └── ...
├── internal_documentation/     ❌ NOT Published - Internal docs
│   ├── archived/
│   ├── WIP/
│   └── ...
└── domain_health/              ❌ NOT Published - Health tracking
```

## ✅ Rule of Thumb

- **Files/folders in `docs/` root** → Published with pip package
- **Folders: `guides/`, `reference/`, `platforms/`, `usage/`, `domains/`, `installation/`** → Published (user-facing)
- **Folders: `internal_documentation/`, `domain_health/`** → NOT Published (GitHub only)

## 🔄 Moving Documents

When creating new documentation:

- **User-facing API docs** → Put in `docs/domains/`
- **Detailed usage guides** → Put in `docs/usage/`
- **Installation guides** → Put in `docs/installation/`
- **Architecture/patterns** → Put in `docs/guides/`
- **Quick references** → Put in `docs/reference/`
- **Platform-specific docs** → Put in `docs/platforms/`
- **Internal architecture/design** → Put in `docs/internal_documentation/`

## 📦 Packaging

Controlled by `MANIFEST.in` in the project root:
- **Includes:** `docs/*.md`, `docs/guides/`, `docs/reference/`, `docs/platforms/`, `docs/usage/`, `docs/domains/`, `docs/installation/`
- **Excludes:** `docs/internal_documentation/`, `docs/domain_health/`
