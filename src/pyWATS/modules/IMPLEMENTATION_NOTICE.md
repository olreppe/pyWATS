# Module Implementation Guide

This document provides guidance for implementing new module methods in pyWATS.

**Last Updated:** 2025-10-13

---

## Authentication: Already Handled ✅

All authentication issues are handled globally in `WatsHttpClient` (located in `src/pyWATS/rest_api/_http_client.py`). You **do not need to patch authentication** for every function you implement.

### What's Fixed Automatically

The following work for **ALL** REST API calls without any special handling:

1. **Authentication headers** - The monkey-patch injects `Authorization: Basic <token>` into every request
2. **Content-Type and Accept headers** - Automatically added to all requests  
3. **Empty headers override** - The patched `request()` method merges headers correctly

### Standard Usage

For most endpoints, just use the generated client normally:

```python
from ..rest_api.public.api.product import product_get_by_id

def get_product(self, product_id: str) -> Product:
    """Get a product by ID."""
    response = product_get_by_id.sync(
        client=self.http_client,  # Authentication handled automatically
        id=product_id
    )
    return response  # Works out of the box!
```

---

## Response Parsing: May Need Per-Endpoint Fixes ⚠️

Some endpoints may have mismatches between the OpenAPI spec and the actual API implementation. These require case-by-case handling.

### Common Issues

#### 1. Response Format Mismatches

**Symptom:**
```
ValueError: dictionary update sequence element #0 has length 3; 2 is required
```

**Cause:** The API returns a list `[{...}]` but the generated client expects a dict `{...}` (or vice versa).

**Solution:** Parse the raw response manually:

```python
def submit_report(self, report: Report) -> str:
    """Submit a report to WATS."""
    try:
        # Get raw response instead of using sync_detailed()
        from ..rest_api.public.api.report import report_post_wsjf as rp
        kwargs = rp._get_kwargs(body=report.model_dump())
        raw_response = self.http_client.get_httpx_client().request(**kwargs)
        
        if raw_response.status_code == 200:
            response_json = raw_response.json()
            
            # Handle list vs dict mismatch
            if isinstance(response_json, list) and len(response_json) > 0:
                result_dict = response_json[0]
            else:
                result_dict = response_json
            
            # Parse the corrected structure
            parsed = ResponseModel.from_dict(result_dict)
            return parsed.id
        else:
            raise WATSException(f"HTTP {raw_response.status_code}: {raw_response.text}")
            
    except Exception as e:
        raise WATSException(f"Failed to submit report: {str(e)}")
```

#### 2. Missing or Extra Fields in Response Models

**Symptom:**
```
AttributeError: 'ResponseModel' object has no attribute 'fieldName'
KeyError: 'required_field'
```

**Cause:** The API returns fields that aren't in the generated model, or the model expects fields that aren't in the response.

**Solution A - Use raw JSON:**
```python
response_json = raw_response.json()
# Work with the dict directly instead of parsing to model
return response_json.get('id')
```

**Solution B - Update spec and regenerate:**
```bash
# Fix the OpenAPI spec, then regenerate the client
# Document the issue in WORKAROUNDS.md
```

#### 3. Query Parameters Not Generated

**Symptom:**
The generated endpoint function doesn't accept OData parameters like `$filter`, `$top`, `$skip`, `$orderby`.

**Cause:** The OpenAPI spec didn't properly define these query parameters.

**Solution:** Pass them manually in the request:

```python
def find_reports(self, filter: str = None, top: int = None) -> List[Report]:
    """Find reports with OData filtering."""
    # Build URL with query parameters manually
    params = {}
    if filter:
        params['$filter'] = filter
    if top:
        params['$top'] = str(top)
    
    # Make request with custom params
    httpx_client = self.http_client.get_httpx_client()
    response = httpx_client.get("/api/Report/Query", params=params)
    
    if response.status_code == 200:
        return [ReportModel.from_dict(r) for r in response.json()]
    else:
        raise WATSException(f"Query failed: {response.status_code}")
```

---

## Implementation Workflow

When implementing a new module method, follow this workflow:

### Step 1: Try the Standard Approach First

```python
def new_method(self, param: str) -> Result:
    """Description of what this method does."""
    response = endpoint_function.sync(
        client=self.http_client,
        param=param
    )
    return response
```

