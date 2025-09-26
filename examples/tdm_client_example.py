"""
Example usage of the TDMClient class - the main TDM interface equivalent to C# TDM class.

This example demonstrates how to use the TDMClient for various TDM operations,
including registration, report creation, and submission.
"""

from pyWATS import TDMClient
from pyWATS.tdm_client import SubmitMethod, APIStatusType


def main():
    """Demonstrate TDMClient usage."""
    
    # Create TDM client instance (equivalent to C# TDM class)
    tdm = TDMClient()
    
    # Setup API configuration
    tdm.setup_api(
        data_dir="./wats_data",
        location="TestLab", 
        purpose="Production Testing",
        persist=False
    )
    
    # Configure connection properties
    tdm.station_name = "TestStation01"
    tdm.validation_mode = tdm.validation_mode.ThrowExceptions
    tdm.test_mode = tdm.test_mode.Active
    
    try:
        # Register client with server (equivalent to C# RegisterClient)
        # In real usage, you'd use actual server credentials
        print("Registering client with WATS server...")
        tdm.register_client(
            base_url="https://ola.wats.com",
            token="cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="
        )
        
        # Initialize API and connect to server
        print("Initializing API...")
        tdm.initialize_api(
            try_connect_to_server=True,
            download_metadata=True
        )
        
        print(f"API Status: {tdm.status}")
        print(f"Client State: {tdm.client_state}")
        
        if tdm.status == APIStatusType.Online:
            print("Successfully connected to WATS server!")
            
            # Get available operation types
            operation_types = tdm.get_operation_types()
            print(f"Available operation types: {len(operation_types)}")
            for op_type in operation_types[:3]:  # Show first 3
                print(f"  - {op_type['name']} (Code: {op_type['code']})")
            
            # Get repair types
            repair_types = tdm.get_repair_types()
            print(f"Available repair types: {len(repair_types)}")
            
            # Create a UUT report (equivalent to C# CreateUUTReport)
            print("\nCreating UUT report...")
            # Use the first available operation type instead of hardcoded "TEST_OP"
            operation_type = operation_types[0] if operation_types else {"code": "DEFAULT_OP", "name": "Default Operation"}
            uut_report = tdm.create_uut_report(
                operator_name="TestOperator",
                part_number="PART001",
                revision="Rev1",
                serial_number="SN12345",
                operation_type=operation_type['code'],  # Use actual operation type code
                sequence_file_name="test_sequence.py",
                sequence_file_version="1.0.0"
            )
            
            print(f"Created UUT report with ID: {uut_report['report_id']}")
            
            # Submit report (equivalent to C# Submit)
            print("Submitting UUT report...")
            success = tdm.submit_report(uut_report, SubmitMethod.Automatic)
            if success:
                print("UUT report submitted successfully!")
            else:
                print("Failed to submit UUT report")
            
            # Create a UUR report (repair report)
            if repair_types:
                print("\nCreating UUR report...")
                uur_report = tdm.create_uur_report(
                    operator_name="RepairTech",
                    repair_type=repair_types[0],  # Use first available repair type
                    uut_report=uut_report  # Associated with the UUT report
                )
                
                print(f"Created UUR report with ID: {uur_report['report_id']}")
                
                # Submit repair report
                success = tdm.submit_report(uur_report, SubmitMethod.Automatic)
                if success:
                    print("UUR report submitted successfully!")
            
            # Check pending reports
            pending_count = tdm.get_pending_report_count()
            if pending_count > 0:
                print(f"\nPending reports: {pending_count}")
                # Submit pending reports
                submitted = tdm.submit_pending_reports()
                print(f"Submitted {submitted} pending reports")
            
            # Test ping functionality
            if tdm.ping():
                print("Server ping successful")
            
            # Access sub-modules (equivalent to C# properties)
            if tdm.statistics:
                print("Statistics module available")
            if tdm.analytics:
                print("Analytics module available")
            if tdm.reports:
                print("Reports module available")
        
        else:
            print("Failed to connect to server - working in offline mode")
            print(f"Pending reports will be saved to: {tdm.data_dir}")
            
            # Even in offline mode, you can create and queue reports
            uut_report = tdm.create_uut_report(
                operator_name="OfflineOperator",
                part_number="OFFLINE_PART",
                revision="Rev1",
                serial_number="OFFLINE_SN001",
                operation_type={"code": "OFFLINE_OP", "name": "Offline Test"},
                sequence_file_name="offline_test.py",
                sequence_file_version="1.0.0"
            )
            
            # Submit offline (will save to queue)
            success = tdm.submit_report(uut_report, SubmitMethod.Offline)
            if success:
                print("Report saved to offline queue")
    
    except Exception as e:
        print(f"Error: {e}")
        if tdm.last_service_exception:
            print(f"Last service exception: {tdm.last_service_exception}")
    
    finally:
        # Cleanup
        tdm.unregister_client()
        print("TDM client disconnected")


def example_with_context_manager():
    """Example using context manager pattern."""
    
    print("\n--- Context Manager Example ---")
    
    with TDMClient() as tdm:
        tdm.setup_api(data_dir="./temp_wats")
        tdm.station_name = "ContextStation"
        
        # Create report without server connection (offline mode)
        report = tdm.create_uut_report(
            operator_name="ContextOperator",
            part_number="CTX_PART",
            revision="1.0",
            serial_number="CTX001",
            operation_type={"code": "CTX_TEST", "name": "Context Test"},
            sequence_file_name="context_test.py",
            sequence_file_version="1.0"
        )
        
        # Save offline
        tdm.submit_report(report, SubmitMethod.Offline)
        print("Report saved in context manager")
    
    print("Context manager closed automatically")


if __name__ == "__main__":
    main()
    example_with_context_manager()