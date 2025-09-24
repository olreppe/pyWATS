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
    from pyWATS.tdm import Statistics, Analytics, Reports
    from pyWATS.connection import create_connection
    
    # Create connection
    connection = create_connection(
        base_url="https://your-wats-server.com",
        token="your_token"
    )
    
    # Initialize TDM modules
    statistics = Statistics(connection)
    analytics = Analytics(connection)
    reports = Reports(connection)
    
    # Use the modules
    last_result = statistics.get_last_result("PART001", "TEST_OP")
    trend_data = statistics.get_trend("PART001", "TEST_OP")
    measurements = analytics.get_aggregated_measurements("PG001", "L1", 30)
"""

from .statistics import Statistics
from .analytics import Analytics
from .reports import Reports

__all__ = [
    "Statistics",
    "Analytics",
    "Reports"
]