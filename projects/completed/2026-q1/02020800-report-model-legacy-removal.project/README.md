# Report Model V1/V2/V3 Cleanup

**Project ID:** report-model-legacy-removal  
**Sprint Size:** 3-5 days  
**Priority:** Medium  
**Status:** Ready to Start  

---

## 🎯 Goal

Remove all legacy report model implementations (V1, V2, V3) leaving only the current production model, reducing codebase size and maintenance burden.

---

## 📋 Problem Statement

The codebase contains multiple report model versions from migration iterations:
- **V1 models:** Original implementation (report_models_old/)
- **V2 models:** First migration attempt
- **V3 models:** Second iteration
- **Current models:** Production version in use

**Issues:**
- Code duplication and confusion
- Increased maintenance burden
- Larger repository size
- Risk of using wrong model version
- Import confusion for developers

---

## ✅ Acceptance Criteria

**Must Have:**
- [ ] All V1 report models removed from `src/pywats/domains/report/report_models_old/`
- [ ] All V2 model references removed
- [ ] All V3 model references removed
- [ ] Only current production models remain
- [ ] All imports updated to current models
- [ ] All tests passing (no broken references)
- [ ] Documentation updated to remove legacy model mentions

**Must NOT:**
- [ ] Break any current production code
- [ ] Remove models still in use
- [ ] Delete migration scripts without archiving

**Nice to Have:**
- [ ] Archive migration history in docs/internal_documentation/completed/
- [ ] Document the final model structure
- [ ] Performance comparison before/after

---

## 🔍 Discovery Phase

### Step 1: Identify All Legacy Models (2 hours)

**Search for:**
```powershell
# Find V1/V2/V3 model files
Get-ChildItem -Path "src" -Filter "*report_model*" -Recurse | Select-String "v1|v2|v3|_old"

# Find all imports of old models
Select-String -Path "src" -Pattern "from.*report_models_(old|v1|v2|v3)" -Recurse
Select-String -Path "tests" -Pattern "from.*report_models_(old|v1|v2|v3)" -Recurse
Select-String -Path "examples" -Pattern "from.*report_models_(old|v1|v2|v3)" -Recurse

# Find migration scripts
Get-ChildItem -Path "." -Filter "*migration*" -Recurse
Get-ChildItem -Path "." -Filter "*migrate*" -Recurse
```

**Document:**
- List of all legacy model files
- List of all imports to update
- List of tests that reference legacy models
- Migration scripts to archive

---

## 🗑️ Removal Strategy

### Phase 1: Safe Removal Preparation (1 day)

**Tasks:**
1. Run full test suite to establish baseline
2. Create branch: `cleanup/remove-legacy-report-models`
3. Archive migration scripts to docs/internal_documentation/completed/migrations/
4. Document current model structure as "final"

**Deliverables:**
- Baseline test results (should be 193+ passing)
- Migration archive folder created
- Current model documentation

---

### Phase 2: Remove Legacy Model Files (1 day)

**Remove in order:**

1. **V1 Models (report_models_old/)**
   ```
   src/pywats/domains/report/report_models_old/
   ├── uut/
   ├── uur/
   ├── common/
   └── __init__.py
   ```

2. **V2 Model References**
   - Search for `_v2` suffixes
   - Remove any V2 compatibility layers

3. **V3 Model References**
   - Search for `_v3` suffixes
   - Remove any V3 compatibility layers

**After each removal:**
- Run tests: `pytest tests/domains/report/ -v`
- Fix any broken imports
- Verify no references remain

---

### Phase 3: Update Imports & References (1 day)

**Files likely to update:**
- `examples/report/*.py` - Example scripts
- `tests/domains/report/*.py` - Test files
- `tests/integration/*.py` - Integration tests
- `docs/domains/report.md` - Documentation

**Process:**
```powershell
# For each file with legacy imports:
# 1. Update import statement
# 2. Verify it still works
# 3. Run related tests
# 4. Commit incrementally
```

---

### Phase 4: Documentation Cleanup (0.5 day)

**Update:**
- `docs/domains/report.md` - Remove legacy model mentions
- `docs/MIGRATION.md` - Add "Migration Complete" note
- `CHANGELOG.md` - Document cleanup in next version
- `docs/internal_documentation/completed/` - Archive migration history

**Create:**
- `docs/internal_documentation/completed/report_model_migrations/README.md`
  - Document the evolution V1 → V2 → V3 → Final
  - Why each migration happened
  - Final model structure

---

### Phase 5: Verification & Testing (0.5 day)

**Comprehensive Testing:**
```bash
# Full test suite
pytest tests/ -v

# Specific report tests
pytest tests/domains/report/ -v
pytest tests/integration/ -k report -v

# Type checking
mypy src/pywats/domains/report/

# Example scripts
python examples/report/create_uut_report.py
python examples/report/step_types.py
```

**Manual Verification:**
- No references to `report_models_old`
- No references to `_v1`, `_v2`, `_v3`
- All examples run successfully
- Documentation mentions only current models

---

## 📂 Files Involved

**Delete:**
- `src/pywats/domains/report/report_models_old/` (entire directory)
- Any `*_v1.py`, `*_v2.py`, `*_v3.py` model files
- Migration scripts (after archiving)

**Update:**
- `examples/report/*.py` - Update imports if needed
- `tests/domains/report/*.py` - Remove legacy model tests
- `docs/domains/report.md` - Remove old model references
- `docs/MIGRATION.md` - Document completion

**Create:**
- `docs/internal_documentation/completed/report_model_migrations/README.md`
- `docs/internal_documentation/completed/report_model_migrations/MIGRATION_HISTORY.md`

---

## 🧪 Testing Strategy

**Before Removal:**
```bash
# Establish baseline
pytest tests/ -v > baseline_tests.txt
```

**During Removal:**
```bash
# After each phase
pytest tests/domains/report/ -v
pytest tests/integration/ -k report -v
```

**After Completion:**
```bash
# Full regression
pytest tests/ -v

# Should match baseline or better
# Expected: 193+ passing, 0 failures
```

---

## 🚨 Rollback Plan

If issues discovered:
1. Revert branch: `git reset --hard origin/main`
2. Review what broke
3. Update removal strategy
4. Try again with more incremental approach

---

## 📊 Success Metrics

**Code Reduction:**
- [ ] Removed 500+ lines of legacy code
- [ ] Reduced import confusion
- [ ] Cleaner directory structure

**Quality:**
- [ ] All tests passing (193+)
- [ ] 0 mypy errors
- [ ] 0 references to old models

**Documentation:**
- [ ] Migration history archived
- [ ] Current model structure documented
- [ ] No outdated references

---

## 🔗 Dependencies

**Blocked By:** None (all migrations complete)  
**Blocks:** None (cleanup is independent)

**Related:**
- V3 migration completed (see commit history)
- All production code uses current models

---

## 📝 Implementation Checklist

- [ ] Create cleanup branch
- [ ] Run baseline tests
- [ ] Search for all legacy model files
- [ ] Archive migration scripts
- [ ] Remove report_models_old/ directory
- [ ] Remove V2 references
- [ ] Remove V3 references
- [ ] Update all imports
- [ ] Update documentation
- [ ] Run full test suite
- [ ] Manual verification
- [ ] Create migration history docs
- [ ] Merge to main
- [ ] Update CHANGELOG

---

**Ready to Start:** ✅ All migrations complete, safe to remove legacy code
