# Test Plan - Enum Standardization

**Created:** February 1, 2026  
**Target Coverage:** >90%  
**Test Framework:** pytest

---

## Test File Structure

```
tests/domains/report/test_status_enum_conversion.py
```

---

## Test Classes

### 1. TestStepStatusConversion

#### Test: Exact Values
```python
def test_exact_values():
    """Original format still works."""
    assert StepStatus("P") == StepStatus.Passed
    assert StepStatus("F") == StepStatus.Failed
    assert StepStatus("S") == StepStatus.Skipped
    assert StepStatus("D") == StepStatus.Done
    assert StepStatus("E") == StepStatus.Error
    assert StepStatus("T") == StepStatus.Terminated
```

#### Test: Full Names (Case Variations)
```python
def test_full_names_case_insensitive():
    """Full names work with any casing."""
    assert StepStatus("Passed") == StepStatus.Passed
    assert StepStatus("PASSED") == StepStatus.Passed
    assert StepStatus("passed") == StepStatus.Passed
    assert StepStatus("Pass") == StepStatus.Passed
    assert StepStatus("PASS") == StepStatus.Passed
    
    assert StepStatus("Failed") == StepStatus.Failed
    assert StepStatus("failed") == StepStatus.Failed
    assert StepStatus("FAIL") == StepStatus.Failed
```

#### Test: Common Aliases
```python
def test_aliases():
    """Common aliases work."""
    # Passed aliases
    assert StepStatus("OK") == StepStatus.Passed
    assert StepStatus("ok") == StepStatus.Passed
    assert StepStatus("success") == StepStatus.Passed
    
    # Failed aliases
    assert StepStatus("Fail") == StepStatus.Failed
    assert StepStatus("failure") == StepStatus.Failed
    assert StepStatus("NG") == StepStatus.Failed
    
    # Other aliases
    assert StepStatus("skip") == StepStatus.Skipped
    assert StepStatus("complete") == StepStatus.Done
    assert StepStatus("err") == StepStatus.Error
    assert StepStatus("abort") == StepStatus.Terminated
```

#### Test: Enum Member Access
```python
def test_enum_members_unchanged():
    """Enum member access still works."""
    assert StepStatus.Passed.value == "P"
    assert StepStatus.Failed.value == "F"
    assert StepStatus.Passed.name == "Passed"
    
    # Member comparison
    assert StepStatus.Passed == StepStatus.Passed
    assert StepStatus.Passed != StepStatus.Failed
```

#### Test: Invalid Values
```python
def test_invalid_values():
    """Invalid values raise clear errors."""
    with pytest.raises(ValueError, match="Invalid step status"):
        StepStatus("INVALID")
    
    with pytest.raises(ValueError, match="Invalid step status"):
        StepStatus("X")
    
    with pytest.raises(ValueError, match="must be string"):
        StepStatus(123)
```

#### Test: Properties
```python
def test_properties():
    """Convenience properties work."""
    # full_name
    assert StepStatus("P").full_name == "Passed"
    assert StepStatus("OK").full_name == "Passed"
    
    # is_passing
    assert StepStatus.Passed.is_passing == True
    assert StepStatus.Done.is_passing == True
    assert StepStatus.Failed.is_passing == False
    
    # is_failure
    assert StepStatus.Failed.is_failure == True
    assert StepStatus.Error.is_failure == True
    assert StepStatus.Terminated.is_failure == True
    assert StepStatus.Passed.is_failure == False
```

#### Test: Serialization
```python
def test_serialization():
    """Serialization produces correct WATS API format."""
    from pywats.domains.report.report_models.uut import UUTReport
    
    report = UUTReport.create(sequence="Test")
    report.overall_status = StepStatus("Passed")  # Full word input
    
    data = report.model_dump(mode="json", by_alias=True)
    assert data["UUT"]["Head"]["Status"] == "P"  # Single letter output
```

---

### 2. TestReportStatusConversion

#### All Same Tests as StepStatus, Except:
```python
def test_no_skipped_status():
    """ReportStatus does not have Skipped."""
    with pytest.raises(ValueError):
        ReportStatus("Skipped")
    
    with pytest.raises(ValueError):
        ReportStatus("S")
    
    # StepStatus has it
    assert StepStatus("Skipped") == StepStatus.Skipped  # OK
```

---

### 3. TestStatusFilterConversion

#### Test: Exact Values (Full Words)
```python
def test_exact_values():
    """StatusFilter uses full words."""
    assert StatusFilter("Passed") == StatusFilter.PASSED
    assert StatusFilter("Failed") == StatusFilter.FAILED
    assert StatusFilter("Error") == StatusFilter.ERROR
```

#### Test: Case Insensitive
```python
def test_case_insensitive():
    """StatusFilter accepts any case."""
    assert StatusFilter("PASSED") == StatusFilter.PASSED
    assert StatusFilter("passed") == StatusFilter.PASSED
    assert StatusFilter("Pass") == StatusFilter.PASSED
```

#### Test: Aliases
```python
def test_aliases():
    """StatusFilter supports aliases."""
    assert StatusFilter("OK") == StatusFilter.PASSED
    assert StatusFilter("fail") == StatusFilter.FAILED
    assert StatusFilter("p") == StatusFilter.PASSED
```

#### Test: UPPERCASE Member Names
```python
def test_uppercase_members():
    """StatusFilter uses UPPERCASE member names."""
    assert StatusFilter.PASSED.name == "PASSED"
    assert StatusFilter.FAILED.name == "FAILED"
    assert StatusFilter.PASSED.value == "Passed"
```

