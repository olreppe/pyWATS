"""
Test Utilities

Common utilities and helpers for pyWATS testing.
"""

import sys
import os
from typing import Optional, Tuple
from datetime import datetime
import time

# Add src to path for importing pyWATS
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pyWATS.tdm_client import TDMClient, APIStatusType
from .test_config import (
    TEST_BASE_URL, TEST_AUTH_TOKEN, TEST_STATION_NAME, 
    TEST_DATA_DIR, TEST_LOCATION, TEST_PURPOSE,
    REPORT_PROCESSING_WAIT, MAX_LOAD_RETRIES, RETRY_DELAY
)


class TestResult:
    """Test result container with status and details."""
    
    def __init__(self, success: bool, message: str, details: Optional[dict] = None):
        self.success = success
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()
    
    def __str__(self):
        status = "✅ PASS" if self.success else "❌ FAIL"
        return f"{status}: {self.message}"


def setup_test_client() -> Tuple[Optional[TDMClient], TestResult]:
    """
    Set up a TDM client for testing.
    
    Returns:
        Tuple of (TDMClient instance, TestResult)
    """
    try:
        # Create TDM client
        client = TDMClient()
        
        # Configure API settings
        client.setup_api(
            data_dir=TEST_DATA_DIR,
            location=TEST_LOCATION,
            purpose=TEST_PURPOSE,
            persist=False
        )
        client.station_name = TEST_STATION_NAME
        
        # Register with server
        client.register_client(base_url=TEST_BASE_URL, token=TEST_AUTH_TOKEN)
        client.initialize_api(try_connect_to_server=True, download_metadata=True)
        
        if client.status != APIStatusType.Online:
            return client, TestResult(False, f"Client not online. Status: {client.status}")
            
        return client, TestResult(True, "Test client setup successful")
        
    except Exception as e:
        return None, TestResult(False, f"Failed to setup test client: {e}")


def wait_and_retry_load(client: TDMClient, report_id: str, max_retries: int = MAX_LOAD_RETRIES) -> Tuple[Optional[dict], TestResult]:
    """
    Load a report with retry logic.
    
    Args:
        client: TDM client instance
        report_id: Report ID to load
        max_retries: Maximum number of retry attempts
        
    Returns:
        Tuple of (report_data or None, TestResult)
    """
    # Initial wait for processing
    time.sleep(REPORT_PROCESSING_WAIT)
    
    for attempt in range(1, max_retries + 1):
        try:
            if not client._connection or not client._connection._client:
                return None, TestResult(False, "No connection available")
                
            url = f"/api/Report/Wsjf/{report_id}"
            response = client._connection._client.get(url)
            
            if response.status_code == 200:
                if response.text.strip():
                    try:
                        report_data = response.json()
                        return report_data, TestResult(
                            True, 
                            f"Successfully loaded report on attempt {attempt}",
                            {"attempt": attempt, "response_size": len(response.content)}
                        )
                    except Exception as json_error:
                        if attempt < max_retries:
                            time.sleep(RETRY_DELAY)
                            continue
                        return None, TestResult(False, f"JSON parse error: {json_error}")
                else:
                    if attempt < max_retries:
                        time.sleep(RETRY_DELAY)  
                        continue
                    return None, TestResult(False, "Empty response after all retries")
            else:
                if attempt < max_retries:
                    time.sleep(RETRY_DELAY)
                    continue
                return None, TestResult(False, f"HTTP {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            if attempt < max_retries:
                time.sleep(RETRY_DELAY)
                continue
            return None, TestResult(False, f"Request failed after {max_retries} attempts: {e}")
    
    return None, TestResult(False, f"Failed to load report after {max_retries} attempts")


def cleanup_test_client(client: Optional[TDMClient]) -> TestResult:
    """
    Clean up test client resources.
    
    Args:
        client: TDM client to cleanup
        
    Returns:
        TestResult indicating cleanup status
    """
    try:
        if client:
            # Perform cleanup
            client.unregister_client()
            
        return TestResult(True, "Test client cleanup successful")
        
    except Exception as e:
        return TestResult(False, f"Cleanup failed: {e}")


def print_test_header(test_name: str):
    """Print a formatted test header."""
    print(f"\n{'='*60}")
    print(f" {test_name}")
    print(f"{'='*60}")


def print_test_result(result: TestResult):
    """Print a formatted test result."""
    print(f"{result}")
    if result.details:
        for key, value in result.details.items():
            print(f"  {key}: {value}")