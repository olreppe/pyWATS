# Domain Health Checks

**Purpose:** Living documentation tracking the health and quality of each pyWATS domain.

**Last Updated:** 2026-01-26  
**Status:** Active - Updated with each domain change

---

## Overview

This directory contains **unified health checks** for all pyWATS domains, replacing the previous separate `release_reviews/` and `DOMAIN_STATUS/` folders. Each domain gets a single, comprehensive health check document that combines:

- ✅ **Quality scoring** (architecture, models, error handling, docs, testing)
- ✅ **Current status** (what's good, what needs work)
- ✅ **Pending work** (high/medium/low priority tasks)
- ✅ **Change history** (evolution over time)

---

## Current Health Scores

| Domain | Score | Grade | Status | Last Updated |
|--------|-------|-------|--------|--------------|
| [Analytics](analytics.md) | 48/50 | A | ✅ Excellent | 2026-01-26 |
| [Production](production.md) | 48/50 | A | ✅ Excellent | 2026-01-26 |
| [Product](product.md) | 47/50 | A | ✅ Excellent | 2026-01-26 |
| [RootCause](rootcause.md) | 46/50 | A | ✅ Excellent | 2026-01-26 |
| [Software](software.md) | 46/50 | A | ✅ Excellent | 2026-01-26 |
| [Asset](asset.md) | 46/50 | A | ✅ Excellent | 2026-01-26 |
| [Process](process.md) | 46/50 | A | ✅ Excellent | 2026-01-26 |
| [Report](report.md) | 41/50 | B+ | ✅ Good | 2026-01-26 |

**Overall Average:** 46.0/50 (A) ✅

---

## Grading Scale

| Grade | Score | Description |
|-------|-------|-------------|
| **A** | 45-50 | Excellent - Production ready |
| **B** | 40-44 | Good - Minor improvements needed |
| **C** | 35-39 | Acceptable - Moderate improvements needed |
| **D** | 30-34 | Poor - Major improvements needed |
| **F** | <30 | Critical - Significant refactoring required |

---

## Scoring Categories

Each domain is scored across 5 categories (max 10 points each):

### 1. Architecture (10 points)
- Service→Repository→HttpClient pattern compliance
- Proper layering and separation of concerns
- Internal API isolation (if applicable)

### 2. Models (10 points)
- Pydantic model quality and documentation
- Model size and complexity
- Field documentation and examples

### 3. Error Handling (10 points)
- ErrorHandler.handle_response() usage
- ValueError validations
- Error message clarity

### 4. Documentation (10 points)
- Docstring coverage and quality
- Args/Returns/Raises documentation
- Code examples

### 5. Testing (10 points)
- Acceptance test coverage
- Unit test coverage (target >80%)
- Test scenario completeness

---

## Update Workflow

### When to Update Health Checks

**Required Updates:**
- ✅ Before each release (part of `scripts/bump.ps1`)
- ✅ After major refactoring of a domain
- ✅ When fixing identified issues

**Recommended Updates:**
- ⚠️ Monthly review of all domains
- ⚠️ When adding significant new features
- ⚠️ When changing domain architecture

### How to Update

**Manual Update:**
1. Open the domain health check file (e.g., `analytics.md`)
2. Update the relevant sections:
   - Quick Status scores
   - Pending Work (mark completed tasks)
   - Change History (add new row)
3. Update **Last Updated** date and **Version**
4. Commit changes with message: `docs: Update {domain} health check - {reason}`

**Automated Update (Recommended):**
```powershell
# Run the health check script for a specific domain
.\scripts\domain_health_check.ps1 -Domain analytics

# Or check all domains
.\scripts\domain_health_check.ps1 -All

# Dry run to preview changes
.\scripts\domain_health_check.ps1 -Domain report -DryRun
```

---

## Common Patterns

### All Domains (✅ Excellent Across Board)

1. **Architecture Compliance** - All follow Service→Repository→HttpClient
2. **Error Handling** - ErrorHandler.handle_response() implemented (Jan 2026)
3. **Magic Numbers** - Eliminated (Jan 2026)
4. **Internal API Separation** - Properly isolated where applicable
5. **Pydantic Models** - All use AliasChoices for camelCase/snake_case

### Common Improvement Areas

| Issue | Affected Domains | Priority |
|-------|------------------|----------|
| `Raises:` docstrings | ✅ ALL COMPLETE | ~~LOW~~ DONE |
| More code examples needed | Report | MEDIUM |
| Large model files (>500 lines) | Report (UURReport 650+), Analytics (models.py 1802) | LOW |

---

## Integration with Development Workflow

### Pre-Release Checklist

Before running `scripts/bump.ps1`, ensure:
- [ ] Domain health checks are up-to-date (< 3 months old)
- [ ] All identified HIGH priority issues are resolved or documented
- [ ] New features have corresponding health check updates

### Pull Request Checklist

When modifying domain code:
- [ ] Update corresponding health check file
- [ ] Mark completed pending work items
- [ ] Add new pending work if issues identified
- [ ] Update score if significant changes made

### Issue Tracking

When creating GitHub issues for domain improvements:
- Link to specific health check section
- Reference current score and target score
- Tag with domain label (`domain:analytics`, `domain:report`, etc.)

---

## Historical Context

### Previous Documentation Systems

**`release_reviews/` (Archived Jan 2026):**
- Purpose: Pre-release quality audits
- Format: Detailed function-by-function reviews
- Status: ✅ Migrated to domain_health/
- Location: `docs/internal_documentation/archived/release_reviews/`

**`DOMAIN_STATUS/` (Archived Jan 2026):**
- Purpose: Living development documentation
- Format: Template-driven with architecture diagrams
- Status: ✅ Migrated to domain_health/
- Location: `docs/internal_documentation/archived/DOMAIN_STATUS/`

### Why Merge Them?

1. **Single source of truth** - No conflicting information
2. **Less maintenance** - One file to update per domain
3. **Actionable** - Clear scores drive prioritization
4. **Lightweight** - Not overwhelming like old STATUS docs
5. **Trackable** - Change history shows evolution

---

## Files in This Directory

| File | Purpose |
|------|---------|
| **README.md** | This file - Overview and workflow guide |
| **TEMPLATE.md** | Standard template for creating new domain health checks |
| **analytics.md** | Analytics domain health check |
| **asset.md** | Asset domain health check |
| **process.md** | Process domain health check |
| **product.md** | Product domain health check |
| **production.md** | Production domain health check |
| **report.md** | Report domain health check |
| **rootcause.md** | RootCause domain health check |
| **software.md** | Software domain health check |

---

## Maintenance Scripts

### Domain Health Check Script

Location: `scripts/domain_health_check.ps1`

**Features:**
- Automated score calculation
- Stale check detection (>3 months old)
- Markdown formatting validation
- Git commit integration

**Usage:**
```powershell
# Check single domain
.\scripts\domain_health_check.ps1 -Domain analytics

# Check all domains
.\scripts\domain_health_check.ps1 -All

# Find stale checks (>3 months)
.\scripts\domain_health_check.ps1 -FindStale

# Preview without committing
.\scripts\domain_health_check.ps1 -Domain report -DryRun
```

### Integration with Bump Script

The `scripts/bump.ps1` script now includes a health check reminder:
```powershell
Write-Step "Checking Domain Health"
$staleHealthChecks = Get-ChildItem "docs/internal_documentation/domain_health/*.md" | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddMonths(-3) }
    
if ($staleHealthChecks) {
    Write-Warning "Health checks older than 3 months: $($staleHealthChecks.Name -join ', ')"
    # Prompts user to update before continuing
}
```

---

## FAQ

**Q: How often should health checks be updated?**
A: Minimum every 3 months, or whenever making significant changes to a domain.

**Q: What if a domain score drops?**
A: Document the reason in Change History, create GitHub issues for improvements, prioritize based on severity.

**Q: Can I add custom categories to health checks?**
A: Yes, but update TEMPLATE.md first and apply consistently across all domains.

**Q: What happens if I don't update health checks?**
A: The bump script will warn you. It's not blocking, but keeping them updated ensures release quality.

**Q: How do I add a new domain?**
A: Copy TEMPLATE.md to `{domain}.md`, fill in all sections, add to README.md table, update scripts.

---

## Contact

For questions or suggestions about the health check system:
- GitHub Issues: https://github.com/olreppe/pyWATS/issues
- Tag: `documentation`, `internal-docs`

---

**Last System Update:** 2026-01-26  
**Next Review:** 2026-04-26 (3 months)
