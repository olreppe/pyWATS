"""
Tests for ImportMode functionality.

Tests automatic status calculation and failure propagation in Active mode.
"""
import pytest
from pywats.domains.report import ImportMode
from pywats.domains.report.enums import ImportMode
from pywats.domains.report.import_mode import (
    set_import_mode, 
    get_import_mode, 
    is_active_mode,
    apply_failure_propagation
)
from pywats.domains.report.report_models.uut.step import Step, StepStatus
from pywats.shared.enums import CompOp
from pywats.domains.report.report_models.uut.steps import LimitMeasurement, SequenceCall
from pywats.domains.report.report_models.uut.uut_report import UUTReport


class TestImportModeEnum:
    """Test ImportMode enum values."""
    
    def test_import_mode_values(self):
        """Test that ImportMode has correct values."""
        assert ImportMode.Import.value == "Import"
        assert ImportMode.Active.value == "Active"
    
    def test_import_mode_is_enum(self):
        """Test that ImportMode is an enum."""
        assert hasattr(ImportMode, '__members__')
        assert len(ImportMode.__members__) == 2


class TestImportModeContext:
    """Test ImportMode context management."""
    
    def setup_method(self):
        """Reset to Import mode before each test."""
        set_import_mode(ImportMode.Import)
    
    def test_default_mode_is_import(self):
        """Test that default mode is Import."""
        set_import_mode(ImportMode.Import)  # Reset
        assert get_import_mode() == ImportMode.Import
        assert not is_active_mode()
    
    def test_set_active_mode(self):
        """Test setting Active mode."""
        set_import_mode(ImportMode.Active)
        assert get_import_mode() == ImportMode.Active
        assert is_active_mode()
    
    def test_set_import_mode(self):
        """Test setting Import mode."""
        set_import_mode(ImportMode.Active)
        set_import_mode(ImportMode.Import)
        assert get_import_mode() == ImportMode.Import
        assert not is_active_mode()
    
    def test_invalid_mode_raises_error(self):
        """Test that invalid mode raises TypeError."""
        with pytest.raises(TypeError):
            set_import_mode("Active")
        with pytest.raises(TypeError):
            set_import_mode(1)


class TestCompOpEvaluate:
    """Test CompOp.evaluate() method for status calculation."""
    
    def test_log_always_passes(self):
        """LOG comparison always passes."""
        assert CompOp.LOG.evaluate(100, 0, 200) is True
        assert CompOp.LOG.evaluate(-100, None, None) is True
    
    def test_eq_equal(self):
        """EQ passes when value equals low_limit."""
        assert CompOp.EQ.evaluate(5.0, 5.0) is True
        assert CompOp.EQ.evaluate(5.0, 5.1) is False
    
    def test_ne_not_equal(self):
        """NE passes when value does not equal low_limit."""
        assert CompOp.NE.evaluate(5.0, 5.1) is True
        assert CompOp.NE.evaluate(5.0, 5.0) is False
    
    def test_gt_greater_than(self):
        """GT passes when value > low_limit."""
        assert CompOp.GT.evaluate(10, 5) is True
        assert CompOp.GT.evaluate(5, 5) is False
        assert CompOp.GT.evaluate(4, 5) is False
    
    def test_lt_less_than(self):
        """LT passes when value < low_limit."""
        assert CompOp.LT.evaluate(4, 5) is True
        assert CompOp.LT.evaluate(5, 5) is False
        assert CompOp.LT.evaluate(6, 5) is False
    
    def test_ge_greater_or_equal(self):
        """GE passes when value >= low_limit."""
        assert CompOp.GE.evaluate(10, 5) is True
        assert CompOp.GE.evaluate(5, 5) is True
        assert CompOp.GE.evaluate(4, 5) is False
    
    def test_le_less_or_equal(self):
        """LE passes when value <= low_limit."""
        assert CompOp.LE.evaluate(4, 5) is True
        assert CompOp.LE.evaluate(5, 5) is True
        assert CompOp.LE.evaluate(6, 5) is False
    
    def test_gele_within_range_inclusive(self):
        """GELE passes when low <= value <= high."""
        assert CompOp.GELE.evaluate(5, 0, 10) is True
        assert CompOp.GELE.evaluate(0, 0, 10) is True
        assert CompOp.GELE.evaluate(10, 0, 10) is True
        assert CompOp.GELE.evaluate(-1, 0, 10) is False
        assert CompOp.GELE.evaluate(11, 0, 10) is False
    
    def test_gtlt_within_range_exclusive(self):
        """GTLT passes when low < value < high."""
        assert CompOp.GTLT.evaluate(5, 0, 10) is True
        assert CompOp.GTLT.evaluate(0, 0, 10) is False
        assert CompOp.GTLT.evaluate(10, 0, 10) is False
    
    def test_gelt_ge_low_lt_high(self):
        """GELT passes when value >= low AND value < high."""
        assert CompOp.GELT.evaluate(5, 0, 10) is True
        assert CompOp.GELT.evaluate(0, 0, 10) is True
        assert CompOp.GELT.evaluate(10, 0, 10) is False
    
    def test_gtle_gt_low_le_high(self):
        """GTLE passes when value > low AND value <= high."""
        assert CompOp.GTLE.evaluate(5, 0, 10) is True
        assert CompOp.GTLE.evaluate(0, 0, 10) is False
        assert CompOp.GTLE.evaluate(10, 0, 10) is True
    
    def test_ltgt_outside_range_exclusive(self):
        """LTGT passes when value < low OR value > high."""
        assert CompOp.LTGT.evaluate(-1, 0, 10) is True
        assert CompOp.LTGT.evaluate(11, 0, 10) is True
        assert CompOp.LTGT.evaluate(5, 0, 10) is False
        assert CompOp.LTGT.evaluate(0, 0, 10) is False
        assert CompOp.LTGT.evaluate(10, 0, 10) is False
    
    def test_lege_outside_range_inclusive(self):
        """LEGE passes when value <= low OR value >= high."""
        assert CompOp.LEGE.evaluate(-1, 0, 10) is True
        assert CompOp.LEGE.evaluate(0, 0, 10) is True
        assert CompOp.LEGE.evaluate(10, 0, 10) is True
        assert CompOp.LEGE.evaluate(11, 0, 10) is True
        assert CompOp.LEGE.evaluate(5, 0, 10) is False
    
    def test_missing_limits_pass(self):
        """Missing limits default to pass."""
        assert CompOp.GELE.evaluate(100, None, None) is True
        assert CompOp.GT.evaluate(100, None) is True


