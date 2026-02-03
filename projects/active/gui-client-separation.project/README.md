# GUI/Client Separation & Framework Refactoring

**Status:** 🚧 In Progress  
**Priority:** P2  
**Timeline:** 2-3 weeks  
**Created:** February 3, 2026  
**Owner:** Architecture Team

---

## 📋 Objective

Analyze and implement separation of GUI components from the pyWATS Client service, establishing a reusable UI framework architecture that supports multiple applications (Client Configurator, standalone tools) without code duplication.

**Key Goals:**
- Separate GUI concerns from client service logic
- Rename and reorganize "gui" → proper application structure
- Create reusable UI framework for future applications
- Establish clear boundaries and interfaces

---

## 🎯 Success Criteria

⏳ **Analysis Phase:**
- [ ] Complete architecture analysis of current GUI/client coupling
- [ ] Evaluate framework options (PySide6 patterns, widget libraries)
- [ ] Document recommended separation strategy
- [ ] Cost/benefit analysis (complexity vs gains)

⏳ **Design Phase:**
- [ ] Proposed folder structure and naming conventions
- [ ] Reusable framework components identified
- [ ] Interface contracts defined (GUI ↔ Client)
- [ ] Migration path for existing GUI code

⏳ **Decision:**
- [ ] Architecture decision recorded (ADR)
- [ ] Implementation plan approved
- [ ] Breaking changes documented

---

## 📊 Metrics

- **Current State:** GUI tightly coupled with `pywats_client`
- **Target State:** Modular UI framework + decoupled applications
- **Breaking Changes:** TBD (minimize via adapters)

---

## 🔗 Quick Links

- [Analysis](01_ANALYSIS.md) - Problem statement and architecture review
- [Implementation Plan](02_IMPLEMENTATION_PLAN.md) - Phased execution strategy
- [Progress](03_PROGRESS.md) - Session notes and discoveries
- [TODO](04_TODO.md) - Task checklist
- [Original Request](../../make_this_a_project/GUI_CLIENT_SEPARATION.md)

---

## 📝 Notes

This is an **analysis and design project** leading to an implementation project. Focus is on making the right architectural decisions before refactoring code.
