# Control Panel Manager Tool

The Control Panel Manager is a comprehensive administrative tool for managing WATS configuration across all domains. It provides a unified interface for managing assets, products, production, software, and process configuration.

## Overview

| Aspect | Details |
|--------|---------|
| **Tool Name** | `control_panel` |
| **Category** | Admin |
| **Profiles** | `full`, `admin` |
| **Purpose** | Manage WATS configuration across all domains |

## Domains

The Control Panel operates across five domains:

### Asset Domain
Manage test equipment, fixtures, and calibration.

| Entity Type | Operations | Description |
|-------------|------------|-------------|
| `asset` | list, get, create, delete, set_state | Physical assets (test equipment, fixtures) |
| `asset_type` | list, get | Asset categories |

### Product Domain
Manage products, revisions, and BOM.

| Entity Type | Operations | Description |
|-------------|------------|-------------|
| `product` | list, get, create | Part numbers with metadata |
| `revision` | list, get, create | Product revisions |
| `product_group` | list | Product groupings |

### Production Domain
Manage units, phases, and assembly relationships.

| Entity Type | Operations | Description |
|-------------|------------|-------------|
| `unit` | get, create, set_phase, verify | Production units (serialized items) |
| `phase` | list, get | Unit phases (Under Production, Finalized, etc.) |
| `assembly` | add_child, remove_child, verify | Parent-child relationships |

### Software Domain
Manage software packages and deployment.

| Entity Type | Operations | Description |
|-------------|------------|-------------|
| `package` | list, get, create, delete, release, revoke | Software packages |
| `virtual_folder` | list | Package deployment folders |

### Process Domain
View process/operation definitions (read-only).

| Entity Type | Operations | Description |
|-------------|------------|-------------|
| `test_operation` | list, get | UUT test operations |
| `repair_operation` | list, get | UUR repair operations |
| `wip_operation` | list, get | WIP tracking operations |

## Usage

### Basic Pattern

```python
# Domain + Operation + (optional) Entity Type + (optional) Parameters
control_panel(
    domain="asset",           # Which domain
    operation="list",         # What to do
    entity_type="asset",      # Which entity (defaults to primary)
    parameters={...}          # Operation-specific parameters
)
```

### Operations

| Operation | Purpose | Common Parameters |
|-----------|---------|-------------------|
| `list` | List all entities | `filter`, `top` |
| `get` | Get specific entity | `identifier` required |
| `create` | Create new entity | Entity-specific params |
| `update` | Modify entity | `identifier` + params |
| `delete` | Remove entity | `identifier` + `confirm_destructive=true` |
| `set_state` | Change asset state | `identifier`, `state` |
| `set_phase` | Change unit phase | `serial_number`, `part_number`, `phase` |
| `add_child` | Add to assembly | Parent and child identifiers |
| `remove_child` | Remove from assembly | Parent and child identifiers |
| `verify` | Verify unit/assembly | `serial_number`, `part_number` |
| `release` | Release package | `identifier` |
| `revoke` | Revoke package | `identifier` + `confirm_destructive=true` |

## Examples

### List All Assets

```python
control_panel(
    domain="asset",
    operation="list"
)
```

### Get Specific Product

```python
control_panel(
    domain="product",
    operation="get",
    identifier="PN-123456"
)
```

### Create an Asset

```python
control_panel(
    domain="asset",
    operation="create",
    parameters={
        "serial_number": "EQUIP-001",
        "type_id": "uuid-of-asset-type",
        "name": "Test Station Alpha",
        "location": "Lab A"
    }
)
```

### Set Asset State

```python
control_panel(
    domain="asset",
    operation="set_state",
    identifier="EQUIP-001",
    parameters={"state": "IN_MAINTENANCE"}
)
```

Valid states: `IN_OPERATION`, `IN_TRANSIT`, `IN_MAINTENANCE`, `IN_CALIBRATION`, `IN_STORAGE`, `SCRAPPED`

### Set Unit Phase

```python
control_panel(
    domain="production",
    operation="set_phase",
    identifier="SN-001",
    parameters={
        "part_number": "PN-123456",
        "phase": "Finalized",
        "comment": "Passed all tests"
    }
)
```

### Verify Unit Grade

```python
control_panel(
    domain="production",
    operation="verify",
    identifier="SN-001",
    parameters={
        "part_number": "PN-123456",
        "revision": "A"
    }
)
```

Returns: grade, status, pass metrics if verification rules are configured.

### Add Component to Assembly

