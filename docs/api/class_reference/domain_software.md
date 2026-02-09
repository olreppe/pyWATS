# pywats.domains.software - Class Reference

Auto-generated class reference for `pywats.domains.software`.

---

## `software.async_repository`

### `AsyncSoftwareRepository`

_Async Software distribution data access layer._

---

## `software.async_service`

### `AsyncSoftwareService`

_Async Software distribution business logic layer._

---

## `software.enums`

### `PackageStatus(str, Enum)`

_Software package status_

**Class Variables:**
- `DRAFT`
- `PENDING`
- `RELEASED`
- `REVOKED`

---

## `software.models`

### `Package(PyWATSModel)`

_Represents a software distribution package._

**Class Variables:**
- `package_id: Optional[...]`
- `name: Optional[...]`
- `description: Optional[...]`
- `version: Optional[...]`
- `status: Optional[...]`
- `install_on_root: Optional[...]`
- `root_directory: Optional[...]`
- `priority: Optional[...]`
- `tags: Optional[...]`
- `created_utc: Optional[...]`
- `modified_utc: Optional[...]`
- `created_by: Optional[...]`
- `modified_by: Optional[...]`
- `files: Optional[...]`

---

### `PackageFile(PyWATSModel)`

_Represents a file within a software package._

**Class Variables:**
- `file_id: Optional[...]`
- `filename: Optional[...]`
- `path: Optional[...]`
- `size: Optional[...]`
- `checksum: Optional[...]`
- `created_utc: Optional[...]`
- `modified_utc: Optional[...]`
- `attributes: Optional[...]`

---

### `PackageTag(PyWATSModel)`

_Represents a tag/metadata on a software package._

**Class Variables:**
- `key: Optional[...]`
- `value: Optional[...]`

---

### `VirtualFolder(PyWATSModel)`

_Represents a virtual folder in Production Manager._

**Class Variables:**
- `folder_id: Optional[...]`
- `name: Optional[...]`
- `path: Optional[...]`
- `description: Optional[...]`

---
