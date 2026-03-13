
# GUI/Client-Service Architecture Cleanup for Beta Release

**Created:** February 14, 2026, 15:45  
**Last Updated:** February 15, 2026, 10:00  
**Status:** ✅ Complete (100%)

---

## Problem Statement

This project merges the GUI cleanup for beta release with a full audit and refactor of the client/service architecture and test environment. The goal is to ensure:

1. The GUI is clean, usable, and production-ready for beta
2. The client/service architecture supports multi-instance setups (two-client model, A/B)
3. Test fixtures and environment are isolated, defaulting to client A unless multi-client features are tested
4. Client A is maintained as a persistent, simulated live installation: service autostarts on system startup, tray icon is always visible, and the running instance uses the latest code
4. Service > client > UI startup sequence is enforced in all tests and usage
5. Server URL and tokens remain persistent in all configs
6. Documentation is updated for maintainers

**User Requirements**:
> "I want to make sure the GUI is cleaned up and working. I have some objections to the whole gui, with the pages and their contents. Also, the client/service/test setup must be robust and easy to maintain."
> "I want to make sure the GUI is cleaned up and working. I have some objections to the whole gui, with the pages and their contents."

---



## Persistent Client A Installation

**Goal:**
Maintain client A as a simulated live installation:
- Service for client A autostarts on system startup (Windows Service, systemd, or launchd)
- Tray icon is always visible when service/client/GUI is running, even outside development
- Installation uses the most recent code (auto-updates with project changes)
- Useful for real-world testing and as a reference for production deployments

### Primary Goals
1. Fix page scaling issues (readable at all window sizes)
2. Make Dashboard the default starting page
3. Add client metadata to Dashboard (name, station, location, purpose, GPS toggle)
4. Add Disconnect button with reconnection flow
5. Disable non-essential tabs (rootcause, asset, product, production, software)
6. Reduce prominence of credentials/tokens (move to Advanced)
7. Enforce two-client (A/B) model for all tests and fixtures
8. Ensure service > client > UI startup for all tests and usage
9. Validate server URL/token persistence in all configs
10. Update documentation for maintainers
11. Ensure client A is always running as a persistent, autostarting, live installation with tray icon

### Secondary Goals
11. Assess multi-server config support (separate instances per server)
12. Clean up redundant information across pages
13. Improve overall UX consistency
14. Remove or refactor any inter-client DB coordination logic

---


## Success Criteria

- [ ] Dashboard shows: client name, station name, location, purpose, GPS toggle
- [ ] Dashboard is the default starting page
- [ ] All pages scale properly (readable at 800x600 minimum)
- [ ] Only relevant tabs visible: Dashboard, Converters, Connection, Setup, Location, Log, About
- [ ] Disconnect button prominently visible, reconnection flow works
- [ ] Connection credentials moved to Advanced section
- [ ] Multi-server config assessment complete with recommendation
- [ ] Zero regressions in existing functionality
- [ ] Only two client fixtures (A/B) used in all tests
- [ ] Default to client A for all tests unless multi-client features are tested
- [ ] All directory references and services set up/cleaned for both clients in tests
- [ ] Service > client > UI startup enforced in all tests and usage
- [ ] Server URL and tokens remain in all configs
- [ ] Documentation updated to reflect merged architecture

---


## Scope

### In Scope
- Main window tab organization
- Dashboard page redesign
- Connection page simplification
- Scaling/sizing fixes
- Tab visibility management
- Multi-server config analysis
- Client/service architecture audit and refactor
- Test fixture and environment cleanup (two-client model)
- Documentation and config audit for client/service/test setup

### Out of Scope
- New features unrelated to usability or architecture/test conformance
- Complete UI redesign
- Theme changes
- Performance optimizations (unless blocking)

---


## Timeline

**Estimated Effort**: 12-16 hours  
**Target Completion**: February 17, 2026

---


## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing page layouts | High | Test all pages after changes |
| Multi-server config complexity | Medium | Start with analysis, defer if complex |
| Scaling fixes affect styling | Medium | Test on multiple screen sizes |
| User workflow disruption | Low | Keep changes incremental |
| Test fixture refactor breaks CI | Medium | Run all tests after fixture changes |
| Service/client startup sequence errors | Medium | Add integration tests for startup |
| Config persistence bugs | Medium | Add config validation tests |

---


## Next Steps

1. Update analysis and implementation plan to include merged architecture/test requirements
2. Add/merge TODOs for client/service/test environment cleanup
3. Mark project as ready to start
4. Begin with test fixture and startup sequence audit
5. Proceed with GUI/UX cleanup phases
6. Update documentation as changes are made

---


**Project Lead**: AI Agent  
**Stakeholder**: User (ola.lund.reppe)
