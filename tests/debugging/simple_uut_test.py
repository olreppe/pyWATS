import pytest
from pyWATS.tdm.models.wsjf_reports import UUTReport, CompOperatorType
from pyWATS.tdm_client import TDMClient

def test_submit_uut_report():
    # Create a UUT report
    uut = UUTReport(
        pn="TEST_PART_001",
        sn="TEST_SN_12345",
        rev="A",
        process_code="1001"
    )

    # Create root sequence
    root_seq = uut.create_root_sequence_call("MainSequence", "1.0")

    # Add a single numeric step
    numeric_step = root_seq.add_numeric_limit_step("Voltage Test")
    numeric_step.add_test(
        value=5.0,
        comp_operator=CompOperatorType.GELE,
        low_limit=4.5,
        high_limit=5.5,
        unit="V"
    )

    # Submit the report
    client = TDMClient()
    response = client.submit_report(uut)

    