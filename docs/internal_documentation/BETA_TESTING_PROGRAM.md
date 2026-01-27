# pyWATS Beta Testing Program

> **Version**: 1.0  
> **Last Updated**: January 2026

This document provides guidelines for running a beta testing program for pyWATS, with special focus on platforms that cannot be fully tested in CI environments.

---

## Overview

### Why Beta Testing?

Despite comprehensive CI testing, some platform-specific issues can only be discovered on real hardware in production-like environments:

| Platform | CI Coverage | Beta Need | Primary Concerns |
|----------|-------------|-----------|------------------|
| Windows 10/11 | 95% | Low | Antivirus, UAC variations |
| Ubuntu/Debian | 90% | Low | Desktop vs server differences |
| **RHEL/Rocky** | 75% | **High** | SELinux policy gaps |
| **macOS** | 80% | **Medium** | Gatekeeper, code signing |
| **Raspberry Pi** | 60% | **Medium** | ARM performance, memory |
| Docker | 95% | Low | Volume permissions |

### Beta Testing Goals

1. **Validate SELinux policies** on RHEL/Rocky Linux in enforcing mode
2. **Test macOS Gatekeeper** behavior without code signing
3. **Verify ARM64 performance** on Raspberry Pi 4/5
4. **Collect real-world feedback** on installation experience
5. **Build FAQ** from actual customer issues

---

## Beta Tester Recruitment

### Ideal Beta Testers

| Criteria | Requirement | Priority |
|----------|-------------|----------|
| Platform coverage | At least 1 tester per critical platform | Critical |
| Technical ability | Can run commands, read logs, report issues | High |
| Production similarity | Environment similar to typical customer | High |
| Availability | Can respond within 48 hours | Medium |
| WATS familiarity | Existing WATS users preferred | Low |

### Recruitment Channels

1. **Existing Customers** - Contact customers who:
   - Have requested Python/Linux support
   - Are using WATS on non-Windows platforms
   - Have expressed interest in beta programs

2. **Internal Teams** - Ask colleagues who have:
   - RHEL/Rocky test machines
   - Mac development machines
   - Raspberry Pi devices

3. **Partner Organizations** - Reach out to:
   - Integration partners
   - OEM customers
   - Technical universities

### Minimum Beta Cohort

| Platform | Minimum Testers | Ideal Testers |
|----------|-----------------|---------------|
| RHEL 8/9 (SELinux) | 2 | 4 |
| Rocky/Alma Linux | 1 | 2 |
| macOS (Intel) | 1 | 2 |
| macOS (Apple Silicon) | 1 | 2 |
| Raspberry Pi | 1 | 2 |
| Ubuntu Server | 1 | 2 |
| **Total** | **7** | **14** |

---

## Beta Program Structure

### Phase 1: Installation Testing (Week 1)

**Goal**: Verify installation works on each platform

**Tasks for Testers**:
1. Download pyWATS package
2. Run installation command
3. Run `python scripts/validate_install.py --full`
4. Report results (pass/fail + logs)

**Expected Time**: 30 minutes per tester

### Phase 2: Service Testing (Week 2)

**Goal**: Verify service starts and runs correctly

**Tasks for Testers**:
1. Install as system service
2. Configure with test WATS server
3. Verify service starts on boot
4. Run `pywats-client diagnose`
5. Leave running for 24 hours
6. Check logs for errors

**Expected Time**: 1-2 hours setup + passive monitoring

### Phase 3: Integration Testing (Week 3)

**Goal**: Verify end-to-end functionality

**Tasks for Testers**:
1. Submit test report to WATS
2. Monitor file folder for automatic upload
3. Test service restart scenarios
4. Test network disconnection/reconnection

**Expected Time**: 2-3 hours

### Phase 4: Feedback Collection (Week 4)

**Goal**: Gather insights and documentation

**Tasks for Testers**:
1. Complete feedback survey
2. Document any workarounds used
3. Rate difficulty of each step
4. Suggest documentation improvements

**Expected Time**: 30 minutes

---

## Platform-Specific Testing

### RHEL/Rocky Linux with SELinux

**This is the highest-priority beta testing area.**

#### SELinux Testing Checklist