```python
control_panel(
    domain="production",
    operation="add_child",
    entity_type="assembly",
    parameters={
        "parent_serial": "PARENT-001",
        "parent_part": "PN-ASSY",
        "child_serial": "CHILD-001",
        "child_part": "PN-COMP"
    }
)
```

### Create Product Revision

```python
control_panel(
    domain="product",
    operation="create",
    entity_type="revision",
    parameters={
        "part_number": "PN-123456",
        "revision": "B",
        "name": "Updated revision"
    }
)
```

### Release Software Package

```python
control_panel(
    domain="software",
    operation="release",
    identifier="package-uuid-here"
)
```

### Delete Asset (Requires Confirmation)

```python
control_panel(
    domain="asset",
    operation="delete",
    identifier="EQUIP-001",
    confirm_destructive=True  # Required for destructive operations
)
```

## Destructive Operations

The following operations require `confirm_destructive=True`:

- `delete` (any domain)
- `revoke` (software packages)

This prevents accidental data loss when using the tool.

## Error Handling

The tool returns a `ControlPanelResult` with:

| Field | Description |
|-------|-------------|
| `success` | Boolean indicating operation success |
| `message` | Human-readable result message |
| `data` | Single item data (for get/create operations) |
| `items` | List of items (for list operations) |
| `count` | Number of items returned |

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Missing required parameters" | Required fields not provided | Check parameters for operation |
| "Identifier required" | get/update/delete without identifier | Provide `identifier` field |
| "Destructive operation requires confirm_destructive=true" | Trying to delete/revoke | Add `confirm_destructive=True` |
| "Unknown entity type" | Invalid entity_type for domain | Check valid entity types |
| "Not found" | Entity doesn't exist | Verify identifier is correct |

## Integration with Other Tools

The Control Panel is often used in conjunction with:

| Tool | Integration Pattern |
|------|---------------------|
| `analyze_unit` | View unit history, then manage in Control Panel |
| `analyze_yield` | Identify issues, then adjust configuration |
| Asset analysis tools | Check asset health, then update state |

### Example Workflow: Unit Investigation

1. **Analyze unit** with `analyze_unit`:
   ```python
   analyze_unit(serial_number="SN-001", part_number="PN-123")
   ```

2. **Based on findings**, update unit phase:
   ```python
   control_panel(
       domain="production",
       operation="set_phase",
       identifier="SN-001",
       parameters={
           "part_number": "PN-123",
           "phase": "Scrapped",
           "comment": "Multiple failures - components damaged"
       }
   )
   ```

## Profile Configuration

### Full Profile
All tools including Control Panel.

### Admin Profile
Control Panel + Unit Analysis:
- `control_panel` - Full administrative capability
- `analyze_unit` - View unit data for context

## Technical Details

### Input Model

```python
class ControlPanelInput(ToolInput):
    domain: ManagementDomain          # Required
    operation: OperationType          # Required
    entity_type: Optional[str]        # Defaults to primary entity
    identifier: Optional[str]         # For get/update/delete
    parameters: Optional[Dict]        # Operation-specific
    confirm_destructive: bool = False # For delete/revoke
```

### Result Model

```python
class ControlPanelResult(BaseModel):
    domain: ManagementDomain
    operation: OperationType
    entity_type: str
    success: bool
    message: str
    data: Optional[Dict]      # Single item
    items: Optional[List]     # Multiple items
    count: int                # Item count
```

## API Coverage

The Control Panel wraps the following pyWATS API services:

| Domain | Service | Methods Used |
|--------|---------|--------------|
| Asset | `api.asset` | `get_assets`, `get_asset`, `create_asset`, `delete_asset`, `set_asset_state`, `get_asset_types`, `get_asset_type` |
| Product | `api.product` | `get_products`, `get_product`, `create_product`, `get_revisions`, `get_revision`, `create_revision`, `get_groups` |
| Production | `api.production` | `get_unit`, `create_units`, `set_unit_phase`, `get_unit_grade`, `get_phases`, `get_phase`, `add_child_to_assembly`, `remove_child_from_assembly`, `verify_assembly` |
| Software | `api.software` | `get_packages`, `get_package`, `get_package_by_name`, `create_package`, `delete_package`, `delete_package_by_name`, `submit_for_review`, `release_package`, `revoke_package`, `get_virtual_folders` |
| Process | `api.process` | `get_test_operations`, `get_repair_operations`, `get_wip_operations`, `get_processes`, `get_test_operation`, `get_repair_operation`, `get_wip_operation`, `get_process` |
