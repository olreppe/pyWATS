# pyWATS Quick Reference

> **Version:** 0.2.x | **Python:** 3.10+ | [Full Documentation](https://github.com/olreppe/pyWATS)

---

## Installation

```bash
# API only (minimal)
pip install pywats-api

# Full client with GUI
pip install pywats-api[client]

# Headless client (no GUI - for Raspberry Pi, servers)
pip install pywats-api[client-headless]
```

---

## Quick Start

### Async (Recommended)

```python
from pywats import AsyncWATS

async with AsyncWATS("https://your-server.wats.com", token="your-token") as api:
    reports = await api.report.get_reports()
    assets = await api.asset.get_assets()
```

### Sync (Simple scripts)

```python
from pywats import WATS

with WATS("https://your-server.wats.com", token="your-token") as api:
    reports = api.report.get_reports()
```

---

## Authentication

```python
# Option 1: Token directly
api = AsyncWATS(url, token="your-api-token")

# Option 2: Environment variables
#   WATS_BASE_URL=https://your-server.wats.com
#   WATS_AUTH_TOKEN=your-api-token
api = AsyncWATS.from_env()

# Option 3: Username/password (gets token automatically)
api = AsyncWATS(url, username="user", password="pass")
```

---

## Common Operations

### Reports

```python
# Get recent reports
reports = await api.report.get_reports()

# Get single report by ID
report = await api.report.get_report("guid-here")

# Query with OData filter
reports = await api.report.query(
    filter="status eq 'Failed'",
    top=100,
    orderby="startDateTime desc"
)

# Create report from UUT
report = await api.report.create_report(uut_report)
```

### Assets (Units Under Test)

```python
# Get all assets
assets = await api.asset.get_assets()

# Get by serial number
asset = await api.asset.get_by_serial("SN12345")

# Create asset
asset = await api.asset.create(
    serial_number="SN12345",
    part_number="PN-001",
    revision="A"
)

# Update asset
await api.asset.update(asset_id, revision="B")
```

### Products

```python
# Get all products
products = await api.product.get_products()

# Get by part number
product = await api.product.get_product("PN-001")

# Create product
product = await api.product.create_product(
    part_number="PN-002",
    name="Widget Pro",
    description="Advanced widget"
)
```

### Analytics

```python
# Get yield data
yield_data = await api.analytics.get_yield(
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31),
    group_by="month"
)

# Get failure pareto
failures = await api.analytics.get_failure_pareto(
    part_number="PN-001",
    top=10
)
```

---

## Safe OData Filtering

```python
from pywats.shared.odata import ODataFilterBuilder, escape_string

# ✅ Safe - use the builder
filter = (ODataFilterBuilder()
    .field("status").eq("Failed")
    .field("partNumber").eq("PN-001")
    .build())
# Result: "status eq 'Failed' and partNumber eq 'PN-001'"

# ✅ Safe - escape user input
user_input = "O'Brien"
safe_filter = f"name eq '{escape_string(user_input)}'"
# Result: "name eq 'O''Brien'"

# ❌ UNSAFE - never do this!
# filter = f"name eq '{user_input}'"  # SQL injection risk!
```

### Filter Builder Operators

```python
builder = ODataFilterBuilder()

# Comparison
builder.field("status").eq("Passed")       # status eq 'Passed'
builder.field("count").ne(0)               # count ne 0
builder.field("value").gt(100)             # value gt 100
builder.field("value").ge(100)             # value ge 100
builder.field("value").lt(100)             # value lt 100
builder.field("value").le(100)             # value le 100

# String functions
builder.field("name").contains("test")     # contains(name, 'test')
builder.field("name").startswith("pre")    # startswith(name, 'pre')
builder.field("name").endswith("fix")      # endswith(name, 'fix')

# Null checks
builder.field("value").is_null()           # value eq null
builder.field("value").is_not_null()       # value ne null

# In list
builder.field("status").in_list(["A", "B"]) # (status eq 'A' or status eq 'B')

# OR conditions
builder.field("a").eq(1).use_or().field("b").eq(2)  # a eq 1 or b eq 2
```

---

## Error Handling

```python
from pywats.exceptions import (
    WATSAPIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError
)

try:
    report = await api.report.get_report(report_id)
except AuthenticationError:
    print("Invalid or expired token")
except NotFoundError:
    print("Report not found")
except ValidationError as e:
    print(f"Invalid input: {e.details}")
except RateLimitError:
    print("Too many requests - slow down")
except WATSAPIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

---

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `WATS_BASE_URL` | Server URL (e.g., `https://demo.wats.com`) |
| `WATS_AUTH_TOKEN` | API token |
| `WATS_USERNAME` | Username (alternative to token) |
| `WATS_PASSWORD` | Password (alternative to token) |
| `WATS_TIMEOUT` | Request timeout in seconds (default: 30) |
| `WATS_VERIFY_SSL` | SSL verification (`true`/`false`) |

### Client Config File

Location: `~/.pywats/config.json`

```json
{
  "base_url": "https://your-server.wats.com",
  "auth_token": "your-token",
  "station_name": "TestStation01",
  "timeout": 30,
  "verify_ssl": true
}
```

---

## Async Patterns

### Running async code from sync context

```python
import asyncio
from pywats import AsyncWATS

async def main():
    async with AsyncWATS(url, token=token) as api:
        return await api.report.get_reports()

# Run from sync code
reports = asyncio.run(main())
```

### Parallel requests

```python
async with AsyncWATS(url, token=token) as api:
    # Run multiple requests in parallel
    reports, assets, products = await asyncio.gather(
        api.report.get_reports(),
        api.asset.get_assets(),
        api.product.get_products()
    )
```

### Batch processing

```python
async def process_reports(report_ids: list[str]):
    async with AsyncWATS(url, token=token) as api:
        tasks = [api.report.get_report(id) for id in report_ids]
        reports = await asyncio.gather(*tasks)
        return reports
```

---

## Common Gotchas

| Issue | Solution |
|-------|----------|
| `RuntimeError: no running event loop` | Use `asyncio.run()` or run inside async function |
| `AuthenticationError` on first call | Token may be expired; get a new one |
| `SSL certificate verify failed` | Set `verify_ssl=False` for self-signed certs |
| `TimeoutError` on large queries | Increase timeout or add pagination |
| Empty results from filter | Check OData syntax; use `ODataFilterBuilder` |

---

## Links

- 📚 [Full Documentation](https://github.com/olreppe/pyWATS)
- 🐛 [Report Issues](https://github.com/olreppe/pyWATS/issues)
- 📝 [Changelog](https://github.com/olreppe/pyWATS/blob/main/CHANGELOG.md)
- 🔄 [Migration Guide](https://github.com/olreppe/pyWATS/blob/main/MIGRATION.md)
