# {DOMAIN/COMPONENT} Health Check

**Last Updated:** {Date}  
**Version:** v{X.X.XbX}  
**Reviewer:** {AI/Human}  
**Health Score:** {X}/80 ({Grade})  
**Component Type:** {Domain/Core/Client/Service/GUI/Queue/Tools/Shared}

---

## Quick Status

| Category | Score | Status | Notes |
|----------|-------|--------|-------|
| Architecture | {0-10} | ✅/⚠️/❌ | Layering, patterns, dependencies, file sizes |
| Models/Types | {0-10} | ✅/⚠️/❌ | Data models, validation, documentation |
| Error Handling | {0-10} | ✅/⚠️/❌ | Exception handling, error messages, recovery |
| Documentation | {0-10} | ✅/⚠️/❌ | Docstrings, examples, API docs, user guides |
| Testing | {0-10} | ✅/⚠️/❌ | Unit/integration coverage, edge cases, test quality |
| API Surface | {0-10} | ✅/⚠️/❌ | Naming, types, consistency, versioning |
| **Performance** | {0-10} | ✅/⚠️/❌ | Resource usage, caching, optimization, bottlenecks |
| **Observability** | {0-10} | ✅/⚠️/❌ | Logging, metrics, tracing, diagnostics |
| **Total** | **{X}/80** | **{Grade}** | Overall component health |

**Grade Scale (80-point system):**
- A+ (76-80): Elite - Industry benchmark quality
- A (70-75): Excellent - Production ready, highly polished
- A- (64-69): Very Good - Minor refinements possible
- B+ (58-63): Good - Some improvements needed
- B (52-57): Acceptable - Notable improvements needed
- B- (46-51): Fair - Multiple areas need work
- C (36-45): Needs Work - Significant improvements required
- D (26-35): Poor - Major refactoring needed
- F (<26): Critical - Not production ready

---

## 1. Architecture & Design

**Pattern Compliance:** ✅/⚠️/❌

**Component Structure:**
- Primary Location: `src/pywats/{component_path}/`
- Main Classes: {List key classes}
- Architecture Pattern: {e.g., Service→Repository→Client, MVC, Module-based, etc.}
- Compliance: {notes on pattern adherence}
- Issues: {any architectural problems}

**Dependencies:**
- Internal dependencies: {List key internal dependencies}
- External dependencies: {List key external dependencies}
- Dependency injection: {YES/NO - how implemented}
- Circular dependencies: {NONE/List if any}

**File Organization:**
- Total files: {count}
- Largest files: {file names and sizes}
- Module cohesion: ✅/⚠️/❌
- Separation of concerns: ✅/⚠️/❌

**Refactor Opportunities:**
- {Specific improvement 1}
- {Specific improvement 2}

**Component Diagram:**
```
{Component} --> {Dependencies}
{Component} --> {Models/Types}
{Additional relationships}
```

---

## 2. Model/Type Quality

**Files:** 
- {model_file.py} ({X} lines)
- {Other model/type files}

**Key Models/Types:**

| Model/Type | Fields/Attributes | Lines | Quality | Notes |
|------------|-------------------|-------|---------|-------|
| {Name} | {count} | {LOC} | ✅/⚠️/❌ | {issues/strengths} |
| {Name} | {count} | {LOC} | ✅/⚠️/❌ | {issues/strengths} |

