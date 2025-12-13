# pyWATS - Core API Library

Python API library for WATS (Web-based Automated Test System) - A comprehensive library for interacting with WATS test data management systems.

## Features

- **Product Management**: Create, read, update products and BOMs
- **Asset Management**: Manage test equipment and assets
- **Report Creation**: Submit UUT (Unit Under Test) and UUR (Unit Under Repair) reports
- **Production Management**: Handle serial numbers and production data
- **RootCause Ticketing**: Manage failure tickets and root cause analysis
- **Statistics & Analytics**: Query test data and generate insights
- **Station Management**: Configure test station metadata

## Installation

```bash
pip install pywats
```

## Quick Start

```python
from pywats import pyWATS, WATSFilter

# Initialize API
api = pyWATS(
    base_url="https://your-server.wats.com",
    token="your_base64_encoded_token"
)

# Test connection
if api.test_connection():
    print(f"Connected! Server version: {api.get_version()}")

# Get products
products = api.product.get_products()
for product in products:
    print(f"{product.part_number}: {product.name}")

# Query recent test reports
filter = WATSFilter(top_count=10)
headers = api.report.query_uut_headers(filter)
for header in headers:
    print(f"Serial: {header.serial_number}, Status: {header.status}")
```

## Authentication

pyWATS uses Base64-encoded credentials for authentication:

```python
import base64

# Create token from username:password
credentials = f"{username}:{password}"
token = base64.b64encode(credentials.encode()).decode()

api = pyWATS(base_url="https://your-server.wats.com", token=token)
```

## Logging

Enable debug logging to see detailed API operations:

```python
from pywats import enable_debug_logging

# Enable debug mode for all pyWATS operations
enable_debug_logging()

# Or configure logging manually
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('pywats').setLevel(logging.DEBUG)
```

## Core Modules

### Product Module
```python
# Get all products
products = api.product.get_products()

# Get specific product with revisions
product = api.product.get_product("PART-001")
revisions = api.product.get_product_revisions("PART-001")

# Create new product
from pywats import Product
product = Product(part_number="NEW-001", name="New Product")
api.product.create_product(product)
```

### Report Module
```python
from pywats.models import UUTReport, Step, NumericStep

# Create test report
report = UUTReport(
    pn="PART-001",
    sn="SN-12345",
    rev="A",
    pass_fail=True,
    start_date_time="2024-01-01T10:00:00Z"
)

# Add test steps
report.steps.append(NumericStep(
    step_name="Voltage Test",
    step_type="NumericLimitTest",
    value=5.0,
    comp_operator="GELE",
    low_limit=4.5,
    high_limit=5.5,
    status=1
))

# Submit report
api.report.submit_uut_report(report)
```

### Production Module
```python
# Register new serial number
unit = api.production.register_unit(
    part_number="PART-001",
    serial_number="SN-12345",
    revision="A"
)

# Query units
from pywats import WATSFilter
filter = WATSFilter(part_number="PART-001")
units = api.production.query_units(filter)
```

## Station Configuration

Configure test station metadata that's included with all reports:

```python
from pywats import Station, StationConfig, Purpose

# Define station configuration
config = StationConfig(
    station_id="TEST-STATION-01",
    location="Building A, Floor 2",
    purposes=[Purpose.DEVELOPMENT, Purpose.PRODUCTION]
)

# Register station
Station.register(config)

# Station info is automatically included in reports
```

## Documentation

- [Full Documentation](https://github.com/olreppe/pyWATS/tree/main/docs)
- [API Architecture](https://github.com/olreppe/pyWATS/blob/main/docs/ARCHITECTURE.md)
- [Report Module Guide](https://github.com/olreppe/pyWATS/blob/main/docs/usage/REPORT_MODULE.md)
- [Product Module Guide](https://github.com/olreppe/pyWATS/blob/main/docs/usage/PRODUCT_MODULE.md)

## Requirements

- Python >= 3.8
- httpx >= 0.24.0
- pydantic >= 1.10.0
- python-dateutil >= 2.8.0
- attrs >= 22.0.0

## Related Packages

- **pywats-client-headless**: CLI and HTTP API for headless operation
- **pywats-client-gui**: Desktop GUI application with Qt
- **pywats-client-service**: Core client services (base for headless/GUI)

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please visit:
- GitHub: https://github.com/olreppe/pyWATS
- Issues: https://github.com/olreppe/pyWATS/issues
