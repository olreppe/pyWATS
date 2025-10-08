"""
Comprehensive pyWATS API Example

This example demonstrates the pyWATS API structure including:
- API initialization with server connection
- Working with different modules (report, product, app, etc.)
- Creating and managing reports
- Using the REST API through the HTTP client
- Configuration management

This showcases the pyWATS API functionality using the object-oriented design.
"""

import sys
import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

# Add src to path so we can import pyWATS
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pyWATS import WATSApi, PyWATSConfig
from pyWATS.exceptions import (
    WATSException,
    WATSAPIError,
    WATSConnectionError,
    WATSAuthenticationError
)


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def print_subsection(title: str) -> None:
    """Print a formatted subsection header."""
    print(f"\n--- {title} ---")


def print_report_summary(report) -> None:
    """Print a summary of a report."""
    # Handle both new WSJF models and legacy dictionary format
    if hasattr(report, 'type'):
        # New WSJF model format
        report_type = report.type
        report_id = str(report.id)
        serial_number = report.sn
        part_number = report.pn
        operator = report.info.operator if report.info else 'N/A'
    else:
        # Legacy dictionary format
        report_type = report.get('report_type', 'Unknown')
        report_id = report.get('report_id', 'N/A')
        serial_number = report.get('serial_number', 'N/A')
        part_number = report.get('part_number', 'N/A')
        operator = report.get('operator_name', 'N/A')
    
    print(f"  Type: {report_type}")
    print(f"  ID: {report_id}")
    print(f"  Serial Number: {serial_number}")
    print(f"  Part Number: {part_number}")
    print(f"  Operator: {operator}")


def demonstrate_api_setup() -> WATSApi:
    """Demonstrate WATSApi setup and configuration."""
    print_section("WATS API SETUP")
    
    # Method 1: Using configuration
    print("[1] Creating WATSApi with PyWATSConfig...")
    config = PyWATSConfig.from_environment()
    print(f"    ✓ Configuration loaded:")
    print(f"    ✓ Base URL: {config.BASE_URL}")
    print(f"    ✓ Location: {config.LOCATION}")
    print(f"    ✓ Station Name: {config.STATION_NAME}")
    
    api = WATSApi(config=config)
    print("    ✓ WATSApi created successfully with config")
    
    # Method 2: Direct initialization (alternative)
    print("\n[2] Alternative: Direct initialization...")
    # BASE_URL = "https://py.wats.com"
    # AUTH_TOKEN = "cHlXQVRTX1Rlc3Rpbmc6NWUwYVY3enhJN3E2OUx6ZlE4bDZiMiFPcHB1NmI4"
    # api_direct = WATSApi(base_url=BASE_URL, token=AUTH_TOKEN)
    print("    ✓ Direct initialization available if needed")
    
    return api


def demonstrate_connection_testing(api: WATSApi) -> bool:
    """Demonstrate connection testing and HTTP client usage."""
    print_section("CONNECTION TESTING")
    
    try:
        print("[1] Testing HTTP client connection...")
        
        # Access the HTTP client for direct API calls
        http_client = api.http_client
        print(f"    ✓ HTTP Client available: {http_client}")
        print(f"    ✓ Base URL: {http_client._base_url}")
        
        # Test a simple API call
        print("\n[2] Testing API connectivity...")
        try:
            # Try a simple endpoint to test connection using the underlying httpx client
            with http_client.get_httpx_client() as client:
                response = client.get("/api/System/Status")
                if response.status_code == 200:
                    print("    ✓ Successfully connected to WATS server!")
                    print(f"    ✓ Response status: {response.status_code}")
                    return True
                else:
                    print(f"    ⚠ Server responded with status: {response.status_code}")
                    return False
        except Exception as conn_error:
            print(f"    ⚠ Connection test failed: {conn_error}")
            print("    ℹ Will continue with offline demonstrations")
            return False
            
    except Exception as e:
        print(f"    ✗ Connection setup failed: {e}")
        print("    ⚠ Will demonstrate offline mode")
        return False