**Quality Assessment:**
- ✅ **Strengths:** {What's good}
- ⚠️ **Issues:** {What needs improvement}

**Validation:**
- Input validation: {Coverage %} - ✅/⚠️/❌
- Type checking: {Coverage %} - ✅/⚠️/❌  
- Schema validation: {Implementation notes}

**Model Size Analysis:**
- Large models (>500 lines): {count} - {list if any}
- Refactoring candidates: {notes}

---

## 3. Code Quality Checks

### Exception Handling

| Check | Status | Notes |
|-------|--------|-------|
| ErrorHandler/try-catch coverage | ✅/⚠️/❌ | {coverage %} |
| Custom exception types | ✅/⚠️/❌ | {list custom exceptions} |
| Error context/messages | ✅/⚠️/❌ | {clarity assessment} |
| Error recovery logic | ✅/⚠️/❌ | {retry, fallback strategies} |
| Validation checks | ✅/⚠️/❌ | {input validation coverage} |

### Code Smells

**Status:** ✅/⚠️/❌

**Findings:**
- Magic numbers: {List any found or "None - all constants named"}
- Code duplication: {DRY violations if any}
- Long functions (>50 lines): {List if any}
- High complexity: {List complex functions}

### Documentation Quality

| Aspect | Coverage | Status | Notes |
|--------|----------|--------|-------|
| Docstrings | {X}% | ✅/⚠️/❌ | {notes} |
| Args documentation | {X}% | ✅/⚠️/❌ | {notes} |
| Returns documentation | {X}% | ✅/⚠️/❌ | {notes} |
| Raises documentation | {X}% | ✅/⚠️/❌ | {notes} |
| Code examples | {X}% | ✅/⚠️/❌ | {notes} |
| Type hints | {X}% | ✅/⚠️/❌ | {coverage} |

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

## 5. API Surface Quality

**Public API:**
- Total public functions/methods: {count}
- Total public classes: {count}
- Naming consistency: ✅/⚠️/❌
- Type hints coverage: {X}%

**API Stability:**
- Breaking changes: {count in recent versions}
- Deprecation warnings: {count active}
- Versioning strategy: {description}

**Usability:**
- Intuitive naming: ✅/⚠️/❌
- Consistent patterns: ✅/⚠️/❌
- Minimal required params: ✅/⚠️/❌
- Good defaults: ✅/⚠️/❌

**Top Issues:**
1. {Issue with highest priority}
2. {Second priority issue}
3. {Third priority issue}

---

## 6. Performance & Resource Usage

**Resource Consumption:**
- Memory usage: {typical/peak} - ✅/⚠️/❌
- CPU usage: {typical/peak} - ✅/⚠️/❌
- I/O operations: {count/pattern} - ✅/⚠️/❌
- Network calls: {count/pattern} - ✅/⚠️/❌

**Performance Optimizations:**
- Caching: {YES/NO - describe if yes}
- Lazy loading: {YES/NO - describe if yes}
- Connection pooling: {YES/NO - describe if yes}
- Batch operations: {YES/NO - describe if yes}

**Known Bottlenecks:**
- {Bottleneck 1 with impact}
- {Bottleneck 2 with impact}
- {Or "None identified"}

**Performance Tests:**
- Load testing: ✅/❌/⏳
- Stress testing: ✅/❌/⏳
- Benchmarks: ✅/❌/⏳

---

## 7. Observability & Diagnostics

**Logging:**
- Logging framework: {e.g., Python logging, custom}
- Log levels: {DEBUG/INFO/WARNING/ERROR coverage}
- Structured logging: ✅/❌
- Log context (trace IDs, etc.): ✅/❌
- Sensitive data handling: ✅/⚠️/❌

**Metrics/Monitoring:**
- Metrics exposed: {YES/NO - list if yes}
- Health check endpoint: {YES/NO - describe if yes}
- Performance metrics: {list key metrics}
- Business metrics: {list key metrics}

**Tracing:**
- Distributed tracing: {YES/NO - tool if yes}
- Request correlation: ✅/❌
- Span coverage: {X}%

**Diagnostics:**
- Debug mode: {YES/NO}
- Diagnostic endpoints: {list if any}
- Error reporting: {mechanism}
- Debugging tools: {list available tools}

**Observability Score Breakdown:**
- Logging quality: {0-3} points
- Metrics/monitoring: {0-3} points
- Tracing: {0-2} points
- Diagnostics: {0-2} points

---

## 8. Pending Work

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

## 9. Change History

| Date | Version | Score | Changes | Reviewer |
|------|---------|-------|---------|----------|
| {YYYY-MM-DD} | v{X.X.XbX} | {X}/80 | Initial health check | {Name} |

---

## Notes

{Any additional context, decisions, or observations that don't fit above}

---

## Scoring Criteria (80-point system)

### 1. Architecture (10 points)
| Score | Criteria |
|-------|----------|
| 10 | Perfect layering, no circular deps, injectable dependencies, <500 LOC per file, clear separation |
| 8-9 | Good pattern compliance, proper separation, minor layering issues |
| 6-7 | Some layering violations, large files (>800 LOC), mixed concerns |
| 4-5 | Inconsistent patterns, dependency issues, poor separation |
| <4 | No clear architecture, major structural problems |

### 2. Models/Types (10 points)
| Score | Criteria |
|-------|----------|
| 10 | All fields documented, comprehensive validation, type hints, examples, optimal size |
| 8-9 | Good models with proper validation, well documented, reasonable sizes |
| 6-7 | Models work but sparse docs, some validation gaps, large files |
| 4-5 | Missing validations, poor documentation, >1000 LOC files |
| <4 | Incorrect types, no validation, no documentation |

### 3. Error Handling (10 points)
| Score | Criteria |
|-------|----------|
| 10 | 100% coverage, custom exceptions, detailed context, recovery strategies |
| 8-9 | Consistent error handling, clear messages, good coverage |
| 6-7 | Some unhandled errors, inconsistent handling |
| 4-5 | Many unhandled errors, unclear messages |
| <4 | No error handling, crashes on edge cases |

### 4. Documentation (10 points)
| Score | Criteria |
|-------|----------|
| 10 | 100% docstrings with Args/Returns/Raises/Examples, user guides, API docs |
| 8-9 | >90% docstrings, good examples, complete API reference |
| 6-7 | >80% docstrings, some gaps in examples or details |
| 4-5 | <80% docstrings, sparse or missing details |
| <4 | No docstrings, no documentation |

### 5. Testing (10 points)
| Score | Criteria |
|-------|----------|
| 10 | >90% coverage, integration tests, edge cases, performance tests |
| 8-9 | >80% coverage, main scenarios, acceptance tests |
| 6-7 | >70% coverage, some edge case gaps |
| 4-5 | <70% coverage, missing critical scenarios |
| <4 | <50% coverage or no tests |

### 6. API Surface (10 points)
| Score | Criteria |
|-------|----------|
| 10 | Intuitive naming, consistent patterns, full type hints, proper versioning |
| 8-9 | Good naming, types complete, follows conventions |
| 6-7 | Some inconsistencies, missing type hints |
| 4-5 | Confusing API, mixed conventions, incomplete types |
| <4 | Unpythonic API, no types, breaking changes |

### 7. Performance (10 points) — NEW
| Score | Criteria |
|-------|----------|
| 10 | Optimized resource usage, caching, connection pooling, benchmarked |
| 8-9 | Good performance, some optimizations, no major bottlenecks |
| 6-7 | Acceptable performance, minor inefficiencies |
| 4-5 | Performance issues, resource waste, bottlenecks |
| <4 | Major performance problems, resource leaks |

### 8. Observability (10 points) — NEW
| Score | Criteria |
|-------|----------|
| 10 | Structured logging, metrics, tracing, health checks, full diagnostics |
| 8-9 | Good logging, some metrics, health checks |
| 6-7 | Basic logging, limited metrics |
| 4-5 | Minimal logging, no metrics |
| <4 | No logging or observability |

---

**Next Review Due:** {Date - typically 3 months or before next major release}