```bash
# 1. Verify SELinux is enforcing
getenforce
# Expected: Enforcing

# 2. Install pyWATS
sudo dnf install ./pywats-client-*.rpm
# OR: pip install pywats-api[client-headless]

# 3. Install SELinux policy
cd selinux/
sudo ./install-selinux.sh

# 4. Start service
sudo systemctl enable pywats-client
sudo systemctl start pywats-client

# 5. Check for AVC denials
sudo ausearch -m AVC -ts recent

# 6. If denials found, generate policy additions
sudo audit2allow -a -M pywats_local
# Report the generated policy to development team
```

#### Expected Issues

| Issue | Likelihood | Detection | Resolution |
|-------|------------|-----------|------------|
| Network connection denied | High | `ausearch -m AVC` | Add network permission to policy |
| File write denied | Medium | Service won't start | Add file context |
| Socket creation denied | Medium | Health endpoint fails | Add socket permission |
| Exec denied | Low | Python won't run | Check file contexts |

#### Feedback Required

- [ ] `getenforce` output
- [ ] Any AVC denials from `ausearch`
- [ ] Service status after 24 hours
- [ ] `audit2allow` output for any denials

### macOS Testing

#### Gatekeeper Testing Checklist

```bash
# 1. Download pyWATS
pip install pywats-api[client]

# 2. Check for Gatekeeper warnings
# - Note any dialogs that appear
# - Screenshot any security warnings

# 3. If blocked, try:
# System Preferences > Security & Privacy > General
# Click "Allow Anyway" for pyWATS

# 4. Test launchd service
# Follow MACOS_SERVICE.md instructions

# 5. Run diagnostics
pywats-client diagnose
```

#### Expected Issues

| Issue | Likelihood | Resolution |
|-------|------------|------------|
| Gatekeeper blocks Python | Medium | System Preferences allow |
| Keychain access prompt | High | Click "Allow" or "Always Allow" |
| Network permission dialog | High | Click "Allow" |
| launchd not loading | Low | Check plist syntax |

#### Feedback Required

- [ ] macOS version and chip (Intel/Apple Silicon)
- [ ] Screenshots of any security dialogs
- [ ] Gatekeeper workaround steps needed
- [ ] launchd load success/failure

### Raspberry Pi Testing

#### Raspberry Pi Testing Checklist

```bash
# 1. Verify 64-bit OS
uname -m
# Expected: aarch64

# 2. Check available memory
free -h
# Note: 4GB+ recommended

# 3. Install pyWATS (headless)
pip install pywats-api[client-headless]

# 4. Run diagnostics
pywats-client diagnose

# 5. Install as service
sudo cp pywats-client.service /etc/systemd/system/
sudo systemctl enable pywats-client
sudo systemctl start pywats-client

# 6. Monitor resource usage
htop  # Check CPU and memory during operation
```

#### Expected Issues

| Issue | Likelihood | Resolution |
|-------|------------|------------|
| Out of memory | High (2GB models) | Recommend 4GB+ |
| Slow performance | Medium | Expected, document limits |
| 32-bit OS used | Medium | Require 64-bit OS |
| SD card I/O bottleneck | Medium | Recommend USB storage |

#### Feedback Required

- [ ] Raspberry Pi model (4/5, RAM size)
- [ ] OS version (64-bit confirmed)
- [ ] Memory usage during operation
- [ ] Startup time
- [ ] Any performance issues

---

## Feedback Collection

### Issue Reporting Template

When testers encounter issues, ask them to provide:

```markdown
## Environment
- Platform: [e.g., RHEL 9.2, macOS 14.2, Raspberry Pi 5 8GB]
- Python version: [e.g., 3.11.5]
- pyWATS version: [e.g., 0.9.5]
- Installation method: [pip / rpm / deb]

## Issue Description
[What happened]

## Expected Behavior
[What should have happened]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Diagnostic Output
[Paste output of: pywats-client diagnose --json]

## Logs
[Paste relevant log excerpts]

## Screenshots
[If applicable]

## Workaround
[If you found one]
```

### Feedback Survey

Send at the end of beta:

