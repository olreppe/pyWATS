# 🧩 GitHub Agent Prompt for Generating `pyWATS.rest_api` Clients

This document instructs your GitHub agent or CI workflow to generate **Python REST API clients** for both the public and internal WATS APIs using **openapi-python-client**, structured under your existing `pyWATS` project.

---

## 🧭 Objective

Generate typed, Pydantic v2-compatible API clients and models from your OpenAPI specifications (`openapi_public.json`, `openapi_internal.json`) and organize them under:

```
src/pyWATS/rest_api/
├── http_client.py
├── public/
│   ├── report/
│   ├── product/
│   ├── production/
│   └── ...
└── internal/
    ├── report/
    ├── product/
    ├── production/
    └── ...
```

---

## ⚙️ Generation Details

### 1️⃣ Use openapi-python-client

Run the following commands (or their equivalents in your workflow):

```bash
openapi-python-client generate --path openapi_public.json --meta none --output-path src/pyWATS/rest_api/public
openapi-python-client generate --path openapi_internal.json --meta none --output-path src/pyWATS/rest_api/internal
```

- Ensure the latest `openapi-python-client` version is installed (`pip install -U openapi-python-client`).
- The generator should output models using **Pydantic v2**.
- Logical grouping: move endpoints into folders under `report/`, `product/`, `production/`, etc.

---

## 🧱 Unified HTTP Client

After generation, add this custom subclass to `src/pyWATS/rest_api/http_client.py`:

```python
import httpx
from typing import Optional
from pyWATS.rest_api.public.client import Client as BaseClient  # generated base client

class WatsHttpClient(BaseClient):
    """Unified WATS HTTP client for all REST APIs."""

    def __init__(self, base_url: str, base64_token: str, timeout: float = 30.0, **kwargs):
        super().__init__(base_url=base_url, timeout=timeout, **kwargs)
        self._http = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Basic {base64_token}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    def get_httpx_client(self) -> httpx.Client:
        """Override to return the persistent shared httpx.Client."""
        return self._http
```

---

## 🗂️ Final Directory Layout

```
src/
└── pyWATS/
    ├── __init__.py
    ├── rest_api/
    │   ├── __init__.py
    │   ├── http_client.py
    │   ├── public/
    │   │   ├── __init__.py
    │   │   ├── report/
    │   │   ├── product/
    │   │   └── production/
    │   └── internal/
    │       ├── __init__.py
    │       ├── report/
    │       ├── product/
    │       └── production/
    └── ...
```

---

## ✅ Post-Processing

1. Move the generated endpoint modules into the correct logical subfolders (report, product, etc.).
2. Ensure all subfolders contain an `__init__.py`.
3. Optionally, run `ruff` or `black` for cleanup and formatting.

---

## 🧪 Usage Example

```python
from pyWATS.rest_api.http_client import WatsHttpClient
from pyWATS.rest_api.public.report import dynamic_yield

client = WatsHttpClient("https://live.wats.com", base64_token="ZXhhbXBsZXRva2Vu")
data = dynamic_yield.sync(client=client, body={"partNumber": "X123", "testOperation": "Run"})
print(data)
```

---

## 🧰 Optional: Makefile Target

Add this to your `Makefile` to regenerate clients:

```makefile
generate-rest:
	openapi-python-client generate --path openapi_public.json --meta none --output-path src/pyWATS/rest_api/public
	openapi-python-client generate --path openapi_internal.json --meta none --output-path src/pyWATS/rest_api/internal
	@echo "✅ pyWATS REST API clients generated."
```

---

**Authoring Note:**  
This setup gives you:
- Full control of HTTP/auth logic (`WatsHttpClient` subclass).  
- Clean namespace hierarchy under `pyWATS.rest_api`.  
- Regeneration safety — you can delete/rebuild the generated code anytime.
