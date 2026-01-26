# Process Domain

The Process domain provides access to process and operation type definitions. Processes define the types of operations performed on units (e.g., Test, Repair, Assembly). This domain uses an in-memory cache with configurable refresh intervals to optimize performance by reducing API calls. It provides read-only access to process definitions.

## Table of Contents

- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Process Operations](#process-operations)
- [Cache Management](#cache-management)
- [Operation Types](#operation-types)
- [Advanced Usage](#advanced-usage)
- [API Reference](#api-reference)

---

## Quick Start

### Synchronous Usage

```python
from pywats import pyWATS

# Initialize
api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token"
)

# Get test operation
test_op = api.process.get_test_operation("ICT")

if test_op:
    print(f"Operation: {test_op.name}")
    print(f"Code: {test_op.code}")
    print(f"Type: {test_op.process_type}")

# Get repair operation
repair_op = api.process.get_repair_operation("Rework")

# Get operation by name or code
operation = api.process.get_operation("FCT")  # Can be name or code

# Refresh cache manually
api.process.refresh()

print(f"Cache last refreshed: {api.process.last_refresh}")
print(f"Refresh interval: {api.process.refresh_interval} seconds")
```

### Asynchronous Usage

For concurrent requests and better performance:

```python
import asyncio
from pywats import AsyncWATS

async def get_processes():
    async with AsyncWATS(
        base_url="https://your-wats-server.com",
        token="your-api-token"
    ) as api:
        # Get multiple operations concurrently
        ict, fct, repair = await asyncio.gather(
            api.process.get_test_operation("ICT"),
            api.process.get_test_operation("FCT"),
            api.process.get_repair_operation("Rework")
        )
        
        print(f"ICT code: {ict.code if ict else 'N/A'}")
        print(f"FCT code: {fct.code if fct else 'N/A'}")

asyncio.run(get_processes())
```

---

## Core Concepts

### Process (Operation Type)
A **Process** defines a type of operation:
- `name`: Operation name (e.g., "In-Circuit Test")
- `code`: Short code (e.g., "ICT")
- `process_type`: Type (TEST, REPAIR, ASSEMBLY, etc.)
- `description`: Operation description

### Process Types
Common process types:
- **TEST**: Testing operations (ICT, FCT, Functional Test)
- **REPAIR**: Repair and rework operations
- **ASSEMBLY**: Assembly and integration
- **CALIBRATION**: Calibration operations
- **INSPECTION**: Visual or automated inspection

### Caching
The Process service uses in-memory caching:
- **Default refresh**: 300 seconds (5 minutes)
- **Auto-refresh**: Cache refreshes when age exceeds interval
- **Thread-safe**: Uses locks for concurrent access
- **Performance**: Reduces API calls for frequently accessed data

---

## Process Operations

### Get Operation by Code or Name

```python
# Get by code
ict = api.process.get_operation("ICT")

if ict:
    print(f"Name: {ict.name}")
    print(f"Code: {ict.code}")
    print(f"Type: {ict.process_type}")
    print(f"Description: {ict.description}")

# Get by name
fct = api.process.get_operation("Functional Test")

if fct:
    print(f"Found: {fct.name} ({fct.code})")
```

### Get Test Operations

```python
# Get test operation specifically
test_op = api.process.get_test_operation("ICT")

if test_op:
    print(f"Test Operation: {test_op.name}")
    print(f"Code: {test_op.code}")
else:
    print("Test operation not found")

# Try by name or code
fct = api.process.get_test_operation("FCT")
functional = api.process.get_test_operation("Functional Test")

# Both should return the same operation
if fct and functional:
    assert fct.code == functional.code
    print(f"Found: {fct.name}")
```

### Get Repair Operations

```python
# Get repair operation
repair = api.process.get_repair_operation("Rework")

if repair:
    print(f"Repair Operation: {repair.name}")
    print(f"Code: {repair.code}")
    print(f"Type: {repair.process_type}")

# Common repair operations
repair_codes = ["Rework", "Repair", "Debug"]

for code in repair_codes:
    op = api.process.get_repair_operation(code)
    if op:
        print(f"  {code}: {op.name}")
```

### List All Operations

```python
# Get all operations (via cache)
# Note: This accesses internal cache - implementation may vary

all_operations = api.process.get_all_operations()

print(f"=== ALL OPERATIONS ({len(all_operations)}) ===\n")

# Group by type
by_type = {}
for op in all_operations:
    op_type = op.process_type
    if op_type not in by_type:
        by_type[op_type] = []
    by_type[op_type].append(op)

for op_type, ops in sorted(by_type.items()):
    print(f"{op_type}:")
    for op in ops:
        print(f"  {op.code}: {op.name}")
    print()
```

---

## Cache Management

### Check Cache Status

```python
from datetime import datetime

# Get cache info
last_refresh = api.process.last_refresh
refresh_interval = api.process.refresh_interval

print(f"=== CACHE STATUS ===")
print(f"Last refresh: {last_refresh}")
print(f"Refresh interval: {refresh_interval} seconds ({refresh_interval/60:.1f} minutes)")

# Calculate cache age
if last_refresh:
    age = (datetime.now() - last_refresh).total_seconds()
    print(f"Cache age: {age:.0f} seconds")
    
    if age > refresh_interval:
        print("⚠ Cache is stale and will refresh on next access")
    else:
        remaining = refresh_interval - age
        print(f"✓ Cache is fresh ({remaining:.0f} seconds until refresh)")
else:
    print("Cache not initialized")
```

### Manual Refresh

```python
# Force cache refresh
print("Refreshing process cache...")
api.process.refresh()

print(f"Cache refreshed at: {api.process.last_refresh}")
```

### Configure Refresh Interval

```python
# Set custom refresh interval (in seconds)
# 10 minutes = 600 seconds
api.process.refresh_interval = 600

print(f"Refresh interval set to {api.process.refresh_interval} seconds")

# For frequently changing process definitions, use shorter interval
# 1 minute = 60 seconds
api.process.refresh_interval = 60

# For stable definitions, use longer interval
# 1 hour = 3600 seconds
api.process.refresh_interval = 3600
```

### Auto-Refresh Behavior

```python
import time

# Cache auto-refreshes when age exceeds interval
# Set short interval for demo
api.process.refresh_interval = 5  # 5 seconds

# First access - loads cache
op1 = api.process.get_operation("ICT")
print(f"First access: {api.process.last_refresh}")

# Wait for cache to expire
time.sleep(6)

# Next access - auto-refreshes
op2 = api.process.get_operation("FCT")
print(f"After expiry: {api.process.last_refresh}")

# Reset to default
api.process.refresh_interval = 300
```

---

## Operation Types

### Using Processes in Production

```python
# When creating production records, reference processes

from pywats.domains.production.models import UnitInfo

# Get the test operation
test_op = api.process.get_test_operation("ICT")

# Use in unit creation or update
unit = api.production.get_unit("SN12345")

if unit and test_op:
    # Record that unit went through this process
    # (actual method depends on Production API)
    print(f"Unit {unit.serial_number} processed through {test_op.name}")
```

### Using Processes in Reports

```python
# When creating UUT reports, reference the operation

from pywats.domains.report.models import UUTReport

# Get operation
operation = api.process.get_test_operation("FCT")

# Create report with operation reference
report = UUTReport(
    serial_number="SN12345",
    part_number="WIDGET-001",
    operation_type_code=operation.code,  # Reference operation
    station="FCT-01"
)

# Submit report
api.report.submit_uut_report(report)
```

### Validation Helper

```python
def validate_operation_code(code):
    """Validate that an operation code exists"""
    
    operation = api.process.get_operation(code)
    
    if operation:
        print(f"✓ Valid operation: {operation.name} ({operation.code})")
        return True
    else:
        print(f"✗ Invalid operation code: {code}")
        return False

# Use it
validate_operation_code("ICT")  # Valid
validate_operation_code("INVALID")  # Invalid
```

---

## Advanced Usage

### Operation Lookup Table

```python
def build_operation_lookup():
    """Build quick lookup table for operations"""
    
    # Get all operations
    all_ops = api.process.get_all_operations()
    
    # Build lookup by code
    by_code = {op.code: op for op in all_ops}
    
    # Build lookup by name (lowercase for case-insensitive)
    by_name = {op.name.lower(): op for op in all_ops}
    
    return by_code, by_name

# Use it
code_lookup, name_lookup = build_operation_lookup()

# Fast lookups
ict = code_lookup.get("ICT")
fct = name_lookup.get("functional test")

print(f"ICT: {ict.name if ict else 'Not found'}")
print(f"FCT: {fct.name if fct else 'Not found'}")
```

### Process Type Report

```python
def process_type_report():
    """Generate report of operations by type"""
    
    all_ops = api.process.get_all_operations()
    
    # Group by type
    by_type = {}
    for op in all_ops:
        op_type = op.process_type
        if op_type not in by_type:
            by_type[op_type] = []
        by_type[op_type].append(op)
    
    print("=" * 70)
    print("PROCESS TYPE REPORT")
    print("=" * 70)
    
    for op_type in sorted(by_type.keys()):
        ops = by_type[op_type]
        print(f"\n{op_type} ({len(ops)} operations):")
        
        for op in sorted(ops, key=lambda x: x.code):
            print(f"  {op.code:<10} {op.name}")
    
    print("\n" + "=" * 70)
    print(f"Total: {len(all_ops)} operations")
    print("=" * 70)

# Use it
process_type_report()
```

### Find Operations by Prefix

```python
def find_operations_by_prefix(prefix):
    """Find operations with codes starting with prefix"""
    
    all_ops = api.process.get_all_operations()
    
    matching = [
        op for op in all_ops 
        if op.code.startswith(prefix.upper())
    ]
    
    print(f"=== OPERATIONS STARTING WITH '{prefix}' ({len(matching)}) ===")
    
    for op in matching:
        print(f"{op.code}: {op.name}")
        print(f"  Type: {op.process_type}")

# Use it
find_operations_by_prefix("T")  # All test operations
find_operations_by_prefix("R")  # All repair operations
```

### Operation Usage Tracking

```python
def track_operation_usage(operation_code, days=7):
    """Track how often an operation is used in reports"""
    from datetime import datetime, timedelta
    
    # Verify operation exists
    operation = api.process.get_operation(operation_code)
    
    if not operation:
        print(f"Operation '{operation_code}' not found")
        return
    
    # Query reports with this operation using OData
    headers = api.report.query_uut_headers(
        odata_filter=f"processCode eq {operation_code}",
        top=1000
    )
    
    print(f"=== USAGE: {operation.name} ({operation.code}) ===")
    print(f"Period: Last {days} days")
    print(f"Reports: {len(headers)}")
    
    # Breakdown by station
    by_station = {}
    for header in headers:
        station = header.station_name
        by_station[station] = by_station.get(station, 0) + 1
    
    print("\nBy Station:")
    for station, count in sorted(by_station.items()):
        print(f"  {station}: {count}")

# Use it
track_operation_usage("ICT", days=30)
```

### Cached Access Pattern

```python
class ProcessCache:
    """Wrapper for cached process access with fallback"""
    
    def __init__(self, api):
        self.api = api
        self._cache = {}
    
    def get_operation(self, code_or_name):
        """Get operation with local cache layer"""
        
        # Check local cache first
        if code_or_name in self._cache:
            return self._cache[code_or_name]
        
        # Get from API (uses API's cache)
        operation = self.api.process.get_operation(code_or_name)
        
        # Store in local cache
        if operation:
            self._cache[code_or_name] = operation
            self._cache[operation.code] = operation
            self._cache[operation.name] = operation
        
        return operation
    
    def clear_cache(self):
        """Clear local cache"""
        self._cache.clear()

# Use it
cache = ProcessCache(api)

# First access - loads from API
op1 = cache.get_operation("ICT")

# Second access - uses local cache
op2 = cache.get_operation("ICT")

# Clear when needed
cache.clear_cache()
```

---

## Practical Examples

### Operation Type Filtering with Validation

```python
from typing import List, Optional, Dict, Any
from pywats.exceptions import PyWATSError

def get_valid_operation_code(
    api, 
    operation_type: str,
    code_or_name: str
) -> Optional[int]:
    """
    Get a validated operation code for the specified type.
    
    Useful for report submission where you need to ensure
    the operation code matches the expected type.
    
    Args:
        api: pyWATS API instance
        operation_type: "test", "repair", or "wip"
        code_or_name: Operation code (int) or name (str)
        
    Returns:
        Valid operation code or None if invalid
        
    Example:
        >>> code = get_valid_operation_code(api, "test", "ICT")
        >>> if code:
        ...     report.process_code = code
    """
    type_methods = {
        "test": api.process.get_test_operation,
        "repair": api.process.get_repair_operation,
        "wip": api.process.get_wip_operation
    }
    
    get_method = type_methods.get(operation_type.lower())
    if not get_method:
        raise ValueError(f"Invalid operation_type: {operation_type}. Use 'test', 'repair', or 'wip'")
    
    # Handle int or str input
    identifier = int(code_or_name) if str(code_or_name).isdigit() else code_or_name
    
    operation = get_method(identifier)
    return operation.code if operation else None

def list_operations_by_type(api) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group all operations by their type for easy reference.
    
    Returns dict like:
    {
        "test": [{"code": 100, "name": "ICT"}, ...],
        "repair": [{"code": 500, "name": "Rework"}, ...],
        "wip": [{"code": 200, "name": "Assembly"}, ...]
    }
    """
    return {
        "test": [
            {"code": op.code, "name": op.name} 
            for op in api.process.get_test_operations()
        ],
        "repair": [
            {"code": op.code, "name": op.name} 
            for op in api.process.get_repair_operations()
        ],
        "wip": [
            {"code": op.code, "name": op.name} 
            for op in api.process.get_wip_operations()
        ]
    }

# Usage
ops_by_type = list_operations_by_type(api)
print("Available Test Operations:")
for op in ops_by_type["test"]:
    print(f"  {op['code']}: {op['name']}")

# Validate before report submission
code = get_valid_operation_code(api, "test", "ICT")
if code:
    print(f"Using operation code {code} for test report")
else:
    print("Warning: ICT operation not found, using default")
    code = api.process.get_default_test_code()
```

### Smart Process Cache with Prefetch

```python
from datetime import datetime, timedelta
from typing import Dict, Optional, Set
import threading

class SmartProcessCache:
    """
    Enhanced process cache with prefetch and usage tracking.
    
    Features:
    - Prefetches commonly used operations on init
    - Tracks usage for analytics
    - Thread-safe with automatic refresh
    - Configurable stale threshold
    """
    
    def __init__(self, api, stale_minutes: int = 5):
        self.api = api
        self.stale_threshold = timedelta(minutes=stale_minutes)
        self._cache: Dict[str, tuple] = {}  # key -> (operation, timestamp)
        self._usage_count: Dict[str, int] = {}
        self._lock = threading.Lock()
        self._prefetch_common()
    
    def _prefetch_common(self) -> None:
        """Prefetch common operation types"""
        common_codes = [100, 500]  # Default test and repair
        common_names = ["ICT", "FCT", "Rework", "Assembly"]
        
        for code in common_codes:
            self._fetch_and_cache(code)
        for name in common_names:
            self._fetch_and_cache(name)
    
    def _fetch_and_cache(self, identifier) -> Optional[object]:
        """Fetch operation and update cache"""
        op = self.api.process.get_process(identifier)
        if op:
            now = datetime.now()
            with self._lock:
                # Cache by code and name
                self._cache[str(op.code)] = (op, now)
                self._cache[op.name.lower()] = (op, now)
        return op
    
    def _is_stale(self, timestamp: datetime) -> bool:
        """Check if cached entry is stale"""
        return datetime.now() - timestamp > self.stale_threshold
    
    def get(self, code_or_name) -> Optional[object]:
        """
        Get operation with smart caching.
        
        Args:
            code_or_name: Operation code (int) or name (str)
            
        Returns:
            ProcessInfo or None
        """
        key = str(code_or_name).lower() if isinstance(code_or_name, str) else str(code_or_name)
        
        with self._lock:
            if key in self._cache:
                op, timestamp = self._cache[key]
                
                # Track usage
                self._usage_count[key] = self._usage_count.get(key, 0) + 1
                
                # Return if fresh
                if not self._is_stale(timestamp):
                    return op
        
        # Refresh stale or missing entry
        return self._fetch_and_cache(code_or_name)
    
    def get_usage_stats(self) -> Dict[str, int]:
        """Get operation usage statistics"""
        with self._lock:
            return dict(sorted(
                self._usage_count.items(), 
                key=lambda x: x[1], 
                reverse=True
            ))
    
    def refresh_all(self) -> None:
        """Force refresh of all cached operations"""
        self.api.process.refresh()
        with self._lock:
            keys = list(self._cache.keys())
        for key in keys:
            self._fetch_and_cache(key)

# Usage
cache = SmartProcessCache(api, stale_minutes=10)

# Fast cached access
op = cache.get("ICT")  # Uses cache if fresh
op = cache.get(100)    # Also cached

# Check what's being used most
print("Operation usage stats:")
for code, count in cache.get_usage_stats().items():
    print(f"  {code}: {count} lookups")
```

### Test Workflow with Operation Validation

```python
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class WorkflowStage(Enum):
    """Standard test workflow stages"""
    ICT = "ICT"          # In-Circuit Test
    FCT = "FCT"          # Functional Test
    BURN_IN = "BURN_IN"  # Burn-in / Stress Test
    FVT = "FVT"          # Final Verification Test
    REPAIR = "REPAIR"    # Repair/Rework
    PACK = "PACK"        # Packaging

@dataclass
class WorkflowConfig:
    """Configuration for a test workflow"""
    stages: list  # List of WorkflowStage
    operation_codes: dict  # Stage -> operation code mapping
    
def build_workflow(api, stages: list) -> WorkflowConfig:
    """
    Build a validated workflow configuration.
    
    Ensures all specified stages have valid operation codes
    configured in the WATS system.
    
    Args:
        api: pyWATS API instance
        stages: List of WorkflowStage values
        
    Returns:
        WorkflowConfig with validated operation codes
        
    Raises:
        ValueError: If any stage doesn't have a matching operation
    """
    operation_codes = {}
    missing = []
    
    for stage in stages:
        # Try to find matching operation
        if stage == WorkflowStage.REPAIR:
            op = api.process.get_repair_operation(stage.value)
        else:
            op = api.process.get_test_operation(stage.value)
        
        if op:
            operation_codes[stage] = op.code
        else:
            # Try by code for common defaults
            if stage == WorkflowStage.ICT:
                operation_codes[stage] = 100  # Common ICT code
            elif stage == WorkflowStage.REPAIR:
                operation_codes[stage] = 500  # Common repair code
            else:
                missing.append(stage.value)
    
    if missing:
        available = [p.name for p in api.process.get_processes()]
        raise ValueError(
            f"Missing operations for stages: {missing}. "
            f"Available: {available}"
        )
    
    return WorkflowConfig(stages=stages, operation_codes=operation_codes)

def run_workflow_stage(
    api,
    workflow: WorkflowConfig,
    stage: WorkflowStage,
    serial_number: str
) -> dict:
    """
    Execute a workflow stage and return result.
    
    Args:
        api: pyWATS API instance
        workflow: Validated WorkflowConfig
        stage: Stage to execute
        serial_number: Unit under test serial number
        
    Returns:
        Dict with stage execution details
    """
    if stage not in workflow.stages:
        raise ValueError(f"Stage {stage} not in workflow")
    
    operation_code = workflow.operation_codes[stage]
    operation = api.process.get_process_by_code(operation_code)
    
    return {
        "stage": stage.value,
        "operation_code": operation_code,
        "operation_name": operation.name if operation else "Unknown",
        "serial_number": serial_number,
        "ready": True
    }

# Usage: Define and validate a workflow
workflow = build_workflow(api, [
    WorkflowStage.ICT,
    WorkflowStage.FCT,
    WorkflowStage.FVT
])

print("Workflow Configuration:")
for stage, code in workflow.operation_codes.items():
    op = api.process.get_process_by_code(code)
    print(f"  {stage.value}: Code {code} ({op.name if op else 'N/A'})")

# Execute stage
result = run_workflow_stage(api, workflow, WorkflowStage.ICT, "UNIT-001")
print(f"\nReady to run {result['operation_name']} on {result['serial_number']}")
```

---

## API Reference

### ProcessService Methods

#### Operation Queries
- `get_operation(code_or_name)` → `Optional[ProcessInfo]` - Get operation by code or name
- `get_test_operation(code_or_name)` → `Optional[ProcessInfo]` - Get test operation
- `get_repair_operation(code_or_name)` → `Optional[ProcessInfo]` - Get repair operation
- `get_all_operations()` → `List[ProcessInfo]` - Get all operations (from cache)

#### Cache Management
- `refresh()` → `None` - Force cache refresh
- `refresh_interval` → `int` - Get/set refresh interval in seconds
- `last_refresh` → `datetime` - Get last refresh timestamp

### Models

#### ProcessInfo
- `id`: int - Process ID
- `name`: str - Operation name
- `code`: str - Short code
- `process_type`: str - Type (TEST, REPAIR, etc.)
- `description`: str - Operation description

### Cache Behavior

- **Default Refresh**: 300 seconds (5 minutes)
- **Auto-Refresh**: When cache age exceeds refresh_interval
- **Thread-Safe**: Uses threading.Lock for concurrent access
- **Read-Only**: Process definitions are read-only via API

---

## Best Practices

1. **Use the cache** - Don't bypass caching for frequent lookups
2. **Set appropriate interval** - Balance freshness vs performance
3. **Lookup by code** - Codes are more stable than names
4. **Validate codes** - Check operation exists before using
5. **Refresh on startup** - Ensure cache is fresh when application starts
6. **Monitor cache age** - Track when last refresh occurred
7. **Use in reports** - Reference operation codes in test reports
8. **Handle missing operations** - Gracefully handle unknown codes

---

## See Also

- [Report Domain](report.md) - Use operation codes in test reports
- [Production Domain](production.md) - Track operations performed on units
- [Analytics Domain](analytics.md) - Analyze data by operation type
