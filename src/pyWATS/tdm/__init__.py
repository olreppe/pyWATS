"""
pyWATS TDM (Test Data Management) Module

This module provides comprehensive TDM functionality for WATS including:
- Statistics and trend analysis
- Data aggregation and reporting
- Performance monitoring
- Test result analysis

The TDM module provides analytical capabilities for test data stored in WATS,
enabling statistical analysis, trend monitoring, and performance insights.

Example usage:
    from pyWATS.tdm import Statistics, Analytics, Reports, TDMClient
    from pyWATS.connection import create_connection
    
    # Option 1: Use individual TDM modules with connection
    connection = create_connection(
        base_url="https://your-wats-server.com",
        token="your_token"
    )
    
    statistics = Statistics(connection)
    analytics = Analytics(connection)
    reports = Reports(connection)
    
    # Use the modules
    last_result = statistics.get_last_result("PART001", "TEST_OP")
    trend_data = statistics.get_trend("PART001", "TEST_OP")
    measurements = analytics.get_aggregated_measurements("PG001", "L1", 30)
    
    # Option 2: Use the main TDM client (equivalent to C# TDM class)
    tdm = TDMClient()
    tdm.setup_api(data_dir="./wats_data", location="TestLab", purpose="Production")
    tdm.register_client("https://your-wats-server.com", "username", "password")
    tdm.initialize_api(try_connect_to_server=True)
    
    # Create and submit reports
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
"""

# Conditionally import Statistics to avoid circular imports during package init
try:
    from .statistics import Statistics as _Statistics
    Statistics = _Statistics  # Expose as pyWATS.tdm.Statistics
except ImportError:
    # Create a placeholder during circular import resolution
    class Statistics:
        def __init__(self, connection=None):
            self.connection = connection
from .analytics import Analytics
from .reports import Reports

# Import the main TDM client - place it in the parent package to avoid circular imports
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from ..tdm_client import TDMClient
except ImportError:
    # Handle potential import issues during development
    TDMClient = None

__all__ = [
    "Statistics",
    "Analytics", 
    "Reports",
    "TDMClient"
]