class TestLimitMeasurementCalculateStatus:
    """Test LimitMeasurement.calculate_status() method."""
    
    def test_log_returns_pass(self):
        """LOG comparison returns Passed."""
        meas = LimitMeasurement(value=100.0, comp_op=CompOp.LOG)
        assert meas.calculate_status() == "P"
    
    def test_gele_pass(self):
        """GELE within range returns Passed."""
        meas = LimitMeasurement(value=5.0, comp_op=CompOp.GELE, low_limit=0.0, high_limit=10.0)
        assert meas.calculate_status() == "P"
    
    def test_gele_fail_below(self):
        """GELE below range returns Failed."""
        meas = LimitMeasurement(value=-1.0, comp_op=CompOp.GELE, low_limit=0.0, high_limit=10.0)
        assert meas.calculate_status() == "F"
    
    def test_gele_fail_above(self):
        """GELE above range returns Failed."""
        meas = LimitMeasurement(value=11.0, comp_op=CompOp.GELE, low_limit=0.0, high_limit=10.0)
        assert meas.calculate_status() == "F"
    
    def test_string_comp_op_handled(self):
        """String comp_op value is handled."""
        meas = LimitMeasurement(value=5.0, comp_op="GELE", low_limit=0.0, high_limit=10.0)
        assert meas.calculate_status() == "P"


class TestFailParentOnFailure:
    """Test fail_parent_on_failure property and propagation."""
    
    def setup_method(self):
        """Reset to Import mode before each test."""
        set_import_mode(ImportMode.Import)
    
    def test_default_value_is_true(self):
        """fail_parent_on_failure defaults to True."""
        seq = SequenceCall(name="Test")
        assert seq.fail_parent_on_failure is True
    
    def test_propagate_failure_sets_parent_failed(self):
        """propagate_failure sets parent status to Failed."""
        parent = SequenceCall(name="Parent")
        child = SequenceCall(name="Child")
        child.parent = parent
        
        child.propagate_failure()
        
        assert child.status == StepStatus.Failed
        assert parent.status == StepStatus.Failed
    
    def test_propagate_stops_when_flag_false(self):
        """Propagation stops when fail_parent_on_failure is False."""
        grandparent = SequenceCall(name="Grandparent")
        parent = SequenceCall(name="Parent")
        parent.fail_parent_on_failure = False
        parent.parent = grandparent
        child = SequenceCall(name="Child")
        child.parent = parent
        
        child.propagate_failure()
        
        assert child.status == StepStatus.Failed
        assert parent.status == StepStatus.Failed
        assert grandparent.status == StepStatus.Passed  # Not propagated


