# pywats.domains.scim - Class Reference

Auto-generated class reference for `pywats.domains.scim`.

---

## `scim.async_repository`

### `AsyncScimRepository`

_Async repository for SCIM API operations._

---

## `scim.async_service`

### `AsyncScimService`

_Async service for SCIM user provisioning operations._

---

## `scim.models`

### `ScimListResponse(PyWATSModel)`

_Represents a SCIM list response._

**Class Variables:**
- `total_results: Optional[...]`
- `items_per_page: Optional[...]`
- `start_index: Optional[...]`
- `resources: Optional[...]`
- `schemas: Optional[...]`
- `model_config`

---

### `ScimPatchOperation(PyWATSModel)`

_Represents a single SCIM patch operation._

**Class Variables:**
- `op: Optional[...]`
- `path: Optional[...]`
- `value: Optional[...]`

---

### `ScimPatchRequest(PyWATSModel)`

_Represents a SCIM patch request body._

**Class Variables:**
- `schemas: Optional[...]`
- `operations: Optional[...]`

---

### `ScimToken(PyWATSModel)`

_Represents a SCIM JWT token response._

**Class Variables:**
- `token: Optional[...]`
- `expires_utc: Optional[...]`
- `duration_days: Optional[...]`
- `model_config`

---

### `ScimUser(PyWATSModel)`

_Represents a SCIM user resource._

**Class Variables:**
- `id: Optional[...]`
- `user_name: Optional[...]`
- `display_name: Optional[...]`
- `active: Optional[...]`
- `external_id: Optional[...]`
- `name: Optional[...]`
- `emails: Optional[...]`
- `schemas: Optional[...]`
- `meta: Optional[...]`
- `model_config`

---

### `ScimUserEmail(PyWATSModel)`

_SCIM user email entry._

**Class Variables:**
- `value: Optional[...]`
- `type: Optional[...]`
- `primary: Optional[...]`

---

### `ScimUserName(PyWATSModel)`

_SCIM user name components._

**Class Variables:**
- `formatted: Optional[...]`
- `given_name: Optional[...]`
- `family_name: Optional[...]`

---
