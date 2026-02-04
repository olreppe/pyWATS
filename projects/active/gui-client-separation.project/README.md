# GUI Framework & Application Template

**Status:** ⚠️ EXPERIMENTAL - Not Approved for Production  
**Progress:** 15% (Framework + Template + Configurator scaffold created)  
**Priority:** P1  
**Timeline:** 4-5 weeks (reduced from 10)  
**Created:** February 3, 2026  
**Updated:** February 4, 2026  
**Owner:** Architecture Team

---

## ⚠️ CRITICAL CONSTRAINTS

1. **Platform Independence**: DO NOT alter `src/pywats_client/` or service implementation
2. **Scope**: Simple config/alarming GUIs only (not advanced features)
3. **Old GUI**: DO NOT deprecate - old GUI must remain fully functional
4. **Documentation**: NO user-facing docs or examples until approved
5. **Release**: NOT in release flow - this is an experiment
6. **Revert-Ready**: User must be able to go back to old GUI at any time

---

## 📋 Objective

Create a reusable GUI framework with proven implementation (Configurator refactor), scaffolded template for future apps, and pilot AI-powered analytics application.

**Phase 1 Deliverables:**
1. **Shared Framework** (`pywats_ui.framework`) - Reusable base classes, dialogs, widgets
2. **Client Configurator** (Refactored) - Migrate existing GUI to new framework
3. **Application Template** - Scaffolded starter for new apps (cookiecutter-style)
4. **AI Chat Pilot** - LLM-powered test data analysis (process capability, SPC, RCA)

**Future Applications** (Post-Phase 1):
- Yield Monitor - Real-time dashboards
- Software Package Manager - Package distribution
- Client Monitor - Service health monitoring
- Additional apps using template

**Key Goals:**
- ✅ Shared UI framework (proven with Configurator)
- ✅ Application template (accelerates new app development)
- ✅ AI Chat pilot (validates framework for data-intensive apps)
- ✅ Independent applications (can run standalone)
- ✅ Common API/client access
- ✅ Optional inter-app communication (IPC/message bus)
- ✅ Consistent look & feel
- ✅ Extensible architecture for future apps
- ✅ **Graceful transition** (old GUI coexists during migration)

---

## 🎯 Success Criteria

⏳ **Analysis Phase:**
- [ ] Map current Configurator features and architecture
- [ ] Research Qt/PySide6 patterns for reusable framework
- [ ] Design application template structure
- [ ] Define AI Chat pilot requirements (LLM integration, data analysis)
- [ ] Cost/benefit analysis (framework investment vs gains)

⏳ **Design Phase:**
- [ ] Framework API specification (BaseApplication, BaseMainWindow)
- [ ] Shared component library (dialogs, widgets, themes)
- [ ] Application template scaffold (cookiecutter or manual)
- [ ] AI Chat architecture (LLM integration, data pipeline)
- [ ] IPC architecture (optional, if needed)

⏳ **Implementation Phase:**
- [ ] Create `pywats_ui.framework` package
- [ ] Implement shared components (base classes, dialogs, widgets)
- [ ] Refactor Configurator to use new framework
- [ ] Create application template with documentation
- [ ] Implement AI Chat pilot (LLM integration, analytics UI)
- [ ] IPC/communication layer (if designed)

⏳ **Testing & Deployment:**
- [ ] Configurator fully functional in new framework
- [ ] Template generates working starter app
- [ ] AI Chat pilot demonstrates LLM analytics
- [ ] Framework reduces code duplication by 50%+
- [ ] Documentation and examples complete

---

## 📊 Metrics

- **Phase 1 Applications:** 2 (Configurator refactor + AI Chat pilot)
- **Application Template:** 1 scaffolded starter
- **Shared Framework Goal:** 50%+ code reuse
- **Current State:** 1 tightly coupled GUI (configurator)
- **Target State:** Independent apps + reusable framework + template
- **Breaking Changes:** Import paths only (user-facing APIs stable)
- **Timeline:** 4-5 weeks (vs 10 weeks for full 4-app implementation)

---

## 🔗 Quick Links

- [Analysis](01_ANALYSIS.md) - Problem statement and architecture review
- [Implementation Plan](02_IMPLEMENTATION_PLAN.md) - Phased execution strategy
- [Progress](03_PROGRESS.md) - Session notes and discoveries
- [TODO](04_TODO.md) - Task checklist
- [Original Request](../../make_this_a_project/GUI_CLIENT_SEPARATION.md)

---

##Phase 1 Focus (This Project):**
- **Configurator:** Prove framework works (refactor existing GUI)
- **Template:** Enable rapid app development (scaffold with docs)
- **AI Chat:** Pilot LLM integration (process capability, SPC, RCA)

**AI Chat Pilot Requirements (User to provide details):**
- LLM-powered test data analysis
- Process capability analysis (Cp, Cpk, Pp, Ppk)
- Statistical Process Control (SPC charts, control limits)
- Root Cause Analysis (RCA) suggestions
- Interactive chat interface for queries
- Integration with pyWATS analytics APIs

**Future Applications (Phase 2+):**
- Yield Monitor: Real-time analytics dashboard
- Software Package Manager: Distribution and deployment
- Client Monitor: Service health and diagnostics
- Any new apps using the template

**Python Implementation Considerations:**
- PySide6 for Qt-based GUI framework
- Shared base classes (BaseApplication, BaseMainWindow)
- Common dialogs and widgets library
- Theme/styling system
- LLM integration (OpenAI API, local models, or custom)
- Optional IPC via QLocalSocket or message bus

This project creates **framework + template** first, then validates with 2 apps (Configurator + AI Chat)

This project will create **NEW applications** (Yield Monitor, Package Manager, Monitor) while refactoring the existing configurator into the new framework.
