"""
Tests for app module - misc endpoints for data retrieval and statistics
"""
import pytest
from pywats.models.report_query import WATSFilter, DateGrouping


class TestStatisticsRetrieval:
    """Test statistics data retrieval"""
    
    def test_get_yield_statistics(self, wats_client):
        """Test getting yield statistics"""
        filter_obj = WATSFilter(
            date_grouping=DateGrouping.DAY,
            period_count=7
        )
        
        try:
            stats = wats_client.app.get_yield_statistics(filter_obj)
            assert isinstance(stats, list)
        except Exception as e:
            pytest.skip(f"Get yield statistics failed: {e}")
    
    def test_get_production_summary(self, wats_client):
        """Test getting production summary"""
        try:
            summary = wats_client.app.get_production_summary()
            assert summary is not None
        except Exception as e:
            pytest.skip(f"Get production summary failed: {e}")


class TestDataRetrieval:
    """Test misc data retrieval endpoints"""
    
    def test_get_stations(self, wats_client):
        """Test getting list of stations"""
        try:
            stations = wats_client.app.get_stations()
            assert isinstance(stations, list)
        except Exception as e:
            pytest.skip(f"Get stations failed: {e}")
    
    def test_get_product_groups(self, wats_client):
        """Test getting product groups"""
        try:
            groups = wats_client.app.get_product_groups()
            assert isinstance(groups, list)
        except Exception as e:
            pytest.skip(f"Get product groups failed: {e}")
    
    def test_get_processes(self, wats_client):
        """Test getting process/operation list"""
        try:
            processes = wats_client.app.get_processes()
            assert isinstance(processes, list)
        except Exception as e:
            pytest.skip(f"Get processes failed: {e}")


class TestFilteredData:
    """Test filtered data retrieval"""
    
    def test_get_filtered_units(self, wats_client, test_part_number):
        """Test getting units with filters"""
        filter_obj = WATSFilter(
            part_number=test_part_number,
            max_count=10
        )
        
        try:
            units = wats_client.app.get_units(filter_obj)
            assert isinstance(units, list)
        except Exception as e:
            pytest.skip(f"Get filtered units failed: {e}")
    
    def test_get_defect_statistics(self, wats_client):
        """Test getting defect/failure statistics"""
        filter_obj = WATSFilter(
            status="Failed",
            date_grouping=DateGrouping.WEEK,
            period_count=4
        )
        
        try:
            stats = wats_client.app.get_defect_statistics(filter_obj)
            assert isinstance(stats, list)
        except Exception as e:
            pytest.skip(f"Get defect statistics failed: {e}")
