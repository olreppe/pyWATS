# Sphinx Documentation Enhancement Plan

**Date:** February 1, 2026  
**Goal:** Make Sphinx-generated documentation comprehensive with domain knowledge and usage examples

---

## Problem Statement

Current Sphinx documentation (`docs/api/`) is bare-bones - it only auto-generates from docstrings without:
- Domain context (what is WATS, why use analytics, etc.)
- Practical usage examples
- Common patterns and use cases
- Best practices
- Links to health assessments

The rich content exists in `docs/domains/` and `docs/usage/` but isn't integrated into Sphinx output.

---

## Solution Implemented

### Analytics Domain (✅ Complete)

Created comprehensive `docs/api/domains/analytics.rst` with:

1. **Domain Overview** - What analytics does, use cases, health score
2. **Quick Start** - 3 practical examples (yield, measurements, async)
3. **Core Concepts** - Type-safe enums, WATSFilter, MeasurementPath
4. **Common Use Cases** - 4 real-world patterns:
   - Dashboard creation
   - Trend analysis
   - Process comparison
   - Failure analysis
5. **Advanced Features** - Dynamic yield, OEE, Unit Flow
6. **API Reference** - Auto-generated from docstrings
7. **Models** - Key data models documented
8. **Best Practices** - 5 actionable recommendations
9. **Related Documentation** - Cross-links to other guides
10. **Domain Health** - Link to health assessment

**Result:** ~480 lines of comprehensive documentation vs. previous 30 lines

---

## Domains Needing Enhancement

### Priority 1: Core Data Domains (High Usage)

| Domain | Current Lines | Target Lines | Priority | Status |
|--------|---------------|--------------|----------|--------|
| Analytics | 30 → 480 | ✅ Complete | High | ✅ DONE |
| Report | ~35 | ~600 | High | 📋 Ready |
| Product | ~35 | ~450 | High | 📋 Ready |
| Production | ~35 | ~500 | High | 📋 Ready |

### Priority 2: Analysis & Tracking Domains

| Domain | Current Lines | Target Lines | Priority | Status |
|--------|---------------|--------------|----------|--------|
| Asset | ~35 | ~400 | Medium | 📋 Ready |
| Software | ~35 | ~350 | Medium | 📋 Ready |
| RootCause | ~35 | ~450 | Medium | 📋 Ready |
| Process | ~35 | ~300 | Medium | 📋 Ready |

### Priority 3: Identity & Admin

| Domain | Current Lines | Target Lines | Priority | Status |
|--------|---------------|--------------|----------|--------|
| SCIM | ~30 | ~250 | Low | 📋 Ready |

---

## Template Structure

Each enhanced domain RST file should include:

```restructuredtext
Domain Name
===========

[Overview paragraph - what it does]

**Use Cases:**
- Bullet list of real-world uses

**Domain Health:** [Score] ([Grade]) - [Status]

---

Quick Start
-----------

[3-4 practical examples]

---

Core Concepts
-------------

[Key types, enums, objects explained]

---

Common Use Cases
----------------

[4-6 real-world patterns with code]

---

Advanced Features
-----------------

[Complex scenarios]

---

API Reference
-------------

.. autoclass:: ...

Models
------

.. autoclass:: ...

Best Practices
--------------

[5-7 actionable tips]

---

Related Documentation
---------------------

[Cross-links]

---

Domain Health
-------------

[Score, link to health doc, recent improvements]
```

---

## Source Material for Each Domain

Content should be extracted from:

1. **`docs/domains/{domain}.md`** - API reference with quick starts
2. **`docs/usage/{domain}-domain.md`** - Detailed usage guides with patterns
3. **`docs/domain_health/{domain}.md`** - Health scores and assessments
4. **`examples/{domain}/`** - Working code examples

---

## Implementation Approach

