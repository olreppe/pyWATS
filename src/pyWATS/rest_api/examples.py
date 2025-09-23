"""
REST API Usage Examples

This module demonstrates how to use the pyWATS REST API client.
"""

import os
from datetime import datetime, timedelta
from pyWATS.rest_api import WATSClient, get_default_client, models, endpoints


def basic_client_usage():
    """Example of basic client setup and usage."""
    
    # Method 1: Use environment variables
    # Set WATS_BASE_URL, WATS_AUTH_TOKEN, WATS_REFERRER in environment
    client = get_default_client()
    
    # Method 2: Create client directly
    client = WATSClient(
        base_url="https://your-wats-server.com",
        auth_token="your_auth_token_here",
        referrer="https://your-wats-server.com/dashboard"
    )
    
    # Method 3: Use context manager
    with WATSClient(base_url="https://your-wats-server.com") as client:
        # Client will be automatically closed
        version = endpoints.app.get_version(client)
        print(f"WATS Version: {version}")


def authentication_example():
    """Example of authentication and token management."""
    
    # Get authentication token
    client = WATSClient(base_url="https://your-wats-server.com")
    
    # Get token (requires initial authentication)
    token_data = endpoints.auth.get_token(client=client)
    print(f"Token: {token_data}")
    
    # Set token for future requests
    client.set_auth_token(token_data["token"])
    
    # Get token with specific identifier
    token_with_id = endpoints.auth.get_token_with_identifier(
        identifier="my_app_token",
        client=client
    )


def app_endpoints_example():
    """Example of using App endpoints for analytics and measurements."""
    
    client = get_default_client()
    
    # Create a filter for the last 30 days
    filter_data = models.PublicWatsFilter(
        part_number="PCB123",
        test_operation="FinalTest",
        date_from=datetime.now() - timedelta(days=30),
        date_to=datetime.now(),
        top_count=100
    )
    
    # Get aggregated measurements
    measurements = endpoints.app.get_aggregated_measurements(
        filter_data=filter_data,
        measurement_paths="MainSequence¶Voltage Test¶¶Voltage1",
        client=client
    )
    print(f"Measurements: {measurements}")
    
    # Get dynamic yield analysis
    yield_data = endpoints.app.get_dynamic_yield(
        filter_data=filter_data,
        dimensions="partNumber;testOperation;fpy desc",
        client=client
    )
    print(f"Yield Data: {yield_data}")
    
    # Get product groups
    product_groups = endpoints.app.get_product_groups(client=client)
    print(f"Product Groups: {product_groups}")
    
    # Get levels
    levels = endpoints.app.get_levels(client=client)
    print(f"Levels: {levels}")


def asset_management_example():
    """Example of asset management operations."""
    
    client = get_default_client()
    
    # Get all assets with OData filtering
    assets = endpoints.asset.get_assets(
        odata_filter="state eq 1",  # In Operation
        odata_top=50,
        client=client
    )
    print(f"Assets in operation: {len(assets)}")
    
    # Create a new asset
    new_asset = models.Asset(
        serial_number="FIXTURE001",
        asset_name="Test Fixture 1",
        type_id="12345678-1234-1234-1234-123456789abc",  # Asset type ID
        description="Primary test fixture",
        location="Production Line 1"
    )
    
    created_asset = endpoints.asset.create_asset(new_asset, client=client)
    print(f"Created asset: {created_asset}")
    
    # Update asset count
    endpoints.asset.update_asset_count(
        serial_number="FIXTURE001",
        increment_by=1,
        client=client
    )
    
    # Post a message to asset log
    message = models.AssetMessage(content="Maintenance completed")
    endpoints.asset.post_asset_message(
        message=message,
        serial_number="FIXTURE001",
        client=client
    )
    
    # Get asset status
    status = endpoints.asset.get_asset_status(
        serial_number="FIXTURE001",
        client=client
    )
    print(f"Asset status: {status}")


def production_management_example():
    """Example of production management operations."""
    
    client = get_default_client()
    
    # Create units
    units = [
        models.Unit(
            serial_number="SN001",
            part_number="PCB123",
            revision="Rev1.0",
            batch_number="BATCH001"
        ),
        models.Unit(
            serial_number="SN002", 
            part_number="PCB123",
            revision="Rev1.0",
            batch_number="BATCH001"
        )
    ]
    
    result = endpoints.production.create_units(units, client=client)
    print(f"Units created: {result}")
    
    # Set unit phase
    endpoints.production.set_unit_phase(
        serial_number="SN001",
        part_number="PCB123",
        phase=16,  # Finalized
        client=client
    )
    
    # Get unit verification
    verification = endpoints.production.get_unit_verification(
        serial_number="SN001",
        part_number="PCB123",
        client=client
    )
    print(f"Unit verification: {verification}")
    
    # Get serial number types
    sn_types = endpoints.production.get_serial_number_types(client=client)
    print(f"Serial number types: {sn_types}")


