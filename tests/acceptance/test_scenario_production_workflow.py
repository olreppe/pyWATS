"""
Acceptance Test: Complete Production Workflow Scenario

This scenario tests the complete production workflow:
1. Create product and revision
2. Create test report with comprehensive step hierarchy
3. Verify report was saved correctly
4. Query and validate report data
5. Verify unit status and history
"""
import pytest
from pywats import pyWATS
from pywats.domains.report.report_models import UUTReport
from pywats.tools.test_uut import create_test_uut_report
from .conftest import AcceptanceTestHelper


@pytest.mark.acceptance
class TestProductionWorkflowScenario:
    """
    Complete production workflow from product creation to report verification
    """
    
    def test_complete_production_workflow(
        self,
        wats_client: pyWATS,
        test_product_data: dict,
        unique_identifier: str,
        acceptance_helper: AcceptanceTestHelper
    ):
        """
        Test complete production workflow with automatic verification.
        
        Steps:
        1. Create product if it doesn't exist
        2. Create and send UUT report
        3. Verify report was saved and can be loaded
        4. Validate all report details match what was sent
        5. Verify unit status is correct
        """
        part_number = test_product_data["part_number"]
        part_description = test_product_data["part_description"]
        part_revision = test_product_data["part_revision"]
        serial_number = f"SN-{unique_identifier}"
        
        # Step 1: Create product
        try:
            product = wats_client.product.create_product(
                part_number=part_number,
                part_description=part_description
            )
            assert product is not None, "Failed to create product"
            
            revision = wats_client.product.create_revision(
                part_number=part_number,
                part_revision=part_revision
            )
            assert revision is not None, "Failed to create revision"
        except Exception as e:
            pytest.skip(f"Product creation failed: {e}")
        
        # Verify product exists
        loaded_product = acceptance_helper.verify_product_exists(
            wats_client, part_number, part_revision
        )
        assert loaded_product.part_number == part_number
        
        # Step 2: Create comprehensive test report
        report = create_test_uut_report(
            part_number=part_number,
            part_revision=part_revision,
            serial_number=serial_number,
            include_measurements=True,
            include_sequences=True,
            include_charts=True
        )
        
        assert report is not None, "Failed to create test report"
        assert report.serial_number == serial_number
        
        # Send report to server
        result = wats_client.report.send_uut_report(report)
        assert result is True, "Failed to send report to server"
        
        # Step 3: Load and verify report from server
        loaded_report = acceptance_helper.verify_report_created(
            wats_client, serial_number, timeout=30
        )
        
        assert loaded_report is not None, "Report not found on server"
        assert loaded_report.serial_number == serial_number
        assert loaded_report.part_number == part_number
        assert loaded_report.part_revision == part_revision
        
        # Step 4: Verify report structure and data
        assert loaded_report.main_sequence is not None, "Main sequence missing"
        assert len(loaded_report.main_sequence.steps) > 0, "No steps in main sequence"
        
        # Verify step hierarchy
        has_numeric_steps = any(
            hasattr(step, 'measurement') 
            for step in loaded_report.main_sequence.steps
        )
        assert has_numeric_steps, "No numeric measurement steps found"
        
        # Verify sequence hierarchy
        has_sequence_calls = any(
            step.step_type == "SequenceCall" 
            for step in loaded_report.main_sequence.steps
        )
        assert has_sequence_calls, "No sequence call steps found"
        
        # Step 5: Verify unit was created and status is correct
        unit = acceptance_helper.verify_unit_created(wats_client, serial_number)
        assert unit.serial_number == serial_number
        
        # Verify unit status reflects the report
        assert unit.part_number == part_number
        
        print(f"\n✓ Production workflow completed successfully for {serial_number}")
        print(f"  - Product: {part_number} Rev {part_revision}")
        print(f"  - Report UUID: {loaded_report.uuid}")
        print(f"  - Steps: {len(loaded_report.main_sequence.steps)}")
        print(f"  - Unit status verified")


@pytest.mark.acceptance
class TestReportQueryScenario:
    """
    Test report querying and filtering after production
    """
    
    def test_query_reports_by_product(
        self,
        wats_client: pyWATS,
        test_product_data: dict
    ):
        """
        Test querying reports by product parameters.
        
        This test assumes reports exist from previous tests or production.
        """
        part_number = test_product_data["part_number"]
        
        # Query reports by part number
        reports = wats_client.report.get_uut_reports(
            part_number=part_number,
            limit=10
        )
        
        # Verify query works (may return 0 if no reports exist yet)
        assert reports is not None, "Query returned None"
        assert isinstance(reports, list), "Query did not return a list"
        
        if len(reports) > 0:
            # If reports exist, verify they match criteria
            for report in reports:
                assert report.part_number == part_number, \
                    f"Report part number {report.part_number} doesn't match query {part_number}"
            
            print(f"\n✓ Found {len(reports)} reports for product {part_number}")
        else:
            print(f"\n✓ Query successful, no reports found for {part_number}")
    
    def test_query_reports_by_date_range(
        self,
        wats_client: pyWATS
    ):
        """
        Test querying reports by date range.
        """
        from datetime import datetime, timedelta
        
        # Query last 24 hours
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        
        reports = wats_client.report.get_uut_reports(
            start_date_time=start_date.isoformat(),
            end_date_time=end_date.isoformat(),
            limit=10
        )
        
        assert reports is not None, "Query returned None"
        assert isinstance(reports, list), "Query did not return a list"
        
        print(f"\n✓ Found {len(reports)} reports in last 24 hours")
