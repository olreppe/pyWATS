"""Tests for Station auto-detection functionality."""

import os
import socket
import pytest
from unittest.mock import patch

from pywats.core.station import Station, StationRegistry, get_default_station, Purpose


class TestStationAutoDetection:
    """Test suite for station auto-detection."""
    
    def setup_method(self):
        """Clear environment variables before each test."""
        if 'PYWATS_STATION' in os.environ:
            del os.environ['PYWATS_STATION']
        if 'COMPUTERNAME' in os.environ:
            # Save original value for Windows
            self.original_computername = os.environ.get('COMPUTERNAME')
    
    def teardown_method(self):
        """Restore environment after each test."""
        if 'PYWATS_STATION' in os.environ:
            del os.environ['PYWATS_STATION']
        # Restore COMPUTERNAME on Windows
        if hasattr(self, 'original_computername') and self.original_computername:
            os.environ['COMPUTERNAME'] = self.original_computername
    
    def test_auto_detect_from_pywats_station_env(self):
        """Test auto-detection from PYWATS_STATION environment variable."""
        os.environ['PYWATS_STATION'] = 'PRODUCTION-LINE-01'
        
        station = get_default_station()
        
        assert station.name == 'PRODUCTION-LINE-01'
        assert station.location == ""
        assert station.purpose == Purpose.DEVELOPMENT
    
    def test_auto_detect_normalizes_case(self):
        """Test that station names are normalized to uppercase."""
        os.environ['PYWATS_STATION'] = 'test-station-lowercase'
        
        station = get_default_station()
        
        assert station.name == 'TEST-STATION-LOWERCASE'
    
    def test_auto_detect_strips_whitespace(self):
        """Test that whitespace is stripped from station names."""
        os.environ['PYWATS_STATION'] = '  STATION-WITH-SPACES  '
        
        station = get_default_station()
        
        assert station.name == 'STATION-WITH-SPACES'
    
    def test_auto_detect_from_computername_when_no_pywats_station(self):
        """Test fallback to COMPUTERNAME when PYWATS_STATION not set."""
        # Ensure PYWATS_STATION is not set
        if 'PYWATS_STATION' in os.environ:
            del os.environ['PYWATS_STATION']
        
        os.environ['COMPUTERNAME'] = 'WINDOWS-PC-01'
        
        station = get_default_station()
        
        assert station.name == 'WINDOWS-PC-01'
    
    def test_auto_detect_from_hostname_when_no_env_vars(self):
        """Test fallback to socket.gethostname() when no env vars set."""
        # Clear both environment variables
        if 'PYWATS_STATION' in os.environ:
            del os.environ['PYWATS_STATION']
        
        # Mock COMPUTERNAME to not exist
        with patch.dict(os.environ, {}, clear=False):
            # Remove COMPUTERNAME if it exists
            os.environ.pop('COMPUTERNAME', None)
            
            station = get_default_station()
            
            # Should use socket.gethostname()
            expected_name = socket.gethostname().upper()
            assert station.name == expected_name
    
    def test_auto_detect_priority_pywats_over_computername(self):
        """Test that PYWATS_STATION has priority over COMPUTERNAME."""
        os.environ['PYWATS_STATION'] = 'PYWATS-STATION'
        os.environ['COMPUTERNAME'] = 'COMPUTER-NAME'
        
        station = get_default_station()
        
        assert station.name == 'PYWATS-STATION'
    
    def test_station_registry_auto_detect(self):
        """Test StationRegistry.auto_detect() static method."""
        os.environ['PYWATS_STATION'] = 'AUTO-DETECTED-STATION'
        
        station = StationRegistry.auto_detect()
        
        assert station.name == 'AUTO-DETECTED-STATION'
        assert isinstance(station, Station)
    
    def test_station_registry_auto_detect_matches_get_default_station(self):
        """Test that StationRegistry.auto_detect() matches get_default_station()."""
        os.environ['PYWATS_STATION'] = 'TEST-STATION'
        
        station1 = StationRegistry.auto_detect()
        station2 = get_default_station()
        
        assert station1.name == station2.name
        assert station1.location == station2.location
        assert station1.purpose == station2.purpose


class TestStationFromHostname:
    """Test existing from_hostname() method still works."""
    
    def test_from_hostname_uses_socket_hostname(self):
        """Test that from_hostname() uses socket.gethostname()."""
        station = Station.from_hostname()
        
        expected_name = socket.gethostname().upper()
        assert station.name == expected_name
    
    def test_from_hostname_with_custom_location(self):
        """Test from_hostname() with custom location."""
        station = Station.from_hostname(location="Building A, Floor 2")
        
        assert station.location == "Building A, Floor 2"
        assert station.name == socket.gethostname().upper()
    
    def test_from_hostname_with_custom_purpose(self):
        """Test from_hostname() with custom purpose."""
        station = Station.from_hostname(purpose=Purpose.PRODUCTION)
        
        assert station.purpose == Purpose.PRODUCTION
        assert station.name == socket.gethostname().upper()


class TestStationAutoDetectionIntegration:
    """Integration tests for auto-detection in workflows."""
    
    def setup_method(self):
        """Clear environment variables before each test."""
        if 'PYWATS_STATION' in os.environ:
            del os.environ['PYWATS_STATION']
    
    def teardown_method(self):
        """Clear environment variables after each test."""
        if 'PYWATS_STATION' in os.environ:
            del os.environ['PYWATS_STATION']
    
    def test_zero_config_workflow(self):
        """Test zero-configuration workflow with auto-detection."""
        os.environ['PYWATS_STATION'] = 'PRODUCTION-CELL-A1'
        
        # User doesn't specify station - auto-detected
        station = get_default_station()
        
        assert station.name == 'PRODUCTION-CELL-A1'
        assert station.purpose == Purpose.DEVELOPMENT  # Default
    
    def test_manual_override_still_works(self):
        """Test that manual station creation still works."""
        os.environ['PYWATS_STATION'] = 'AUTO-STATION'
        
        # User explicitly creates station (overrides auto-detection)
        manual_station = Station(
            name="MANUAL-STATION",
            location="Lab 1",
            purpose=Purpose.PRODUCTION
        )
        
        assert manual_station.name == "MANUAL-STATION"
        assert manual_station.location == "Lab 1"
        assert manual_station.purpose == Purpose.PRODUCTION
        
        # Auto-detection still works for other code
        auto_station = get_default_station()
        assert auto_station.name == 'AUTO-STATION'
    
    def test_registry_with_auto_detected_default(self):
        """Test using auto-detected station as registry default."""
        os.environ['PYWATS_STATION'] = 'HUB-STATION'
        
        registry = StationRegistry()
        
        # Set auto-detected station as default
        registry.set_default(StationRegistry.auto_detect())
        
        # Active station should be auto-detected
        assert registry.active is not None
        assert registry.active.name == 'HUB-STATION'
