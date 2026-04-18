# Manual Inspection Domain

**Created:** March 20, 2026  
**Last Updated:** April 18, 2026  
**Status:** ✅ Phase 1 Complete — Released as v0.5.0b6

---

## Problem Statement

pyWATS has no support for WATS Manual Inspection functionality. The WATS server exposes
a set of `/api/internal/ManualInspection/` endpoints for managing inspection definitions,
relations, sequences, and inspecting individual units. Users currently have no way to
interact with this functionality via pyWATS.

Beyond the core API domain, there is also a need for a Qt6-based desktop operator
interface (**pyWATS-OI**) that allows shop-floor operators to execute manual inspection
sequences. This OI application will be built on top of the pyWATS ManualInspection domain
and will form the test bed for a set of extended, locally-executed step types not available
in the standard WATS web app.

---

## Objectives

### Phase 1 — Core pyWATS Domain
1. Implement `manual_inspection` domain following existing domain patterns
2. Cover all relevant API endpoints (definitions, relations, sequences, MI details)
3. Support reading, building and writing inspection sequences — matching current web app behavior
4. Provide sync + async service variants via `SyncServiceWrapper`
5. Register domain in `pyWATS` alongside existing domains
6. Add tests and at least one usage example

### Phase 2 — pyWATS-OI (two apps in `pywats_ui`)
7. Add two new apps to `src/pywats_ui/apps/`:
   - `sequence_designer/` — GUI for building and managing MI sequences (author/edit definitions, steps, relations)
   - `operator_interface/` — Shop-floor OI for executing any manual work (scan unit → step through → submit)
8. OI mimics the WATS web app MI workflow but is more customizable
9. Use as integration test harness for the ManualInspection domain
10. Operators can execute sequences, record results, and submit to WATS

### Phase 3 — Extended Step Types (Domain + OI)
11. Add extended step types executed locally by OI (not WATS server steps):
    - Conditional flow (if/else, for/next, branching)
    - Dynamic subsequence calling (by computed name, part number, tag, etc.)
    - Multi-numeric limit steps
    - Advanced box building via `product.BoxBuild` templates
    - Relative limits (limits derived from earlier step values, with simple expressions)
    - Batch inspections (multiple units simultaneously)
    - Python steps (fully configurable scripts, interact with OI GUI and UUTReport)
12. Evaluate and prototype **pyScript** — a lightweight markup/scripting language for
    configuring OI GUI layout and step expressions.

---

## Success Criteria

### Phase 1
- All targeted endpoints covered by repository methods
- Sync and async service available
- Tests pass alongside existing suite
- Example script in `examples/manual_inspection/`
- CHANGELOG updated

### Phase 2
- pyWATS-OI application launches, connects to WATS, lists and executes sequences
- Results submitted to WATS match what the web app would produce
- Documented setup / run instructions

### Phase 3
- All extended step types implemented in OI engine
- Batch inspection mode functional
- Python step can read/write UUTReport and display prompts in OI GUI
- pyScript spec documented (even if minimal initial implementation)

---

## Scope

**Phase 1 in scope:** Definition CRUD, relation management, sequence management, MI detail queries  
**Phase 1 out of scope (deferred):** XAML endpoint, WWF binary file (`GetWatswwfContent`)  
**Phase 2:** Two new apps in `src/pywats_ui/apps/` — `sequence_designer` and `operator_interface`  
**Phase 3:** Extended step types are OI-local features that write results back via pyWATS API

---

## References

- See `02_IMPLEMENTATION_PLAN.md` for full phased plan
- See `01_ANALYSIS.md` for API surface, risks, and open questions
- Existing domain reference: `src/pywats/domains/process/`
- Product BoxBuild reference: `src/pywats/domains/product/`