def demonstrate_app_module(api: WATSApi) -> None:
    """Demonstrate app module functionality."""
    print_section("APP MODULE FUNCTIONALITY")
    
    try:
        print("[1] Accessing app module...")
        app_module = api.app
        print("    ✓ App module accessed successfully")
        
        print("\n[2] Configuring system settings...")
        # Configure system for testing
        app_module.configure_system(
            data_dir="./wats_api_data",
            location="pyWATS Demo Lab", 
            purpose="API Development Testing"
        )
        print("    ✓ System configured successfully")
        
        print("\n[3] Getting configuration...")
        config = app_module.get_configuration()
        print(f"    ✓ Configuration retrieved:")
        for key, value in config.items():
            print(f"      {key}: {value}")
            
    except Exception as e:
        print(f"    ✗ App module error: {e}")


def demonstrate_report_module(api: WATSApi, is_online: bool) -> tuple[Optional[Any], Optional[Any]]:
    """Demonstrate report module functionality."""
    print_section("REPORT MODULE FUNCTIONALITY")
    
    uut_report = None
    uur_report = None
    
    try:
        print("[1] Accessing report module...")
        report_module = api.report
        print("    ✓ Report module accessed successfully")
        
        if is_online:
            print("\n[2] Getting operation types...")
            try:
                operation_types = report_module.get_operation_types()
                print(f"    ✓ Found {len(operation_types)} operation types")
                
                # Show first few operation types
                for i, op_type in enumerate(operation_types[:3]):
                    print(f"    {i+1}. {op_type.get('name', 'Unknown')} (Code: {op_type.get('code', 'N/A')})")
                    
            except Exception as e:
                print(f"    ⚠ Could not retrieve operation types: {e}")
                operation_types = []
        else:
            print("\n[2] Using mock operation types (offline mode)...")
            operation_types = [
                {'id': 'demo-op-1', 'code': '10', 'name': 'Demo Test Operation'},
                {'id': 'demo-op-2', 'code': '20', 'name': 'Demo Calibration'}
            ]
            print(f"    ✓ Created {len(operation_types)} mock operation types")
        
        print("\n[3] Creating UUT report...")
        try:
            uut_report = report_module.create_uut_report(
                operator="Demo_Operator",
                part_number="DEMO_PART_001",
                revision="Rev_A",
                serial_number=f"DEMO_SN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                operation_type="Demo Test Operation",
                sequence_file="demo_test_sequence.py",
                version="1.2.3",
                station_name="Demo_Station",
                location="Demo Lab",
                purpose="API Testing"
            )
            print("    ✓ UUT report created successfully")
            print_report_summary(uut_report)
            
        except Exception as e:
            print(f"    ✗ Failed to create UUT report: {e}")
        
        print("\n[4] Creating UUR report...")
        try:
            uur_report = report_module.create_uur_report(
                operator="Repair_Technician",
                repair_type="Component Replacement",
                operation_type="Repair Operation",
                serial_number=f"REPAIR_SN_{datetime.now().strftime('%H%M%S')}",
                part_number="REPAIR_PART",
                revision="Rev_B",
                station_name="Repair_Station",
                location="Repair Lab",
                purpose="Component Repair"
            )
            print("    ✓ UUR report created successfully")
            print_report_summary(uur_report)
            
        except Exception as e:
            print(f"    ✗ Failed to create UUR report: {e}")
        
        if is_online and (uut_report or uur_report):
            print("\n[5] Submitting reports...")
            try:
                if uut_report:
                    uut_id = report_module.submit_report(uut_report)
                    print(f"    ✓ UUT report submitted with ID: {uut_id}")
                    
                if uur_report:
                    uur_id = report_module.submit_report(uur_report)
                    print(f"    ✓ UUR report submitted with ID: {uur_id}")
                    
            except Exception as e:
                print(f"    ✗ Report submission failed: {e}")
        else:
            print("\n[5] Skipping report submission (offline mode or no reports)")
            
    except Exception as e:
        print(f"    ✗ Report module error: {e}")
    
    return uut_report, uur_report