class TestActiveModeBehavior:
    """Test behavior in Active mode."""
    
    def setup_method(self):
        """Set Active mode before each test."""
        set_import_mode(ImportMode.Active)
    
    def teardown_method(self):
        """Reset to Import mode after each test."""
        set_import_mode(ImportMode.Import)
    
    def test_add_numeric_step_auto_calculates_pass(self):
        """In Active mode, numeric step auto-calculates passing status."""
        seq = SequenceCall(name="Root")
        
        step = seq.add_numeric_step(
            name="Voltage",
            value=5.0,
            comp_op=CompOp.GELE,
            low_limit=0.0,
            high_limit=10.0
        )
        
        # NumericStep uses use_enum_values=True, so status is stored as string
        assert step.status == "P" or step.status == StepStatus.Passed
    
    def test_add_numeric_step_auto_calculates_fail(self):
        """In Active mode, numeric step auto-calculates failing status."""
        seq = SequenceCall(name="Root")
        
        step = seq.add_numeric_step(
            name="Voltage",
            value=15.0,  # Outside limits
            comp_op=CompOp.GELE,
            low_limit=0.0,
            high_limit=10.0
        )
        
        # NumericStep uses use_enum_values=True, so status is stored as string
        assert step.status == "F" or step.status == StepStatus.Failed
    
    def test_add_numeric_step_explicit_status_overrides(self):
        """Explicit status overrides auto-calculation."""
        seq = SequenceCall(name="Root")
        
        step = seq.add_numeric_step(
            name="Voltage",
            value=15.0,  # Would fail
            comp_op=CompOp.GELE,
            low_limit=0.0,
            high_limit=10.0,
            status="P"  # Explicit pass
        )
        
        # NumericStep uses use_enum_values=True, so status is stored as string
        assert step.status == "P" or step.status == StepStatus.Passed
    
    def test_failure_propagates_to_parent(self):
        """Failing step propagates failure to parent in Active mode."""
        root = SequenceCall(name="Root")
        
        step = root.add_numeric_step(
            name="Voltage",
            value=15.0,  # Outside limits - will fail
            comp_op=CompOp.GELE,
            low_limit=0.0,
            high_limit=10.0
        )
        
        # NumericStep uses use_enum_values=True, so status is stored as string
        assert step.status == "F" or step.status == StepStatus.Failed
        assert root.status == StepStatus.Failed


class TestImportModeBehavior:
    """Test behavior in Import mode (default)."""
    
    def setup_method(self):
        """Set Import mode before each test."""
        set_import_mode(ImportMode.Import)
    
    def test_add_numeric_step_defaults_to_pass(self):
        """In Import mode, numeric step defaults to Passed."""
        seq = SequenceCall(name="Root")
        
        step = seq.add_numeric_step(
            name="Voltage",
            value=15.0,  # Would fail in Active mode
            comp_op=CompOp.GELE,
            low_limit=0.0,
            high_limit=10.0
        )
        
        # NumericStep uses use_enum_values=True, so status is stored as string
        assert step.status == "P" or step.status == StepStatus.Passed
    
    def test_no_failure_propagation(self):
        """In Import mode, failure does not propagate."""
        root = SequenceCall(name="Root")
        
        # Explicitly set failure
        step = root.add_numeric_step(
            name="Voltage",
            value=15.0,
            comp_op=CompOp.GELE,
            low_limit=0.0,
            high_limit=10.0,
            status="F"  # Explicit fail
        )
        
        # NumericStep uses use_enum_values=True, so status is stored as string
        assert step.status == "F" or step.status == StepStatus.Failed
        assert root.status == StepStatus.Passed  # Parent not affected


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def setup_method(self):
        """Reset to Import mode before each test."""
        set_import_mode(ImportMode.Import)
    
    def test_nested_propagation(self):
        """Test failure propagation through multiple levels."""
        set_import_mode(ImportMode.Active)
        
        root = SequenceCall(name="Root")
        level1 = root.add_sequence_call(name="Level1")
        level2 = level1.add_sequence_call(name="Level2")
        
        # Add failing step at deepest level
        step = level2.add_numeric_step(
            name="DeepMeasurement",
            value=100.0,
            comp_op=CompOp.GELE,
            low_limit=0.0,
            high_limit=10.0
        )
        
        # NumericStep uses use_enum_values=True, so status is stored as string
        assert step.status == "F" or step.status == StepStatus.Failed
        assert level2.status == StepStatus.Failed
        assert level1.status == StepStatus.Failed
        assert root.status == StepStatus.Failed
    
    def test_log_does_not_fail(self):
        """LOG comparison never causes failure."""
        set_import_mode(ImportMode.Active)
        
        seq = SequenceCall(name="Root")
        
        step = seq.add_numeric_step(
            name="LogValue",
            value=float('inf'),  # Any value
            comp_op=CompOp.LOG
        )
        
        # NumericStep uses use_enum_values=True, so status is stored as string
        assert step.status == "P" or step.status == StepStatus.Passed
        assert seq.status == StepStatus.Passed