def product_management_example():
    """Example of product management operations."""
    
    client = get_default_client()
    
    # Create a product
    product = models.Product(
        part_number="PCB123",
        name="Main Circuit Board",
        description="Primary PCB for device",
        state=1  # Active
    )
    
    created_product = endpoints.product.create_product(product, client=client)
    print(f"Created product: {created_product}")
    
    # Create a product revision
    revision = models.ProductRevision(
        product_id=created_product.product_id,
        revision="Rev1.0",
        name="Initial Release",
        description="First production revision",
        state=1  # Active
    )
    
    created_revision = endpoints.product.create_product_revision(revision, client=client)
    print(f"Created revision: {created_revision}")
    
    # Query products with OData
    products = endpoints.product.query_products(
        odata_filter="partNumber eq 'PCB123'",
        client=client
    )
    print(f"Found products: {products}")


def report_management_example():
    """Example of report management operations."""
    
    client = get_default_client()
    
    # Query report headers with OData
    reports = endpoints.report.query_report_headers(
        odata_filter="partNumber eq 'PCB123'",
        odata_top=10,
        odata_orderby="start desc",
        client=client
    )
    print(f"Found {len(reports)} reports")
    
    if reports:
        report = reports[0]
        print(f"Latest report: {report}")
        
        # Get report in WSJF format
        wsjf_report = endpoints.report.get_wsjf_report(
            report_id=report.uuid,
            detail_level=7,  # Full detail
            client=client
        )
        print(f"WSJF Report keys: {wsjf_report.keys()}")
        
        # Get report attachments
        try:
            attachments = endpoints.report.get_attachments(
                report_id=report.uuid,
                client=client
            )
            print(f"Attachments size: {len(attachments)} bytes")
        except Exception as e:
            print(f"No attachments found: {e}")


def internal_endpoints_example():
    """Example of using internal endpoints."""
    
    # Internal endpoints require proper referrer header
    client = WATSClient(
        base_url="https://your-wats-server.com",
        auth_token="your_token",
        referrer="https://your-wats-server.com/dashboard"
    )
    
    # Get available system languages
    languages = endpoints.internal.get_available_system_languages(client=client)
    print(f"Available languages: {languages}")
    
    # Get logged in username
    username = endpoints.internal.get_logged_in_username(client=client)
    print(f"Logged in user: {username}")
    
    # Get role permissions
    permissions = endpoints.internal.get_role_permissions(client=client)
    print(f"User permissions: {permissions}")
    
    # Check specific permissions
    perm_check = endpoints.internal.check_permissions(
        permissions="1,2,3",  # Comma-separated permission IDs
        client=client
    )
    print(f"Permission check: {perm_check}")


def error_handling_example():
    """Example of error handling."""
    
    from pyWATS.rest_api.exceptions import (
        WATSAPIException, AuthenticationError, NotFoundError
    )
    
    client = get_default_client()
    
    try:
        # This might fail if asset doesn't exist
        asset = endpoints.asset.get_asset_by_serial_number("NONEXISTENT", client=client)
    except NotFoundError as e:
        print(f"Asset not found: {e}")
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
    except WATSAPIException as e:
        print(f"API error: {e} (Status: {e.status_code})")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Note: These examples require proper WATS server configuration
    # and authentication. Set up environment variables:
    # WATS_BASE_URL=https://your-wats-server.com
    # WATS_AUTH_TOKEN=your_token_here
    # WATS_REFERRER=https://your-wats-server.com/dashboard
    
    print("pyWATS REST API Examples")
    print("=" * 40)
    
    try:
        print("\n1. Basic Client Usage")
        basic_client_usage()
        
        print("\n2. Authentication Example")
        authentication_example()
        
        print("\n3. App Endpoints Example")
        app_endpoints_example()
        
        print("\n4. Asset Management Example")
        asset_management_example()
        
        print("\n5. Production Management Example")
        production_management_example()
        
        print("\n6. Product Management Example")
        product_management_example()
        
        print("\n7. Report Management Example")
        report_management_example()
        
        print("\n8. Internal Endpoints Example")
        internal_endpoints_example()
        
        print("\n9. Error Handling Example")
        error_handling_example()
        
    except Exception as e:
        print(f"Example failed: {e}")
        print("Make sure to configure WATS server connection properly.")