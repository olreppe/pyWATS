# pyWATS Package Overview

This document provides an overview of the pyWATS package ecosystem and helps you choose the right package for your needs.

## Package Structure

pyWATS is distributed as four separate pip packages, each serving different use cases:

### 1. pywats (Core API Library)
**What it is**: Core Python library for WATS API integration

**Use when**:
- You want to integrate WATS into your own Python application
- You need programmatic access to WATS data
- You're building custom automation or test frameworks
- You want to create test reports programmatically

**Dependencies**: Minimal (httpx, pydantic, python-dateutil, attrs)

**Installation**:
```bash
pip install pywats
```

**Quick Example**:
```python
from pywats import pyWATS, WATSFilter

api = pyWATS(base_url="https://wats.example.com", token="token")
products = api.product.get_products()
```

---

### 2. pywats-client-service (Client Service Framework)
**What it is**: Core client services including converter framework, queue management, and background services

**Use when**:
- You're building a custom client application
- You need converter management capabilities
- You want queue processing and retry logic
- You're creating a custom GUI or CLI tool

**Dependencies**: pywats, watchdog, aiofiles

**Installation**:
```bash
pip install pywats-client-service
```

**Note**: This is typically used as a dependency, not directly installed by end users.

---

### 3. pywats-client-headless (Headless Client)
**What it is**: Complete client with CLI and HTTP API, no GUI required

**Use when**:
- Running on servers without display (Linux servers, Raspberry Pi)
- Automating test data collection in CI/CD pipelines
- Managing test stations remotely via HTTP API
- Setting up as system service/daemon
- Embedded systems and IoT devices
- Docker containers

**Dependencies**: pywats, pywats-client-service, aiohttp

**Installation**:
```bash
pip install pywats-client-headless
```

**Quick Example**:
```bash
# Initialize and start
pywats-client config init
pywats-client start --api --api-port 8765

# Control via HTTP
curl http://localhost:8765/status
```

---

### 4. pywats-client-gui (Desktop GUI Application)
**What it is**: Full-featured desktop application with Qt GUI

**Use when**:
- You need a user-friendly desktop application
- Running on Windows, macOS, or Linux desktop
- You want visual management of converters and queue
- Operators need a graphical interface
- You need real-time status monitoring

**Dependencies**: pywats, pywats-client-service, PySide6

**Installation**:
```bash
pip install pywats-client-gui
```

**Quick Example**:
```bash
# Launch GUI
pywats-client-gui
```

---

## Dependency Tree

```
pywats (core API)
    ↓
pywats-client-service (client framework)
    ↓
    ├── pywats-client-headless (CLI + HTTP API)
    │   - For: Servers, Raspberry Pi, automation
    │   - No GUI dependencies
    │
    └── pywats-client-gui (Desktop application)
        - For: Desktop users
        - Requires: Qt/PySide6
```

## Comparison Matrix

| Feature | pywats | client-service | client-headless | client-gui |
|---------|--------|----------------|-----------------|------------|
| WATS API Access | ✅ | ✅ | ✅ | ✅ |
| Converter Framework | ❌ | ✅ | ✅ | ✅ |
| Queue Management | ❌ | ✅ | ✅ | ✅ |
| CLI Interface | ❌ | ❌ | ✅ | ❌ |
| HTTP API | ❌ | ❌ | ✅ | ❌ |
| Desktop GUI | ❌ | ❌ | ❌ | ✅ |
| Daemon Mode | ❌ | ❌ | ✅ | ❌ |
| Headless Operation | ✅ | ✅ | ✅ | ❌ |
| Systemd Integration | ❌ | ❌ | ✅ | ❌ |
| Qt Dependencies | ❌ | ❌ | ❌ | ✅ |
| Raspberry Pi Ready | ✅ | ✅ | ✅ | ⚠️ |

✅ = Supported | ❌ = Not applicable | ⚠️ = Possible but not recommended

## Use Case Examples

### Example 1: Custom Test Script
**Goal**: Submit test results from your test framework

**Package**: `pywats`

```bash
pip install pywats
```

```python
from pywats import pyWATS
from pywats.models import UUTReport

api = pyWATS(base_url="https://wats.example.com", token="token")
report = UUTReport(pn="PART-001", sn="SN-12345", ...)
api.report.submit_uut_report(report)
```

---

### Example 2: Raspberry Pi Test Station
**Goal**: Automated test data collection on Raspberry Pi

**Package**: `pywats-client-headless`