```
1. How would you rate the installation experience? (1-5)

2. How long did installation take?
   [ ] < 15 minutes
   [ ] 15-30 minutes
   [ ] 30-60 minutes
   [ ] > 1 hour

3. Did you need to use any workarounds? (Yes/No)
   If yes, describe:

4. How clear was the documentation? (1-5)

5. What would you improve about the documentation?

6. Did you encounter any issues not covered in docs? (Yes/No)
   If yes, describe:

7. Would you recommend pyWATS to others on your platform? (1-5)

8. Any other feedback?
```

---

## Triage and Resolution

### Issue Priority Matrix

| Severity | Impact | Example | Response Time |
|----------|--------|---------|---------------|
| P0 Critical | Blocks installation | Service won't start | 24 hours |
| P1 High | Major feature broken | Reports not uploading | 48 hours |
| P2 Medium | Workaround available | SELinux denial with fix | 1 week |
| P3 Low | Minor inconvenience | Confusing error message | Next release |

### Resolution Workflow

1. **Receive issue report** → Create internal tracking ticket
2. **Reproduce if possible** → Document reproduction steps
3. **Analyze root cause** → Determine fix approach
4. **Implement fix** → Code change or documentation update
5. **Build beta update** → Provide updated package to tester
6. **Verify fix** → Tester confirms resolution
7. **Document** → Update FAQ, troubleshooting guide

---

## Communication

### Weekly Beta Update

Send every Monday during beta:

```
Subject: pyWATS Beta Week [N] Update

Hi beta testers,

## Progress
- [N] testers completed Phase [X]
- [N] issues reported, [N] resolved

## This Week's Focus
- [Testing focus for this week]

## Known Issues
- [Issue 1] - Workaround: [description]
- [Issue 2] - Fix in progress

## Action Items
- [What testers should do this week]

## Resources
- Diagnose command: pywats-client diagnose
- Validate script: python scripts/validate_install.py
- Docs: [link to documentation]

Thanks for your help!
```

### Slack/Teams Channel

Create a dedicated channel for beta testers:
- Quick questions and answers
- Real-time troubleshooting
- Sharing workarounds
- Community building

---

## Timeline

| Week | Phase | Activities |
|------|-------|------------|
| -2 | Prep | Recruit testers, prepare packages |
| -1 | Prep | Send welcome emails, share access |
| 1 | Install | Installation testing |
| 2 | Service | Service operation testing |
| 3 | Integration | End-to-end testing |
| 4 | Feedback | Survey and documentation |
| 5 | Analysis | Compile results, plan fixes |
| 6 | Fixes | Implement critical fixes |
| 7+ | GA | General availability release |

---

## Success Criteria

### Minimum for GA Release

- [ ] At least 1 successful RHEL installation with SELinux enforcing
- [ ] SELinux policy covers all necessary permissions
- [ ] At least 1 successful macOS installation
- [ ] Gatekeeper workaround documented
- [ ] At least 1 successful Raspberry Pi installation
- [ ] Resource requirements documented
- [ ] All P0/P1 issues resolved
- [ ] FAQ covers common issues

### Quality Targets

| Metric | Target |
|--------|--------|
| Installation success rate | > 90% first attempt |
| Service uptime (24h test) | > 99% |
| Documentation clarity score | > 4.0 / 5.0 |
| Tester recommendation score | > 4.0 / 5.0 |

---

## Appendix: Tester Welcome Email

```
Subject: Welcome to the pyWATS Beta Testing Program

Hi [Name],

Thank you for joining the pyWATS beta testing program! Your feedback will help us ensure pyWATS works reliably on [Platform].

## Getting Started

1. Download pyWATS: [link]
2. Follow installation guide: [link]
3. Run validation: python scripts/validate_install.py
4. Report any issues: [link to issue template]

## Your Testing Environment

Please confirm:
- Platform: [Platform]
- Version: [OS version]
- Python: [Python version]

## Support

- Documentation: [link]
- Issue reporting: [link]
- Slack channel: [link] (optional)
- Email: [beta-support@example.com]

## Timeline

- Week 1: Installation testing
- Week 2: Service testing
- Week 3: Integration testing
- Week 4: Feedback survey

Expected time commitment: 3-5 hours total over 4 weeks.

Thank you for helping make pyWATS better!

Best regards,
The pyWATS Team
```
