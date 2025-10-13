# REST API Client Workarounds

This document describes known issues with the generated OpenAPI client and the workarounds implemented in pyWATS.

**Last Updated:** 2025-10-13

---

## Issue #1: Empty Headers Override Client Defaults

### Problem
The generated OpenAPI client code creates empty headers dictionaries in endpoint functions, which override the httpx client's default headers. This causes authentication headers (and other default headers) to be missing from HTTP requests.

### Example
In `src/pyWATS/rest_api/public/api/report/report_post_wsjf.py`:
```python
def _get_kwargs(*, body: Dict[str, Any]) -> dict[str, Any]:
    headers: dict[str, Any] = {}  # <-- Empty dict created
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Report/WSJF",
        "json": body,
    }
    _kwargs["headers"] = headers  # <-- Overrides client headers
    return _kwargs
```

### Workaround
**Location:** `src/pyWATS/rest_api/_http_client.py`

The `WatsHttpClient` class monkey-patches the httpx `Client.request()` method during initialization to intercept all requests and inject authentication headers before they are sent.

```python
def _patched_request(*args, **kwargs):
    """Intercept and inject authentication headers"""
    request_headers = kwargs.get('headers', {})
    # Merge our custom headers with request headers
    merged_headers = {}
    merged_headers.update(_custom_headers)
    merged_headers.update(request_headers_dict)
    kwargs['headers'] = merged_headers
    return _original_request(*args, **kwargs)
```

### Impact
- All HTTP requests have correct authentication headers
- No changes needed to generated client code
- Transparent to users of the API

---

## Issue #2: AuthenticatedClient Bearer Token Logic

### Problem
The `AuthenticatedClient` class automatically formats the Authorization header as:
```python
self._headers[self.auth_header_name] = f"{self.prefix} {self.token}"
```

When we pass `token=""` and `prefix=""`, this results in `Authorization: " "` (a space), which is then overridden by the empty headers from Issue #1, leaving an empty Authorization header.

### Workaround
**Location:** `src/pyWATS/rest_api/_http_client.py`

We bypass the parent class's header logic entirely:

1. Don't pass headers to `super().__init__()`
2. Create our own `httpx.Client` with correct headers
3. Never call `super().get_httpx_client()`
4. Set `self.prefix = ""` to prevent any Bearer token logic

```python
def __init__(self, base_url: str, token: str, **kwargs):
    # Create headers with Basic auth
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Initialize parent WITHOUT headers
    super().__init__(base_url=base_url, token="", **kwargs)
    self.prefix = ""
    
    # Create our own httpx client
    self._custom_httpx_client = httpx.Client(
        base_url=base_url,
        headers=headers,
        # ... other settings
    )
```

### Impact
- WATS API requires Basic authentication instead of Bearer
- All requests use `Authorization: Basic <token>` header
- Parent class's Bearer token logic is completely bypassed

---

## Issue #3: API Returns List, Client Expects Dict

### Problem
The `/api/Report/WSJF` endpoint returns a JSON array with one element:
```json
[{"ID": "uuid", "uuid": "uuid", "Report_ID": 1}]
```

But the OpenAPI spec (and generated client) expects a single object:
```json
{"ID": "uuid", "uuid": "uuid", "Report_ID": 1}
```

This causes `VirincoWATSModelsStoreInsertReportResult.from_dict()` to fail with:
```
ValueError: dictionary update sequence element #0 has length 3; 2 is required
```

### Workaround
**Location:** `src/pyWATS/modules/report.py` in `create_report()` method

We manually handle the HTTP response and extract the first element from the list:

```python
# Get raw response
kwargs = report_post_wsjf._get_kwargs(body=wsjf_data)
raw_response = self.http_client.get_httpx_client().request(**kwargs)

response_json = raw_response.json()

# Extract first element if it's a list
if isinstance(response_json, list) and len(response_json) > 0:
    result_dict = cast(Dict[str, Any], response_json[0])
elif isinstance(response_json, dict):
    result_dict = cast(Dict[str, Any], response_json)

# Now parse the dict
parsed_result = VirincoWATSModelsStoreInsertReportResult.from_dict(result_dict)
```

### Impact
- Report submission works correctly
- Bypasses the generated `sync_detailed()` method
- Handles both list and dict responses (future-proof if API changes)

---

## Future Improvements

### Short-term
1. Document these workarounds in code comments
2. Add unit tests to verify workarounds continue to function
3. Monitor API changes that might make workarounds obsolete

### Long-term
1. **Fix OpenAPI Specification**
   - Update the spec to correctly describe the list response for `/api/Report/WSJF`
   - Add proper security schemes for Basic authentication
   - Ensure all response formats match actual API behavior

2. **Regenerate Client**
   - Use updated OpenAPI spec to regenerate the client
   - Test thoroughly to ensure issues are resolved

3. **Alternative Solutions**
   - Consider using a different OpenAPI generator (e.g., `openapi-generator` instead of `openapi-python-client`)
   - Evaluate patching the generator template to merge headers instead of replacing them
   - Write a custom post-generation script to fix known issues

4. **API Changes**
   - Work with API maintainers to standardize response formats
   - Consider adding a flag to return dict instead of list (breaking change)
   - Document expected vs actual behavior in API documentation

---

## Testing

When modifying these workarounds, verify:

1. **Authentication works:**
   ```python
   api = WATSApi(base_url="https://server.wats.com", token="<base64_token>")
   report = api.report.create_uut_report(...)
   # Should succeed with 200 OK
   ```

2. **Headers are correct:**
   - Check that `Authorization: Basic <token>` is present in requests
   - Verify `Content-Type: application/json` is set
   - Ensure no `Authorization: ` (empty) headers

3. **Report submission works:**
   ```python
   report_id = api.report.submit_report(report)
   # Should return valid UUID string
   ```

4. **Error handling:**
   - Test with invalid token (should get 401)
   - Test with malformed report (should get 400)
   - Verify WATSException messages are helpful

---

## Contact

For questions about these workarounds or to report new issues:
- Review the code in `src/pyWATS/rest_api/_http_client.py`
- Check the inline documentation in affected modules
- Open an issue in the repository with reproducible examples
