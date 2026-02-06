# Documentation Improvement Initiatives

**Date:** February 1, 2026  
**Status:** Planned (postponed from active)  
**Estimated Effort:** 2-4 weeks  

---

## Overview

Two major documentation improvement initiatives have been analyzed and are ready for implementation when prioritized.

---

## Initiative 1: Sphinx Documentation Enhancement

### Goal
Make Sphinx-generated API documentation comprehensive with domain knowledge, practical examples, and best practices.

### Current State
- Basic auto-generated docstrings only
- Missing domain context and use cases
- No integration of rich content from `docs/domains/` and `docs/usage/`

### Progress
- ✅ **Analytics domain complete** (~480 lines, comprehensive)
- 📋 **8 domains remaining**

### Remaining Work

**Priority 1: Core Data Domains** (~5-8 hours)
- Report domain (~600 lines) - UUT/UUR reports, step types, factory methods
- Product domain (~450 lines) - Products, revisions, BOMs, box build
- Production domain (~500 lines) - Serial numbers, assembly, verification

**Priority 2: Analysis Domains** (~8 hours)
- Asset domain (~400 lines)
- Software domain (~350 lines)
- RootCause domain (~450 lines)
- Process domain (~300 lines)

**Priority 3: Admin** (~2 hours)
- SCIM domain (~250 lines)

### Approach
Each enhanced domain RST includes:
1. Domain overview and use cases
2. Quick start examples (3-4 practical scenarios)
3. Core concepts explained
4. Common use cases with code (4-6 patterns)
5. Advanced features
6. Auto-generated API reference
7. Model documentation
8. Best practices (5-7 tips)
9. Cross-links to related docs
10. Domain health score and status

### Source Material
- `docs/domains/{domain}.md` - API reference
- `docs/usage/{domain}-domain.md` - Usage guides
- `docs/domain_health/{domain}.md` - Health assessments
- `examples/{domain}/` - Working examples

---

## Initiative 2: Documentation Structure Consolidation

### Goal
Reduce maintenance burden by eliminating duplication and streamlining documentation structure.

### Current Issues Identified

**1. Duplication** (3x maintenance burden)
- `domains/*.md` - API reference (11 files)
- `usage/*-domain.md` - Detailed guides (9 files)  
- `api/domains/*.rst` - Sphinx-generated (duplicate)
- Same information maintained in 3 places

**2. Overlapping Guides**
- Multiple architecture files (architecture.md, client-architecture.md, component-architecture.md)
- Thread safety, security, IPC spread across files
- Unclear which file to check

**3. Installation Guides** (8 separate files)
- Windows, Linux, macOS, Docker, Package Manager, Development, Virtual Environment, Troubleshooting
- Could be consolidated into 1 file with platform tabs

**4. Entry Point Confusion**
- INDEX.md vs README.md vs getting-started.md
- Multiple "starting points"

### Recommendations

**Quick Wins** (High impact, low effort)
1. ✅ Gitignore `api/_build/` - ALREADY DONE
2. Delete `domains/*.md` (Sphinx has these)
3. Consolidate 8 installation guides → 1 file with tabs
4. Merge overlapping guides

**Medium Effort**
1. Move examples from usage/*.md to runnable code in `examples/`
2. Improve docstrings for better auto-generation
3. Set up auto-deploy to Read the Docs

**Strategic Considerations**
1. Consider migrating to MkDocs Material (simpler, modern)
2. Add interactive API explorer
3. Implement versioned documentation

### Success Metrics
| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Source files | ~80 | ~25 | 70% reduction |
| Duplication | ~30 instances | 0 | 100% elimination |
| Auto-gen vs manual | 20/80 | 70/30 | Focus on generation |
| Time to first API call | ~15 min | 5 min | 3x faster |
| Maintenance time | ~2h/week | ~30min/week | 75% reduction |

---

## Implementation Strategy

### Phase 1: Continue Sphinx Enhancement
- Complete remaining 8 domains
- Establishes comprehensive baseline

### Phase 2: Consolidate Structure  
- Merge installation guides
- Remove duplicates
- Streamline entry points

### Phase 3: Optimize for Maintenance
- Auto-generate from code
- Single source of truth for examples
- Deploy automation

---

## When to Resume

**Prerequisites:**
- Current development work stabilized
- Time available for focused documentation work
- Decision on MkDocs vs Sphinx long-term

**Best Time:**
- Between major feature releases
- During documentation sprint
- When onboarding new contributors

---

## References

Original analysis documents:
- `active/SPHINX_DOCUMENTATION_ENHANCEMENT_PLAN.md`
- `active/DOCUMENTATION_AUDIT_2026.md`

Related:
- `completed/CSHARP_PYTHON_FEATURE_ALIGNMENT.md` - Feature parity achieved
