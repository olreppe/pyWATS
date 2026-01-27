# {DOMAIN} Domain Health Check

**Last Updated:** {Date}  
**Version:** v{X.X.XbX}  
**Reviewer:** {AI/Human}  
**Health Score:** {X}/60 ({Grade})

---

## Quick Status

| Category | Score | Status | Notes |
|----------|-------|--------|-------|
| Architecture | {0-10} | ✅/⚠️/❌ | Service→Repository→HttpClient compliance, file sizes |
| Models | {0-10} | ✅/⚠️/❌ | Pydantic quality, documentation, validation |
| Error Handling | {0-10} | ✅/⚠️/❌ | ErrorHandler usage, custom exceptions, context |
| Documentation | {0-10} | ✅/⚠️/❌ | Docstrings, examples, Raises complete |
| Testing | {0-10} | ✅/⚠️/❌ | Coverage %, acceptance tests, edge cases |
| API Surface | {0-10} | ✅/⚠️/❌ | Naming, types, consistency, deprecation |
| **Total** | **{X}/60** | **{Grade}** | Overall domain health |

**Grade Scale:**
- A+ (58-60): Elite - Industry benchmark
- A (54-57): Excellent - Production ready, highly polished
- A- (50-53): Very Good - Minor refinements possible
- B+ (46-49): Good - Some improvements needed
- B (42-45): Acceptable - Notable improvements needed
- B- (38-41): Fair - Multiple areas need work
- C (30-37): Needs Work - Significant improvements required
- D (20-29): Poor - Major refactoring needed
- F (<20): Critical - Not production ready

---

## 1. Architecture & Design

**Pattern Compliance:** ✅/⚠️/❌

**Service Layer:**
- Location: `src/pywats/domains/{domain}/async_service.py`
- Class: `Async{Domain}Service` (async-first architecture)
- Compliance: {notes on delegation, business logic}
- Issues: {any architectural problems}

**Repository Layer:**
- Location: `src/pywats/domains/{domain}/repository.py`
- HTTP Client usage: {notes}
- ErrorHandler integration: {notes}

**Internal API Separation:**
- Internal endpoints: {YES/NO - list if YES}
- Properly separated: ✅/❌

**Refactor Opportunities:**
- {Specific improvement 1}
- {Specific improvement 2}

**Class Diagram:**
```
{DomainService} --> {DomainRepository} --> HttpClient
{DomainService} --> {Model1}, {Model2}
{Additional relationships}
```

---

## 2. Model Quality

**Files:** 
- `models.py` ({X} lines)
- {Other model files}

**Key Models:**

| Model | Fields | Lines | Quality | Notes |
|-------|--------|-------|---------|-------|
| {ModelName} | {count} | {LOC} | ✅/⚠️/❌ | {issues/strengths} |
| {ModelName} | {count} | {LOC} | ✅/⚠️/❌ | {issues/strengths} |

**Quality Assessment:**
- ✅ **Strengths:** {What's good}
- ⚠️ **Issues:** {What needs improvement}

**Model Size Analysis:**
- Large models (>500 lines): {count} - {list if any}
- Refactoring candidates: {notes}

---

## 3. Code Quality Checks

### Exception Handling

| Check | Status | Notes |
|-------|--------|-------|
| ErrorHandler.handle_response() usage | ✅/⚠️/❌ | {coverage %} |
| ValueError validations | ✅/⚠️/❌ | {coverage notes} |
| Proper error messages | ✅/⚠️/❌ | {clarity assessment} |

### Magic Numbers

**Status:** ✅/⚠️/❌

**Findings:**
- {List any magic numbers found}
- {Or state "None found - all values are named constants/parameters"}

### Documentation Quality

| Aspect | Coverage | Status | Notes |
|--------|----------|--------|-------|
| Docstrings | {X}% | ✅/⚠️/❌ | {notes} |
| Args documentation | {X}% | ✅/⚠️/❌ | {notes} |
| Returns documentation | {X}% | ✅/⚠️/❌ | {notes} |
| Raises documentation | {X}% | ✅/⚠️/❌ | {notes} |
| Code examples | {X}% | ✅/⚠️/❌ | {notes} |

---

## 4. Testing Coverage

**Acceptance Tests:** `tests/acceptance/{domain}/`

**Test Scenarios:**

| Scenario | Status | File | Notes |
|----------|--------|------|-------|
| {Scenario 1} | ✅/❌/⏳ | {file} | {notes} |
| {Scenario 2} | ✅/❌/⏳ | {file} | {notes} |
| {Scenario 3} | ✅/❌/⏳ | {file} | {notes} |

**Coverage Gaps:**
- {Missing test 1}
- {Missing test 2}

**Unit Test Coverage:** {X}% (target: >80%)

---

## 5. Function Inventory

**Service Functions:** {count}
**Repository Functions:** {count}

**Top Issues:**
1. {Issue with highest priority}
2. {Second priority issue}
3. {Third priority issue}

**Detailed Function Review:** (Optional - link to separate document if very detailed)
- See: `docs/internal_documentation/archived/release_reviews/{DOMAIN}_DOMAIN_REVIEW.md`

---

## 6. Pending Work

### High Priority
- [ ] {Task} - {Owner} - {Target Date}
- [ ] {Task} - {Owner} - {Target Date}

### Medium Priority
- [ ] {Task} - {Owner} - {Target Date}
- [ ] {Task} - {Owner} - {Target Date}

### Low Priority / Nice to Have
- [ ] {Task}
- [ ] {Task}

### Blockers
- {Blocker 1 with details}
- {Blocker 2 with details}

---

## 7. Change History

| Date | Version | Score | Changes | Reviewer |
|------|---------|-------|---------|----------|
| {YYYY-MM-DD} | v{X.X.XbX} | {X}/50 | Initial health check | {Name} |

---

## Notes

{Any additional context, decisions, or observations that don't fit above}

---

**Next Review Due:** {Date - typically 3 months or before next major release}
