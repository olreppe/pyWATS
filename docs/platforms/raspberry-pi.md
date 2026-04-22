# Raspberry Pi 4/5 Setup Guide

> **Last Updated**: March 30, 2026  
> **Applies to**: Raspberry Pi 4 (4GB/8GB), Raspberry Pi 5, Raspberry Pi 400  
> **OS**: Raspberry Pi OS 64-bit (Bookworm or later)

This guide covers two deployment modes:

1. **API-only** — Use pyWATS as a Python library to submit test reports from your own scripts
2. **Headless client** — Run pyWATS as a background service that watches folders, processes queues, and submits reports automatically

---

## Prerequisites

### Hardware
- Raspberry Pi 4 (4GB+ RAM recommended) or Pi 5
- MicroSD card (32GB+ recommended) or USB SSD
- Network connection (Ethernet or Wi-Fi)
- Power supply (official USB-C recommended)

### Software
- **Raspberry Pi OS 64-bit** (Bookworm or later)
- Python 3.10+ (ships with Bookworm)

> **Important**: Use the **64-bit** OS. The 32-bit (armhf) variant is not supported.

### Verify your setup

```bash
# Confirm 64-bit OS
uname -m
# Expected: aarch64

# Confirm Python version
python3 --version
# Expected: Python 3.11.x or later
```

---

## Option 1: API-Only (Library)

Use this when you want to write your own Python scripts that submit test data to WATS.

### Install

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv -y

# Create a project directory
mkdir ~/pywats-project && cd ~/pywats-project

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install pyWATS (API library only — no GUI, no service)
pip install pywats-api
```

### Verify

```python
python3 -c "import pywats; print(pywats.__version__)"
```

### Usage example

```python
#!/usr/bin/env python3
"""Submit a test report from a Raspberry Pi test station."""

from pywats import WatsApi

# Connect to your WATS server
api = WatsApi(
    server_url="https://your-company.wats.com",
    api_token="your-api-token"
)

# Submit a report from a JSON/WSJF file
with open("/path/to/report.json") as f:
    result = api.submit_report(f.read())
    print(f"Submitted: {result.id}")
```

### Run on boot (cron)

If you have a script that should run periodically:

```bash
# Edit crontab
crontab -e

# Run every 5 minutes
*/5 * * * * /home/pi/pywats-project/.venv/bin/python /home/pi/pywats-project/submit_reports.py >> /home/pi/pywats-project/cron.log 2>&1
```

---

## Option 2: Headless Client (Background Service)

Use this when you want pyWATS to run continuously as a service — watching folders for new test files, managing an offline queue, and submitting reports automatically.

### Install

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv -y

# Create project directory
mkdir ~/pywats && cd ~/pywats

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install pyWATS headless client (no Qt/GUI dependencies)
pip install pywats-api[client-headless]
```

### Configure

```bash
# Interactive setup — prompts for server URL, token, station name
pywats-client config init

# Or non-interactive
pywats-client config init \
    --server-url https://your-company.wats.com \
    --api-token YOUR_API_TOKEN \
    --station-name RPI4-TESTSTATION-01 \
    --non-interactive
```

### Test the connection

```bash
pywats-client test-connection
```

### Run manually (foreground)

Good for testing before setting up as a service:

```bash
# Basic start
pywats-client start

# With HTTP management API (for remote monitoring)
pywats-client start --api --api-port 8080
```

### Install as a systemd service

This makes pyWATS start automatically on boot and restart on failure.

**1. Create a dedicated system user:**

```bash
sudo useradd --system --home-dir /var/lib/pywats --create-home --shell /usr/sbin/nologin pywats
```

**2. Set up the installation under the service user:**

```bash
sudo -u pywats bash -c '
  cd /var/lib/pywats
  python3 -m venv .venv
  source .venv/bin/activate
  pip install pywats-api[client-headless]
'
```

**3. Copy your configuration:**

```bash
sudo mkdir -p /etc/pywats
sudo cp ~/.pywats_client/config.json /etc/pywats/
sudo chown -R pywats:pywats /etc/pywats
```

**4. Create the systemd service file:**

