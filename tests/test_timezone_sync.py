"""Test timezone synchronization between start and start_utc fields."""

from datetime import datetime, timezone, timedelta
from pywats.domains.report.report_models import UUTReport
from pywats.domains.report.report_models.uut.uut_info import UUTInfo


def test_default_behavior():
    """Test that default factory creates both times correctly."""
    report = UUTReport(
        pn="TEST001",
        sn="SN001",
        rev="A",
        process_code=10,
        station_name="Station1",
        location="Lab",
        purpose="Test",
        info=UUTInfo(operator="TestOp")
    )
    
    print(f"start:     {report.start}")
    print(f"start_utc: {report.start_utc}")
    
    assert report.start is not None, "start should be set by default"
    assert report.start_utc is not None, "start_utc should be computed"
    assert report.start.tzinfo is not None, "start should have timezone"
    assert report.start_utc.tzinfo is not None, "start_utc should have timezone"
    
    # Verify they represent the same moment in time
    diff = abs((report.start - report.start_utc).total_seconds())
    assert diff < 1, f"Times should be equivalent, diff: {diff}s"
    
    # Verify start_utc is actually UTC
    assert report.start_utc.tzinfo == timezone.utc, "start_utc should be UTC"


def test_set_local_time_only():
    """Test setting only local start time."""
    local_time = datetime(2025, 12, 12, 14, 30, 0).astimezone()
    
    report = UUTReport(
        pn="TEST002",
        sn="SN002",
        rev="A",
        process_code=10,
        station_name="Station1",
        location="Lab",
        purpose="Test",
        start=local_time,
        info=UUTInfo(operator="TestOp")
    )
    
    print(f"Input:     {local_time}")
    print(f"start:     {report.start}")
    print(f"start_utc: {report.start_utc}")
    
    assert report.start == local_time, "start should match input"
    assert report.start_utc is not None, "start_utc should be computed"
    
    # Verify they're synchronized
    expected_utc = local_time.astimezone(timezone.utc)
    assert report.start_utc == expected_utc, f"start_utc should be {expected_utc}"


def test_set_utc_time_only():
    """Test setting only UTC time."""
    utc_time = datetime(2025, 12, 12, 13, 30, 0, tzinfo=timezone.utc)
    
    report = UUTReport(
        pn="TEST003",
        sn="SN003",
        rev="A",
        process_code=10,
        station_name="Station1",
        location="Lab",
        purpose="Test",
        start_utc=utc_time,
        info=UUTInfo(operator="TestOp")
    )
    
    print(f"Input UTC: {utc_time}")
    print(f"start:     {report.start}")
    print(f"start_utc: {report.start_utc}")
    
    assert report.start_utc == utc_time, "start_utc should match input"
    assert report.start is not None, "start should be computed from start_utc"
    
    # Verify start is local time equivalent
    expected_local = utc_time.astimezone()
    assert report.start == expected_local, f"start should be {expected_local}"


def test_set_both_times():
    """Test setting both times explicitly."""
    local_time = datetime(2025, 12, 12, 14, 30, 0).astimezone()
    utc_time = local_time.astimezone(timezone.utc)
    
    report = UUTReport(
        pn="TEST004",
        sn="SN004",
        rev="A",
        process_code=10,
        station_name="Station1",
        location="Lab",
        purpose="Test",
        start=local_time,
        start_utc=utc_time,
        info=UUTInfo(operator="TestOp")
    )
    
    print(f"Input local: {local_time}")
    print(f"Input UTC:   {utc_time}")
    print(f"start:       {report.start}")
    print(f"start_utc:   {report.start_utc}")
    
    assert report.start == local_time, "start should match input"
    assert report.start_utc == utc_time, "start_utc should match input"


def test_naive_datetime_handling():
    """Test that naive datetimes are converted to timezone-aware."""
    naive_time = datetime(2025, 12, 12, 14, 30, 0)  # No timezone
    
    report = UUTReport(
        pn="TEST005",
        sn="SN005",
        rev="A",
        process_code=10,
        station_name="Station1",
        location="Lab",
        purpose="Test",
        start=naive_time,
        info=UUTInfo(operator="TestOp")
    )
    
    print(f"Input (naive): {naive_time}")
    print(f"start:         {report.start}")
    print(f"start_utc:     {report.start_utc}")
    
    assert report.start.tzinfo is not None, "Naive datetime should be made aware"
    assert report.start_utc is not None, "start_utc should be computed"
    assert report.start_utc.tzinfo == timezone.utc, "start_utc should be UTC"


def test_serialization_excludes_start_utc():
    """Test that start_utc is excluded from JSON serialization."""
    report = UUTReport(
        pn="TEST006",
        sn="SN006",
        rev="A",
        process_code=10,
        station_name="Station1",
        location="Lab",
        purpose="Test",
        info=UUTInfo(operator="TestOp")
    )
    
    json_data = report.model_dump(mode="json", by_alias=True, exclude_none=True)
    
    print(f"JSON keys: {list(json_data.keys())}")
    print(f"'start' in JSON: {'start' in json_data}")
    print(f"'startUTC' in JSON: {'startUTC' in json_data}")
    
    assert 'start' in json_data, "start should be in JSON"
    assert 'startUTC' not in json_data, "startUTC should be excluded from JSON"
    
    print(f"\nstart value: {json_data['start']}")


def test_deserialization_includes_start_utc():
    """Test that start_utc is populated when deserializing from server."""
    # Simulate server response with both fields
    server_data = {
        "id": "12345678-1234-1234-1234-123456789012",
        "type": "T",
        "pn": "TEST007",
        "sn": "SN007",
        "rev": "A",
        "processCode": 10,
        "machineName": "Station1",
        "location": "Lab",
        "purpose": "Test",
        "result": "P",
        "start": "2025-12-12T14:30:00+01:00",
        "startUTC": "2025-12-12T13:30:00+00:00",
        "uutInfo": {"operator": "TestOp"}
    }
    
    report = UUTReport.model_validate(server_data)
    
    print(f"start:     {report.start}")
    print(f"start_utc: {report.start_utc}")
    
    assert report.start is not None, "start should be deserialized"
    assert report.start_utc is not None, "start_utc should be deserialized"
    
    # Verify times are correct
    from datetime import datetime, timezone
    expected_local = datetime(2025, 12, 12, 14, 30, 0).replace(
        tzinfo=timezone(timedelta(hours=1))
    )
    expected_utc = datetime(2025, 12, 12, 13, 30, 0, tzinfo=timezone.utc)
    
    assert report.start == expected_local, f"start should be {expected_local}"
    assert report.start_utc == expected_utc, f"start_utc should be {expected_utc}"
