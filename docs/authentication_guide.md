# pyWATS Authentication and Connection Guide

This document describes the new authentication and connection management features added to pyWATS.

## Overview

The pyWATS library now includes:
- **Connection Management**: Centralized configuration for WATS API access
- **Authentication**: Basic Authentication support with token-based auth
- **Example Usage**: Complete working examples in `main.py`

## Quick Start

### 1. Install Dependencies

Make sure you have the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Create a Connection

```python
from pyWATS.connection import create_connection

# Create connection with your WATS server details
connection = create_connection(
    base_url="https://your-wats-server.com",
    token="your_base64_encoded_token"
)

# Test the connection
if connection.test_connection():
    print("Connected successfully!")
```

### 3. Use REST API Endpoints

```python
from pyWATS.rest_api.endpoints.asset import get_assets, get_asset_by_id

# Get assets (returns top 10 by default)
assets = get_assets(odata_top=10)

# Get specific asset by ID
asset = get_asset_by_id("your-asset-id")
```

## Authentication

### Basic Authentication

The WATS API uses HTTP Basic Authentication. You need:
- **Base URL**: Your WATS server URL (e.g., `https://your-server.wats.com`)
- **Token**: Base64 encoded credentials in format `username:password`

### Example Token Generation

If you have credentials like `username:password`, encode them to Base64:
```python
import base64
credentials = "username:password"
token = base64.b64encode(credentials.encode()).decode()
```

## Environment Variables

You can configure the connection using environment variables:

```bash
export WATS_BASE_URL="https://your-wats-server.com"
export WATS_AUTH_TOKEN="your_base64_encoded_token"
export WATS_TIMEOUT="30.0"  # Optional
export WATS_REFERRER="https://your-wats-server.com/dashboard"  # Optional
```

Then create connection from environment:
```python
from pyWATS.connection import create_connection_from_env

connection = create_connection_from_env()
if connection:
    print("Connected using environment variables!")
```

## Example Configuration

The `main.py` file includes example configuration:

```python
BASE_URL = "https://ola.wats.com"  # Replace with your server
AUTH_TOKEN = "cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="  # Replace with your token
```

## Available Endpoints

The library includes several endpoint modules:

- **Asset Management**: `pyWATS.rest_api.endpoints.asset`
  - `get_assets()` - List assets
  - `get_asset_by_id()` - Get asset by ID
  - `get_asset_by_serial_number()` - Get asset by serial number
  - `create_asset()` - Create or update asset
  - `delete_asset()` - Delete asset

- **Production**: `pyWATS.rest_api.endpoints.production`
- **Reports**: `pyWATS.rest_api.endpoints.report`
- **Products**: `pyWATS.rest_api.endpoints.product`

## Error Handling

The library provides comprehensive error handling:

```python
from pyWATS.rest_api.exceptions import WATSAPIException, AuthenticationError

try:
    assets = get_assets()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    print(f"Status code: {e.status_code}")
except WATSAPIException as e:
    print(f"API error: {e}")
```

## Running the Example

To run the complete example:

```bash
python main.py
```

This will:
1. Create a connection to the WATS API
2. Test the connection
3. Demonstrate various asset operations
4. Show error handling examples

## OData Query Support

Many endpoints support OData query parameters:

```python
# Get top 5 assets ordered by name
assets = get_assets(
    odata_top=5,
    odata_orderby="name"
)

# Get assets with filter
assets = get_assets(
    odata_filter="state eq 1",  # Assets in operation
    odata_top=10
)
```

## File Structure

```
pyWATS/
??? connection.py              # Connection management
??? rest_api/
?   ??? client.py             # HTTP client with auth
?   ??? endpoints/            # API endpoint modules
?   ?   ??? asset.py         # Asset operations
?   ?   ??? production.py    # Production operations
?   ?   ??? ...
?   ??? models/              # Data models
?   ??? exceptions.py        # Custom exceptions
??? __init__.py
```

## Tips

1. **Replace Example Values**: Update `BASE_URL` and `AUTH_TOKEN` with your actual server details
2. **Environment Variables**: Use environment variables for production deployments
3. **Error Handling**: Always wrap API calls in try-catch blocks
4. **Connection Testing**: Use `connection.test_connection()` to verify connectivity
5. **OData Queries**: Use OData parameters for efficient data filtering

## Next Steps

1. Replace the example configuration with your actual WATS server details
2. Explore other endpoint modules (production, reports, etc.)
3. Implement your specific business logic using the available endpoints
4. Add proper error handling for your use cases