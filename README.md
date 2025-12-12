# pyWATS

A Python library for interacting with the WATS (Web-based Automated Test System) API.

## Features

- **pyWATS Library** (`src/pywats/`) - Core API library for WATS integration
  - Product management
  - Asset management  
  - Report creation and submission
  - Production/serial number management
  - RootCause ticket system
  - Statistics and analytics

- **pyWATS Client** (`src/pywats_client/`) - Desktop GUI application
  - Connection management
  - Converter configuration
  - Report queue management

## Installation

```bash
# Clone the repository
git clone https://github.com/olreppe/pyWATS.git
cd pyWATS

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -e .
```

## Configuration

1. Copy `.env.template` to `.env`
2. Update with your WATS credentials:

```env
WATS_BASE_URL=https://your-server.wats.com
WATS_AUTH_TOKEN=your_base64_encoded_token
```

## Quick Start

```python
from pywats import pyWATS, WATSFilter

# Initialize API
api = pyWATS(
    base_url="https://your-server.wats.com",
    token="your_token"
)

# Test connection
if api.test_connection():
    print(f"Connected! Server version: {api.get_version()}")

# Get products
products = api.product.get_products()
for p in products:
    print(f"{p.part_number}: {p.name}")

# Query recent reports
filter = WATSFilter(top_count=10)
headers = api.report.query_uut_headers(filter)
```

### Enable Debug Logging

```python
from pywats import pyWATS, enable_debug_logging

# Quick debug mode - shows all library operations
enable_debug_logging()

# Or configure logging your way
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('pywats').setLevel(logging.DEBUG)

# Now use the API with detailed logging
api = pyWATS(base_url="...", token="...")
```

See [LOGGING_STRATEGY.md](LOGGING_STRATEGY.md) for comprehensive logging documentation.

## Running the GUI Client

```bash
python -m pywats_client
```

### GUI Configuration

The GUI supports modular tab configuration and logging control:

- **Tab Visibility**: Show/hide tabs (Software, SN Handler, etc.) based on your needs
- **Logging Integration**: Automatic pyWATS library logging when debug mode is enabled
- **Multiple Instances**: Run multiple client instances with separate configurations

See [GUI Configuration Guide](src/pywats_client/GUI_CONFIGURATION.md) for detailed setup instructions.

## Project Structure

```
pyWATS/
├── src/
│   ├── pywats/              # Core library
│   │   ├── models/          # Pydantic data models
│   │   ├── modules/         # High-level API modules
│   │   └── rest_api/        # REST API wrappers
│   └── pywats_client/       # GUI application
│       ├── core/            # Core client functionality
│       ├── gui/             # GUI components
│       └── services/        # Background services
├── converters/              # User converter plugins
├── docs/                    # Documentation
│   ├── api_specs/           # OpenAPI specifications
│   ├── examples/            # Usage examples
│   └── gui_screens/         # GUI screenshots
├── pyproject.toml           # Project configuration
└── requirements.txt         # Dependencies
```

## Documentation

### Architecture & Design

- [Architecture Overview](docs/ARCHITECTURE.md) - System design and layered architecture
- [API Specifications](docs/api_specs/) - OpenAPI specs for WATS server

### Module Usage Guides

- [Report Module](docs/usage/REPORT_MODULE.md) - Test reports and factory methods ⭐
- [Product Module](docs/usage/PRODUCT_MODULE.md) - Product/BOM management
- [Production Module](docs/usage/PRODUCTION_MODULE.md) - Serial number and unit tracking
- [Asset Module](docs/usage/ASSET_MODULE.md) - Equipment management (coming soon)

### Additional Documentation

- [Basic Usage Example](docs/examples/basic_usage.py)
- [REST API Instructions](docs/REST_API_INSTRUCTION.md)
- [Quick Reference](QUICK_REFERENCE.md) - API quick reference
- [Logging Strategy](LOGGING_STRATEGY.md) - Comprehensive logging guide ⭐
- [GUI Configuration](src/pywats_client/GUI_CONFIGURATION.md) - Client GUI setup and tab customization ⭐

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_report.py

# Run with coverage
pytest --cov=src --cov-report=html
```

## License

Proprietary - Virinco
