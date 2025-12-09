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

## Running the GUI Client

```bash
python -m pywats_client
```

## Development Workflow

### Working with GitHub Copilot

GitHub Copilot can work on tasks in separate branches while you continue your local development:

- Assign refactoring, documentation, or other tasks to agents
- Agents work asynchronously in their own branches
- Review and merge agent work when ready

See [GitHub Copilot Workflow Guide](docs/GITHUB_COPILOT_WORKFLOW.md) for details on parallel development with agents.

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

- [Basic Usage Example](docs/examples/basic_usage.py)
- [REST API Instructions](docs/REST_API_INSTRUCTION.md)
- [API Specifications](docs/api_specs/)
- [GitHub Copilot Workflow](docs/GITHUB_COPILOT_WORKFLOW.md) - Working with agents on parallel branches

## License

Proprietary - Virinco
