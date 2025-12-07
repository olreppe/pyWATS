# TDM Example Documentation

## Overview

The `tdm_example.py` file provides a comprehensive demonstration of the pyWATS TDMClient functionality, which is the Python equivalent of the C# TDM class. This example showcases the complete TDM workflow including finding, loading, creating, and submitting UUT and UUR reports.

## What This Example Demonstrates

### 1. **TDM Client Setup and Configuration**
- Creating a TDMClient instance
- Configuring API settings (data directory, location, purpose)
- Setting station properties and validation modes

### 2. **Connection Management** 
- Registering client with WATS server
- Initializing API with different modes
- Testing server connectivity with ping functionality

### 3. **Metadata Operations**
- Retrieving available operation types from server
- Getting repair types and their requirements
- Handling offline scenarios with mock data

### 4. **Finding Existing Reports**
- Demonstrating how to query for existing reports
- Checking pending local reports in queue
- Simulating report discovery workflows

### 5. **Loading Reports from Server**
- Loading complete report details by ID
- Accessing report steps, measurements, and results
- Handling server communication for report retrieval

### 6. **Creating New Reports**

#### UUT (Unit Under Test) Reports:
- Creating comprehensive UUT reports with:
  - Test steps and timing information
  - Measurements with limits and results
  - Overall test results and duration
  - Operator and part information

#### UUR (Unit Under Repair) Reports:
- Creating repair reports with:
  - Repair activities and parts used
  - Verification measurements
  - Technician information and timestamps
  - Association with original UUT reports

### 7. **Report Submission**
- **Online submission**: Direct transmission to server
- **Offline submission**: Local queuing for later transmission
- **Automatic submission**: Intelligent mode selection based on connectivity
- Error handling and retry mechanisms

### 8. **Pending Reports Management**
- Checking pending report counts
- Batch submission of queued reports
- Monitoring submission success/failure

### 9. **Additional Features**
- Access to TDM sub-modules (Statistics, Analytics, Reports)
- Configuration inspection and status monitoring
- Proper cleanup and disconnection procedures

## Usage

### Running the Example

```bash
# From the pyWATS root directory
python tdm_example.py
```

### Configuration

The example uses the following default configuration (modify as needed):

```python
BASE_URL = "https://ola.wats.com"
AUTH_TOKEN = "cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="
```

**Note**: Replace these with your actual WATS server credentials.

### Example Output

The demonstration provides detailed output showing:
- ✓ Successful operations
- ✗ Failed operations with error messages  
- ⚠ Warning conditions (offline mode, fallbacks)
- ℹ Informational messages and tips

## Key Features Showcased

### Online Mode
When server connection is available:
- Reports are submitted directly to server
- Metadata is downloaded from server
- Real-time status updates are available

### Offline Mode  
When server is unavailable:
- Reports are queued locally for later submission
- Mock metadata is used for demonstration
- Automatic retry when connection is restored

### Error Handling
- Comprehensive exception catching and reporting
- Graceful degradation in offline scenarios
- Detailed error messages and troubleshooting information

## Code Structure

The example is organized into logical sections:

1. **Setup Functions**: Client creation and configuration
2. **Connection Functions**: Registration and initialization  
3. **Metadata Functions**: Operation/repair type retrieval
4. **Report Functions**: Finding, loading, creating reports
5. **Submission Functions**: Various submission methods
6. **Management Functions**: Pending report handling
7. **Utility Functions**: Additional features and cleanup

## Integration with pyWATS Architecture

The TDMClient integrates seamlessly with the existing pyWATS components:

- **REST API Client**: Uses WATSConnection for server communication
- **TDM Modules**: Provides access to Statistics, Analytics, Reports modules
- **MES Integration**: Can work alongside MES modules for complete workflow

## Real-World Usage Patterns

This example demonstrates patterns suitable for:

### Test Station Integration
```python
# Production test station
tdm = TDMClient()
tdm.setup_api(data_dir="/wats/data", location="ProductionLine1", purpose="Final Test")
# ... create and submit test reports
```

### Repair Station Workflow  
```python
# Repair bench
tdm = TDMClient()
# Load failed UUT report, perform repairs, create UUR report
uur_report = tdm.create_uur_report(operator="TechA", repair_type=repair_type, uut_report=failed_uut)
```

### Batch Processing
```python
# Offline data processing
tdm = TDMClient()
tdm.initialize_api(try_connect_to_server=False)  # Offline mode
# Process multiple reports, submit when online
```

## Comparison with C# TDM Class

This Python implementation provides equivalent functionality to the C# TDM class:

| C# TDM Method | Python TDMClient Method | Purpose |
|---------------|------------------------|---------|
| `RegisterClient()` | `register_client()` | Server registration |
| `InitializeAPI()` | `initialize_api()` | API initialization |
| `CreateUUTReport()` | `create_uut_report()` | UUT report creation |
| `CreateUURReport()` | `create_uur_report()` | UUR report creation |
| `Submit()` | `submit_report()` | Report submission |
| `GetOperationTypes()` | `get_operation_types()` | Metadata retrieval |
| `SubmitPendingReports()` | `submit_pending_reports()` | Queue management |

## Files Created

- **`tdm_example.py`**: Main comprehensive demonstration
- **`TDM_EXAMPLE_README.md`**: This documentation file
- **Previous files**:
  - `src/pyWATS/tdm_client.py`: TDMClient implementation
  - `examples/tdm_client_example.py`: Basic usage examples
  - `TDM_CLIENT_IMPLEMENTATION.md`: Implementation details

## Next Steps

After running this example, explore:

1. **Integration**: Incorporate TDMClient into your test systems
2. **Customization**: Modify report structures for your specific needs  
3. **Automation**: Build automated test sequences using the TDM workflow
4. **Analysis**: Use the TDM sub-modules for data analysis and reporting

For more information, see the complete implementation documentation in `TDM_CLIENT_IMPLEMENTATION.md`.