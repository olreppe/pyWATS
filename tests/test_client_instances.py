"""
Tests demonstrating the test instance infrastructure.

These tests show how to use ClientA and ClientB fixtures for testing.
"""
import pytest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pywats import pyWATS
    from pywats_client.core.config import ClientConfig
    from pywats_client.app import pyWATSApplication


class TestClientInstances:
    """Test that client instances are properly configured."""

    def test_client_a_config_exists(self, client_config_a: "ClientConfig") -> None:
        """Test Client A configuration is loaded correctly."""
        assert client_config_a is not None
        assert client_config_a.instance_name == "Test Client A"
        assert client_config_a.station_name == "TEST-STATION-A"
        assert client_config_a.location == "Test Lab Alpha"
        # Service address is loaded from config file, verify it's not empty
        assert client_config_a.service_address, "Service address should be configured"

    def test_client_b_config_exists(self, client_config_b: "ClientConfig") -> None:
        """Test Client B configuration is loaded correctly."""
        assert client_config_b is not None
        assert client_config_b.instance_name == "Test Client B"
        assert client_config_b.station_name == "TEST-STATION-B"
        assert client_config_b.location == "Test Lab Beta"
        # Client B has converters disabled
        assert client_config_b.converters_enabled is False

    def test_client_configs_are_different(
        self, 
        client_config_a: "ClientConfig", 
        client_config_b: "ClientConfig"
    ) -> None:
        """Test that Client A and B have different configurations."""
        assert client_config_a.instance_id != client_config_b.instance_id
        assert client_config_a.instance_name != client_config_b.instance_name
        assert client_config_a.station_name != client_config_b.station_name


class TestAPIClients:
    """Test API clients from test instances."""

    @pytest.mark.client_a
    def test_wats_client_a_connection(self, wats_client: "pyWATS") -> None:
        """Test that Client A can connect to WATS server."""
        # Verify connection by getting version
        version = wats_client.app.get_version()
        assert version is not None

    @pytest.mark.client_b
    def test_wats_client_b_connection(self, wats_client_b: "pyWATS") -> None:
        """Test that Client B can connect to WATS server."""
        # Verify connection by getting version  
        version = wats_client_b.app.get_version()
        assert version is not None

    def test_both_clients_access_same_server(
        self, 
        wats_client: "pyWATS", 
        wats_client_b: "pyWATS"
    ) -> None:
        """Test both clients connect to the same server."""
        version_a = wats_client.app.get_version()
        version_b = wats_client_b.app.get_version()
        # Both should get the same version from the same server
        assert version_a == version_b


class TestClientApplications:
    """Test full client applications."""

    @pytest.mark.client_a
    def test_client_app_a_initializes(self, client_app_a: "pyWATSApplication") -> None:
        """Test Client A application initializes correctly."""
        from pywats_client.app import ApplicationStatus
        
        assert client_app_a is not None
        assert client_app_a.config is not None
        assert client_app_a.config.instance_name == "Test Client A"
        # Should start in stopped state
        assert client_app_a.status == ApplicationStatus.STOPPED

    @pytest.mark.client_b
    def test_client_app_b_initializes(self, client_app_b: "pyWATSApplication") -> None:
        """Test Client B application initializes correctly."""
        from pywats_client.app import ApplicationStatus
        
        assert client_app_b is not None
        assert client_app_b.config is not None
        assert client_app_b.config.instance_name == "Test Client B"
        assert client_app_b.status == ApplicationStatus.STOPPED

    def test_applications_are_independent(
        self, 
        client_app_a: "pyWATSApplication", 
        client_app_b: "pyWATSApplication"
    ) -> None:
        """Test that Client A and B applications are independent instances."""
        # Different config objects
        assert client_app_a.config is not client_app_b.config
        # Different instance IDs
        assert client_app_a.config.instance_id != client_app_b.config.instance_id


class TestInstanceManager:
    """Test the test instance manager itself."""

    def test_manager_lists_instances(self, test_instance_manager) -> None:
        """Test that instance manager lists all instances."""
        instances = test_instance_manager.list_instances()
        
        assert "A" in instances
        assert "B" in instances
        assert instances["A"].name == "Test Client A"
        assert instances["B"].name == "Test Client B"

    def test_manager_creates_data_directories(self, test_instance_manager) -> None:
        """Test that instance manager creates data directories."""
        data_dir_a = test_instance_manager.get_instance_data_dir("A")
        data_dir_b = test_instance_manager.get_instance_data_dir("B")
        
        assert data_dir_a.exists()
        assert data_dir_b.exists()
        assert data_dir_a != data_dir_b


class TestScenarios:
    """Example test scenarios using different clients."""

    @pytest.mark.integration
    def test_product_retrieval_client_a(self, wats_client: "pyWATS") -> None:
        """Retrieve products using Client A."""
        products = wats_client.product.get_products()
        assert isinstance(products, list)
        # Log for debugging
        if products:
            print(f"Client A retrieved {len(products)} products")

    @pytest.mark.integration
    def test_product_retrieval_client_b(self, wats_client_b: "pyWATS") -> None:
        """Retrieve products using Client B (same result, different config)."""
        products = wats_client_b.product.get_products()
        assert isinstance(products, list)
        if products:
            print(f"Client B retrieved {len(products)} products")

    @pytest.mark.integration  
    def test_simultaneous_operations(
        self, 
        wats_client: "pyWATS", 
        wats_client_b: "pyWATS"
    ) -> None:
        """Test both clients can operate simultaneously."""
        # Both clients fetch data at the same time
        products_a = wats_client.product.get_products()
        products_b = wats_client_b.product.get_products()
        
        # Should get same data (same server)
        assert len(products_a) == len(products_b)
