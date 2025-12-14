# pyWATS MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for interacting with WATS (Web-based Automated Test System) manufacturing test data.

This server allows AI assistants like Claude, ChatGPT, and VS Code Copilot to query and analyze your WATS test data.

## Features

| Tool | Description |
|------|-------------|
| `wats_test_connection` | Test connection to WATS server |
| `wats_get_products` | List products/part numbers |
| `wats_get_reports` | Query test reports with filters |
| `wats_get_report_details` | Get detailed report with steps |
| `wats_get_failures` | Get recent test failures |
| `wats_get_yield` | Calculate yield statistics |
| `wats_get_assets` | List equipment/assets |
| `wats_get_rootcause_tickets` | Get issue tracking tickets |
| `wats_search_serial` | Search test history by serial |

## Installation

```bash
pip install pywats-api[mcp]
```

Or from source:
```bash
pip install -e ".[mcp]"
```

## Configuration

Set environment variables:

```bash
export WATS_BASE_URL="https://your-company.wats.com"
export WATS_AUTH_TOKEN="your_base64_encoded_token"
```

### Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "wats": {
      "command": "python",
      "args": ["-m", "pywats_mcp"],
      "env": {
        "WATS_BASE_URL": "https://your-company.wats.com",
        "WATS_AUTH_TOKEN": "your_token_here"
      }
    }
  }
}
```

### VS Code (Copilot)

Add to your VS Code settings (`.vscode/settings.json` or user settings):

```json
{
  "mcp": {
    "servers": {
      "wats": {
        "command": "python",
        "args": ["-m", "pywats_mcp"],
        "env": {
          "WATS_BASE_URL": "https://your-company.wats.com",
          "WATS_AUTH_TOKEN": "your_token_here"
        }
      }
    }
  }
}
```

## Usage Examples

Once configured, you can ask your AI assistant:

- "Show me yesterday's test failures"
- "What's the yield for Product X this week?"
- "Search for all tests of serial number ABC123"
- "Which assets need calibration?"
- "List open RootCause tickets"
- "Get details for report [id]"

## Running Standalone

```bash
# Set environment variables first
export WATS_BASE_URL="https://your-company.wats.com"
export WATS_AUTH_TOKEN="your_token"

# Run the server
python -m pywats_mcp
```

## Requirements

- Python 3.10+
- pywats-api
- mcp (Model Context Protocol SDK)

## License

MIT License - see LICENSE file in the root directory.
