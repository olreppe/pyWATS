# Target Platforms for Out-of-the-Box Installation

**Context**

This document prioritizes operating system platforms for a non-technical, factory-floor–friendly installation of a test-equipment connectivity service (ICT, AIO, FCT, EOL, AOI, X-ray, SPI, etc.).

Key assumptions:
- A **separate, dedicated Windows desktop implementation already exists** and is *not* the priority here.
- Development and testing currently happen on Windows, which biases visibility but not strategic importance.
- The goal is **maximum deployment coverage with minimum installer friction** for non-technical users.
- Long lifecycle, stability, and service-style operation matter more than developer convenience.

---

## Priority 1 — Immediate Gaps to Close

These are platforms you are *very likely already encountering* and where weakness causes real adoption pain.

### 1. Windows Server 2019 / 2022 (64-bit)
**Why this is critical**
- Commonly used for centralized data collectors, gateways, and on‑prem TDM components
- Preferred by IT departments over desktop Windows
- Designed for headless, long-running services

**Typical usage**
- Aggregation point for multiple testers
- Secure integration point to MES / QMS / SPC systems

**Risk if unsupported well**
- IT resistance
- Manual installs, brittle service setups
- Lost enterprise deals

---

### 2. Windows 10 / 11 IoT Enterprise (LTSC)
**Why this is critical**
- Extremely common on AOI, SPI, X-ray, and inline inspection systems
- Long lifecycle (10+ years)
- Locked-down environments with limited admin access

**Typical usage**
- Embedded PCs supplied by test equipment vendors
- Systems that rarely get OS upgrades

**Risk if unsupported well**
- Installer failures due to missing assumptions
- Problems with services, permissions, or updates
- Support escalations that are hard to debug remotely

---

## Priority 2 — High-Return Cross-Platform Coverage

These platforms significantly expand coverage beyond Windows without exploding support cost.

### 3. Ubuntu LTS (20.04 / 22.04 / 24.04)
**Why this matters**
- Most common Linux distribution in manufacturing
- Frequently used for custom FCT rigs and gateways
- Predictable release and support cycles

**Typical usage**
- Headless collectors
- Edge devices
- Custom-built testers

**Why start here for Linux**
- Best documentation
- Best community support
- Lowest friction for packaging and upgrades

---

### 4. Debian Stable
**Why this matters**
- Used in embedded and appliance-style systems
- Valued for stability over novelty

**Typical usage**
- Vendor-supplied test controllers
- Industrial PCs with minimal UI

**Note**
If Ubuntu LTS works correctly, Debian is usually a small incremental step.

---

## Priority 3 — Enterprise and Regulated Manufacturing

These platforms matter in automotive, aerospace, medical, and highly regulated environments.

### 5. Red Hat Enterprise Linux (RHEL)
**Why this matters**
- Corporate IT standard in many global manufacturers
- Long validation and qualification cycles

**Typical usage**
- Centralized collectors
- Secure plant-level servers

**Key consideration**
Packaging and support expectations are higher than on community distros.

---

### 6. Rocky Linux / AlmaLinux
**Why this matters**
- Practical replacements for CentOS
- Increasingly common due to cost sensitivity

**Typical usage**
- Same roles as RHEL, but without licensing costs

**Note**
Supporting one usually gives you the other with minimal extra work.

---

## Priority 4 — Packaging and Deployment Multipliers

These are not OSes themselves but dramatically reduce friction in certain environments.

### 7. Virtual Machine Appliance (Windows Server or Linux)
**Why this matters**
- "Install once, deploy everywhere"
- Avoids touching tester OS images

**Typical usage**
- Plants with strict IT controls
- Quick pilots and proofs of concept

---

### 8. Docker (Linux-first)
**Why this matters**
- Increasingly used for central services
- Excellent for CI/CD and reproducibility

**Important limitation**
Docker is **not suitable as the only option** for non-technical users or test stations.

---

## De-Prioritized (For This Product Line)

These platforms offer low return for the target audience:

- Windows desktop editions (already covered elsewhere)
- macOS
- ARM-based Windows
- Exotic or niche Linux distributions
- RTOS / microcontroller environments

---

## Strategic Summary

If you want the **biggest practical impact**, focus in this order:

1. Harden Windows Server support
2. Validate and explicitly support Windows IoT Enterprise
3. Deliver a rock-solid Ubuntu LTS experience
4. Expand to Debian and enterprise Linux where required

A platform that installs cleanly, runs quietly as a service, and never needs operator attention will win more deployments than one that is merely "cross-platform" on paper.

---

*This document is intended to guide roadmap and installer strategy discussions and can be updated as field data accumulates.*