```bash
pip install pywats-client-headless

# Configure
pywats-client config init

# Run as service
sudo systemctl enable pywats-client
sudo systemctl start pywats-client

# Access from PC: http://raspberry-pi.local:8765/status
```

---

### Example 3: Desktop Test Station (with operators)
**Goal**: User-friendly desktop application for test operators

**Package**: `pywats-client-gui`

```bash
pip install pywats-client-gui
pywats-client-gui
```

Operators can:
- See real-time status
- Configure converters visually
- Monitor queue
- View logs
- Troubleshoot issues

---

### Example 4: CI/CD Integration
**Goal**: Automated testing in Jenkins/GitHub Actions

**Package**: `pywats-client-headless`

```yaml
# GitHub Actions example
- name: Setup WATS Client
  run: |
    pip install pywats-client-headless
    pywats-client config set service_address ${{ secrets.WATS_URL }}
    pywats-client config set api_token ${{ secrets.WATS_TOKEN }}

- name: Submit Test Results
  run: |
    pywats-client start --no-gui
```

---

### Example 5: Custom GUI Application
**Goal**: Build your own GUI with custom features

**Package**: `pywats` + `pywats-client-service`

```bash
pip install pywats pywats-client-service
```

You get:
- Full API access
- Converter framework
- Queue management
- You build your own UI (Tkinter, web, etc.)

---

## Installation Decision Tree

```
Do you need a GUI?
├─ Yes → pywats-client-gui
└─ No
   ├─ Need CLI/HTTP API? 
   │  └─ Yes → pywats-client-headless
   └─ No
      ├─ Need converters/queue?
      │  └─ Yes → pywats-client-service
      └─ No → pywats (core API)
```

## Version Compatibility

All packages use synchronized version numbers:
- Current: 2.0.0
- All packages with the same version are tested together
- Mix and match versions at your own risk

## System Requirements

### pywats
- Python >= 3.8
- Works on: Linux, Windows, macOS, Raspberry Pi, embedded systems
- RAM: <50MB
- No display required

### pywats-client-service
- Python >= 3.8
- Works on: Linux, Windows, macOS, Raspberry Pi, embedded systems
- RAM: <100MB
- No display required

### pywats-client-headless
- Python >= 3.8
- Works on: Linux, Windows, macOS, Raspberry Pi, embedded systems
- RAM: <150MB
- No display required

### pywats-client-gui
- Python >= 3.8
- Works on: Linux (X11/Wayland), Windows 10+, macOS 10.15+
- RAM: ~200-300MB (Qt libraries)
- Requires: Display, windowing system
- Not recommended for: Raspberry Pi (GUI too heavy)

## License

All packages: MIT License

## Support & Documentation

- **Homepage**: https://github.com/olreppe/pyWATS
- **Issues**: https://github.com/olreppe/pyWATS/issues
- **Docs**: https://github.com/olreppe/pyWATS/tree/main/docs

### Package-Specific Docs
- [pywats API Docs](https://github.com/olreppe/pyWATS/blob/main/docs/ARCHITECTURE.md)
- [pywats-client-headless Guide](https://github.com/olreppe/pyWATS/blob/main/src/pywats_client/control/HEADLESS_GUIDE.md)
- [pywats-client-gui Guide](https://github.com/olreppe/pyWATS/blob/main/src/pywats_client/GUI_CONFIGURATION.md)

## Migration from Monorepo

If you previously used a monorepo installation:

**Before**:
```bash
git clone https://github.com/olreppe/pyWATS.git
pip install -e .
```

**Now**:
```bash
# Choose based on your needs
pip install pywats                  # API only
pip install pywats-client-headless  # CLI/API
pip install pywats-client-gui       # Desktop GUI
```

## FAQ

**Q: Which package do I need?**
A: See the decision tree above, or start with `pywats-client-gui` for desktop, `pywats-client-headless` for servers.

**Q: Can I install multiple packages?**
A: Yes, but typically you only need one client package (headless OR gui, not both).

**Q: Do I need to install dependencies manually?**
A: No, pip automatically installs all dependencies.

**Q: Can I use pywats without a client?**
A: Yes! `pywats` is the core API library and can be used standalone in your own applications.

**Q: Which is better for Raspberry Pi?**
A: Use `pywats-client-headless`. The GUI version works but is heavy due to Qt.

**Q: Can I run the headless client on Windows?**
A: Yes, it works on Windows, Linux, and macOS.

**Q: Do I need pywats-client-service?**
A: It's automatically installed as a dependency of headless/GUI clients. You rarely install it directly.