def demonstrate_product_module(api: WATSApi, is_online: bool) -> None:
    """Demonstrate product module functionality."""
    print_section("PRODUCT MODULE FUNCTIONALITY")
    
    try:
        print("[1] Accessing product module...")
        product_module = api.product
        print("    ✓ Product module accessed successfully")
        
        if is_online:
            print("\n[2] Getting all products...")
            try:
                products = product_module.get_all()
                print(f"    ✓ Found {len(products)} products")
                
                # Show first few products
                for i, product in enumerate(products[:3]):
                    name = product.get('name', 'Unknown')
                    part_number = product.get('partNumber', 'N/A')
                    print(f"    {i+1}. {name} (Part: {part_number})")
                    
            except Exception as e:
                print(f"    ⚠ Could not retrieve products: {e}")
        else:
            print("\n[2] Offline mode - skipping product retrieval")
            
    except Exception as e:
        print(f"    ✗ Product module error: {e}")


def demonstrate_direct_api_calls(api: WATSApi, is_online: bool) -> None:
    """Demonstrate direct HTTP client usage for custom API calls."""
    print_section("DIRECT API CALLS")
    
    try:
        print("[1] Using HTTP client for direct API access...")
        http_client = api.http_client
        print("    ✓ HTTP client available for custom calls")
        
        if is_online:
            print("\n[2] Making direct API calls...")
            
            # Example: Get system information
            try:
                with http_client.get_httpx_client() as client:
                    response = client.get("/api/System/Info")
                    if response.status_code == 200:
                        system_info = response.json()
                        print("    ✓ System info retrieved:")
                        print(f"      Version: {system_info.get('version', 'Unknown')}")
                        print(f"      Environment: {system_info.get('environment', 'Unknown')}")
                    else:
                        print(f"    ⚠ System info request failed: {response.status_code}")
            except Exception as e:
                print(f"    ⚠ System info request error: {e}")
            
            # Example: Get current user info
            try:
                with http_client.get_httpx_client() as client:
                    response = client.get("/api/User/Current")
                    if response.status_code == 200:
                        user_info = response.json()
                        print("    ✓ User info retrieved:")
                        print(f"      User: {user_info.get('username', 'Unknown')}")
                        print(f"      Roles: {user_info.get('roles', [])}")
                    else:
                        print(f"    ⚠ User info request failed: {response.status_code}")
            except Exception as e:
                print(f"    ⚠ User info request error: {e}")
        else:
            print("\n[2] Offline mode - skipping direct API calls")
            print("    ℹ Example endpoints available:")
            print("      GET /api/System/Info - System information")
            print("      GET /api/User/Current - Current user information")
            print("      GET /api/Report - Report queries")
            print("      POST /api/Report - Report submission")
            
    except Exception as e:
        print(f"    ✗ Direct API calls error: {e}")


def demonstrate_configuration_management() -> None:
    """Demonstrate configuration management features."""
    print_section("CONFIGURATION MANAGEMENT")
    
    try:
        print("[1] Default configuration...")
        default_config = PyWATSConfig()
        print("    ✓ Default configuration loaded:")
        config_dict = default_config.to_dict()
        for key, value in config_dict.items():
            if 'token' in key.lower():
                print(f"      {key}: [HIDDEN]")
            else:
                print(f"      {key}: {value}")
        
        print("\n[2] Environment-based configuration...")
        env_config = PyWATSConfig.from_environment()
        print("    ✓ Environment configuration loaded")
        print(f"    ✓ Uses environment variables if available")
        print(f"    ✓ Falls back to defaults otherwise")
        
        print("\n[3] Configuration in SERVER_AND_TOKEN.md...")
        if os.path.exists("SERVER_AND_TOKEN.md"):
            print("    ✓ SERVER_AND_TOKEN.md file exists")
            print("    ✓ Contains debugging configuration")
            print("    ✓ Available for development use")
        else:
            print("    ⚠ SERVER_AND_TOKEN.md file not found")
            
    except Exception as e:
        print(f"    ✗ Configuration management error: {e}")


