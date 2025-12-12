"""
Shared fixtures and utilities for acceptance tests
"""
import pytest
from typing import Generator
from pywats import pyWATS


@pytest.fixture(scope="module")
def wats_client() -> Generator[pyWATS, None, None]:
    """
    Provides a pyWATS client instance for acceptance tests.
    Uses module scope to reuse the connection across tests in the same module.
    """
    client = pyWATS()
    yield client
    # Cleanup if needed


@pytest.fixture(scope="function")
def unique_identifier() -> str:
    """
    Generates a unique identifier for test data to avoid conflicts.
    """
    import time
    return f"acceptance_test_{int(time.time() * 1000)}"


@pytest.fixture
def test_product_data(unique_identifier: str) -> dict:
    """
    Provides test product data for acceptance scenarios.
    """
    return {
        "part_number": f"ACPT-PROD-{unique_identifier}",
        "part_description": f"Acceptance Test Product {unique_identifier}",
        "part_revision": "A"
    }


@pytest.fixture
def test_asset_data(unique_identifier: str) -> dict:
    """
    Provides test asset data for acceptance scenarios.
    """
    return {
        "name": f"ACPT-ASSET-{unique_identifier}",
        "asset_type": "Station"
    }


class AcceptanceTestHelper:
    """
    Helper class for common acceptance test operations
    """
    
    @staticmethod
    def verify_report_created(client: pyWATS, serial_number: str, timeout: int = 30) -> dict:
        """
        Verify that a report was created by loading it from the server.
        
        Args:
            client: pyWATS client instance
            serial_number: Serial number to search for
            timeout: Maximum time to wait for report (seconds)
            
        Returns:
            The loaded report data
            
        Raises:
            AssertionError: If report cannot be found or loaded
        """
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Try to get the report
                reports = client.report.get_uut_reports(
                    serial_number=serial_number,
                    limit=1
                )
                
                if reports and len(reports) > 0:
                    report = reports[0]
                    # Load full report details
                    full_report = client.report.get_uut_report(report.uuid)
                    return full_report
                    
            except Exception as e:
                # Report might not be available yet
                pass
                
            time.sleep(1)
        
        raise AssertionError(
            f"Report for serial number {serial_number} not found within {timeout} seconds"
        )
    
    @staticmethod
    def verify_unit_created(client: pyWATS, serial_number: str) -> dict:
        """
        Verify that a unit was created by loading it from the server.
        
        Args:
            client: pyWATS client instance
            serial_number: Serial number to verify
            
        Returns:
            The loaded unit data
            
        Raises:
            AssertionError: If unit cannot be found
        """
        unit = client.production.get_unit(serial_number)
        assert unit is not None, f"Unit {serial_number} not found"
        return unit
    
    @staticmethod
    def verify_product_exists(client: pyWATS, part_number: str, part_revision: str = None) -> dict:
        """
        Verify that a product exists by loading it from the server.
        
        Args:
            client: pyWATS client instance
            part_number: Part number to verify
            part_revision: Optional part revision
            
        Returns:
            The loaded product data
            
        Raises:
            AssertionError: If product cannot be found
        """
        products = client.product.get_product(part_number=part_number)
        assert products is not None and len(products) > 0, \
            f"Product {part_number} not found"
        
        if part_revision:
            revisions = client.product.get_revisions(part_number=part_number)
            matching_revision = next(
                (r for r in revisions if r.part_revision == part_revision),
                None
            )
            assert matching_revision is not None, \
                f"Revision {part_revision} not found for product {part_number}"
            return matching_revision
        
        return products[0]


@pytest.fixture
def acceptance_helper() -> AcceptanceTestHelper:
    """
    Provides helper utilities for acceptance tests.
    """
    return AcceptanceTestHelper()
