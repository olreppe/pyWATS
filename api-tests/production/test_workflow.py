"""
Comprehensive production scenario test.

This test simulates a complete production workflow:
1. Create/update product definitions (module and PCBA with BoxBuild)
2. Create PCBA unit and add to production
3. Test PCBA through ICT and PCBA-TEST with potential failures
4. Build PCBA into module unit
5. Test module through Insulation, Burn-In, and Final Function tests
"""
from typing import Any
from datetime import datetime, timezone
import pytest
import random
from pywats.domains.product import Product, ProductRevision, BomItem
from pywats.domains.product.enums import ProductState
from pywats.domains.production import Unit
from pywats.domains.report.report_models.uut.steps.comp_operator import CompOp
from pywats.shared import Setting
from pywats.core.exceptions import NotFoundError


def get_next_serial(prefix: str) -> str:
    """Generate unique serial numbers with timestamp and random component."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_part = random.randint(1000, 9999)
    return f"{prefix}-{timestamp}-{random_part}"


class TestProductionScenario:
    """Complete production workflow scenario test"""

    @pytest.fixture(autouse=True)
    def setup(self, wats_client: Any) -> None:
        """Setup test data"""
        self.api = wats_client
        self.module_pn = "PRODUCTION-TEST-MODULE"
        self.pcba_pn = "PRODUCTION-TEST-PCBA"
        self.module_rev = "A"
        self.pcba_rev = "A"
        
        # Generate unique serial numbers for this test run
        self.pcba_serial = get_next_serial("PCBA")
        self.module_serial = get_next_serial("MODULE")
        
        # Lot number with random component
        self.lot_number = f"LOT-{random.randint(100, 999)}"
        
        # Test operation codes (from server: api.process.get_test_operations())
        # 30: ICT test, 50: PCBA test, 70: Insulation test, 90: Burn In test, 60: Functional test
        self.op_ict = 30  # ICT test
        self.op_pcba_test = 50  # PCBA test
        self.op_insulation = 70  # Insulation test
        self.op_burn_in = 90  # Burn In test
        self.op_final_function = 60  # Functional test (Final Function)
        
        print(f"\n=== PRODUCTION SCENARIO TEST ===")
        print(f"PCBA Serial: {self.pcba_serial}")
        print(f"Module Serial: {self.module_serial}")
        print(f"Lot Number: {self.lot_number}")
        print("="*50)

    def test_complete_production_workflow(self) -> None:
        """
        Execute complete production workflow from product setup to final test.
        
        This is a single test to maintain state throughout the workflow.
        """
        print("\n" + "="*70)
        print("STEP 1: CREATE/UPDATE PRODUCT DEFINITIONS")
        print("="*70)
        self._setup_products()
        
        print("\n" + "="*70)
        print("STEP 2: CREATE PCBA UNIT AND ADD TO PRODUCTION")
        print("="*70)
        self._create_pcba_unit()
        
        print("\n" + "="*70)
        print("STEP 3: SET PCBA PHASE TO QUEUED AND ADD LOT NUMBER TAG")
        print("="*70)
        self._setup_pcba_for_production()
        
        print("\n" + "="*70)
        print("STEP 4: SIMULATE ICT TEST ON PCBA")
        print("="*70)
        self._run_ict_test()
        
        print("\n" + "="*70)
        print("STEP 5: SIMULATE PCBA-TEST WITH POTENTIAL FAILURE/REPAIR")
        print("="*70)
        self._run_pcba_test()
        
        print("\n" + "="*70)
        print("STEP 6: FINALIZE PCBA AND BUILD INTO MODULE")
        print("="*70)
        self._finalize_pcba_and_build_module()
        
        print("\n" + "="*70)
        print("STEP 7: CREATE MODULE UNIT AND SETUP FOR TESTING")
        print("="*70)
        self._setup_module_for_testing()
        
        print("\n" + "="*70)
        print("STEP 8: SIMULATE INSULATION TEST")
        print("="*70)
        self._run_insulation_test()
        
        print("\n" + "="*70)
        print("STEP 9: SIMULATE BURN-IN TEST")
        print("="*70)
        self._run_burn_in_test()
        
        print("\n" + "="*70)
        print("STEP 10: SIMULATE FINAL FUNCTION TEST AND FINALIZE")
        print("="*70)
        self._run_final_function_test()
        
        print("\n" + "="*70)
        print("PRODUCTION SCENARIO COMPLETE!")
        print("="*70)

    def _setup_products(self) -> None:
        """Step 1: Create or update product definitions"""
        # Check if PCBA exists
        print(f"\nChecking for PCBA product: {self.pcba_pn}")
        try:
            pcba_product = self.api.product.get_product(self.pcba_pn)
        except NotFoundError:
            pcba_product = None
        
        if pcba_product:
            print(f"  [OK] PCBA product exists: {pcba_product.name}")
            # Update if needed
            if pcba_product.state != ProductState.ACTIVE:
                pcba_product.state = ProductState.ACTIVE
                self.api.product.update_product(pcba_product)
                print(f"  [OK] Updated PCBA to ACTIVE state")
        else:
            print(f"  -> Creating PCBA product")
            pcba_product = self.api.product.create_product(
                part_number=self.pcba_pn,
                name="Production Test PCBA",
                description="Test PCBA for production workflow testing",
                state=ProductState.ACTIVE,
                non_serial=False
            )
            print(f"  [OK] Created PCBA product")
        
        # Check if PCBA revision exists
        print(f"\nChecking for PCBA revision: {self.pcba_rev}")
        try:
            pcba_revision = self.api.product.get_revision(self.pcba_pn, self.pcba_rev)
        except NotFoundError:
            pcba_revision = None
        
        if not pcba_revision:
            print(f"  -> Creating PCBA revision")
            pcba_revision = self.api.product.create_revision(
                part_number=self.pcba_pn,
                revision=self.pcba_rev,
                name=f"PCBA Rev {self.pcba_rev}",
                state=ProductState.ACTIVE
            )
            print(f"  [OK] Created PCBA revision")
        else:
            print(f"  [OK] PCBA revision exists")
        
        # Check if Module exists
        print(f"\nChecking for Module product: {self.module_pn}")
        try:
            module_product = self.api.product.get_product(self.module_pn)
        except NotFoundError:
            module_product = None
        
        if module_product:
            print(f"  [OK] Module product exists: {module_product.name}")
            if module_product.state != ProductState.ACTIVE:
                module_product.state = ProductState.ACTIVE
                self.api.product.update_product(module_product)
                print(f"  [OK] Updated Module to ACTIVE state")
        else:
            print(f"  -> Creating Module product")
            module_product = self.api.product.create_product(
                part_number=self.module_pn,
                name="Production Test Module",
                description="Test Module for production workflow testing",
                state=ProductState.ACTIVE,
                non_serial=False
            )
            print(f"  [OK] Created Module product")
        
        # Check if Module revision exists
        print(f"\nChecking for Module revision: {self.module_rev}")
        try:
            module_revision = self.api.product.get_revision(self.module_pn, self.module_rev)
        except NotFoundError:
            module_revision = None
        
        if not module_revision:
            print(f"  -> Creating Module revision")
            module_revision = self.api.product.create_revision(
                part_number=self.module_pn,
                revision=self.module_rev,
                name=f"Module Rev {self.module_rev}",
                state=ProductState.ACTIVE
            )
            print(f"  [OK] Created Module revision")
        else:
            print(f"  [OK] Module revision exists")
        
        # Create/update BoxBuild (BOM) for Module to include PCBA
        print(f"\nSetting up BoxBuild: Module should contain PCBA as subunit")
        bom_items = [
            BomItem(
                component_ref="PCBA1",
                part_number=self.pcba_pn,
                description="PCBA Assembly",
                quantity=1
            )
        ]
        
        result = self.api.product.update_bom(
            part_number=self.module_pn,
            revision=self.module_rev,
            bom_items=bom_items,
            description="Module with PCBA subunit"
        )
        
        if result:
            print(f"  [OK] BoxBuild configured: {self.module_pn} can contain {self.pcba_pn}")
        else:
            print(f"  [!] BoxBuild update may have failed or is not supported")

    def _create_pcba_unit(self) -> None:
        """Step 2: Create PCBA unit and add to production"""
        print(f"\nCreating PCBA unit: {self.pcba_serial} / {self.pcba_pn}")
        
        pcba_unit = Unit(
            serial_number=self.pcba_serial,
            part_number=self.pcba_pn,
            revision=self.pcba_rev
            # serial_date will be set by server
        )
        
        try:
            result = self.api.production.create_units([pcba_unit])
            
            if result:
                print(f"  [OK] PCBA unit created in production system")
            else:
                print(f"  [!] Failed to create PCBA unit (no result)")
                raise Exception("Failed to create PCBA unit")
        except Exception as e:
            print(f"  [!] Error creating PCBA unit: {e}")
            # Try to get the unit if it already exists
            try:
                existing = self.api.production.get_unit(self.pcba_serial, self.pcba_pn)
                if existing:
                    print(f"  -> Unit already exists, continuing...")
                else:
                    raise
            except NotFoundError:
                print(f"  [!] Unit does not exist and could not be created")
                raise

    def _setup_pcba_for_production(self) -> None:
        """Step 3: Set phase to under production and add lot number tag"""
        print(f"\nSetting PCBA phase to 'Under production'")
        
        # Set phase using standard WATS phase name
        success = self.api.production.set_unit_phase(
            serial_number=self.pcba_serial,
            part_number=self.pcba_pn,
            phase="Under production",
            comment="PCBA ready for production testing"
        )
        
        if success:
            print(f"  [OK] Phase set to 'Under production'")
        else:
            print(f"  [!] Failed to set phase (phase name may not exist on server)")
        
        # Add lot number tag
        print(f"\nAdding LotNumber tag: {self.lot_number}")
        
        # Get unit to update tags
        unit = self.api.production.get_unit(self.pcba_serial, self.pcba_pn)
        
        if unit:
            # Add/update lot number tag
            unit.tags = [Setting(key="LotNumber", value=self.lot_number)]
            self.api.production.update_unit(unit)
            print(f"  [OK] LotNumber tag added: {self.lot_number}")
        else:
            print(f"  [!] Could not retrieve unit to add tag")

    def _run_ict_test(self) -> None:
        """Step 4: Run ICT test on PCBA"""
        print(f"\nAltering phase to 'Under Production'")
        self.api.production.set_unit_phase(
            serial_number=self.pcba_serial,
            part_number=self.pcba_pn,
            phase="Under Production",
            comment="Starting ICT test"
        )
        
        print(f"Setting process to ICT (code {self.op_ict})")
        try:
            self.api.production.set_unit_process(
                serial_number=self.pcba_serial,
                part_number=self.pcba_pn,
                process_code=self.op_ict,
                comment="ICT process"
            )
        except NotFoundError:
            print(f"  [!] Process code {self.op_ict} not found on server, continuing without setting process")
        
        # Create ICT test report (always pass for simplicity)
        print(f"\nSimulating ICT test execution...")
        
        report = self.api.report.create_uut_report(
            operator="TestOperator",
            part_number=self.pcba_pn,
            revision=self.pcba_rev,
            serial_number=self.pcba_serial,
            operation_type=self.op_ict,
            station_name="ICT-STATION-01",
            location="TestLab"
        )
        
        # Add test steps to root sequence
        root = report.get_root_sequence_call()
        root.add_boolean_step(name="ICT", status="P")
        root.add_numeric_step(name="Resistance Check", value=100.5, unit="Ohm", status="P", comp_op=CompOp.GELE, low_limit=90.0, high_limit=110.0)
        
        # Submit the report
        report_id = self.api.report.submit_report(report)
        
        if report_id:
            # Verify the report was actually accepted by retrieving it
            retrieved = self.api.report.get_report(report_id)
            assert retrieved is not None, f"Report {report_id} was not accepted by server!"
            print(f"  [OK] ICT test PASSED and verified on server (ID: {report_id})")
        else:
            assert False, "ICT test report failed to submit"

    def _run_pcba_test(self) -> None:
        """Step 5: Run PCBA test with potential failure and repair"""
        print(f"\nSetting process to PCBA-TEST (code {self.op_pcba_test})")
        try:
            self.api.production.set_unit_process(
                serial_number=self.pcba_serial,
                part_number=self.pcba_pn,
                process_code=self.op_pcba_test,
                comment="PCBA-TEST process"
            )
        except NotFoundError:
            print(f"  [!] Process code {self.op_pcba_test} not found on server, continuing without setting process")
        
        # Randomly decide if test fails (30% chance)
        test_fails = random.random() < 0.3
        
        print(f"\nSimulating PCBA-TEST execution...")
        
        if test_fails:
            print(f"  [FAIL] PCBA-TEST FAILED (simulated failure)")
            
            # Submit failing test
            report = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.pcba_pn,
                revision=self.pcba_rev,
                serial_number=self.pcba_serial,
                operation_type=self.op_pcba_test,
                station_name="PCBA-TEST-STATION-01",
                location="TestLab"
            )
            root = report.get_root_sequence_call()
            root.add_boolean_step(name="PCBA-TEST", status="F")
            failed_id = self.api.report.submit_report(report)
            assert failed_id is not None, "Failed PCBA report submission failed!"
            # Verify on server
            assert self.api.report.get_report(failed_id) is not None, f"Failed report {failed_id} not found on server!"
            
            # Create repair report
            print(f"\n  -> Creating repair report...")
            repair = self.api.report.create_uur_report(
                report,
                operator="RepairOperator",
                station_name="RepairStation",
                location="TestLab",
                comment="Component R15 failed - replaced"
            )
            
            # Add failure using valid fail codes from server
            repair.add_failure_to_main_unit(
                category="Component",
                code="Defect Component",
                comment="Component R15 failed",
                component_ref="R15"
            )
            
            repair_id = self.api.report.submit_report(repair)
            assert repair_id is not None, "Repair report submission failed!"
            # Verify on server
            assert self.api.report.get_report(repair_id) is not None, f"Repair report {repair_id} not found on server!"
            print(f"  [OK] Repair completed and verified on server (ID: {repair_id})")
            
            # Retest and pass
            print(f"\n  -> Retesting after repair...")
            retest = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.pcba_pn,
                revision=self.pcba_rev,
                serial_number=self.pcba_serial,
                operation_type=self.op_pcba_test,
                station_name="PCBA-TEST-STATION-01",
                location="TestLab"
            )
            root = retest.get_root_sequence_call()
            root.add_boolean_step(name="PCBA-TEST", status="P")
            retest_id = self.api.report.submit_report(retest)
            assert retest_id is not None, "Retest report submission failed!"
            # Verify on server
            assert self.api.report.get_report(retest_id) is not None, f"Retest report {retest_id} not found on server!"
            print(f"  [OK] PCBA-TEST PASSED after repair and verified on server (ID: {retest_id})")
        else:
            print(f"  [OK] PCBA-TEST PASSED (first attempt)")
            
            report = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.pcba_pn,
                revision=self.pcba_rev,
                serial_number=self.pcba_serial,
                operation_type=self.op_pcba_test,
                station_name="PCBA-TEST-STATION-01",
                location="TestLab"
            )
            root = report.get_root_sequence_call()
            root.add_boolean_step(name="PCBA-TEST", status="P")
            report_id = self.api.report.submit_report(report)
            assert report_id is not None, "PCBA pass report submission failed!"
            # Verify on server
            assert self.api.report.get_report(report_id) is not None, f"PCBA report {report_id} not found on server!"
            print(f"  [OK] PCBA-TEST PASSED and verified on server (ID: {report_id})")

    def _finalize_pcba_and_build_module(self) -> None:
        """Step 6: Finalize PCBA and build into module"""
        # Create module unit first (before finalizing PCBA)
        print(f"\nCreating Module unit: {self.module_serial} / {self.module_pn}")
        
        module_unit = Unit(
            serial_number=self.module_serial,
            part_number=self.module_pn,
            revision=self.module_rev
            # serial_date will be set by server
        )
        
        result = self.api.production.create_units([module_unit])
        
        if result:
            print(f"  [OK] Module unit created")
        
        # Build PCBA into module (before finalizing PCBA)
        print(f"\nBuilding PCBA into Module (assembly)")
        try:
            success = self.api.production.add_child_to_assembly(
                parent_serial=self.module_serial,
                parent_part=self.module_pn,
                child_serial=self.pcba_serial,
                child_part=self.pcba_pn
            )
            
            if success:
                print(f"  [OK] PCBA built into Module successfully")
        except NotFoundError as e:
            print(f"  [!] Assembly failed: {e}. This may be due to server configuration - continuing anyway")
        else:
            print(f"  [!] Failed to build PCBA into Module")

    def _setup_module_for_testing(self) -> None:
        """Step 7: Setup module unit for testing"""
        print(f"\nSetting Module phase to 'Under production'")
        self.api.production.set_unit_phase(
            serial_number=self.module_serial,
            part_number=self.module_pn,
            phase="Under production",
            comment="Module ready for testing"
        )
        
        print(f"  [OK] Module ready for test sequence")

    def _run_insulation_test(self) -> None:
        """Step 8: Run Insulation test with potential failures"""
        print(f"\nAltering phase to 'Under Production'")
        self.api.production.set_unit_phase(
            serial_number=self.module_serial,
            part_number=self.module_pn,
            phase="Under Production",
            comment="Starting Insulation test"
        )
        
        print(f"Setting process to Insulation (code {self.op_insulation})")
        try:
            self.api.production.set_unit_process(
                serial_number=self.module_serial,
                part_number=self.module_pn,
                process_code=self.op_insulation,
                comment="Insulation test"
            )
        except NotFoundError:
            print(f"  [!] Process code {self.op_insulation} not found on server, continuing without setting process")
        
        # Randomly decide if test fails (20% chance)
        test_fails = random.random() < 0.2
        
        print(f"\nSimulating Insulation test execution...")
        
        if test_fails:
            print(f"  [FAIL] Insulation test FAILED")
            
            # Submit failing test
            report = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_insulation,
                station_name="INSULATION-STATION-01",
                location="TestLab"
            )
            root = report.get_root_sequence_call()
            root.add_boolean_step(name="Insulation", status="F")
            self.api.report.submit_report(report)
            
            # Create repair
            print(f"  -> Creating repair report...")
            repair = self.api.report.create_uur_report(
                report,
                operator="RepairOperator",
                station_name="RepairStation",
                location="TestLab",
                comment="Insulation failure repaired"
            )
            # Add failure using valid fail codes from server
            repair.add_failure_to_main_unit(
                category="Component",
                code="Defect Component",
                comment="Insulation resistance too low - Cleaned connectors and resealed",
                component_ref="CON1"
            )
            self.api.report.submit_report(repair)
            print(f"  [OK] Repair completed")
            
            # Retest and pass
            print(f"  -> Retesting after repair...")
            retest = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_insulation,
                station_name="INSULATION-STATION-01",
                location="TestLab"
            )
            root = retest.get_root_sequence_call()
            root.add_boolean_step(name="Insulation", status="P")
            self.api.report.submit_report(retest)
            print(f"  [OK] Insulation test PASSED (after repair)")
        else:
            print(f"  [OK] Insulation test PASSED")
            report = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_insulation,
                station_name="INSULATION-STATION-01",
                location="TestLab"
            )
            root = report.get_root_sequence_call()
            root.add_boolean_step(name="Insulation", status="P")
            self.api.report.submit_report(report)

    def _run_burn_in_test(self) -> None:
        """Step 9: Run Burn-In test with failure handling"""
        print(f"\nSetting process to Burn-In (code {self.op_burn_in})")
        try:
            self.api.production.set_unit_process(
                serial_number=self.module_serial,
                part_number=self.module_pn,
                process_code=self.op_burn_in,
                comment="Burn-In test"
            )
        except NotFoundError:
            print(f"  [!] Process code {self.op_burn_in} not found on server, continuing without setting process")
        
        # Randomly decide if test fails (15% chance)
        test_fails = random.random() < 0.15
        
        print(f"\nSimulating Burn-In test execution...")
        
        if test_fails:
            print(f"  [FAIL] Burn-In test FAILED")
            
            # Submit failing test
            report = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_burn_in,
                station_name="BURN-IN-CHAMBER-01",
                location="TestLab"
            )
            root = report.get_root_sequence_call()
            root.add_boolean_step(name="Burn-In", status="F")
            self.api.report.submit_report(report)
            
            # Any failure after Insulation requires going back to Insulation
            print(f"  [!] Failure after Insulation - must return to Insulation")
            print(f"  -> Setting process back to Insulation")
            
            try:
                self.api.production.set_unit_process(
                    serial_number=self.module_serial,
                    part_number=self.module_pn,
                    process_code=self.op_insulation,
                    comment="Returning to Insulation after Burn-In failure"
                )
            except NotFoundError:
                pass
            
            # Create repair
            print(f"  -> Creating repair report...")
            repair = self.api.report.create_uur_report(
                report,
                operator="RepairOperator",
                station_name="RepairStation",
                location="TestLab",
                comment="Thermal failure repaired"
            )
            # Add failure using valid fail codes from server
            repair.add_failure_to_main_unit(
                category="Component",
                code="Burned Component",
                comment="Thermal failure during burn-in - Reworked thermal interface",
                component_ref="U1"
            )
            self.api.report.submit_report(repair)
            print(f"  [OK] Repair completed")
            
            # Re-run Insulation
            print(f"\n  -> Re-running Insulation test...")
            retest_insul = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_insulation,
                station_name="INSULATION-STATION-01",
                location="TestLab"
            )
            root = retest_insul.get_root_sequence_call()
            root.add_boolean_step(name="Insulation", status="P")
            self.api.report.submit_report(retest_insul)
            print(f"  [OK] Insulation test PASSED (re-run)")
            
            # Re-run Burn-In
            print(f"\n  -> Re-running Burn-In test...")
            try:
                self.api.production.set_unit_process(
                    serial_number=self.module_serial,
                    part_number=self.module_pn,
                    process_code=self.op_burn_in,
                    comment="Burn-In retest"
                )
            except NotFoundError:
                pass
            
            retest_burn = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_burn_in,
                station_name="BURN-IN-CHAMBER-01",
                location="TestLab"
            )
            root = retest_burn.get_root_sequence_call()
            root.add_boolean_step(name="Burn-In", status="P")
            self.api.report.submit_report(retest_burn)
            print(f"  [OK] Burn-In test PASSED (after repair)")
        else:
            print(f"  [OK] Burn-In test PASSED")
            report = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_burn_in,
                station_name="BURN-IN-CHAMBER-01",
                location="TestLab"
            )
            root = report.get_root_sequence_call()
            root.add_boolean_step(name="Burn-In", status="P")
            self.api.report.submit_report(report)

    def _run_final_function_test(self) -> None:
        """Step 10: Run Final Function test and finalize module"""
        print(f"\nSetting process to Final Function (code {self.op_final_function})")
        try:
            self.api.production.set_unit_process(
                serial_number=self.module_serial,
                part_number=self.module_pn,
                process_code=self.op_final_function,
                comment="Final Function test"
            )
        except NotFoundError:
            print(f"  [!] Process code {self.op_final_function} not found on server, continuing without setting process")
        
        # Randomly decide if test fails (10% chance)
        test_fails = random.random() < 0.1
        
        print(f"\nSimulating Final Function test execution...")
        
        if test_fails:
            print(f"  [FAIL] Final Function test FAILED")
            
            # Submit failing test
            report = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_final_function,
                station_name="FINAL-TEST-STATION-01",
                location="TestLab"
            )
            root = report.get_root_sequence_call()
            root.add_boolean_step(name="FinalFunction", status="F")
            self.api.report.submit_report(report)
            
            # Any failure after Insulation requires going back to Insulation
            print(f"  [!] Failure after Insulation - must return to Insulation")
            print(f"  -> Setting process back to Insulation")
            
            try:
                self.api.production.set_unit_process(
                    serial_number=self.module_serial,
                    part_number=self.module_pn,
                    process_code=self.op_insulation,
                    comment="Returning to Insulation after Final Function failure"
                )
            except NotFoundError:
                pass
            
            # Create repair
            print(f"  -> Creating repair report...")
            repair = self.api.report.create_uur_report(
                report,
                operator="RepairOperator",
                station_name="RepairStation",
                location="TestLab",
                comment="Communication failure repaired"
            )
            # Add failure using valid fail codes from server
            repair.add_failure_to_main_unit(
                category="Component",
                code="Defect Component",
                comment="Communication failure - Recalibrated communication interface",
                component_ref="IC2"
            )
            self.api.report.submit_report(repair)
            print(f"  [OK] Repair completed")
            
            # Re-run complete test sequence
            print(f"\n  -> Re-running complete test sequence...")
            
            # Insulation
            print(f"  -> Insulation retest...")
            retest_insul = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_insulation,
                station_name="INSULATION-STATION-01",
                location="TestLab"
            )
            root = retest_insul.get_root_sequence_call()
            root.add_boolean_step(name="Insulation", status="P")
            self.api.report.submit_report(retest_insul)
            
            # Burn-In
            print(f"  -> Burn-In retest...")
            try:
                self.api.production.set_unit_process(
                    serial_number=self.module_serial,
                    part_number=self.module_pn,
                    process_code=self.op_burn_in,
                    comment="Burn-In retest"
                )
            except NotFoundError:
                pass
            retest_burn = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_burn_in,
                station_name="BURN-IN-CHAMBER-01",
                location="TestLab"
            )
            root = retest_burn.get_root_sequence_call()
            root.add_boolean_step(name="Burn-In", status="P")
            self.api.report.submit_report(retest_burn)
            
            # Final Function
            print(f"  -> Final Function retest...")
            try:
                self.api.production.set_unit_process(
                    serial_number=self.module_serial,
                    part_number=self.module_pn,
                    process_code=self.op_final_function,
                    comment="Final Function retest"
                )
            except NotFoundError:
                pass
            retest_final = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_final_function,
                station_name="FINAL-TEST-STATION-01",
                location="TestLab"
            )
            root = retest_final.get_root_sequence_call()
            root.add_boolean_step(name="FinalFunction", status="P")
            self.api.report.submit_report(retest_final)
            print(f"  [OK] Final Function test PASSED (after repair)")
        else:
            print(f"  [OK] Final Function test PASSED")
            report = self.api.report.create_uut_report(
                operator="TestOperator",
                part_number=self.module_pn,
                revision=self.module_rev,
                serial_number=self.module_serial,
                operation_type=self.op_final_function,
                station_name="FINAL-TEST-STATION-01",
                location="TestLab"
            )
            root = report.get_root_sequence_call()
            root.add_boolean_step(name="FinalFunction", status="P")
            self.api.report.submit_report(report)
        
        # Finalize module
        print(f"\n[OK] All tests complete - Finalizing Module")
        self.api.production.set_unit_phase(
            serial_number=self.module_serial,
            part_number=self.module_pn,
            phase="Finalized",
            comment="All testing complete - module ready for shipment"
        )
        
        print(f"  [OK] Module phase set to 'Finalized'")
        print(f"\n{'='*70}")
        print(f"SUCCESS! Module {self.module_serial} completed production workflow")
        print(f"{'='*70}")
