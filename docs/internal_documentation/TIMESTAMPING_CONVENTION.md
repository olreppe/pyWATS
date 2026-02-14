# Timestamping Convention for pyWATS Documentation

**Created:** February 14, 2026  
**Last Updated:** February 14, 2026  
**Status:** Active

---

## 📅 Purpose

To maintain clarity on document currency and prevent accumulation of outdated documentation, all working documents in the pyWATS repository must be timestamped.

---

## 📝 When to Timestamp

### ✅ ALWAYS Timestamp These:

| Document Type | Example | Format |
|---------------|---------|--------|
| Project Documents | README.md, 01_ANALYSIS.md | Header with Created + Last Updated |
| Architecture Decisions | ARCHITECTURE_DECISION_*.md | Header with Created + Last Updated |
| Status Summaries | CODE_QUALITY_SUMMARY_2026-02-03.md | In filename + header |
| Implementation Plans | 02_IMPLEMENTATION_PLAN.md | Header with Created + Last Updated |
| Progress Reports | 03_PROGRESS.md | Header + timestamped entries |
| Analysis Reports | DOCSTRING_COVERAGE_AUDIT_2026-02-01.md | In filename |
| Session Notes | SESSION_STATUS_2026-02-02.md | In filename |
| Completion Summaries | COMPLETION_SUMMARY.md | Header with completion date |

### ⚠️ SOMETIMES Timestamp These:

| Document Type | When to Timestamp |
|---------------|-------------------|
| Test Strategy Docs | If snapshotting test approach at a point in time |
| Working Notes | If they might be referenced later (not ephemeral) |
| Meeting Notes | Always timestamp these for historical context |

### ❌ NEVER Timestamp These:

| Document Type | Why Not |
|---------------|---------|
| Source Code | Use git history instead |
| Auto-Generated Docs | Rebuild from source; no manual timestamp needed |
| README files | Unless it's a snapshot/summary (project READMEs should have timestamps) |
| Configuration Files | Version-controlled; git provides timestamp |

---

## 🏷️ Naming Conventions

### For Files
Use `YYYYMMDD` or `YYYY-MM-DD` format in filenames for date-specific documents:

**Examples:**
- ✅ `CODE_QUALITY_SUMMARY_2026-02-03.md`
- ✅ `DOCSTRING_COVERAGE_AUDIT_2026-02-01.md`
- ✅ `SESSION_STATUS_2026-02-02.md`
- ✅ `VERIFYING_REPORT_MODEL_2026-02-01.md`

**Avoid:**
- ❌ `code_quality_summary.md` (no date)
- ❌ `audit_02-01.md` (incomplete date)

### For Project Folders
Use `MMDDHHMM-{project-name}.project/` format when archiving to `projects/completed/`:

**Examples:**
- ✅ `02140900-api-performance-optimization.project/`
- ✅ `02031400-logging-consolidation/`
- ✅ `01280000-backwards-compat-cleanup/`

**Format:** `MMDDHHMM` = Month-Day-Hour-Minute
- `0214` = February 14
- `0900` = 09:00 (9 AM)

---

## 📋 Document Header Format

**Standard Template:**
```markdown
# Document Title

**Created:** February 14, 2026  
**Last Updated:** February 14, 2026 - 14:30  
**Status:** Active | Outdated | Archived

---

{Document content}
```

**Completion Summary Variant:**
```markdown
# Project Name - Completion Summary

**Project ID:** {id}  
**Status:** ✅ COMPLETE  
**Started:** February 13, 2026  
**Completed:** February 14, 2026  
**Duration:** 2 days

---

{Summary content}
```

---

## 🔄 Update Rules

### When to Update "Last Updated"
- Significant content changes (not typo fixes)
- Adding new sections or analysis
- Major revisions to conclusions or recommendations
- Whenever status changes

### How to Mark Documents Outdated
1. Change status: `**Status:** Outdated`
2. Add note at top:
   ```markdown
   > ⚠️ **OUTDATED**: Superseded by [New Document](link) on February 20, 2026
   ```
3. During quarterly cleanup, evaluate if document should be:
   - **Kept**: Still useful for historical reference
   - **Deleted**: No longer relevant

---

## 📂 Organization by Quarter

### Completed Projects
Move to `projects/completed/{quarter}/`:
- `projects/completed/2026-q1/` (January-March 2026)
- `projects/completed/2026-q2/` (April-June 2026)
- etc.

### Internal Documentation
Status snapshots go to `docs/internal_documentation/completed/{quarter}/`:
- `docs/internal_documentation/completed/2026-q1/`
- Keep only if historically useful (delete outdated planning docs)

---

## 🧹 Quarterly Cleanup Checklist

**Every quarter (Feb, May, Aug, Nov):**

1. **Review all active documents** in `docs/internal_documentation/`
   - Mark outdated ones with `Status: Outdated`
   - Move still-relevant ones to `completed/{current-quarter}/`

2. **Clean up completed projects**
   - Verify all have timestamps in folder names
   - Delete truly obsolete ones (no historical value)

3. **Archive decisions**
   - Architecture decisions → Keep with timestamps
   - Status snapshots → Keep if useful for trends
   - Outdated plans → Delete

4. **Update this document**
   - Add new patterns discovered
   - Remove patterns that didn't work
   - Update "Last Updated" timestamp

---

## 💡 Best Practices

### DO:
- ✅ Update timestamps when making significant changes
- ✅ Use clear status indicators (Active, Outdated, Archived)
- ✅ Reference superseding documents when marking something outdated
- ✅ Include timestamps in progress logs (`03_PROGRESS.md`)
- ✅ Timestamp all micro-sprint completion summaries

### DON'T:
- ❌ Batch-update timestamps at end of day (update as you go)
- ❌ Forget to rename project folders when moving to completed/
- ❌ Keep outdated planning documents "just in case"
- ❌ Create documents without timestamps (prevents future confusion)

---

## 📊 Example Project Timeline

```
February 13, 2026 - 09:00: Project created
├── projects/active/converter-testing.project/
│   ├── README.md (Created: Feb 13, Last Updated: Feb 13 - 09:00)
│   ├── 01_ANALYSIS.md (Created: Feb 13, Last Updated: Feb 13 - 10:30)
│   ├── 02_IMPLEMENTATION_PLAN.md (Created: Feb 13, Last Updated: Feb 13 - 11:00)
│   └── 03_PROGRESS.md (Created: Feb 13, Last Updated: Feb 14 - 14:00)

February 14, 2026 - 15:00: Project completed
├── Renamed to: 02141500-converter-testing.project/
├── Moved to: projects/completed/2026-q1/02141500-converter-testing.project/
└── COMPLETION_SUMMARY.md added (Completed: February 14, 2026)
```

---

## 🔗 Related Documents

- [Project Workflow Instructions](../projects/.agent_instructions.md) - Full project templates
- [Copilot Instructions](../.github/copilot-instructions.md) - Base instructions for agents
- [CHANGELOG Standards](../.github/copilot-instructions.md#changelog-standards) - How to document changes

---

**Next Review:** May 1, 2026 (Q2 cleanup)
