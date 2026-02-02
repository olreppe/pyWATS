---
name: run-prerelease
description: Run pre-release checks (tests, mypy, flake8) and provide go/no-go recommendation
argument-hint: "Optional: specific checks to run, e.g., 'tests only' or 'mypy strict'"
---

You are my pre-release validation assistant for the pyWATS repository.

## Goal
Run comprehensive pre-release checks and provide a go/no-go recommendation for release.

## Input from User
{{args}}

## Steps

### 1. Determine Checks to Run

**Default (full check):**
- All unit tests
- Type checking (mypy)
- Linting (flake8)
- Example validation (run 3-5 key examples)
- CHANGELOG review

**User-specified:**
Parse {{args}} for specific checks if provided

### 2. Run Tests

**Command:**
```bash
pytest -v
```

**Check for:**
- All tests passing? (target: 97%+ pass rate)
- Any new failures since last run?
- Test count (should be ~416+)
- Skipped tests reasonable? (target: <15 skipped)

**Report:**
- ✅ {X} tests passing
- ⚠️ {Y} tests skipped
- ❌ {Z} tests failed (if any)

### 3. Run Type Checking

**Command:**
```bash
mypy src/pywats --config-file pyproject.toml
```

**Check for:**
- Error count (target: <20 errors)
- Any new errors since last check?
- Severity of errors (some stub file errors acceptable)

**Report:**
- ✅ {X} errors found (down from {previous})
- ⚠️ {List critical errors if any}
- 📊 Error trend: improving/stable/regressing

### 4. Run Linting

**Command:**
```bash
flake8 src/pywats --max-line-length=120 --exclude=__pycache__,*.pyi
```

**Check for:**
- Any critical issues? (undefined names, syntax errors)
- Code style violations (should be minimal)

**Report:**
- ✅ No critical issues
- ⚠️ {X} style warnings (acceptable if minor)

### 5. Validate Examples

**Run 3-5 key examples:**
```bash
python examples/getting_started/01_connection.py
python examples/report/basic_report_examples.py
python examples/product/basic_product_examples.py
```

**Check for:**
- Examples execute without errors?
- Output makes sense?
- Any deprecation warnings?

**Report:**
- ✅ {X}/{Y} examples ran successfully
- ⚠️ {List any failures}

### 6. Review CHANGELOG

**Check `CHANGELOG.md`:**
- Is `[Unreleased]` section populated?
- Are entries well-formatted?
- Do entries match recent commits?
- Any missing notable changes?

**Report:**
- ✅ CHANGELOG current with {X} entries
- ⚠️ Missing: {suggest any notable unreported changes}

### 7. Check Version Numbers

**Verify consistency:**
- `pyproject.toml` → version
- `docs/api/conf.py` → release, version
- Do they match?
- Does version follow semver?

**Report:**
- ✅ Version consistent: {version}
- ⚠️ Inconsistency found: {details}

### 8. Review Git State

**Check:**
```bash
git status
git log --oneline -10
```

**Report:**
- Working tree clean?
- All changes committed?
- Any uncommitted files?
- Recent commits make sense?

### 9. Go/No-Go Decision

**GO if:**
- ✅ 95%+ tests passing
- ✅ <20 mypy errors (or improving trend)
- ✅ No critical flake8 issues
- ✅ Examples run successfully
- ✅ CHANGELOG complete
- ✅ Version numbers consistent

**NO-GO if:**
- ❌ Test failures (unless known/acceptable)
- ❌ New critical mypy errors
- ❌ Examples broken
- ❌ CHANGELOG incomplete
- ❌ Version mismatch

**CAUTION if:**
- ⚠️ Minor issues (skipped tests, style warnings)
- ⚠️ Unreleased section not comprehensive

### 10. Provide Recommendation

**Format:**
```markdown
## Pre-Release Check Results

### Summary: {GO ✅ | NO-GO ❌ | CAUTION ⚠️}

**Tests:** {X passing, Y skipped, Z failed}
**Type Checking:** {X errors}
**Linting:** {Pass/Issues}
**Examples:** {X/Y passing}
**CHANGELOG:** {Complete/Needs update}
**Version:** {Consistent/Mismatch}

### Issues Found
{List any blockers or concerns}

### Recommended Actions
{What to fix before release, if any}

### Next Steps
{If GO: commit, tag, build, publish}
{If NO-GO: fix issues, re-run checks}
```

## Output Format
1. Run each check sequentially
2. Report results as you go
3. Provide final summary with recommendation
4. List specific actions needed

## Special Cases

**If user specifies partial check:**
- Run only specified checks
- Note which checks were skipped
- Recommend full check before actual release

**If automated script exists:**
```bash
.\scripts\pre_release_check.ps1
```
- Offer to run that instead
- Parse and report its output
- Add any manual checks not in script

## Reference
- Standards: `.github/copilot-instructions.md` → "Pre-Release Checklist"
- Script: `scripts/pre_release_check.ps1` (if exists)
