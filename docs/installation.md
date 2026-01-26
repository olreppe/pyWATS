# PyWATS Installation Guide

Complete guide for installing PyWATS from PyPI with different configurations.

## 📦 Core Package

### Basic Installation
```bash
pip install pywats-api
```

**What's Included:**
- Core API library (`pywats`)
- HTTP client (httpx)
- Data validation (pydantic 2.0+)
- Date utilities (python-dateutil)
- Python 3.10+

**Use this for:**
- Writing Python scripts to interact with WATS API
- Building custom integrations
- Server-side automation

---

## 🎨 Optional Components

### 1. Full GUI Client (Desktop)

```bash
pip install pywats-api[client]
```

**Additional Dependencies:**
- PySide6 (Qt GUI framework)
- watchdog (file monitoring)
- aiofiles (async file operations)

**Platforms:** Windows, macOS, Linux desktop

**Use this for:**
- Desktop application with GUI
- Interactive converter configuration
- Visual report queue management

**Launch:**
```bash
pywats-client
```
or
```bash
python -m pywats_client
```

---

### 2. Headless Client (Servers/Raspberry Pi)

```bash
pip install pywats-api[client-headless]
```

**Additional Dependencies:**
- watchdog (file monitoring)
- aiofiles (async file operations)
- **No Qt dependencies**

**Platforms:** Linux servers, Raspberry Pi, embedded systems

**Use this for:**
- Server deployments
- Embedded systems
- Headless automation
- Systems without display

**Launch:**
```bash
pywats-client --headless
```

**Control via HTTP API:**
```bash
# Start with HTTP API
pywats-client start --api --api-port 8765

# Check status
curl http://localhost:8765/status

# Remote control
curl -X POST http://localhost:8765/restart
```

---

### 3. Development Tools

```bash
pip install pywats-api[dev]
```

**Additional Dependencies:**
- pytest, pytest-cov (testing)
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)

**Use this for:**
- Contributing to PyWATS
- Running tests
- Code quality checks

**Run Tests:**
```bash
pytest
pytest --cov=src --cov-report=html
```

---

## 🚀 Quick Start Matrix

| Use Case | Install Command | Size |
|----------|----------------|------|
| API Library Only | `pip install pywats-api` | ~5 MB |
| Desktop Client | `pip install pywats-api[client]` | ~150 MB |
| Server/Raspberry Pi | `pip install pywats-api[client-headless]` | ~8 MB |
| Development | `pip install pywats-api[dev]` | ~30 MB |
| Everything | `pip install pywats-api[client,dev]` | ~180 MB |

---

## 🔧 Configuration

### API Credentials

**Option 1: Environment Variables** (Recommended)
```bash
export WATS_BASE_URL="https://your-server.wats.com"
export WATS_AUTH_TOKEN="your_base64_encoded_token"
```

**Option 2: In Code**
```python
from pywats import pyWATS

api = pyWATS(
    base_url="https://your-server.wats.com",
    token="your_base64_encoded_token"
)
```

### Token Generation

Get your authentication token from WATS:
1. Log into WATS web interface
2. Go to Settings → API Access
3. Generate a new API token
4. Copy the base64-encoded token

---

## 📚 Next Steps

After installation:

1. **Test Connection:**
   ```python
   from pywats import pyWATS
   
   api = pyWATS(base_url="...", token="...")
   if api.test_connection():
       print("Connected!")
   ```

2. **Read Documentation:**
   - [README.md](../README.md) - Getting started
   - [CHANGELOG.md](../CHANGELOG.md) - Version history
   - [INDEX.md](INDEX.md) - Detailed documentation

3. **Run Examples:**
   ```bash
   python docs/examples/basic_usage.py
   ```

4. **Configure Client:**
   ```bash
   pywats-client config init
   ```

---

## 🔄 Upgrading

Update to the latest version:
```bash
pip install --upgrade pywats-api
```

Update with specific extras:
```bash
pip install --upgrade pywats-api[client]
```

---

## 🐛 Troubleshooting

### Import Errors
```bash
# Verify installation
pip show pywats-api

# Reinstall if needed
pip uninstall pywats-api
pip install pywats-api
```

### Qt/GUI Issues (Client)
```bash
# Install full client extras
pip install pywats-api[client]

# Verify PySide6
python -c "from PySide6 import QtWidgets"
```

---

## 📦 Package Information

- **PyPI:** https://pypi.org/project/pywats-api/
- **GitHub:** https://github.com/olreppe/pyWATS
- **Current Version:** 0.1.0b2
- **License:** MIT
- **Python:** 3.10+
- **WATS Server:** 2025.3.9.824 or later

---

## 🆘 Support

- **Issues:** https://github.com/olreppe/pyWATS/issues
- **Email:** support@virinco.com
- **Website:** https://wats.com
