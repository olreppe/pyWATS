# Archived Documentation (docs/old/)

This folder contains documentation that was consolidated or replaced during the February 2026 documentation reorganization.

## What's Here

### domains/ (11 files)
Old markdown files documenting WATS domains. These have been **replaced by runnable examples** in `examples/domains/`:

**Replaced by:**
- `examples/domains/report_examples.py` - Report domain
- `examples/domains/product_examples.py` - Product domain
- `examples/domains/production_examples.py` - Production domain
- `examples/domains/analytics_examples.py` - Analytics domain
- `examples/domains/software_examples.py` - Software domain
- `examples/domains/rootcause_examples.py` - Root cause domain
- `examples/domains/process_examples.py` - Process domain
- `examples/domains/asset_examples.py` - Asset domain
- `examples/domains/box_build_examples.py` - Box build domain

**Why replaced:**
- Static markdown → Runnable code with inline domain knowledge
- Easier to maintain (code must work to run)
- Better for learning (see actual usage patterns)
- Self-documenting (comments explain concepts)

### installation/ (8 files)
Old installation guides for different platforms/modes. These have been **consolidated into one comprehensive guide**.

**Replaced by:**
- `docs/guides/installation.md` (~1,900 lines covering all scenarios)

**Files consolidated:**
- API installation guides
- Client installation guides
- GUI installation guides
- Docker deployment guides
- Service installation guides
- Platform-specific guides

**Why consolidated:**
- Single source of truth
- No duplication of common steps
- Easier to keep consistent
- Better navigation with table of contents

### usage/ (9 files)
Old usage guides and patterns. These have been **replaced by runnable examples and consolidated guides**.

**Replaced by:**
- `examples/domains/*.py` - Domain-specific examples
- `docs/guides/integration-patterns.md` - Integration patterns
- `docs/guides/wats-concepts.md` - Core concepts

**Why replaced:**
- Runnable examples > static descriptions
- Domain knowledge in code comments
- Practical, copy-paste ready examples

## Should You Use These Files?

**No** - Use the new consolidated documentation:

1. **For domain knowledge**: See `examples/domains/` (runnable code)
2. **For installation**: See `docs/guides/installation.md` (all platforms)
3. **For usage patterns**: See `docs/guides/integration-patterns.md` (workflows)
4. **For API reference**: See `docs/api/` (auto-generated)

## Why Keep Them?

These files are kept for:
- **Safety**: Easy to verify nothing important was lost
- **Reference**: Check if old docs had unique info
- **Transition**: Help during the adjustment period

## When to Delete

After you've verified the new documentation covers everything you need, you can delete this entire `docs/old/` folder.

## Comparison

**Old approach:**
- 28 separate markdown files
- Domain docs separate from code
- Installation split across 8 files
- Usage examples in markdown

**New approach:**
- 9 runnable example files (3,585 lines)
- Domain knowledge inline with code
- 1 comprehensive installation guide
- Working code examples you can run

**Result:** 70% fewer files, higher quality, easier to maintain
