# GUI Applications & Shared Framework

**Status:** 🚧 Active - Phase 1 (Analysis)  
**Progress:** 15% → Restarting with new requirements  
**Priority:** P2  
**Timeline:** 3-4 weeks  
**Created:** February 3, 2026  
**Updated:** February 4, 2026  
**Owner:** Architecture Team

---

## 📋 Objective

Design and implement a shared UI framework supporting 4+ independent GUI applications that maximize code reuse while maintaining clean separation. Applications should be able to communicate with each other (optional) and all share access to the same pyWATS API and client service.

**Target Applications (C# Reference):**
1. **Client Configurator** - Service configuration and management
2. **Yield Monitor** - Real-time yield/analytics dashboard
3. **Software Package Manager** - Package distribution and deployment
4. **Client Monitor** - Service health and diagnostics

**Future Potential:**
- Additional monitoring tools
- Report analyzers
- Data visualization apps
- Name changes and new applications expected

**Key Goals:**
- ✅ Shared UI framework (minimal code duplication)
- ✅ Independent applications (can run standalone)
- ✅ Common API/client access
- ✅ Optional inter-app communication (IPC/message bus)
- ✅ Consistent look & feel
- ✅ Extensible architecture for future apps
- ✅ **Graceful transition** (old GUI coexists during migration)

---

## 🎯 Success Criteria

⏳ **Analysis Phase:**
- [ ] Map current C# application features and architecture
- [ ] Define 4 target applications with feature sets
- [ ] Identify common framework components needed
- [ ] Research Qt/PySide6 patterns for multi-app architecture
- [ ] Evaluate IPC options (message bus, shared memory, sockets)
- [ ] Cost/benefit analysis (shared framework vs independent apps)

⏳ **Design Phase:**
- [ ] Folder structure for `pywats_ui` framework + 4 apps
- [ ] Shared framework API (widgets, dialogs, themes, config)
- [ ] IPC architecture (if implementing communication)
- [ ] Data models and validation strategies
- [ ] Authentication/connection sharing patterns

⏳ **Implementation Phase:**
- [ ] Create `pywats_ui` framework package
- [ ] Implement shared components (base windows, dialogs, etc.)
- [ ] Port Client Configurator to new structure
- [ ] Implement Yield Monitor (new)
- [ ] Implement Software Package Manager (new)
- [ ] Implement Client Monitor (new)
- [ ] IPC/communication layer (if designed)

⏳ **Testing & Deployment:**
- [ ] All 4 applications launch independently
- [ ] Shared framework reduces code duplication by 60%+
- [ ] Applications can access same API/client
- [ ] Inter-app communication functional (if implemented)
- [ ] Documentation and examples

---

## 📊 Metrics

- **Target Applications:** 4 (Configurator, Yield Monitor, Package Manager, Monitor)
- **Shared Framework Goal:** 60%+ code reuse across apps
- **Current State:** 1 tightly coupled GUI (configurator)
- **Target State:** Independent apps + shared `pywats_ui` framework
- **Breaking Changes:** Import paths only (user-facing APIs stable)

---

## 🔗 Quick Links

- [Analysis](01_ANALYSIS.md) - Problem statement and architecture review
- [Implementation Plan](02_IMPLEMENTATION_PLAN.md) - Phased execution strategy
- [Progress](03_PROGRESS.md) - Session notes and discoveries
- [TODO](04_TODO.md) - Task checklist
- [Original Request](../../make_this_a_project/GUI_CLIENT_SEPARATION.md)

---

## 📝 Notes

**C# Reference Applications:**
- Client Configurator: Service setup, station configuration
- Yield Monitor: Real-time analytics dashboard
- Software Package Manager: Distribution and deployment
- Client Monitor: Service health and diagnostics

**Python Implementation Considerations:**
- PySide6 for Qt-based GUI framework
- Shared base classes (BaseApplication, BaseMainWindow)
- Common dialogs and widgets library
- Theme/styling system
- Optional IPC via QLocalSocket, message bus, or REST API
- Plugin architecture for extensibility

This project will create **NEW applications** (Yield Monitor, Package Manager, Monitor) while refactoring the existing configurator into the new framework.
