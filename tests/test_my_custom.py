"""
Custom test file - write your test logic here.
"""
import pytest
from pyWATS import WATSApi
from pyWATS.models.report import UUTReport


class TestCustom:
    """Custom test cases."""
    
    def test_my_custom_test(self, http_client):
        """
        Custom test - write your test logic here.
        """
        # Initialize the API yourself
        api = WATSApi(base_url="https://ola.wats.com", token="test_token")
        
        # OR use the http_client from fixture:
        # from pyWATS.rest_api._http_client import WatsHttpClient
        # api = WATSApi(base_url=http_client._base_url, token="")
        
        # Now try: api. (with dot)
        
        # Create a simple UUT:
        uut = api.report.create_uut_report(
            operator="Test Operator",
            part_number="TEST-1234",
            revision="A",
            serial_number="SN0001",
            operation_type="Final Test",
            sequence_file="test_sequence.seq",
            version="1.0.0"
        )
        
        root = uut.get_root_sequence_call()

        root.add_numeric_step(name="MyNumericStep", value=42.0, unit="units")
        api.report.submit_report(report=uut)
        
        pass
