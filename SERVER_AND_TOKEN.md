# Server Configuration for pyWATS Debugging

This file contains the default server configuration for pyWATS development and debugging.

## Server Configuration

**Base URL:** `https://py.wats.com`
**Authentication Token:** `cHlXQVRTX1Rlc3Rpbmc6NWUwYVY3enhJN3E2OUx6ZlE4bDZiMiFPcHB1NmI4`

## Usage in Code

```python
# For testing and debugging, use these values:
BASE_URL = "https://py.wats.com"
AUTH_TOKEN = "cHlXQVRTX1Rlc3Rpbmc6NWUwYVY3enhJN3E2OUx6ZlE4bDZiMiFPcHB1NmI4"

# Register client with pyWATS
pyWATS.register_client(base_url=BASE_URL, token=AUTH_TOKEN)
```

## Environment Variables (Optional)

You can also set these as environment variables:

```bash
# Windows PowerShell
$env:PYWATS_BASE_URL = "https://py.wats.com"
$env:PYWATS_AUTH_TOKEN = "cHlXQVRTX1Rlc3Rpbmc6NWUwYVY3enhJN3E2OUx6ZlE4bDZiMiFPcHB1NmI4"

# Windows Command Prompt
set PYWATS_BASE_URL=https://py.wats.com
set PYWATS_AUTH_TOKEN=cHlXQVRTX1Rlc3Rpbmc6NWUwYVY3enhJN3E2OUx6ZlE4bDZiMiFPcHB1NmI4

# Linux/macOS
export PYWATS_BASE_URL="https://py.wats.com"
export PYWATS_AUTH_TOKEN="cHlXQVRTX1Rlc3Rpbmc6NWUwYVY3enhJN3E2OUx6ZlE4bDZiMiFPcHB1NmI4"
```

## Files That Use This Configuration

- `pyWATS_example.py` - Main demonstration file
- `test_new_api.py` - API testing (if available)
- Development and debugging scripts

## Security Notes

⚠️ **Warning:** This token is for development and testing only. Do not use this token in production environments.

🔒 **Production:** For production use, always use proper authentication tokens and secure token management practices.

## API Integration

The pyWATS API can automatically use these values when debugging is enabled. See the global configuration section in the API documentation for more details.

## Troubleshooting

If you encounter connection issues:

1. Verify the server URL is accessible: `https://py.wats.com`
2. Check that the authentication token is valid
3. Ensure your network allows HTTPS connections to the server
4. Check the server status and availability

## Related Files

- `pyWATS_example.py` - Uses this configuration for demonstrations
- `src/pyWATS/config.py` - Global configuration handling (if implemented)
- `src/pyWATS/connection.py` - Connection management