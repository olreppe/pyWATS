# Linux systemd Service Installation

This guide explains how to install pyWATS Client as a Linux systemd service that auto-starts on system boot.

## Overview

The pyWATS Client can run as a systemd service in the background, automatically starting when Linux boots. This is the recommended setup for production environments.

**System Compatibility:**
- Ubuntu 16.04+ / Debian 8+
- RHEL/CentOS 7+
- Fedora 15+
- Any systemd-based Linux distribution

**Folder Structure:**
- **System-wide**: `/var/lib/pywats/` (configuration, logs, queues)
- **User-specific**: `~/.config/pywats_client/`
- **Service files**: `/etc/systemd/system/`

## Prerequisites

### Required
- Linux with systemd (check: `systemctl --version`)
- Python 3.10 or later
- Root privileges (for system-wide installation)

### Check systemd
```bash
# Verify systemd is running
systemctl --version

# Should show systemd version (e.g., systemd 245)
```

## Installation

### System-Wide Installation (Recommended)

Installs service that runs at boot, before user login.

```bash
# Install pyWATS Client
pip install pywats-api[client]

# Install as systemd service (requires sudo)
sudo python -m pywats_client install-service

# Start the service
sudo systemctl start pywats-service

# Check status
sudo systemctl status pywats-service
```

This creates:
- Service: `pywats-service.service`
- Auto-start: Enabled
- Logs: `journalctl -u pywats-service`
- Data directory: `/var/lib/pywats/`

### User-Level Installation

Installs service that runs when specific user logs in.

```bash
# Install pyWATS Client
pip install pywats-api[client]

# Install as user service (specify your username)
sudo python -m pywats_client install-service --user $USER

# Start the service
sudo systemctl start pywats-service

# Check status
systemctl status pywats-service
```

This creates:
- Service runs as your user account
- Data directory: `~/.config/pywats_client/`
- User-specific permissions

## Multi-Instance Installation

For multi-station setups where you need multiple services (one per test station):

```bash
# Create separate config files
sudo mkdir -p /var/lib/pywats
sudo cp config.json /var/lib/pywats/config_station_a.json
sudo cp config.json /var/lib/pywats/config_station_b.json

# Install service for Station A
sudo python -m pywats_client install-service \
    --instance-id station_a \
    --config /var/lib/pywats/config_station_a.json \
    --user pywats

# Install service for Station B
sudo python -m pywats_client install-service \
    --instance-id station_b \
    --config /var/lib/pywats/config_station_b.json \
    --user pywats

# Start both services
sudo systemctl start pywats-service@station_a
sudo systemctl start pywats-service@station_b
```

Each instance will have:
- Service name: `pywats-service@station_a.service`, `pywats-service@station_b.service`
- Separate configurations
- Independent logging

## Service Management

### Check Service Status

```bash
# Status
sudo systemctl status pywats-service

# Check if enabled
systemctl is-enabled pywats-service

# Check if running
systemctl is-active pywats-service
```

### Start/Stop/Restart

```bash
# Start
sudo systemctl start pywats-service

# Stop
sudo systemctl stop pywats-service

# Restart
sudo systemctl restart pywats-service

# Reload configuration (without restart)
sudo systemctl reload pywats-service
```

### Enable/Disable Auto-Start

```bash
# Enable (auto-start on boot)
sudo systemctl enable pywats-service

# Disable (don't auto-start)
sudo systemctl disable pywats-service

# Check status
systemctl is-enabled pywats-service
```

### View Logs

systemd logs all service output to the journal:

```bash
# View all logs
sudo journalctl -u pywats-service

# Follow logs (live)
sudo journalctl -u pywats-service -f

# Last 50 lines
sudo journalctl -u pywats-service -n 50

# Since last boot
sudo journalctl -u pywats-service -b

# Last hour
sudo journalctl -u pywats-service --since "1 hour ago"

# With timestamps
sudo journalctl -u pywats-service -o short-iso
```

### Uninstall Service

```bash
# Stop and remove
sudo python -m pywats_client uninstall-service

# For specific instance
sudo python -m pywats_client uninstall-service --instance-id station_a

# Verify removal
systemctl list-units | grep pywats
```

## Configuration

### Default Configuration

The service uses configuration from:
- System-wide: `/var/lib/pywats/config.json`
- User-specific: `~/.config/pywats_client/config.json`
- Custom: Specify with `--config` during installation

### Changing Configuration

**Option 1: Using GUI**
1. Run the pyWATS Client GUI
2. It will discover the running service
3. Make configuration changes in the GUI
4. Changes are sent via IPC to the service

**Option 2: Edit config.json**
```bash
# Stop the service
sudo systemctl stop pywats-service

# Edit configuration
sudo nano /var/lib/pywats/config.json

# Start the service
sudo systemctl start pywats-service

# Verify
sudo journalctl -u pywats-service -n 20
```

