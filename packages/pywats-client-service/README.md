# pyWATS Client Service

Core client services for pyWATS - provides converter management, queue processing, connection handling, and background services without GUI dependencies.

## Features

- **Converter Framework**: Plugin system for test data conversion
- **Queue Management**: Automated report queue processing and retry logic
- **Connection Service**: WATS server connection management and health monitoring
- **File Watching**: Automatic detection of new test data files
- **Configuration Management**: Client configuration and credentials storage
- **Instance Management**: Support for multiple client instances

## Installation

```bash
pip install pywats-client-service
```

This package is typically used as a dependency for:
- `pywats-client-headless` - CLI and HTTP API
- `pywats-client-gui` - Desktop GUI application

## Usage

### As a Library

```python
from pywats_client.core import WATSClient, ClientConfig
from pywats_client.services import ConnectionService, QueueService

# Create configuration
config = ClientConfig(
    instance_name="Production Station 1",
    service_address="https://your-server.wats.com",
    api_token="your_base64_token"
)

# Initialize client
async def main():
    client = WATSClient(config)
    await client.start()
    
    # Client services are now running
    # - Connection monitoring
    # - Queue processing
    # - Converter management
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await client.stop()

asyncio.run(main())
```

### Converter System

Create custom converters to transform your test data format into WATS reports:

```python
# converters/my_converter.py
from pywats_client.converters import BaseConverter
from pywats.models import UUTReport

class MyConverter(BaseConverter):
    """Convert my custom test format to WATS UUT reports"""
    
    name = "My Test System Converter"
    description = "Converts .test files to WATS format"
    
    def can_convert(self, file_path: Path) -> bool:
        """Check if this converter can handle the file"""
        return file_path.suffix == '.test'
    
    def convert(self, file_path: Path) -> UUTReport:
        """Convert file to WATS report"""
        # Parse your test data
        data = self.parse_test_file(file_path)
        
        # Create WATS report
        report = UUTReport(
            pn=data['part_number'],
            sn=data['serial_number'],
            rev=data['revision'],
            pass_fail=data['passed'],
            start_date_time=data['start_time']
        )
        
        # Add test steps
        for step in data['steps']:
            report.steps.append(self.create_step(step))
        
        return report
```

Place converters in the `converters/` directory, and they'll be automatically discovered and loaded.

### Queue Service

The queue service manages report submission with automatic retry:

```python
from pywats_client.services import QueueService

async def use_queue():
    queue = QueueService(client_config, api_client)
    await queue.start()
    
    # Queue automatically processes reports
    # - Submits to WATS server
    # - Retries on failure
    # - Tracks submission status
    
    # Get queue status
    status = await queue.get_status()
    print(f"Pending: {status['pending']}")
    print(f"Failed: {status['failed']}")
```

### Connection Service

Monitor WATS server connection health:

```python
from pywats_client.services import ConnectionService

async def monitor_connection():
    conn = ConnectionService(client_config)
    await conn.start()
    
    # Service automatically:
    # - Tests connection periodically
    # - Reports connection status
    # - Handles reconnection
    
    if conn.is_connected():
        version = await conn.get_server_version()
        print(f"Connected to WATS {version}")
```

## Configuration

Configuration is stored in JSON format:

```json
{
    "instance_name": "Production Station 1",
    "service_address": "https://your-server.wats.com",
    "api_token": "base64_encoded_token",
    "converter_path": "./converters",
    "queue_path": "./queue",
    "watch_paths": ["./test_data"],
    "auto_submit": true,
    "retry_failed": true
}
```

Load configuration:

```python
from pywats_client.core import ClientConfig
from pathlib import Path

# Load from file
config = ClientConfig.load_or_create(Path("config.json"))

# Create new
config = ClientConfig(
    instance_name="Station 1",
    service_address="https://wats.example.com",
    api_token="token"
)
config.save(Path("config.json"))
```

## Architecture

```
pywats_client/
├── core/                    # Core functionality
│   ├── client.py           # Main client orchestrator
│   ├── config.py           # Configuration management
│   └── connection_config.py # Connection settings
├── services/               # Background services
│   ├── connection.py       # Connection monitoring
│   ├── queue.py           # Queue processing
│   └── file_watcher.py    # File system monitoring
├── converters/            # Converter framework
│   ├── base.py           # Base converter class
│   └── manager.py        # Converter discovery/loading
└── app.py                # Application orchestration
```

## Requirements

- Python >= 3.8
- pywats >= 2.0.0
- watchdog >= 3.0.0
- aiofiles >= 23.0.0

## Related Packages

- **pywats**: Core API library (required dependency)
- **pywats-client-headless**: CLI and HTTP API (includes this package)
- **pywats-client-gui**: Desktop GUI application (includes this package)

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please visit:
- GitHub: https://github.com/olreppe/pyWATS
- Issues: https://github.com/olreppe/pyWATS/issues
