import pytest
from pyWATS.tdm_client import TDMClient, APIStatusType
from pyWATS.tdm.models.wsjf_reports import CompOperatorType

from tdm.test_config import TEST_BASE_URL, TEST_AUTH_TOKEN

def test_uut_numeric_step_submission():
    # 1. Initialize the API

    # Setup client
    print("[1] Setting up test client...")
    client = TDMClient()
    client.setup_api(
        data_dir="./test_data",
        location="Test Lab",
        purpose="Automated Testing"
    )
    client.station_name = "Test_Station"
    
    # Connect
    client.initialize_api()
    
    if client.status != APIStatusType.Online:
        print(f"❌ Client not online: {client.status}")
        return False
    
    print("    ✅ Client setup successful")

    api = TDMClient()
    api.register_client(TEST_BASE_URL, TEST_AUTH_TOKEN)
    api.initialize_api(try_connect_to_server=True)

    # 2. Create a UUT report
    uut = api.create_uut_report(
        serial_number="SN_TEST_001",
        part_number="PN_TEST_001",
        revision="A",
        operation_type=10,
        sequence_file_name="TestSequence.seq",
        sequence_file_version="1.0.0",
        operator_name="TestOperator"
    )

    # 3. Create a NumericLimitStep
    root_seq = uut.get_root_Sequence_call()
    numeric_step = root_seq.add_numeric_limit_step("Voltage Test")
    numeric_step.add_test(
        value=2.5,
        comp_operator=CompOperatorType.GELE,
        low_limit=2.0,
        high_limit=3.0,
        unit="V"
    )

    # 4. Submit the UUT report and assert success
    result = api.submit_report(uut)
    assert result is True, "UUT report submission failed"

test_uut_numeric_step_submission()