```bash
sudo tee /etc/systemd/system/pywats-client.service > /dev/null << 'EOF'
[Unit]
Description=pyWATS Client Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pywats
Group=pywats
WorkingDirectory=/var/lib/pywats

Environment="PYTHONUNBUFFERED=1"
Environment="PYWATS_CONFIG_DIR=/etc/pywats"
Environment="PYWATS_DATA_DIR=/var/lib/pywats"

ExecStart=/var/lib/pywats/.venv/bin/pywats-client start --api --api-port 8080

# Resource limits (appropriate for Raspberry Pi 4)
MemoryMax=512M
CPUQuota=80%

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/var/lib/pywats /etc/pywats

# Auto-restart on failure
Restart=on-failure
RestartSec=10
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
EOF
```

**5. Enable and start:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable pywats-client
sudo systemctl start pywats-client
```

**6. Verify:**

```bash
# Check service status
sudo systemctl status pywats-client

# View live logs
journalctl -u pywats-client -f

# Check health endpoint
curl http://localhost:8080/health
```

---

## Managing the Service

```bash
# Status
sudo systemctl status pywats-client

# View recent logs
journalctl -u pywats-client -n 50

# Follow logs in real-time
journalctl -u pywats-client -f

# Restart after config changes
sudo systemctl restart pywats-client

# Stop
sudo systemctl stop pywats-client

# Disable auto-start
sudo systemctl disable pywats-client
```

### Remote management (HTTP API)

When started with `--api`, you can manage the client remotely:

```bash
# From another machine on the same network
curl http://raspberrypi.local:8080/health
curl http://raspberrypi.local:8080/status
curl http://raspberrypi.local:8080/queue
```

> **Security note**: By default the API binds to `0.0.0.0` when using `--api`. For production, put it behind a reverse proxy with authentication, or restrict to localhost and use SSH tunneling.

---

## Docker Alternative

If you prefer containers:

```bash
# Install Docker on Raspberry Pi OS
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Log out and back in

# Run pyWATS headless client
docker run -d \
    --name pywats-client \
    --restart unless-stopped \
    -e PYWATS_SERVER_URL=https://your-company.wats.com \
    -e PYWATS_API_TOKEN=your-token \
    -e PYWATS_STATION_NAME=RPI4-DOCKER-01 \
    -v /home/pi/reports:/app/reports \
    -p 8080:8080 \
    ghcr.io/olreppe/pywats-client:latest
```

---

## Performance Tips

| Setting | Recommendation |
|---------|---------------|
| **Storage** | Use a USB SSD instead of MicroSD for better I/O |
| **Swap** | Increase swap to 1GB: `sudo dphys-swapfile swapoff && sudo sed -i 's/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=1024/' /etc/dphys-swapfile && sudo dphys-swapfile setup && sudo dphys-swapfile swapon` |
| **Memory** | The headless client typically uses 50–150MB RAM |
| **CPU** | Queue processing is I/O-bound, not CPU-bound — Pi 4 handles it well |
| **GUI** | Avoid running the Qt GUI on the Pi — use headless mode |
| **Wi-Fi** | Use Ethernet for reliability in production |

---

## Troubleshooting

### "pip install" is slow or fails

```bash
# Use piwheels (pre-built ARM wheels, enabled by default on RPi OS)
pip install --extra-index-url https://www.piwheels.org/simple pywats-api[client-headless]
```

### Service won't start

```bash
# Check logs
journalctl -u pywats-client -n 50 --no-pager

# Run manually to see errors
sudo -u pywats /var/lib/pywats/.venv/bin/pywats-client start
```

### Connection failures

```bash
# Test DNS
ping your-company.wats.com

# Test HTTPS
curl -I https://your-company.wats.com

# Test pyWATS connection
source /var/lib/pywats/.venv/bin/activate
pywats-client test-connection
```

### Permission issues

```bash
# Fix ownership
sudo chown -R pywats:pywats /var/lib/pywats /etc/pywats
```

---

## Next Steps

- [Platform Compatibility Matrix](platform-compatibility.md) — Full platform support details
- [Headless Operation Guide](../../src/pywats_client/control/HEADLESS_GUIDE.md) — Advanced CLI commands and HTTP API
- [CLI Reference](../CLI_REFERENCE.md) — All `pywats-client` commands