**Option 3: Reinstall with new config**
```bash
sudo python -m pywats_client uninstall-service
sudo python -m pywats_client install-service --config /path/to/new/config.json
sudo systemctl start pywats-service
```

## Troubleshooting

### Service Won't Start

1. **Check logs**:
   ```bash
   sudo journalctl -u pywats-service -n 100 --no-pager
   ```

2. **Check service file**:
   ```bash
   sudo systemctl cat pywats-service
   ```

3. **Test service command manually**:
   ```bash
   # Run in foreground for debugging
   python -m pywats_client service --instance-id default
   ```

4. **Verify Python path**:
   ```bash
   which python
   python --version
   ```

5. **Check permissions**:
   ```bash
   ls -la /var/lib/pywats/
   sudo chown -R pywats:pywats /var/lib/pywats/
   ```

### Permission Errors

If the service can't access files:

```bash
# Create dedicated user
sudo useradd -r -s /bin/false pywats

# Set ownership
sudo chown -R pywats:pywats /var/lib/pywats/

# Reinstall with user
sudo python -m pywats_client uninstall-service
sudo python -m pywats_client install-service --user pywats
```

### Service Keeps Restarting

The service is configured to automatically restart on failure. Check why it's failing:

```bash
# View recent crashes
sudo journalctl -u pywats-service --since "10 minutes ago"

# Disable auto-restart temporarily
sudo systemctl edit pywats-service
# Add:
# [Service]
# Restart=no

sudo systemctl daemon-reload
sudo systemctl restart pywats-service
```

### Port Already in Use

If you see "Address already in use" errors:

```bash
# Check what's using the port
sudo netstat -tlnp | grep :8765

# Or with ss
sudo ss -tlnp | grep :8765

# Kill the conflicting process or change port in config
```

### Multiple Instances Conflict

If you see errors about IPC endpoints already in use:

```bash
# List all pyWATS services
systemctl list-units | grep pywats

# Check each one
sudo systemctl status pywats-service
sudo systemctl status pywats-service@station_a

# Ensure each has unique instance-id
```

## Advanced Configuration

### Custom User and Group

```bash
# Create dedicated user
sudo useradd -r -m -d /var/lib/pywats -s /bin/false pywats

# Install with custom user
sudo python -m pywats_client install-service --user pywats
```

### Environment Variables

Edit the service file:

```bash
sudo systemctl edit pywats-service --full
```

Add environment variables:
```ini
[Service]
Environment="PYTHONPATH=/custom/path"
Environment="PYWATS_LOG_LEVEL=DEBUG"
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart pywats-service
```

### Resource Limits

Limit CPU/memory usage:

```bash
sudo systemctl edit pywats-service --full
```

Add limits:
```ini
[Service]
MemoryLimit=512M
CPUQuota=50%
```

### Network Dependencies

If pyWATS needs specific network services:

```bash
sudo systemctl edit pywats-service --full
```

Add dependencies:
```ini
[Unit]
After=network-online.target postgresql.service
Requires=network-online.target
```

## GUI Discovery

When you open the pyWATS Client GUI on Linux:

1. **Discovery**: GUI scans for running service instances via IPC
2. **Instance Selector**: Shows all discovered services
3. **Connect**: Select an instance to view/configure
4. **Status**: Live status updates via IPC

The GUI never auto-starts services - they must be started separately via systemd.

## Comparison with Other Methods

| Method | Auto-Start | Survives Reboot | Crash Recovery | Service Management |
|--------|------------|-----------------|----------------|-------------------|
| **systemd** | ✓ | ✓ | ✓ | systemctl, journalctl |
| **Manual (GUI)** | ✗ | ✗ | ✗ | Terminal |
| **cron @reboot** | ✓ | ✓ | ✗ | crontab |
| **init.d script** | ✓ | ✓ | ✗ | service command |

**Recommendation:** Use systemd for production environments.

## Ubuntu Specific Notes

### Ubuntu 22.04 LTS (Jammy)

Fully supported. systemd 249.

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install pywats-api[client]
sudo python3 -m pywats_client install-service
```

### Ubuntu 20.04 LTS (Focal)

Fully supported. systemd 245.

### Ubuntu 18.04 LTS (Bionic)

Supported. systemd 237.

## See Also

- [GETTING_STARTED.md](GETTING_STARTED.md) - Basic client usage
- [CLIENT_INSTALLATION.md](CLIENT_INSTALLATION.md) - Installation guide
- [docs/refactoring/SEPARATE_SERVICE_GUI_MODE.md](refactoring/SEPARATE_SERVICE_GUI_MODE.md) - Architecture design
- [systemd documentation](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
