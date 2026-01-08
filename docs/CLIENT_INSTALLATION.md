# PyWATS Client - End User Installation Guide

This guide explains how the PyWATS Client is installed and organized on your computer, and how to run it.

## Table of Contents
- [What is PyWATS Client?](#what-is-pywats-client)
- [Installation Options](#installation-options)
- [File Organization](#file-organization)
- [Running the Client](#running-the-client)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## What is PyWATS Client?

PyWATS Client is a desktop application that connects your test station to a WATS server. It:
- **Collects test reports** from your test equipment
- **Converts** them to WATS format using configurable converters
- **Uploads** them to your WATS server
- **Manages** serial numbers and product information
- **Distributes** software packages to test stations

The client can run in two modes:
- **GUI Mode** - Windows/Mac/Linux desktop application with graphical interface
- **Headless Mode** - Command-line only for servers, Raspberry Pi, embedded systems

---

## Installation Options

### Option 1: GUI Desktop Application (Windows/Mac/Linux)

For test stations with a display and keyboard:

```bash
pip install pywats-api[client]
```

**What gets installed:**
- Python package in your Python environment
- GUI application (uses PySide6/Qt)
- Command-line tools
- Background services

**Requirements:**
- Python 3.10 or later
- Display/monitor
- 200 MB disk space

### Option 2: Headless (Servers, Raspberry Pi)

For automated systems without a display:

```bash
pip install pywats-api[client-headless]
```

**What gets installed:**
- Python package (no GUI dependencies)
- Command-line tools only
- Background services

**Requirements:**
- Python 3.10 or later
- 50 MB disk space

---

## File Organization

### Where Files Are Stored

The client creates a dedicated folder for all its data:

#### Windows
```
C:\Users\<YourName>\AppData\Roaming\pyWATS_Client\
├── config.json              # Main configuration
├── pywats_client.log        # Application logs
├── queue\                   # Report queue (pending uploads)
├── converters\              # Your custom converters
├── data\                    # Downloaded software packages
└── reports\                 # Report archive (optional)
```

**Location:** `%APPDATA%\pyWATS_Client\`

#### Linux / Mac
```
~/.config/pywats_client/
├── config.json              # Main configuration
├── pywats_client.log        # Application logs
├── queue/                   # Report queue
├── converters/              # Your custom converters
├── data/                    # Downloaded software
└── reports/                 # Report archive
```

**Location:** `~/.config/pywats_client/`

### What Each Folder Contains

| Folder | Purpose | Can I Delete? |
|--------|---------|---------------|
| **queue/** | Reports waiting to upload | ⚠️ No - reports will be lost |
| **converters/** | Your custom report converters | ❌ No - needed for operation |
| **data/** | Downloaded software packages | ✓ Yes - will re-download |
| **reports/** | Archive of uploaded reports | ✓ Yes - optional backup |
| **config.json** | All settings | ❌ No - will need reconfiguration |
| **pywats_client.log** | Debug/error logs | ✓ Yes - rotates automatically |

### Multiple Instances

You can run multiple client instances on the same computer (e.g., for different test stations):

```
C:\Users\<YourName>\AppData\Roaming\pyWATS_Client\
├── config.json              # Default instance
├── config_station2.json     # Second instance
└── config_station3.json     # Third instance
```

Each instance maintains separate queues, converters, and logs.

---

## Running the Client

### GUI Mode

#### Windows

**Option 1: Start Menu**
After installation, search for "PyWATS Client" in the Start menu.

**Option 2: Command Line**
```bash
python -m pywats_client
```

**Option 3: Python Script**
```python
from pywats_client import run_gui
run_gui()
```

#### Linux / Mac

```bash
# Using installed command
pywats-client gui

# Or directly
python -m pywats_client
```

### Headless Mode

For systems without a display:

```bash
# Start in foreground
pywats-client start

# Start with HTTP API (for remote control)
pywats-client start --api --api-port 8765

# Start as background daemon (Linux/Mac)
pywats-client start --daemon

# Check status
pywats-client status

# Stop daemon
pywats-client stop
```

---

## Configuration

### First-Time Setup

#### Using GUI

1. Launch PyWATS Client
2. Go to **Setup** tab
3. Enter:
   - **Server URL**: Your WATS server (e.g., `https://wats.yourcompany.com`)
   - **Username**: Your WATS username
   - **Password**: Your WATS password
   - **Station Name**: This test station's name (e.g., `ICT-STATION-01`)
4. Click **Test Connection**
5. If successful, click **Save**

#### Using Command Line (Headless)

```bash
# Interactive setup
pywats-client config init

# Non-interactive setup
pywats-client config init \
    --server-url https://wats.yourcompany.com \
    --username your-username \
    --password your-password \
    --station-name ICT-STATION-01 \
    --non-interactive
```

### Configuration File

All settings are stored in `config.json`:

```json
{
  "server_url": "https://wats.yourcompany.com",
  "username": "testuser",
  "api_token": "...",
  "station_name": "ICT-STATION-01",
  "station_location": "Production Line A",
  "log_level": "INFO",
  "auto_start_services": true,
  "connection_check_interval": 60
}
```

**Important:** The password is encrypted and stored as `api_token`.

### Viewing Current Configuration

```bash
# Show all settings
pywats-client config show

# Show as JSON
pywats-client config show --format json

# Get specific value
pywats-client config get server_url
```

### Changing Settings

```bash
# Change station name
pywats-client config set station_name NEW-STATION-NAME

# Enable debug logging
pywats-client config set log_level DEBUG

# Change upload interval
pywats-client config set upload_interval 30
```

Or edit `config.json` directly and restart the client.

---

## How It Works

### Background Services

When the client starts, it runs several background services:

1. **Connection Service** - Monitors connection to WATS server
2. **Queue Service** - Watches for new test reports
3. **Upload Service** - Sends reports to WATS
4. **Software Service** - Downloads software packages (if enabled)

These services run continuously in the background.

### Report Processing Flow

```
Test Equipment
    ↓
[Report File Created]
    ↓
[Converter] → Converts to WATS format
    ↓
[Queue] → Stores temporarily
    ↓
[Upload Service] → Sends to WATS
    ↓
[Archive] → Optionally saves copy
```

### Converters

Converters transform test equipment output into WATS format. They are Python scripts in the `converters/` folder.

**Example converter locations:**
- Windows: `%APPDATA%\pyWATS_Client\converters\my_ict_converter.py`
- Linux: `~/.config/pywats_client/converters/my_ict_converter.py`

See [Converter Architecture](../docs/internal/CONVERTER_ARCHITECTURE.md) for creating custom converters.

---

## Troubleshooting

### Client Won't Start

**Check Python version:**
```bash
python --version
# Should show 3.10 or later
```

**Check installation:**
```bash
pip list | grep pywats
# Should show: pywats-api
```

**View errors:**
```bash
# Windows
type %APPDATA%\pyWATS_Client\pywats_client.log

# Linux/Mac
cat ~/.config/pywats_client/pywats_client.log
```

### Can't Connect to Server

1. **Test URL in browser** - Visit your WATS server URL
2. **Check credentials** - Verify username/password in WATS web interface
3. **Check network** - Ping the server or check firewall
4. **View connection logs:**
   ```bash
   pywats-client config set log_level DEBUG
   pywats-client start
   # Check pywats_client.log for detailed connection errors
   ```

### Reports Not Uploading

1. **Check queue folder** - See if files are piling up
   - Windows: `%APPDATA%\pyWATS_Client\queue\`
   - Linux: `~/.config/pywats_client/queue/`

2. **Check upload service:**
   ```bash
   pywats-client status
   # Should show "Upload Service: Running"
   ```

3. **Manual upload test:**
   ```bash
   pywats-client upload --file path/to/test/report.xml
   ```

### Finding Configuration

**Can't remember where config is?**
```bash
pywats-client config show --format json | grep config_path
```

**Or use default paths:**
- Windows: `%APPDATA%\pyWATS_Client\config.json`
- Linux/Mac: `~/.config/pywats_client/config.json`

### Reset to Defaults

```bash
# Backup current config
# Windows
copy %APPDATA%\pyWATS_Client\config.json %APPDATA%\pyWATS_Client\config.backup.json

# Linux/Mac  
cp ~/.config/pywats_client/config.json ~/.config/pywats_client/config.backup.json

# Delete config (will be recreated with defaults)
# Windows
del %APPDATA%\pyWATS_Client\config.json

# Linux/Mac
rm ~/.config/pywats_client/config.json

# Run setup again
pywats-client config init
```

---

## Advanced Usage

### Multiple Instances

Run separate client instances for different stations:

```bash
# Station 1 (default instance)
pywats-client start

# Station 2 (named instance)
pywats-client --instance station2 config init
pywats-client --instance station2 start

# Station 3 (named instance)
pywats-client --instance station3 config init
pywats-client --instance station3 start
```

Each instance has its own:
- Configuration file
- Queue folder
- Converters
- Log file

### Running as Windows Service

To run automatically on system startup:

```powershell
# Install service (requires admin)
sc create "PyWATS Client" binPath= "python -m pywats_client start" start= auto

# Start service
sc start "PyWATS Client"

# Stop service
sc stop "PyWATS Client"

# Remove service
sc delete "PyWATS Client"
```

### Running as Linux Systemd Service

Create `/etc/systemd/system/pywats-client.service`:

```ini
[Unit]
Description=PyWATS Client
After=network.target

[Service]
Type=simple
User=teststation
ExecStart=/usr/bin/python3 -m pywats_client start
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable pywats-client
sudo systemctl start pywats-client
sudo systemctl status pywats-client
```

---

## Security Considerations

### Credentials Storage

- Passwords are **encrypted** using platform-specific encryption
- **Windows**: Uses DPAPI (Data Protection API)
- **Linux/Mac**: Uses system keyring or file encryption

### Network Security

- All communication with WATS server uses **HTTPS**
- Credentials are never logged
- API tokens are rotated on password change

### File Permissions

Configuration files contain encrypted credentials. Ensure proper file permissions:

```bash
# Linux/Mac - restrict to current user only
chmod 600 ~/.config/pywats_client/config.json

# Windows - use File Properties → Security to restrict access
```

---

## See Also

- [GUI Configuration Guide](../src/pywats_client/GUI_CONFIGURATION.md) - Customize tabs and logging
- [Headless Operation Guide](../src/pywats_client/control/HEADLESS_GUIDE.md) - CLI and HTTP API reference
- [Converter Architecture](../docs/internal/CONVERTER_ARCHITECTURE.md) - Create custom converters
- [Getting Started](GETTING_STARTED.md) - PyWATS API library guide

---

## Support

For issues or questions:
- Check logs: `pywats_client.log` in your config folder
- GitHub Issues: https://github.com/olreppe/pyWATS/issues
- Email: support@virinco.com
