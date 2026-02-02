# TODO: Cross-Platform Service Launcher

**Related Docs:**
- [README](README.md) | [Analysis](01_ANALYSIS.md) | [Plan](02_IMPLEMENTATION_PLAN.md) | [Progress](03_PROGRESS.md)

---

## ✅ Completed
- [x] Project structure setup (README, ANALYSIS, PLAN, PROGRESS, TODO)

## 🚧 In Progress
- [ ] **Phase 1: ServiceManager Core** - **CURRENT**

## 🧠 Planned

### Phase 1: ServiceManager Core (Days 1-2)
- [ ] Step 1.1: Create ServiceManager base class with platform detection
- [ ] Step 1.2: Implement Windows service start/stop methods
- [ ] Step 1.3: Implement Linux service start/stop methods
- [ ] Step 1.4: Implement macOS service start/stop methods

### Phase 2: CLI Commands (Days 2-3)
- [ ] Step 2.1: Create CLI entry point with click framework
- [ ] Step 2.2: Implement 'start' command with lock cleanup
- [ ] Step 2.3: Implement 'stop' command with graceful shutdown
- [ ] Step 2.4: Implement 'status' and 'restart' commands

### Phase 3: Decouple Tray from Service (Days 3-4)
- [ ] Step 3.1: Make tray icon optional (Qt import protection)
- [ ] Step 3.2: Add 'gui' command to launch dashboard
- [ ] Step 3.3: Update tray icon to use ServiceManager

### Phase 4: Testing & Documentation (Days 4-5)
- [ ] Step 4.1: Create unit tests for ServiceManager
- [ ] Step 4.2: Create integration tests for CLI commands
- [ ] Step 4.3: Update documentation (installation, getting-started, README)
- [ ] Step 4.4: Update pyproject.toml entry points and dependencies

### Phase 5: Installer Integration (Day 5)
- [ ] Step 5.1: Update Windows installer (Start Menu shortcuts)
- [ ] Step 5.2: Update Linux packages (Debian, RPM)
- [ ] Step 5.3: Update macOS package

## ⏸️ Blocked/Deferred
(none currently)

---

**Last Updated:** February 2, 2026 14:39
**Total Tasks:** 19
**Completed:** 1
**Remaining:** 18
