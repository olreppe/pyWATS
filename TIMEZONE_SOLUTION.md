# Timezone Handling Documentation

## Problem (Resolved)
All UUT and UUR reports were showing timestamps 1 hour earlier than the actual local time when viewed in the web UI.

## Root Cause
The issue was NOT about what we send to the server, but rather how we handle both `start` and `start_utc` fields during serialization and deserialization.

## Key Findings
1. **Server expects**: Only the `start` field with timezone offset (e.g., `2025-12-12T14:08:05+01:00`)
2. **Server returns**: Both `start` (local time with offset) AND `startUTC` (UTC equivalent)
3. **Problem**: We were excluding `start_utc` from serialization but also preventing proper deserialization

## Solution
Modified `src/pywats/domains/report/report_models/report.py` to implement flexible timezone handling:

### Features
1. **Set either field** - Can set `start` (local time) OR `start_utc` (UTC time)
2. **Automatic synchronization** - The other field is automatically computed
3. **Proper serialization** - Only `start` is sent to server (`start_utc` has `exclude=True`)
4. **Proper deserialization** - Both fields are read from server responses

### Implementation Details

```python
start: Optional[datetime] = Field(
    default=None,
    description="Local start time with timezone offset. Server uses this as authoritative."
)

start_utc: Optional[datetime] = Field(
    default=None,
    validation_alias="startUTC",
    serialization_alias="startUTC",
    exclude=True,  # Not sent to server
    description="UTC equivalent. Auto-computed and kept in sync."
)

@model_validator(mode='after')
def sync_start_times(self) -> 'Report':
    # Case 1: Both set - keep as-is
    # Case 2: Only start set - compute start_utc
    # Case 3: Only start_utc set - compute start
    # Case 4: Neither set - use current time
```

### Usage Examples

```python
# Example 1: Default behavior (current time)
report = wats.report.create_uut_report(...)
# Both start and start_utc are automatically set

# Example 2: Set local time explicitly
report = UUTReport(
    start=datetime(2025, 12, 12, 14, 30, 0).astimezone(),
    ...
)
# start_utc is automatically computed

# Example 3: Set UTC time (less common)
report = UUTReport(
    start_utc=datetime(2025, 12, 12, 13, 30, 0, tzinfo=timezone.utc),
    ...
)
# start is automatically computed as local time

# Example 4: Set both (user takes responsibility for sync)
report = UUTReport(
    start=local_time,
    start_utc=utc_time,
    ...
)
```

## Verification
Confirmed via comprehensive test suites:
- `test_timezone_sync.py` - Tests all synchronization scenarios
- `test_timezone_validation.py` - Integration tests with server
- `test_server_roundtrip.py` - Full round-trip verification
- `test_deserialization_timezone.py` - Deserialization analysis

## Result
✓ Times are now correctly displayed everywhere
✓ API sends only `start` field to server
✓ API correctly reads both fields from server
✓ Automatic synchronization between local and UTC times
✓ Flexible - can set either field as needed
