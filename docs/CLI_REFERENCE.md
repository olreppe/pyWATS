# pyWATS Client CLI Reference

**Version:** 0.3.0b1+  
**Command:** `pywats-client`

---

## Overview

The pyWATS Client CLI provides cross-platform service management and configuration commands. No GUI required - manage your WATS Client service entirely from the command line on Windows, Linux, and macOS.

---

## Installation

```bash
# Install with CLI support (included by default)
pip install pywats-api[client]

# Verify installation
pywats-client --help
```

---

## Quick Start

```bash
# Start the service
pywats-client start

# Check status
pywats-client status

# View configuration
pywats-client config show

# Stop the service
pywats-client stop
```

---

## Command Reference

### Service Management

#### `pywats-client start`
Start the pyWATS Client service.

**Options:**
- `--instance-id TEXT` - Service instance identifier (default: "default")
- `--verbose, -v` - Enable verbose logging

**Example:**
```bash
pywats-client start
pywats-client start --instance-id production
```

**Output:**
```
Starting pyWATS Client service (instance: default)...
  Cleaned 0 stale lock file(s)
✓ Service started successfully!
  PID: 12345
  Logs: /tmp/pywats_client.log
```

---

#### `pywats-client stop`
Stop the pyWATS Client service.

**Options:**
- `--instance-id TEXT` - Service instance identifier

**Example:**
```bash
pywats-client stop
```

**Output:**
```
Stopping pyWATS Client service (instance: default)...
  Stopping PID: 12345
✓ Service stopped successfully!
```

---

#### `pywats-client restart`
Restart the pyWATS Client service.

**Example:**
```bash
pywats-client restart
```

---

#### `pywats-client status`
Show service status and details.

**Example:**
```bash
pywats-client status
```

**Output:**
```
pyWATS Client Service Status (instance: default)
============================================================
  Status:      Running ✓
  PID:         12345
  Uptime:      2h 34m 12s
  Platform:    Windows
  Instance ID: default
  Log File:    C:\Temp\pyWATS_Client\pywats_client.log
============================================================
```

---

#### `pywats-client gui`
Launch the GUI configurator for editing client configuration.

**Example:**
```bash
pywats-client gui
```

**Note:** This command requires GUI dependencies:
```bash
pip install pywats-api[client]  # Includes Qt/PySide6
```

**About the GUI:**
- The GUI is a configuration-only tool (not a full client application)
- Edit instance configuration in a visual interface
- The service does not need to be running to use the configurator
- Changes are saved to `~/.pywats/instances/<instance_id>/client_config.json`

---

### Configuration Management

#### `pywats-client config show`
Display current configuration.

**Options:**
- `--format [json|text]` - Output format (default: text)

**Example:**
```bash
# Human-readable format
pywats-client config show

# JSON format for scripting
pywats-client config show --format json
```

**Output (text format):**
```
pyWATS Client Configuration
============================================================
Config File: C:\Users\user\AppData\Roaming\pyWATS\pywats_api.json
Instance ID: default

Connection:
  Server URL:      https://wats.example.com
  API Key:         abc12345... (hidden)
  Username:        (not set)
  Timeout:         30s
  Retry Attempts:  3

Caching:
  Enabled:         True
  TTL:             300s
  Max Size:        1000 entries

Metrics:
  Enabled:         True
  Port:            9090

Logging:
  Level:           INFO

============================================================
```

---

#### `pywats-client config get <key>`
Get a specific configuration value.

**Arguments:**
- `key` - Configuration key name (supports dot notation)

**Example:**
```bash
pywats-client config get timeout_seconds
# Output: 30

pywats-client config get domains.report.cache_ttl_seconds
# Output: 300
```

---

#### `pywats-client config set <key> <value>`
Set a configuration value.

**Arguments:**
- `key` - Configuration key name
- `value` - New value

**Options:**
- `--type [string|int|float|bool]` - Value type (default: string)

**Examples:**
```bash
# Set string value
pywats-client config set server_url https://new.example.com

# Set integer value
pywats-client config set timeout_seconds 60 --type int

# Set boolean value
pywats-client config set enable_cache true --type bool

# Set float value
pywats-client config set cache_ttl_seconds 300.5 --type float
```

---

#### `pywats-client config reset`
Reset all configuration to defaults.

**Warning:** This action cannot be undone!

**Example:**
```bash
pywats-client config reset
# Prompt: Are you sure you want to reset all settings to defaults? [y/N]:
```

---

#### `pywats-client config path`
Show the configuration file path.

**Example:**
```bash
pywats-client config path
# Output:
# Config File: C:\Users\user\AppData\Roaming\pyWATS\pywats_api.json
#   Status: Exists ✓
```

---

####` config edit`
Open configuration file in default editor.

**Example:**
```bash
pywats-client config edit
```

**Platform Behavior:**
- **Windows:** Opens with `notepad` or default `.json` editor
- **macOS:** Opens with `TextEdit` or default editor
- **Linux:** Opens with `xdg-open` default editor

---

## Multi-Instance Support

Run multiple independent service instances:

```bash
# Start production instance
pywats-client --instance-id production start

# Start development instance
pywats-client --instance-id dev start

# Check status of each
pywats-client --instance-id production status
pywats-client --instance-id dev status

# Each instance has separate config
pywats-client --instance-id production config show
pywats-client --instance-id dev config show
```

**Instance Directories:**
- Default: `%APPDATA%\pyWATS\pywats_api.json` (Windows)
- Custom: `%APPDATA%\pyWATS\instances\{id}\pywats_api.json`

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error (service not running, config error, etc.) |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PYWATS_CONFIG_DIR` | Override config directory | `%APPDATA%\pyWATS` (Windows) |
| `PYWATS_LOG_LEVEL` | Override log level | `INFO` |

---

## Troubleshooting

### Service won't start

```bash
# Check if already running
pywats-client status

# Clean stale locks
pywats-client stop
pywats-client start

# Check logs
pywats-client config path
# View log file in same directory
```

### Configuration errors

```bash
# Reset to defaults
pywats-client config reset

# Manually edit config
pywats-client config edit
```

### Multiple instances conflict

```bash
# Stop all instances
pywats-client --instance-id default stop
pywats-client --instance-id production stop

# Clean locks
# (Automatic on next start)
```

---

## Examples

### Basic workflow

```bash
# 1. Configure service
pywats-client config set server_url https://wats.example.com
pywats-client config set api_key your-api-key-here

# 2. Start service
pywats-client start

# 3. Verify running
pywats-client status

# 4. View logs
pywats-client config path
# Open log file from same directory

# 5. Stop when done
pywats-client stop
```

### Performance tuning

```bash
# Enable HTTP caching
pywats-client config set enable_cache true --type bool

# Set cache TTL to 10 minutes
pywats-client config set cache_ttl_seconds 600 --type int

# Set cache size to 5000 entries
pywats-client config set cache_max_size 5000 --type int

# Restart to apply
pywats-client restart
```

### Monitoring setup

```bash
# Enable Prometheus metrics
pywats-client config set enable_metrics true --type bool

# Set metrics port
pywats-client config set metrics_port 9090 --type int

# Restart service
pywats-client restart

# Verify metrics endpoint
curl http://localhost:9090/metrics
```

---

## See Also

- **User Guide:** `docs/getting-started.md`
- **Configuration Reference:** `docs/CONFIG_SETTINGS_REFERENCE.md`
- **API Documentation:** `docs/api/index.html`

---

**Last Updated:** February 2, 2026  
**Platform Support:** Windows 10+, Linux (systemd), macOS 10.15+