def demonstrate_error_handling(api: WATSApi) -> None:
    """Demonstrate error handling patterns."""
    print_section("ERROR HANDLING")
    
    print("[1] Available exception types...")
    print("    ✓ WATSException - Base exception")
    print("    ✓ WATSAPIError - API-related errors")
    print("    ✓ WATSConnectionError - Connection issues")
    print("    ✓ WATSAuthenticationError - Authentication problems")
    
    print("\n[2] Testing error handling...")
    try:
        # Try to access a non-existent endpoint
        with api.http_client.get_httpx_client() as client:
            response = client.get("/api/NonExistent/Endpoint")
            if response.status_code == 404:
                print("    ✓ 404 handling works correctly")
            else:
                print(f"    ⚠ Unexpected response: {response.status_code}")
    except WATSConnectionError as e:
        print(f"    ✓ Connection error handled: {e}")
    except WATSException as e:
        print(f"    ✓ WATS exception handled: {e}")
    except Exception as e:
        print(f"    ⚠ Unexpected error: {e}")


def main():
    """Main demonstration function."""
    print("="*80)
    print(" COMPREHENSIVE pyWATS API DEMONSTRATION")
    print(" Modern object-oriented API for WATS system interaction")
    print("="*80)
    print(f" Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" pyWATS API Demo")
    print("="*80)
    
    api = None
    
    try:
        # 1. Setup WATS API
        api = demonstrate_api_setup()
        
        # 2. Test connection
        is_online = demonstrate_connection_testing(api)
        
        # 3. Configuration management
        demonstrate_configuration_management()
        
        # 4. App module
        demonstrate_app_module(api)
        
        # 5. Report module
        uut_report, uur_report = demonstrate_report_module(api, is_online)
        
        # 6. Product module
        demonstrate_product_module(api, is_online)
        
        # 7. Direct API calls
        demonstrate_direct_api_calls(api, is_online)
        
        # 8. Error handling
        demonstrate_error_handling(api)
        
        print_section("DEMONSTRATION SUMMARY")
        print("✓ WATSApi Setup and Configuration")
        print("✓ HTTP Client Connection Testing") 
        print("✓ App Module (System Configuration)")
        print("✓ Report Module (UUT/UUR Creation)")
        print("✓ Product Module (Product Management)")
        print("✓ Direct API Calls (Custom Endpoints)")
        print("✓ Configuration Management")
        print("✓ Error Handling Patterns")
        
        if is_online:
            print("\n🌐 Server Connection: ONLINE")
            print("   All API modules functional")
        else:
            print("\n📴 Server Connection: OFFLINE") 
            print("   Demonstrated offline capabilities")
            
        print(f"\n📊 API Modules Available: 7")
        print(f"🔧 HTTP Client: {api.http_client._base_url}")
        print(f"⚙️  Configuration: PyWATSConfig")
        
    except Exception as e:
        print_section("ERROR")
        print(f"✗ Demonstration failed with error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print_section("DEMONSTRATION COMPLETE")
        print("Thank you for exploring the pyWATS API!")
        print("For more information, see:")
        print("  - SERVER_AND_TOKEN.md - Configuration details")
        print("  - src/pyWATS/api.py - Main API class")
        print("  - src/pyWATS/config.py - Configuration management")
        print("  - src/pyWATS/modules/ - Individual API modules")


if __name__ == "__main__":
    main()