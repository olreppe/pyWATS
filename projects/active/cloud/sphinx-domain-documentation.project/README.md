# Sphinx Domain Documentation

**Project ID:** sphinx-domain-documentation  
**Sprint Size:** 2-3 weeks  
**Priority:** Medium  
**Status:** Ready to Start  

---

## 🎯 Goal

Complete Sphinx API documentation for all 8 remaining domains with rich examples, best practices, and cross-domain integration guides.

---

## 📋 Background

**Current State:**
- ✅ Analytics domain documentation complete (~480 lines)
- 📋 8 domains remaining with only basic auto-generated docstrings
- No integration of existing guides from `docs/domains/` and `docs/usage/`

**Why This Matters:**
- Users currently have fragmented documentation across multiple locations
- Auto-generated API docs lack context and examples
- Missing domain-specific best practices and common patterns

---

## ✅ Acceptance Criteria

**Must Have (Sprint Goal):**
- [ ] Complete Sphinx RST files for all 8 remaining domains
- [ ] Each domain includes: overview, quick start, core concepts, common patterns
- [ ] Integrate existing content from `docs/domains/*.md` and `docs/usage/*-domain.md`
- [ ] 3-5 working code examples per domain (from `examples/` folder)
- [ ] Best practices section (5-7 tips each)

**Should Have:**
- [ ] Cross-domain integration guides (e.g., Report + Analytics workflow)
- [ ] Domain health scores included
- [ ] Troubleshooting sections

**Nice to Have:**
- [ ] Interactive examples in Sphinx
- [ ] Video walkthroughs
- [ ] Mermaid diagrams for complex workflows

---

## 📊 Work Breakdown

### Phase 1: Core Data Domains (Week 1 - High Priority)

**Priority 1A: Report Domain** (~8 hours)
- **Scope:** ~600 lines
- **Focus:** UUT/UUR reports, step types, factory methods, WSJF serialization
- **Examples:** report_builder_examples.py, create_uut_report.py, step_types.py
- **Sources:**
  - `docs/domains/report.md` - API reference
  - `docs/usage/report-domain.md` - Usage patterns
  - `examples/report/` - 8+ working examples

**Priority 1B: Product Domain** (~6 hours)
- **Scope:** ~450 lines
- **Focus:** Products, revisions, BOMs, box build templates
- **Examples:** product_examples.py, box_build_template.py
- **Sources:**
  - `docs/domains/product.md`
  - `examples/product/`

**Priority 1C: Production Domain** (~7 hours)
- **Scope:** ~500 lines
- **Focus:** Serial numbers, assembly operations, verification, box build assembly
- **Examples:** production_examples.py, assembly_workflow.py
- **Sources:**
  - `docs/domains/production.md`
  - `docs/usage/production-domain.md`

**Phase 1 Total:** 21 hours (~3 days)

---

### Phase 2: Analysis & Secondary Domains (Week 2)

**Priority 2A: Asset Domain** (~5 hours)
- **Scope:** ~400 lines
- **Focus:** Equipment, calibration, maintenance tracking

**Priority 2B: Software Domain** (~5 hours)
- **Scope:** ~350 lines
- **Focus:** Software versions, dependencies, licenses

**Priority 2C: RootCause Domain** (~6 hours)
- **Scope:** ~450 lines
- **Focus:** Failure analysis, defect tracking, corrective actions

**Priority 2D: Process Domain** (~4 hours)
- **Scope:** ~300 lines
- **Focus:** Manufacturing processes, routing, work instructions

**Phase 2 Total:** 20 hours (~2.5 days)

---

### Phase 3: Admin & Polish (Week 3)

**Priority 3A: SCIM Domain** (~3 hours)
- **Scope:** ~250 lines
- **Focus:** User/group management, access control

**Priority 3B: Cross-Domain Integration** (~8 hours)
- Complete workflow examples combining multiple domains
- E.g., "Report → Analytics → RootCause" pipeline
- Assembly tracking with Product + Production + Asset domains

