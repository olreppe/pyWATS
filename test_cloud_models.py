#!/usr/bin/env python3
"""Test cloud agent's report model implementation"""

from pywats.domains.report.report_models.uut.uut_report import UUTReport
from pywats.domains.report.report_models.uut.uut_info import UUTInfo
from pywats.domains.report.report_models.uut.steps.comp_operator import CompOp
from datetime import datetime
import json

# Create a report WITH uut_info
uut_info = UUTInfo(
    operator="TestOperator",
    fixture_id="Fixture001",
    socket_index=0
)

report = UUTReport(
    pn='TEST-PN-001',
    sn='TEST-SN-001',
    rev='1.0',
    process_code=100,
    station_name='TestStation',
    location='Lab',
    purpose='Test',
    result='P',
    start=datetime.now().astimezone(),
    info=uut_info  # Set the uut info
)

root = report.get_root_sequence_call()

# Add steps to verify cloud agent's step models work
root.add_numeric_step(
    name='Voltage', 
    value=3.3, 
    unit='V', 
    comp_op=CompOp.GELE, 
    low_limit=3.0, 
    high_limit=3.6, 
    status='P'
)

multi_bool = root.add_multi_boolean_step(name='Checks', status='P')
multi_bool.add_measurement(name='USB', status='P')

# Serialize
json_str = report.model_dump_json(by_alias=True, exclude_none=True)
data = json.loads(json_str)

print("✅ Report created and serialized successfully")
print(f"✅ Has 'uut' field in JSON: {'uut' in data}")
if 'uut' in data:
    print(f"✅ UUT info present: {data['uut']}")
print(f"✅ Step count: {len(data['root']['steps'])}")
print(f"✅ Step types: {[s['stepType'] for s in data['root']['steps']]}")

# Deserialize to verify union discrimination works
report2 = UUTReport.model_validate(json.loads(json_str))
print("✅ Deserialization successful - union discrimination works")
print(f"✅ Root has {len(report2.root.steps)} steps")

print("\n=== JSON Payload Sample ===")
print(json.dumps(data, indent=2)[:500])
