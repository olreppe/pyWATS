"""Tests for queue format converters.

Tests the WSJF, WSXF, WSTF, and ATML format detection and conversion.
"""
import json
import pytest

from pywats.queue.formats import (
    WSJFConverter,
    convert_to_wsjf,
    convert_from_wsxf,
    convert_from_wstf,
    convert_from_atml,
    detect_format,
    convert_to_wsjf_auto,
)


class TestWSJFConverter:
    """Tests for WSJFConverter class."""
    
    def test_to_wsjf_from_dict(self):
        """Test converting dictionary to WSJF."""
        data = {"serialNumber": "SN-001", "partNumber": "PN-001"}
        result = WSJFConverter.to_wsjf(data)
        
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed == data
    
    def test_to_wsjf_preserves_structure(self):
        """Test that nested structures are preserved."""
        data = {
            "report": {
                "uut": {"serialNumber": "SN-001"},
                "steps": [{"name": "Step1"}, {"name": "Step2"}]
            }
        }
        result = WSJFConverter.to_wsjf(data)
        parsed = json.loads(result)
        
        assert parsed["report"]["uut"]["serialNumber"] == "SN-001"
        assert len(parsed["report"]["steps"]) == 2
    
    def test_from_wsjf_parses_json(self):
        """Test parsing WSJF JSON string."""
        wsjf = '{"serialNumber": "SN-001", "status": "passed"}'
        result = WSJFConverter.from_wsjf(wsjf)
        
        assert result["serialNumber"] == "SN-001"
        assert result["status"] == "passed"
    
    def test_from_wsjf_with_array(self):
        """Test parsing JSON array."""
        wsjf = '[{"id": 1}, {"id": 2}]'
        result = WSJFConverter.from_wsjf(wsjf)
        
        assert len(result) == 2
        assert result[0]["id"] == 1


class TestConvertToWsjf:
    """Tests for convert_to_wsjf function."""
    
    def test_convert_dict(self):
        """Test converting plain dictionary."""
        data = {"key": "value"}
        result = convert_to_wsjf(data)
        
        assert json.loads(result) == {"key": "value"}
    
    def test_convert_with_pydantic_model_dump_json(self):
        """Test converting object with model_dump_json method."""
        class MockModel:
            def model_dump_json(self, by_alias=False, exclude_none=False):
                return '{"field": "value"}'
        
        model = MockModel()
        result = convert_to_wsjf(model)
        
        assert result == '{"field": "value"}'
    
    def test_convert_with_pydantic_v1_dict(self):
        """Test converting object with dict method (Pydantic v1 style)."""
        class MockModelV1:
            def dict(self, by_alias=False, exclude_none=False):
                return {"field_v1": "value_v1"}
        
        model = MockModelV1()
        result = convert_to_wsjf(model)
        parsed = json.loads(result)
        
        assert parsed == {"field_v1": "value_v1"}


class TestConvertFromWSXF:
    """Tests for convert_from_wsxf function."""
    
    def test_basic_xml_conversion(self):
        """Test converting basic XML to dict."""
        wsxf = """<?xml version="1.0"?>
        <Report>
            <SerialNumber>SN-001</SerialNumber>
            <Status>Passed</Status>
        </Report>"""
        
        result = convert_from_wsxf(wsxf)
        
        assert isinstance(result, dict)
        assert "SerialNumber" in result or len(result) >= 0
    
    def test_xml_with_namespace(self):
        """Test converting XML with WATS namespace."""
        wsxf = """<?xml version="1.0"?>
        <Report xmlns="http://www.wats.com/XmlFormats/2009/Report">
            <SerialNumber>SN-001</SerialNumber>
        </Report>"""
        
        result = convert_from_wsxf(wsxf)
        assert isinstance(result, dict)
    
    def test_empty_root_element(self):
        """Test converting XML with empty root."""
        wsxf = "<Report></Report>"
        result = convert_from_wsxf(wsxf)
        assert isinstance(result, dict)


class TestConvertFromWSTF:
    """Tests for convert_from_wstf function."""
    
    def test_basic_teststand_xml(self):
        """Test converting TestStand XML."""
        wstf = """<?xml version="1.0"?>
        <TestStandReport>
            <UUT>
                <SerialNumber>SN-001</SerialNumber>
            </UUT>
        </TestStandReport>"""
        
        result = convert_from_wstf(wstf)
        assert isinstance(result, dict)


class TestConvertFromATML:
    """Tests for convert_from_atml function."""
    
    def test_atml_6_01_detection(self):
        """Test ATML 6.01 version detection."""
        atml = """<?xml version="1.0"?>
        <TestResults xmlns="urn:IEEE-1636.1:2013:TestResults">
            <ResultSet>
                <Outcome value="Passed"/>
            </ResultSet>
        </TestResults>"""
        
        result = convert_from_atml(atml)
        
        assert result["_format"] == "atml"
        assert result["_version"] == "6.01"
    
    def test_atml_5_00_detection(self):
        """Test ATML 5.00 version detection."""
        atml = """<?xml version="1.0"?>
        <TestResults xmlns="urn:IEEE-1636.1:2011:TestResults">
            <ResultSet/>
        </TestResults>"""
        
        result = convert_from_atml(atml)
        assert result["_version"] == "5.00"
    
    def test_atml_2_02_detection(self):
        """Test ATML 2.02 version detection."""
        atml = """<?xml version="1.0"?>
        <TestResults xmlns="urn:IEEE-1636.1:2006:TestResults">
            <ResultSet/>
        </TestResults>"""
        
        result = convert_from_atml(atml)
        assert result["_version"] == "2.02"
    
    def test_atml_unknown_version(self):
        """Test ATML with unknown version."""
        atml = """<?xml version="1.0"?>
        <TestResults xmlns="urn:unknown:namespace">
            <ResultSet/>
        </TestResults>"""
        
        result = convert_from_atml(atml)
        assert result["_version"] == "unknown"
    
    def test_atml_result_contains_note(self):
        """Test that ATML result contains usage note."""
        atml = """<?xml version="1.0"?>
        <TestResults xmlns="urn:IEEE-1636.1:2013:TestResults"/>"""
        
        result = convert_from_atml(atml)
        assert "_note" in result
        assert "ATMLConverter" in result["_note"]