#### Test: Serialization (Query Format)
```python
def test_serialization():
    """StatusFilter serializes to full words for queries."""
    from pywats.domains.report.models import WATSFilter
    
    filter = WATSFilter(status=StatusFilter("OK"))  # Alias input
    assert filter.status == "Passed"  # Full word output
```

---

### 4. TestExamplePatterns

#### Test: Report Examples Work
```python
def test_example_numeric_step_pattern():
    """Pattern from report_examples.py works."""
    from pywats.domains.report.report_models.uut import UUTReport
    
    report = UUTReport.create(sequence="Example")
    report.add_numeric_step(
        name="Voltage Test",
        value=3.3,
        comp_op="GELE",
        low_limit=3.0,
        high_limit=3.6,
        status="Passed"  # ✅ Now works!
    )
    
    assert report.steps[0].status == StepStatus.Passed
    assert report.steps[0].status.value == "P"
```

#### Test: Multiple Status Formats
```python
def test_mixed_formats_in_report():
    """Report can use different input formats."""
    from pywats.domains.report.report_models.uut import UUTReport
    
    report = UUTReport.create(sequence="Test")
    
    # Different formats all work
    report.add_pass_fail_step(name="Step1", status="Passed")
    report.add_pass_fail_step(name="Step2", status="P")
    report.add_pass_fail_step(name="Step3", status="OK")
    report.add_pass_fail_step(name="Step4", status="pass")
    
    # All serialize to "P"
    for step in report.steps:
        assert step.status.value == "P"
```

---

### 5. TestBackwardCompatibility

#### Test: Existing Code Still Works
```python
def test_exact_match_still_works():
    """All existing exact-match code unchanged."""
    # These always worked, still work
    assert StepStatus("P") == StepStatus.Passed
    assert ReportStatus("P") == ReportStatus.Passed
    assert StatusFilter("Passed") == StatusFilter.PASSED
```

#### Test: Enum Members Unchanged
```python
def test_enum_member_values_unchanged():
    """Enum serialization format unchanged."""
    assert StepStatus.Passed.value == "P"
    assert StepStatus.Failed.value == "F"
    assert ReportStatus.Passed.value == "P"
    assert StatusFilter.PASSED.value == "Passed"
```

---

## Integration Tests

### Test: Report Submission
```python
# In tests/integration/test_report_submission.py
def test_report_with_flexible_status_submits():
    """Report created with status='Passed' submits successfully."""
    from pywats import pyWATS
    from pywats.domains.report.report_models.uut import UUTReport
    
    api = pyWATS(...)
    report = UUTReport.create(sequence="Integration Test")
    
    # Use human-readable status
    report.overall_status = "Passed"
    report.add_numeric_step(
        name="Test",
        value=5.0,
        status="Passed"
    )
    
    # Submit should succeed
    result = api.report.submit(report)
    assert result is not None
```

### Test: Round-Trip
```python
# In tests/integration/test_report_roundtrip.py
def test_status_survives_roundtrip():
    """Status values survive serialization and deserialization."""
    from pywats.domains.report.report_models.uut import UUTReport
    
    # Create with flexible format
    report1 = UUTReport.create(sequence="Test")
    report1.overall_status = "Passed"  # Full word
    
    # Serialize
    json_data = report1.model_dump(mode="json", by_alias=True)
    assert json_data["UUT"]["Head"]["Status"] == "P"
    
    # Deserialize
    report2 = UUTReport.model_validate(json_data)
    assert report2.overall_status == StepStatus.Passed
    assert report2.overall_status.value == "P"
```

---

## Performance Tests

### Test: Conversion Performance
```python
def test_conversion_performance():
    """Enum conversion is fast (<1μs per call)."""
    import time
    
    # First call (miss, triggers _missing_)
    start = time.perf_counter()
    status = StepStatus("Passed")
    first_time = time.perf_counter() - start
    
    # Subsequent calls (cached)
    start = time.perf_counter()
    for _ in range(10000):
        status = StepStatus("Passed")
    avg_time = (time.perf_counter() - start) / 10000
    
    # Should be negligible
    assert avg_time < 0.000001  # < 1μs
```

---

## Manual Test Checklist

- [ ] Run all examples in `examples/domains/report_examples.py`
- [ ] Create report with `status="Passed"`, submit to test WATS instance
- [ ] Query reports with `StatusFilter("OK")`
- [ ] Verify error messages are helpful for invalid values
- [ ] Test in Python 3.9, 3.10, 3.11 (if multi-version support)

---

## Coverage Goals

| Component | Target Coverage |
|-----------|----------------|
| StepStatus | 100% |
| ReportStatus | 100% |
| StatusFilter | 100% |
| Overall | >90% |

---

## Test Execution

```bash
# Run all enum conversion tests
pytest tests/domains/report/test_status_enum_conversion.py -v

# Run with coverage
pytest tests/domains/report/test_status_enum_conversion.py --cov=pywats.domains.report.report_models.common_types --cov=pywats.shared.enums --cov-report=html

# Run integration tests
pytest tests/integration/test_report_submission.py tests/integration/test_report_roundtrip.py -v

# Run all examples
python examples/domains/report_examples.py
```

---

## Success Criteria

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All examples run without errors
- [ ] Coverage >90%
- [ ] No performance degradation
- [ ] Clear error messages for invalid input
- [ ] Backward compatibility 100%