**Priority 3C: Review & Polish** (~4 hours)
- Cross-link validation
- Example testing
- Formatting consistency

**Phase 3 Total:** 15 hours (~2 days)

---

## 📂 Files to Create/Modify

**Create (8 new RST files):**
- `docs/api/domains/report.rst` (~600 lines)
- `docs/api/domains/product.rst` (~450 lines)
- `docs/api/domains/production.rst` (~500 lines)
- `docs/api/domains/asset.rst` (~400 lines)
- `docs/api/domains/software.rst` (~350 lines)
- `docs/api/domains/rootcause.rst` (~450 lines)
- `docs/api/domains/process.rst` (~300 lines)
- `docs/api/domains/scim.rst` (~250 lines)

**Modify:**
- `docs/api/index.rst` - Add new domain links
- `docs/api/domains/index.rst` - Update domain listing

**Reference (existing content to integrate):**
- `docs/domains/*.md` (11 files)
- `docs/usage/*-domain.md` (9 files)
- `examples/*/` folders
- `docs/domain_health/*.md` (health scores)

---

## 🧩 Template Structure

Each domain RST follows this structure (based on analytics.rst):

```rst
1. Domain Overview (2-3 paragraphs)
2. Quick Start (3-4 practical scenarios with code)
3. Core Concepts (key models and relationships)
4. Common Use Cases (4-6 patterns with examples)
5. Advanced Features
6. API Reference (auto-generated)
7. Model Documentation
8. Best Practices (5-7 tips)
9. Related Documentation (cross-links)
10. Domain Health & Status
```

**Estimated Lines:** 300-600 per domain

---

## 🧪 Testing Strategy

**For Each Domain:**
1. Verify all code examples run without errors
2. Check all cross-links resolve correctly
3. Build Sphinx docs without warnings
4. Manual review for clarity and completeness

**Acceptance Test:**
```bash
# Run Sphinx build
python scripts/run_sphinx_build.py

# Should see:
# - 0 warnings
# - All 8 new domains in TOC
# - Working examples tested
```

---

## 📚 Source Material Locations

```
docs/
├─ domains/          # API reference (11 files) → Source for "API Reference" sections
├─ usage/            # Usage guides (9 files) → Source for "Common Use Cases"
├─ domain_health/    # Health scores → Source for "Domain Health" sections
└─ api/domains/      # Sphinx RST (1 complete: analytics.rst) → Template to follow

examples/
├─ analytics/        # Working examples → Source for "Quick Start" and code samples
├─ report/
├─ product/
└─ ...
```

---

## 🚀 Implementation Approach

**Day 1-3: Core Data Domains**
- Use analytics.rst as template
- Focus on Report, Product, Production
- Extract examples from existing files
- Test all code samples

**Day 4-6: Analysis Domains**
- Asset, Software, RootCause, Process
- Similar structure, smaller scope
- Cross-link to core domains

**Day 7-8: Admin & Integration**
- SCIM domain (smallest)
- Cross-domain workflow guides
- Final review and polish

---

## 🔗 Dependencies

**Blocked By:** None (all source material exists)  
**Blocks:** 
- Documentation structure consolidation (separate project)
- User onboarding improvements

---

## 📈 Success Metrics

**Quantitative:**
- [ ] 8/8 domains documented (100% coverage)
- [ ] 24-40 working examples (3-5 per domain)
- [ ] 0 Sphinx build warnings
- [ ] ~3,300 lines of rich documentation

**Qualitative:**
- [ ] New users can find domain examples quickly
- [ ] API reference includes context and best practices
- [ ] Documentation feels cohesive and professional

---

## 📝 Notes

**Future Work (Out of Scope):**
- Documentation consolidation (reducing duplication across docs/domains/, docs/usage/, docs/api/)
- Installation guide consolidation
- Architecture document cleanup

These are tracked separately - keep this sprint focused on Sphinx enhancement only.

---

**Ready to Start:** ✅ Template proven (analytics.rst), source material ready, clear deliverables