### Option 1: Manual Enhancement (Recommended)
- Create comprehensive RST files like analytics.rst
- **Pros:** Full control, best quality
- **Cons:** Time-consuming (~2-4 hours per domain)
- **Effort:** ~24 hours total for all 9 domains

### Option 2: Automated Generation
- Script to convert markdown → RST with enhancements
- **Pros:** Faster, consistent structure
- **Cons:** Requires validation, may miss nuances
- **Effort:** ~8 hours (script) + ~12 hours (review/fixes) = 20 hours

### Option 3: Hybrid Approach (Fastest)
- Use existing markdown as basis
- Add RST-specific enhancements (code blocks, cross-refs)
- **Pros:** Balances speed and quality
- **Cons:** Still requires manual work
- **Effort:** ~16 hours

---

## Next Steps

### Immediate (Priority 1 Domains)

1. **Report Domain** (2-3 hours)
   - Source: docs/domains/report.md (888 lines), docs/usage/report-domain.md (1100+ lines)
   - Focus: UUT/UUR reports, step types, factory methods, query patterns

2. **Product Domain** (2 hours)
   - Source: docs/domains/product.md, docs/usage/product-domain.md
   - Focus: Products, revisions, BOMs, box build templates

3. **Production Domain** (2-3 hours)
   - Source: docs/domains/production.md, docs/usage/production-domain.md
   - Focus: Serial numbers, assembly, unit verification, phases

### Medium Term (Priority 2)

4-7. Asset, Software, RootCause, Process (6-8 hours total)

### Low Priority (Priority 3)

8-9. SCIM (1-2 hours)

---

## Sphinx Configuration Updates

Current `docs/api/conf.py` is well-configured with:
- ✅ Napoleon for Google/NumPy docstrings
- ✅ MyST parser for Markdown support
- ✅ Autodoc with good defaults
- ✅ Intersphinx for Python/httpx/pydantic refs

**No configuration changes needed** - enhancements are content-only.

---

## Validation

After enhancing each domain:

1. **Build Sphinx HTML:**
   ```bash
   cd docs/api
   make html
   # or
   sphinx-build -b html . _build/html
   ```

2. **Check for:**
   - ✅ All code blocks render correctly
   - ✅ Cross-references work
   - ✅ Auto-generated API docs appear
   - ✅ No Sphinx warnings/errors

3. **Compare to markdown:**
   - Content parity with docs/domains/{domain}.md
   - Includes key examples from docs/usage/{domain}-domain.md

---

## Benefits

**For Users:**
- Single comprehensive documentation source (Sphinx HTML)
- Rich examples and patterns in generated docs
- Better discoverability of features
- Cross-referenced navigation

**For Developers:**
- Documentation maintenance in single location
- Sphinx auto-updates from docstrings
- Professional appearance for open-source project
- Easier onboarding for new contributors

---

## Progress Tracking

| Domain | Status | Date | Lines | Notes |
|--------|--------|------|-------|-------|
| Analytics | ✅ Complete | 2026-02-01 | 480 | Full enhancement with all sections |
| Report | 📋 Ready | - | - | High priority - core domain |
| Product | 📋 Ready | - | - | High priority - core domain |
| Production | 📋 Ready | - | - | High priority - core domain |
| Asset | 📋 Ready | - | - | Medium priority |
| Software | 📋 Ready | - | - | Medium priority |
| RootCause | 📋 Ready | - | - | Medium priority |
| Process | 📋 Ready | - | - | Medium priority |
| SCIM | 📋 Ready | - | - | Low priority |

---

## Related Documents

- [Analytics Enhanced RST](../api/domains/analytics.rst) - Example implementation
- [Domain Health](../domain_health/README.md) - Health scores for all domains
- [Domain Guides](../domains/README.md) - Concise API references
- [Usage Guides](../usage/) - Detailed patterns and examples
- [Sphinx Config](../api/conf.py) - Current configuration

---

**Created:** February 1, 2026  
**Next Action:** Enhance Report domain (Priority 1)
