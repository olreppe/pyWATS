"""
Tests for Report discriminated union

Verifies:
- Type-based parsing (type="T" → UUTReport, type="R" → UURReport)
- Polymorphic handling with isinstance()
- parse_report() and parse_reports()
- Type guards (is_uut_report, is_uur_report)
- Serialization/deserialization roundtrips
"""

import pytest
import json

from pywats.domains.report.report_models_v2.report_union import (
    Report,
    parse_report,
    parse_reports,
    serialize_report,
    serialize_reports,
    is_uut_report,
    is_uur_report,
)
from pywats.domains.report.report_models_v2.uut_report import UUTReport
from pywats.domains.report.report_models_v2.uur_report import UURReport


class TestDiscriminatedUnion:
    """Test basic discriminated union parsing."""
    
    def test_parse_uut_report_from_dict(self):
        """Test parsing UUT report from dict."""
        data = {
            'type': 'T',
            'pn': 'ABC123',
            'sn': 'SN-001',
            'rev': 'A',
            'processCode': 100,
            'machineName': 'Station',
            'location': 'Lab',
            'purpose': 'Test'
        }
        
        report = parse_report(data)
        
        assert isinstance(report, UUTReport)
        assert report.type == 'T'
        assert report.common.pn == 'ABC123'
        
    def test_parse_uur_report_from_dict(self):
        """Test parsing UUR report from dict."""
        data = {
            'type': 'R',
            'pn': 'ABC123',
            'sn': 'SN-001',
            'rev': 'A',
            'processCode': 500,
            'machineName': 'Station',
            'location': 'Lab',
            'purpose': 'Repair',
            'uur': {
                'testOperationCode': 100,
                'user': 'John Doe'
            }
        }
        
        report = parse_report(data)
        
        assert isinstance(report, UURReport)
        assert report.type == 'R'
        assert report.common.pn == 'ABC123'
        assert report.uur_info.test_operation_code == 100
        
    def test_parse_uut_from_json_string(self):
        """Test parsing UUT from JSON string."""
        json_str = '''
        {
            "type": "T",
            "pn": "BOARD-X",
            "sn": "B-001",
            "rev": "1.0",
            "processCode": 100,
            "machineName": "TestStation",
            "location": "Lab",
            "purpose": "Test"
        }
        '''
        
        report = parse_report(json_str)
        
        assert isinstance(report, UUTReport)
        assert report.common.pn == 'BOARD-X'
        
    def test_parse_uur_from_json_string(self):
        """Test parsing UUR from JSON string."""
        json_str = '''
        {
            "type": "R",
            "pn": "BOARD-X",
            "sn": "B-001",
            "rev": "1.0",
            "processCode": 500,
            "machineName": "RepairStation",
            "location": "Lab",
            "purpose": "Repair",
            "uur": {
                "testOperationCode": 100,
                "user": "Jane Doe"
            }
        }
        '''
        
        report = parse_report(json_str)
        
        assert isinstance(report, UURReport)
        assert report.common.pn == 'BOARD-X'


class TestTypeGuards:
    """Test type guard functions."""
    
    def test_is_uut_report(self):
        """Test is_uut_report() type guard."""
        uut = UUTReport.create(
            pn="ABC",
            sn="001",
            rev="A",
            process_code=100,
            station_name="Station",
            location="Lab",
            purpose="Test"
        )
        
        assert is_uut_report(uut) is True
        assert is_uur_report(uut) is False
        
    def test_is_uur_report(self):
        """Test is_uur_report() type guard."""
        uur = UURReport.create(
            pn="ABC",
            sn="001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station",
            location="Lab",
            purpose="Repair"
        )
        
        assert is_uur_report(uur) is True
        assert is_uut_report(uur) is False


class TestPolymorphicHandling:
    """Test polymorphic report handling."""
    
    def test_isinstance_narrowing(self):
        """Test TypeScript-style isinstance() narrowing."""
        reports: list[Report] = [
            UUTReport.create(
                pn="UUT-1",
                sn="001",
                rev="A",
                process_code=100,
                station_name="Station",
                location="Lab",
                purpose="Test"
            ),
            UURReport.create(
                pn="UUR-1",
                sn="002",
                rev="A",
                repair_process_code=500,
                test_operation_code=100,
                station_name="Station",
                location="Lab",
                purpose="Repair"
            ),
        ]
        
        uut_count = 0
        uur_count = 0
        
        for report in reports:
            if isinstance(report, UUTReport):
                uut_count += 1
                # TypeScript-style: narrow type, can access UUT-specific fields
                assert report.type == 'T'
            elif isinstance(report, UURReport):
                uur_count += 1
                # TypeScript-style: narrow type, can access UUR-specific fields
                assert report.type == 'R'
                assert report.uur_info.operator is not None
        
        assert uut_count == 1
        assert uur_count == 1
        
    def test_polymorphic_processing(self):
        """Test polymorphic processing of mixed reports."""
        def process_report(report: Report) -> str:
            """Example polymorphic processor."""
            if isinstance(report, UUTReport):
                return f"UUT: {report.common.pn}"
            elif isinstance(report, UURReport):
                return f"UUR: {report.common.pn} by {report.uur_info.operator}"
            else:
                return "Unknown"
        
        uut = UUTReport.create(
            pn="PART1",
            sn="001",
            rev="A",
            process_code=100,
            station_name="Station",
            location="Lab",
            purpose="Test"
        )
        
        uur = UURReport.create(
            pn="PART2",
            sn="002",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station",
            location="Lab",
            purpose="Repair",
            operator="Bob"
        )
        
        assert process_report(uut) == "UUT: PART1"
        assert process_report(uur) == "UUR: PART2 by Bob"


