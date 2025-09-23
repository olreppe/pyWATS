"""
REST API Tests

Unit tests for the pyWATS REST API client and endpoints.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import httpx

from pyWATS.rest_api import (
    WATSClient, get_default_client, models, endpoints,
    WATSAPIException, AuthenticationError, NotFoundError
)


class TestWATSClient:
    """Test cases for WATSClient."""
    
    def test_client_initialization(self):
        """Test client initialization with various parameters."""
        client = WATSClient(
            base_url="https://test.wats.com",
            auth_token="test_token",
            referrer="https://test.wats.com/dashboard"
        )
        
        assert client.base_url == "https://test.wats.com"
        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == "Basic test_token"
        assert client.headers["Referer"] == "https://test.wats.com/dashboard"
    
    def test_set_auth_token(self):
        """Test setting authentication token."""
        client = WATSClient("https://test.wats.com")
        client.set_auth_token("new_token")
        
        assert client.headers["Authorization"] == "Basic new_token"
    
    def test_context_manager(self):
        """Test client as context manager."""
        with WATSClient("https://test.wats.com") as client:
            assert client.base_url == "https://test.wats.com"


class TestModels:
    """Test cases for data models."""
    
    def test_public_wats_filter(self):
        """Test PublicWatsFilter model."""
        filter_data = models.PublicWatsFilter(
            part_number="PCB123",
            serial_number="SN001",
            date_from=datetime(2023, 1, 1),
            top_count=100
        )
        
        assert filter_data.part_number == "PCB123"
        assert filter_data.serial_number == "SN001"
        assert filter_data.top_count == 100
        
        # Test serialization with aliases
        data = filter_data.dict(by_alias=True, exclude_none=True)
        assert "partNumber" in data
        assert "serialNumber" in data
        assert "topCount" in data
    
    def test_asset_model(self):
        """Test Asset model."""
        asset = models.Asset(
            serial_number="FIXTURE001",
            type_id="12345678-1234-1234-1234-123456789abc",
            asset_name="Test Fixture",
            state=models.AssetState.IN_OPERATION
        )
        
        assert asset.serial_number == "FIXTURE001"
        assert asset.asset_name == "Test Fixture"
        assert asset.state == models.AssetState.IN_OPERATION
    
    def test_product_model(self):
        """Test Product model."""
        product = models.Product(
            part_number="PCB123",
            name="Main PCB",
            state=1
        )
        
        assert product.part_number == "PCB123"
        assert product.name == "Main PCB"
        assert product.state == 1


class TestEndpoints:
    """Test cases for API endpoints."""
    
    @patch('httpx.Client.get')
    def test_get_version(self, mock_get):
        """Test getting API version."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = "v1.0.0"
        mock_get.return_value = mock_response
        
        client = WATSClient("https://test.wats.com")
        version = endpoints.app.get_version(client=client)
        
        assert version == "v1.0.0"
        mock_get.assert_called_once_with("/api/App/Version")
    
    @patch('httpx.Client.get')
    def test_get_levels(self, mock_get):
        """Test getting levels."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"levels": ["Level1", "Level2"]}
        mock_get.return_value = mock_response
        
        client = WATSClient("https://test.wats.com")
        levels = endpoints.app.get_levels(client=client)
        
        assert "levels" in levels
        mock_get.assert_called_once_with("/api/App/Levels")
    
    @patch('httpx.Client.post')
    def test_dynamic_yield(self, mock_post):
        """Test dynamic yield endpoint."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"yield_data": "test"}
        mock_post.return_value = mock_response
        
        client = WATSClient("https://test.wats.com")
        filter_data = models.PublicWatsFilter(part_number="PCB123")
        
        result = endpoints.app.get_dynamic_yield(
            filter_data=filter_data,
            dimensions="partNumber;fpy desc",
            client=client
        )
        
        assert result["yield_data"] == "test"
        mock_post.assert_called_once()
    
    @patch('httpx.Client.get')
    def test_get_assets(self, mock_get):
        """Test getting assets with OData filtering."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"assetId": "1", "serialNumber": "FIXTURE001"}]
        mock_get.return_value = mock_response
        
        client = WATSClient("https://test.wats.com")
        assets = endpoints.asset.get_assets(
            odata_filter="state eq 1",
            odata_top=10,
            client=client
        )
        
        assert len(assets) == 1
        assert assets[0]["serialNumber"] == "FIXTURE001"
        mock_get.assert_called_once_with(
            "/api/Asset", 
            params={"$filter": "state eq 1", "$top": 10}
        )
    
    @patch('httpx.Client.put')
    def test_create_asset(self, mock_put):
        """Test creating an asset."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"assetId": "123", "serialNumber": "FIXTURE001"}
        mock_put.return_value = mock_response
        
        client = WATSClient("https://test.wats.com")
        asset = models.Asset(
            serial_number="FIXTURE001",
            type_id="12345678-1234-1234-1234-123456789abc"
        )
        
        result = endpoints.asset.create_asset(asset, client=client)
        
        assert result["assetId"] == "123"
        mock_put.assert_called_once()
    
    @patch('httpx.Client.get')
    def test_query_report_headers(self, mock_get):
        """Test querying report headers."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "uuid": "12345678-1234-1234-1234-123456789abc",
                "serialNumber": "SN001",
                "partNumber": "PCB123"
            }
        ]
        mock_get.return_value = mock_response
        
        client = WATSClient("https://test.wats.com")
        reports = endpoints.report.query_report_headers(
            odata_filter="partNumber eq 'PCB123'",
            odata_top=10,
            client=client
        )
        
        assert len(reports) == 1
        assert reports[0].serial_number == "SN001"
        mock_get.assert_called_once_with(
            "/api/Report/Query/Header",
            params={"$filter": "partNumber eq 'PCB123'", "$top": 10}
        )


class TestErrorHandling:
    """Test cases for error handling."""
    
    @patch('httpx.Client.get')
    def test_authentication_error(self, mock_get):
        """Test authentication error handling."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response
        
        client = WATSClient("https://test.wats.com")
        
        with pytest.raises(AuthenticationError):
            endpoints.app.get_version(client=client)
    
    @patch('httpx.Client.get')
    def test_not_found_error(self, mock_get):
        """Test not found error handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        
        client = WATSClient("https://test.wats.com")
        
        with pytest.raises(NotFoundError):
            endpoints.asset.get_asset_by_serial_number("NONEXISTENT", client=client)
    
    @patch('httpx.Client.get')
    def test_generic_api_error(self, mock_get):
        """Test generic API error handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response
        
        client = WATSClient("https://test.wats.com")
        
        with pytest.raises(WATSAPIException) as exc_info:
            endpoints.app.get_version(client=client)
        
        assert exc_info.value.status_code == 500


class TestIntegration:
    """Integration test cases (require actual WATS server)."""
    
    @pytest.mark.integration
    def test_real_api_connection(self):
        """Test actual API connection (requires environment setup)."""
        # This test requires actual WATS server and credentials
        # Skip if not configured
        import os
        
        if not os.getenv("WATS_BASE_URL") or not os.getenv("WATS_AUTH_TOKEN"):
            pytest.skip("WATS server not configured for integration tests")
        
        client = get_default_client()
        version = endpoints.app.get_version(client=client)
        assert version is not None
    
    @pytest.mark.integration
    def test_end_to_end_workflow(self):
        """Test end-to-end workflow with real API."""
        import os
        
        if not os.getenv("WATS_BASE_URL") or not os.getenv("WATS_AUTH_TOKEN"):
            pytest.skip("WATS server not configured for integration tests")
        
        client = get_default_client()
        
        # Get product groups
        product_groups = endpoints.app.get_product_groups(client=client)
        assert isinstance(product_groups, dict)
        
        # Get levels
        levels = endpoints.app.get_levels(client=client)
        assert isinstance(levels, dict)
        
        # Query some reports
        reports = endpoints.report.query_report_headers(
            odata_top=5,
            client=client
        )
        assert isinstance(reports, list)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])