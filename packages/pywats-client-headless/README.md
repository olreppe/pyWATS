# pyWATS Client Headless

Headless pyWATS client with CLI and HTTP API - perfect for servers, Raspberry Pi, embedded systems, and automated test stations without a display.

## Features

- **CLI Interface**: Full command-line control of the client
- **HTTP Control API**: RESTful API for remote management
- **Daemon Mode**: Run as background service (Linux/Windows)
- **Systemd Integration**: Easy setup as system service
- **No GUI Dependencies**: Minimal dependencies, no Qt required
- **Remote Management**: Control via HTTP from any device
- **Converter Support**: Full converter framework included
- **Queue Management**: Automated report processing

## Installation

```bash
pip install pywats-client-headless
```

### System Requirements

- Python >= 3.8
- Linux, Windows, or macOS
- No display or GUI libraries required

## Quick Start

### Initialize Configuration

```bash
# Create configuration interactively
pywats-client config init

# Or create with parameters
pywats-client config set service_address https://your-server.wats.com
pywats-client config set api_token your_base64_token
pywats-client config set instance_name "Production Station 1"
```

### Test Connection

```bash
pywats-client test-connection
```

### Start Service

```bash
# Run in foreground
pywats-client start

# Run as daemon (background)
pywats-client start --daemon

# Run with HTTP control API
pywats-client start --api --api-port 8765

# Combine daemon and API
pywats-client start --daemon --api
```

### CLI Commands

```bash
# Configuration management
pywats-client config show              # Display current configuration
pywats-client config set key value     # Set configuration value
pywats-client config init              # Initialize new configuration

# Service control
pywats-client start                    # Start service
pywats-client start --daemon           # Start as daemon
pywats-client stop                     # Stop daemon service
pywats-client status                   # Show service status

# Connection testing
pywats-client test-connection          # Test WATS server connection

# Converter management
pywats-client converters list          # List available converters
pywats-client converters test FILE     # Test converter on file

# Version
pywats-client --version                # Show version
```

## HTTP Control API

When running with `--api`, the client exposes a RESTful API for remote control:

### Start with API

```bash
pywats-client start --api --api-port 8765 --api-host 0.0.0.0
```

### API Endpoints

```bash
# Get service status
curl http://localhost:8765/status

# Get configuration
curl http://localhost:8765/config

# Get queue status
curl http://localhost:8765/queue/status

# Get converter list
curl http://localhost:8765/converters

# Restart services
curl -X POST http://localhost:8765/restart

# Pause/resume processing
curl -X POST http://localhost:8765/pause
curl -X POST http://localhost:8765/resume

# Process specific file
curl -X POST http://localhost:8765/process \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/path/to/test/file.txt"}'
```

### API Response Example

```json
{
  "status": "running",
  "connected": true,
  "server_version": "8.0",
  "queue": {
    "pending": 5,
    "processing": 1,
    "failed": 0
  },
  "converters": 3,
  "uptime": 3600
}
```

## Systemd Service (Linux)

Install as system service for automatic startup:

### Create Service File

```bash
sudo nano /etc/systemd/system/pywats-client.service
```

```ini
[Unit]
Description=pyWATS Client Headless Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/pywats
ExecStart=/home/pi/.local/bin/pywats-client start --api --api-port 8765
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable pywats-client
sudo systemctl start pywats-client
sudo systemctl status pywats-client
```

### View Logs

```bash
sudo journalctl -u pywats-client -f
```

## Windows Service

Run as Windows service using `nssm` (Non-Sucking Service Manager):

```powershell
# Install NSSM
choco install nssm

# Create service
nssm install pyWATSClient "C:\Python39\Scripts\pywats-client.exe" "start --daemon --api"
nssm set pyWATSClient AppDirectory "C:\pyWATS"
nssm set pyWATSClient DisplayName "pyWATS Client"
nssm set pyWATSClient Description "WATS test data client service"

# Start service
nssm start pyWATSClient
```

## Raspberry Pi Setup

Perfect for Raspberry Pi test stations:

```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip

# Install pywats-client-headless
pip3 install pywats-client-headless

# Configure
pywats-client config init

# Set up systemd service (see above)
sudo systemctl enable pywats-client
sudo systemctl start pywats-client

# Access from another device
curl http://raspberry-pi.local:8765/status
```

## Docker Deployment

Run in Docker container:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install pywats-client-headless

COPY config.json /app/config.json
COPY converters/ /app/converters/

EXPOSE 8765

CMD ["pywats-client", "start", "--api", "--api-host", "0.0.0.0", "--api-port", "8765"]
```

Build and run:

```bash
docker build -t pywats-client .
docker run -d -p 8765:8765 -v ./data:/app/data pywats-client
```

## Configuration

Configuration is stored in `~/.pywats_client/config.json`:

```json
{
  "instance_name": "Production Station 1",
  "service_address": "https://your-server.wats.com",
  "api_token": "base64_encoded_token",
  "converter_path": "./converters",
  "queue_path": "./queue",
  "watch_paths": ["./test_data"],
  "auto_submit": true,
  "retry_failed": true,
  "retry_interval": 300,
  "max_retries": 3
}
```

## Converters

Place custom converters in the `converters/` directory:

```python
# converters/my_converter.py
from pywats_client.converters import BaseConverter
from pywats.models import UUTReport

class MyConverter(BaseConverter):
    name = "My Converter"
    
    def can_convert(self, file_path):
        return file_path.suffix == '.dat'
    
    def convert(self, file_path):
        # Your conversion logic
        return report
```

## Troubleshooting

### Check Service Status

```bash
pywats-client status
```

### View Logs

Logs are written to `~/.pywats_client/logs/`:

```bash
tail -f ~/.pywats_client/logs/client.log
```

### Test Converter

```bash
pywats-client converters test /path/to/test/file
```

### Connection Issues

```bash
# Test connection
pywats-client test-connection

# Check configuration
pywats-client config show
```

## Requirements

- Python >= 3.8
- pywats >= 2.0.0
- pywats-client-service >= 2.0.0
- aiohttp >= 3.8.0

## Related Packages

- **pywats**: Core API library
- **pywats-client-service**: Client service framework (included)
- **pywats-client-gui**: Desktop GUI application (separate)

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please visit:
- GitHub: https://github.com/olreppe/pyWATS
- Documentation: [Headless Guide](https://github.com/olreppe/pyWATS/blob/main/src/pywats_client/control/HEADLESS_GUIDE.md)
- Issues: https://github.com/olreppe/pyWATS/issues