class TestBatchParsing:
    """Test parsing multiple reports at once."""
    
    def test_parse_reports_from_list(self):
        """Test parsing list of reports (mixed types)."""
        data = [
            {
                'type': 'T',
                'pn': 'UUT-1',
                'sn': '001',
                'rev': 'A',
                'processCode': 100,
                'machineName': 'Station',
                'location': 'Lab',
                'purpose': 'Test'
            },
            {
                'type': 'R',
                'pn': 'UUR-1',
                'sn': '002',
                'rev': 'A',
                'processCode': 500,
                'machineName': 'Station',
                'location': 'Lab',
                'purpose': 'Repair',
                'uur': {
                    'testOperationCode': 100,
                    'user': 'Alice'
                }
            },
            {
                'type': 'T',
                'pn': 'UUT-2',
                'sn': '003',
                'rev': 'A',
                'processCode': 100,
                'machineName': 'Station',
                'location': 'Lab',
                'purpose': 'Test'
            }
        ]
        
        reports = parse_reports(data)
        
        assert len(reports) == 3
        assert isinstance(reports[0], UUTReport)
        assert isinstance(reports[1], UURReport)
        assert isinstance(reports[2], UUTReport)
        
    def test_parse_reports_from_json_string(self):
        """Test parsing list from JSON string."""
        json_str = '''
        [
            {
                "type": "T",
                "pn": "ABC",
                "sn": "001",
                "rev": "A",
                "processCode": 100,
                "machineName": "Station",
                "location": "Lab",
                "purpose": "Test"
            },
            {
                "type": "R",
                "pn": "DEF",
                "sn": "002",
                "rev": "A",
                "processCode": 500,
                "machineName": "Station",
                "location": "Lab",
                "purpose": "Repair",
                "uur": {
                    "testOperationCode": 100,
                    "user": "Bob"
                }
            }
        ]
        '''
        
        reports = parse_reports(json_str)
        
        assert len(reports) == 2
        assert isinstance(reports[0], UUTReport)
        assert isinstance(reports[1], UURReport)


class TestSerialization:
    """Test serialization of reports."""
    
    def test_serialize_uut_report(self):
        """Test serializing UUT report."""
        uut = UUTReport.create(
            pn="PART",
            sn="001",
            rev="A",
            process_code=100,
            station_name="Station",
            location="Lab",
            purpose="Test"
        )
        
        json_str = serialize_report(uut)
        data = json.loads(json_str)
        
        assert data['type'] == 'T'
        assert data['pn'] == 'PART'
        
    def test_serialize_uur_report(self):
        """Test serializing UUR report."""
        uur = UURReport.create(
            pn="PART",
            sn="001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station",
            location="Lab",
            purpose="Repair",
            operator="Alice"
        )
        
        json_str = serialize_report(uur)
        data = json.loads(json_str)
        
        assert data['type'] == 'R'
        assert data['pn'] == 'PART'
        
    def test_serialize_reports_list(self):
        """Test serializing list of reports."""
        reports: list[Report] = [
            UUTReport.create(
                pn="UUT",
                sn="001",
                rev="A",
                process_code=100,
                station_name="Station",
                location="Lab",
                purpose="Test"
            ),
            UURReport.create(
                pn="UUR",
                sn="002",
                rev="A",
                repair_process_code=500,
                test_operation_code=100,
                station_name="Station",
                location="Lab",
                purpose="Repair",
                operator="Bob"
            ),
        ]
        
        json_str = serialize_reports(reports)
        data = json.loads(json_str)
        
        assert len(data) == 2
        assert data[0]['type'] == 'T'
        assert data[1]['type'] == 'R'


class TestRoundtripSerialization:
    """Test full roundtrip (object → JSON → object)."""
    
    def test_uut_roundtrip(self):
        """Test UUT report roundtrip."""
        original = UUTReport.create(
            pn="PART",
            sn="001",
            rev="A",
            process_code=100,
            station_name="Station",
            location="Lab",
            purpose="Test"
        )
        
        # Serialize
        json_str = serialize_report(original)
        
        # Deserialize
        restored = parse_report(json_str)
        
        assert isinstance(restored, UUTReport)
        assert restored.common.pn == original.common.pn
        assert restored.type == original.type
        
    def test_uur_roundtrip(self):
        """Test UUR report roundtrip."""
        original = UURReport.create(
            pn="PART",
            sn="001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station",
            location="Lab",
            purpose="Repair",
            operator="Charlie",
            comment="Fixed capacitor"
        )
        
        # Serialize
        json_str = serialize_report(original)
        
        # Deserialize
        restored = parse_report(json_str)
        
        assert isinstance(restored, UURReport)
        assert restored.common.pn == original.common.pn
        assert restored.uur_info.operator == original.uur_info.operator
        assert restored.uur_info.comment == original.uur_info.comment
        
    def test_mixed_list_roundtrip(self):
        """Test mixed report list roundtrip."""
        original: list[Report] = [
            UUTReport.create(
                pn="UUT",
                sn="001",
                rev="A",
                process_code=100,
                station_name="Station",
                location="Lab",
                purpose="Test"
            ),
            UURReport.create(
                pn="UUR",
                sn="002",
                rev="A",
                repair_process_code=500,
                test_operation_code=100,
                station_name="Station",
                location="Lab",
                purpose="Repair",
                operator="Diana"
            ),
        ]
        
        # Serialize
        json_str = serialize_reports(original)
        
        # Deserialize
        restored = parse_reports(json_str)
        
        assert len(restored) == 2
        assert isinstance(restored[0], UUTReport)
        assert isinstance(restored[1], UURReport)
        assert restored[0].common.pn == original[0].common.pn
        assert restored[1].common.pn == original[1].common.pn


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