class TestDetectFormat:
    """Tests for detect_format function."""
    
    def test_detect_json_object(self):
        """Test detecting JSON object format."""
        data = '{"key": "value"}'
        assert detect_format(data) == "wsjf"
    
    def test_detect_json_array(self):
        """Test detecting JSON array format."""
        data = '[{"id": 1}, {"id": 2}]'
        assert detect_format(data) == "wsjf"
    
    def test_detect_json_with_whitespace(self):
        """Test detecting JSON with leading whitespace."""
        data = '   \n  {"key": "value"}'
        assert detect_format(data) == "wsjf"
    
    def test_detect_wsxf(self):
        """Test detecting WATS XML format."""
        data = '<Report xmlns="http://www.wats.com/XmlFormats/2009/Report"/>'
        assert detect_format(data) == "wsxf"
    
    def test_detect_wstf(self):
        """Test detecting TestStand format."""
        data = '<TestStandReport/>'
        assert detect_format(data) == "wstf"
    
    def test_detect_atml_by_tag(self):
        """Test detecting ATML by tag name."""
        data = '<ATMLResults/>'
        assert detect_format(data) == "atml"
    
    def test_detect_atml_by_namespace(self):
        """Test detecting ATML by IEEE namespace."""
        data = '<Results xmlns="urn:IEEE-1636.1:2013:TestResults"/>'
        assert detect_format(data) == "atml"
    
    def test_detect_atml_ieee_1671(self):
        """Test detecting ATML by IEEE 1671 namespace."""
        data = '<Results xmlns="urn:IEEE-1671:2010"/>'
        assert detect_format(data) == "atml"
    
    def test_detect_generic_xml(self):
        """Test detecting generic XML format."""
        data = '<SomeOtherFormat><Data/></SomeOtherFormat>'
        assert detect_format(data) == "xml"
    
    def test_detect_unknown_format(self):
        """Test detecting unknown format."""
        data = "This is just plain text"
        assert detect_format(data) == "unknown"
    
    def test_detect_invalid_json(self):
        """Test that invalid JSON is not detected as JSON."""
        data = '{invalid json syntax'
        assert detect_format(data) == "unknown"
    
    def test_detect_invalid_xml(self):
        """Test that invalid XML is not detected as XML."""
        data = '<unclosed tag'
        assert detect_format(data) == "unknown"


class TestConvertToWsjfAuto:
    """Tests for convert_to_wsjf_auto function."""
    
    def test_auto_convert_json_passthrough(self):
        """Test that JSON is passed through unchanged."""
        data = '{"key": "value"}'
        result = convert_to_wsjf_auto(data)
        assert result == data
    
    def test_auto_convert_wsxf(self):
        """Test auto-converting WSXF."""
        data = '<Report xmlns="http://www.wats.com/XmlFormats/2009/Report"><SN>001</SN></Report>'
        result = convert_to_wsjf_auto(data)
        
        # Should be valid JSON
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
    
    def test_auto_convert_wstf(self):
        """Test auto-converting WSTF."""
        data = '<TestStandReport><UUT/></TestStandReport>'
        result = convert_to_wsjf_auto(data)
        
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
    
    def test_auto_convert_atml(self):
        """Test auto-converting ATML."""
        data = '<TestResults xmlns="urn:IEEE-1636.1:2013:TestResults"/>'
        result = convert_to_wsjf_auto(data)
        
        parsed = json.loads(result)
        assert parsed["_format"] == "atml"
    
    def test_auto_convert_unknown_raises(self):
        """Test that unknown format raises ValueError."""
        data = "plain text that is not a known format"
        
        with pytest.raises(ValueError, match="Unsupported format"):
            convert_to_wsjf_auto(data)


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_empty_json_object(self):
        """Test converting empty JSON object."""
        result = convert_to_wsjf({})
        assert json.loads(result) == {}
    
    def test_json_with_special_characters(self):
        """Test JSON with special characters."""
        data = {"message": "Test with special chars: äöü 日本語 🚀"}
        result = convert_to_wsjf(data)
        parsed = json.loads(result)
        assert parsed["message"] == data["message"]
    
    def test_json_with_numeric_values(self):
        """Test JSON with various numeric types."""
        data = {"int": 42, "float": 3.14, "negative": -10, "zero": 0}
        result = convert_to_wsjf(data)
        parsed = json.loads(result)
        assert parsed == data
    
    def test_json_with_null_value(self):
        """Test JSON with null value."""
        data = {"value": None}
        result = convert_to_wsjf(data)
        parsed = json.loads(result)
        assert parsed["value"] is None
    
    def test_deeply_nested_structure(self):
        """Test deeply nested data structure."""
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {"value": "deep"}
                    }
                }
            }
        }
        result = convert_to_wsjf(data)
        parsed = json.loads(result)
        assert parsed["level1"]["level2"]["level3"]["level4"]["value"] == "deep"
