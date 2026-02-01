# Error Handling Strategy

> **Status**: ✅ Exception hierarchy COMPLETE, ErrorHandlingMixin COMPLETE

## Implementation Status

| Item | Status | Notes |
|------|--------|-------|
| Exception hierarchy | ✅ Complete | `pywats/core/exceptions.py` |
| WatsApiError base | ✅ Complete | With status_code and details |
| AuthenticationError | ✅ Complete | For 401/403 |
| NotFoundError | ✅ Complete | For 404 |
| ValidationError | ✅ Complete | For 400 |
| ServerError | ✅ Complete | For 500+ |
| ErrorHandlingMixin | ✅ Complete | `pywats_client/gui/error_mixin.py` |
| BasePage integration | ✅ Complete | All pages inherit ErrorHandlingMixin |

## 1. Objectives
*   **Fail Fast, Fail Loud**: Eliminate silent failures. If an API call fails, the application should know exactly why (Network, Auth, Validation, Server).
*   **Strong Typing**: Use specific exception classes rather than returning a generic `Response` object with a status code.
*   **Separation**: Separating "Networking Errors" (HTTP layer) from "Domain Errors" (Business Logic layer).
*   **No Backwards Compatibility**: We are removing the `Response.is_error` checking pattern entirely.

## 2. New Exception Hierarchy (`pywats.core.exceptions`)

We will introduce a strict hierarchy. The base `PyWATSError` will be the catch-all.

```python
class PyWATSError(Exception):
    """Base for all WATS errors."""
    pass

class WatsApiError(PyWATSError):
    """Base for errors returned by the API (HTTP 4xx/5xx)."""
    def __init__(self, message, status_code, details=None):
        self.status_code = status_code
        self.details = details
        super().__init__(f"[{status_code}] {message}")

class AuthenticationError(WatsApiError): # 401/403
    pass

class NotFoundError(WatsApiError):       # 404
    pass

class ValidationError(WatsApiError):     # 400
    pass

class ServerError(WatsApiError):         # 500+
    pass
```

## 3. Core Implementation (`HttpClient`)

The `HttpClient` will no longer return a wrapper that the user has to check. It will validate the response immediately.

```python
# HttpClient.py

async def _request(self, ...):
    response = await self.client.request(...)
    
    if response.is_error:
        self._raise_for_status(response)
        
    # Only returns data if successful
    return response.json()

def _raise_for_status(self, response):
    """Isolate HTTP error parsing logic here."""
    try:
        data = response.json()
        msg = data.get("message") or data.get("detail") or response.reason_phrase
    except:
        msg = response.text
        
    if response.status_code == 401:
        raise AuthenticationError("Invalid Token", 401)
    elif response.status_code == 404:
        raise NotFoundError(msg, 404)
    elif 400 <= response.status_code < 500:
        raise ValidationError(msg, response.status_code, details=data)
    else:
        raise ServerError("WATS Server Error", response.status_code)
```

## 4. Repository Layer Changes

Repositories will no longer need `ErrorHandler.handle_response`. They can assume if the call returns, it is valid data.

**Old Pattern:**
```python
resp = client.get(...)
data = error_handler(resp) # easy to forget
if data:
    return Unit(data)
```

**New Pattern:**
```python
# exceptions propagate automatically up to the caller
data = await client.get(...) 
return Unit(**data)
```

## 5. Handling in the GUI

The GUI is the only place where errors should be "caught" and suppressed (by showing a dialog).

**Global Error Handling Mixin:**
```python
class ErrorHandlingMixin:
    def handle_error(self, e: Exception, context: str):
        if isinstance(e, AuthenticationError):
            self.show_login_dialog() # Trigger re-login
        elif isinstance(e, ValidationError):
            QMessageBox.warning(self, "Invalid Input", str(e))
        elif isinstance(e, ServerError):
            QMessageBox.critical(self, "Server Error", "WATS is acting up...")
        else:
            logger.exception(e)
            QMessageBox.critical(self, "App Error", f"Unexpected error: {e}")
```
