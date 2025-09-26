"""
Test Configuration

Centralized configuration for all pyWATS tests.
"""

# Test server configuration
TEST_BASE_URL = "https://ola.wats.com"
TEST_AUTH_TOKEN = "cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="

# Test data configuration
TEST_STATION_NAME = "pyWATS_Test_Station"
TEST_DATA_DIR = "./test_wats_data"
TEST_LOCATION = "Automated Test Lab"
TEST_PURPOSE = "Automated Testing"

# Known test report IDs on server
KNOWN_FAT_REPORT_ID = "14ca0682-35b9-415d-8c61-de8367c5a9df"

# Test operation configuration  
DEFAULT_TEST_OPERATION_CODE = 122  # ABI Test
DEFAULT_REPAIR_OPERATION_CODE = 500  # Repair

# Timeouts and retries
REPORT_PROCESSING_WAIT = 5  # seconds to wait after submission
MAX_LOAD_RETRIES = 3
RETRY_DELAY = 3  # seconds between retries