### Step 2: Test Thoroughly

Run your implementation and check for:
- ✅ **200 OK responses** - Method works as expected
- ❌ **401 Unauthorized** - Authentication issue (shouldn't happen with `WatsHttpClient`)
- ❌ **ValueError: dictionary update...** - Response format mismatch (need workaround)
- ❌ **AttributeError: object has no attribute...** - Model parsing issue (need workaround)
- ❌ **Response is None** - Unexpected status code or model mismatch

### Step 3: Debug with Raw Response (if needed)

```python
# Add debug code to see what's actually being returned
kwargs = endpoint_function._get_kwargs(param=param)
raw_response = self.http_client.get_httpx_client().request(**kwargs)

print(f"Status: {raw_response.status_code}")
print(f"Headers: {raw_response.headers}")
print(f"Content: {raw_response.json()}")
```

### Step 4: Add Workaround Only if Necessary

If the standard approach fails:
1. Implement a workaround using raw response handling
2. Add a comment explaining why the workaround is needed
3. Document the issue in `src/pyWATS/rest_api/WORKAROUNDS.md`

```python
def new_method(self, param: str) -> Result:
    """Description of what this method does."""
    # WORKAROUND: API returns list but spec says dict
    # See WORKAROUNDS.md Issue #3 for details
    kwargs = endpoint_function._get_kwargs(param=param)
    raw_response = self.http_client.get_httpx_client().request(**kwargs)
    
    if raw_response.status_code == 200:
        response_json = raw_response.json()
        # Handle the mismatch...
        return Result.from_dict(response_json)
    else:
        raise WATSException(f"Failed: {raw_response.status_code}")
```

### Step 5: Document the Issue

If you needed a workaround, add it to `WORKAROUNDS.md`:

```markdown
## Issue #4: Endpoint X Returns Wrong Format

### Problem
The `/api/X/Y` endpoint returns...

### Workaround
**Location:** `src/pyWATS/modules/x.py` in `method_name()`

We manually parse...

### Impact
- Method works correctly
- Bypasses generated client...
```

---

## Error Handling Best Practices

Always wrap REST API calls in proper exception handling:

```python
def method(self, param: str) -> Result:
    """Description."""
    try:
        response = endpoint.sync(client=self.http_client, param=param)
        
        if response is None:
            raise WATSException("No response received from server")
        
        return response
        
    except WATSException:
        # Re-raise WATS exceptions as-is
        raise
    except Exception as e:
        # Wrap unexpected exceptions
        raise WATSException(f"Failed to execute method: {str(e)}")
```

---

## Type Hints and Documentation

Follow these standards for consistency:

```python
from typing import List, Optional, Dict, Any, Union

def method_name(
    self,
    required_param: str,
    optional_param: Optional[int] = None
) -> Union[Result, List[Result]]:
    """
    Brief one-line description.
    
    Longer description with more details about what this method does,
    when to use it, and any important considerations.
    
    Args:
        required_param: Description of this parameter
        optional_param: Description of optional parameter with default behavior
        
    Returns:
        Description of what is returned
        
    Raises:
        WATSException: Description of when this is raised
        WATSNotFoundError: Description of when this is raised
        
    Note:
        Any important notes, workarounds, or special considerations.
        Reference WORKAROUNDS.md if a workaround is used.
        
    Example:
        >>> api = WATSApi(...)
        >>> result = api.module.method_name("param_value")
        >>> print(result)
    """
    pass
```

---

## Summary

✅ **Authentication is automatic** - No special handling needed per endpoint

⚠️ **Response parsing may need fixes** - Check each endpoint, add workarounds as needed

📝 **Document everything** - Comments in code + entries in WORKAROUNDS.md

🧪 **Test thoroughly** - Run your implementation, check for errors, debug with raw responses

The `/api/Report/WSJF` list-vs-dict issue is likely an **exception rather than the rule**. Most endpoints should work fine with the standard approach!

---

## Need Help?

- Review existing module implementations for examples
- Check `WORKAROUNDS.md` for known issues
- Look at `_http_client.py` to understand authentication handling
- Test with Postman to verify actual API behavior vs OpenAPI spec
