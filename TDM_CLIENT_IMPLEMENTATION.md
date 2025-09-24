# TDM Client Implementation Summary

## Overview

This implementation adds the missing TDM root class (`TDMClient`) that serves as the Python equivalent to the C# `TDM` class from the Interface.TDM project. The `TDMClient` provides a comprehensive API for Test Data Management operations in WATS.

## Key Features Implemented

### 1. Connection Management
- **Registration**: `register_client()` - Register with WATS server using base URL and token
- **Initialization**: `initialize_api()` - Initialize API with various modes (sync/async/offline)
- **Connection Testing**: `ping()` - Test server connectivity
- **Cleanup**: `unregister_client()` - Disconnect and clear configuration

### 2. Configuration Management
- **API Setup**: `setup_api()` - Configure data directory, location, and purpose
- **Properties**: Station name, validation mode, test mode, exception handling
- **Data Directory**: Automatic creation and management of local storage

### 3. Report Creation and Management
- **UUT Reports**: `create_uut_report()` - Create Unit Under Test reports
- **UUR Reports**: `create_uur_report()` - Create Unit Under Repair (repair) reports  
- **Report Submission**: `submit_report()` with multiple modes (Online/Offline/Automatic)
- **Offline Queue**: `get_pending_report_count()` and `submit_pending_reports()`

### 4. Metadata Management
- **Operation Types**: `get_operation_types()`, `get_operation_type_by_code()`, `get_operation_type_by_id()`
- **Repair Types**: `get_repair_types()`
- **Caching**: Local caching of metadata with automatic fallback
- **Download**: `_download_metadata()` from server

### 5. Status and State Management
- **API Status**: Online, Offline, Error, NotRegistered, etc.
- **Client State**: Active, NotConfigured, Unknown, etc.
- **Validation**: Exception throwing vs logging modes
- **Test Mode**: Active vs Import modes

### 6. Sub-Module Integration
- **Statistics**: Access to statistics module via `tdm.statistics`
- **Analytics**: Access to analytics module via `tdm.analytics`  
- **Reports**: Access to reports module via `tdm.reports`

## Usage Examples

### Basic Usage
```python
from pyWATS import TDMClient

# Create and configure TDM client
tdm = TDMClient()
tdm.setup_api(data_dir="./wats_data", location="TestLab", purpose="Production")
tdm.register_client("https://your-wats-server.com", "your_token")
tdm.initialize_api(try_connect_to_server=True)

# Create and submit UUT report
uut_report = tdm.create_uut_report(
    operator_name="TestOperator",
    part_number="PART001", 
    revision="Rev1",
    serial_number="SN12345",
    operation_type="TEST_OP",
    sequence_file_name="test_sequence.py",
    sequence_file_version="1.0"
)

success = tdm.submit_report(uut_report)
```

### Context Manager Usage
```python
with TDMClient() as tdm:
    tdm.setup_api(data_dir="./temp_wats")
    # Use tdm client...
# Automatic cleanup on exit
```

### Offline Mode
```python
tdm = TDMClient()
tdm.initialize_api(try_connect_to_server=False)  # Offline mode

# Reports are queued locally
report = tdm.create_uut_report(...)
tdm.submit_report(report, SubmitMethod.Offline)

# Later when online
tdm.initialize_api(try_connect_to_server=True)
submitted_count = tdm.submit_pending_reports()
```

## Architecture Notes

### Naming Conflict Resolution
The class is named `TDMClient` instead of `TDM` to avoid conflicts with the existing `tdm` directory containing the Statistics, Analytics, and Reports modules.

### Connection Integration  
The implementation integrates with the existing `WATSConnection` class and REST API client, providing a higher-level interface while maintaining compatibility with the current pyWATS architecture.

### Error Handling
Comprehensive error handling with configurable exception throwing vs logging, matching the C# implementation's `ValidationModeType` and `RethrowException` patterns.

### Metadata Caching
Local JSON-based caching of operation types and processes, with automatic fallback to cached data when server is unavailable.

## Files Created/Modified

1. **`src/pyWATS/tdm_client.py`** - Main TDMClient implementation (new)
2. **`src/pyWATS/__init__.py`** - Added TDMClient import  
3. **`src/pyWATS/tdm/__init__.py`** - Added TDMClient to TDM module
4. **`examples/tdm_client_example.py`** - Usage examples (new)

## Compatibility

The `TDMClient` is designed to be compatible with the existing pyWATS architecture while providing the comprehensive TDM functionality equivalent to the C# `TDM` class. It can be used alongside or instead of the individual TDM modules (Statistics, Analytics, Reports) depending on the use case.

## Future Enhancements

- Add asynchronous initialization mode
- Implement WRML (WATS Report Markup Language) support
- Add yield monitoring and statistics integration
- Implement converter support for file-based imports
- Add client update/upgrade functionality