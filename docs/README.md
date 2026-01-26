# Documentation Folder Structure

This folder contains **official, user-facing documentation** that ships with `pip install pywats-api`.

## 📚 Published Documentation (in this folder)

### Getting Started
- **[getting-started.md](getting-started.md)** - Complete installation, configuration, logging, and error handling guide

### Domain API Documentation
These files are included in the PyPI package:

- **[INDEX.md](INDEX.md)** - Documentation index and navigation
- **[modules/product.md](modules/product.md)** - Product domain API reference
- **[modules/asset.md](modules/asset.md)** - Asset domain API reference
- **[modules/production.md](modules/production.md)** - Production domain API reference
- **[modules/report.md](modules/report.md)** - Report domain API reference
- **[modules/analytics.md](modules/analytics.md)** - Analytics domain API reference
- **[modules/software.md](modules/software.md)** - Software domain API reference
- **[modules/rootcause.md](modules/rootcause.md)** - RootCause domain API reference
- **[modules/process.md](modules/process.md)** - Process domain API reference

### Module Usage Guides
Detailed guides with comprehensive examples:

- **[usage/](usage/)** - Detailed module guides (report-module.md, product-module.md, etc.)
  - Detailed usage patterns
  - Advanced examples
  - Factory method documentation

### Documentation Examples
Code snippets and examples embedded in documentation:

- **[examples/](examples/)** - Example code referenced in documentation
  - `basic_usage.py` - Getting started example

## 🔒 Internal Documentation (NOT published)

All internal documentation is in separate folders:

- **[internal_documentation/](internal_documentation/)** - Architecture, design docs, AI agent knowledge, internal guides

**These folders are excluded from the pip package.**

## 📁 Folder Structure

```
docs/
├── INDEX.md              ✅ Published - Documentation index
├── README.md             ✅ Published - This file
├── getting-started.md    ✅ Published - Getting started guide
├── architecture.md       ✅ Published - System architecture
├── error-catalog.md      ✅ Published - Error reference
├── modules/              ✅ Published - Domain API docs
│   ├── product.md
│   ├── asset.md
│   ├── report.md
│   └── ...
├── usage/                ✅ Published - Detailed module guides
│   ├── report-module.md
│   ├── product-module.md
│   └── ...
├── installation/         ✅ Published - Installation guides
│   ├── client.md
│   ├── docker.md
│   └── ...
├── internal_documentation/  ❌ NOT Published - Internal docs
│   ├── archived/
│   ├── WIP/
│   └── ...
└── domain_health/        ❌ NOT Published - Health tracking
```

## ✅ Rule of Thumb

- **Files/folders in `docs/` root** → Published with pip package
- **Folders: `usage/`, `modules/`, `installation/`** → Published (user-facing)
- **Folders: `internal_documentation/`, `domain_health/`** → NOT Published (GitHub only)

## 🔄 Moving Documents

When creating new documentation:

- **User-facing API docs** → Put in `docs/modules/`
- **Detailed usage guides** → Put in `docs/usage/`
- **Installation guides** → Put in `docs/installation/`
- **Internal architecture/design** → Put in `docs/internal_documentation/`

## 📦 Packaging

Controlled by `MANIFEST.in` in the project root:
- **Includes:** `docs/*.md`, `docs/usage/`, `docs/modules/`, `docs/installation/`
- **Excludes:** `docs/internal_documentation/`, `docs/domain_health/`
