# Planned Projects

**Purpose:** Focused, sprint-sized projects ready to execute when capacity is available.

**Naming Rule:** Project names must be specific and descriptive. Avoid generic names like "some-work" or "api-quality" - if the name is vague, the scope is too wide.

---

## 📦 Active Projects (Ready to Start)

### 🎯 High Priority

**[windows-service-launcher.project/](windows-service-launcher.project/)**
- **Goal:** Create persistent Windows launcher with stale lock cleanup
- **Sprint:** 1-2 weeks
- **Impact:** Eliminates #1 user frustration - "can't restart service"

**[sphinx-domain-documentation.project/](sphinx-domain-documentation.project/)**
- **Goal:** Complete Sphinx documentation for 8 remaining domains
- **Sprint:** 2-3 weeks
- **Impact:** Professional documentation for BETA release

### 🧹 Medium Priority

**[report-model-legacy-removal.project/](report-model-legacy-removal.project/)**
- **Goal:** Remove V1/V2/V3 report models, keep only current production version
- **Sprint:** 3-5 days
- **Impact:** Reduces codebase size, eliminates confusion

### 🔧 Low Priority

**[sync-wrapper-enhancements.project/](sync-wrapper-enhancements.project/)**
- **Goal:** Add timeout, retry logic, and correlation IDs to sync wrapper
- **Sprint:** 3-5 days
- **Impact:** Improved production reliability and debugging

---

## 📚 Reference Documents

**Workflow Guides:**
- [ai-assisted-micro-sprint-workflow.md](ai-assisted-micro-sprint-workflow.md) - Sprint methodology
- [GitHubCopilot-BestPractices.md](GitHubCopilot-BestPractices.md) - AI coding practices

---

## 🔄 Project Structure

Each project folder contains:
- **README.md** - Sprint overview with clear scope and acceptance criteria
- **ORIGINAL_ANALYSIS.md** (or similar) - Detailed background and research
- **TODO.md** (created when active) - Implementation checklist
- **PROGRESS.md** (created when active) - Daily progress tracking

---

## 📋 Workflow

**Adding New Projects:**
1. Create project folder: `{project-name}.project/`
2. Write sprint-scoped README.md with:
   - Goal (1-2 sentences)
   - Acceptance criteria (clear must-haves)
   - Work breakdown (tasks with estimates)
   - Files involved
3. Add to this README in priority order

**Starting a Project:**
1. Move project folder to `../active/`
2. Create TODO.md from work breakdown
3. Follow [../.agent_instructions.md](../.agent_instructions.md) workflow

**Completing a Project:**
1. Move to `../../docs/internal_documentation/completed/{quarter}/`
2. Update this README
3. Celebrate! 🎉

---

## 🗂️ Archive Locations

**Completed Work:**
- `docs/internal_documentation/completed/2026-q1/` - Finished Q1 2026 projects

**Reference Analysis:**
- `docs/internal_documentation/reference/` - Analysis docs (not actionable projects)
  - CSHARP_PYTHON_FEATURE_ALIGNMENT.md - 50+ page comparison

---

Last Updated: February 1, 2026
