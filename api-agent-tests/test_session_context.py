"""
Tests for session caching and analysis context functionality.

Tests cover:
1. SessionManager - Session lifecycle, TTL, cleanup
2. AnalysisSession - Pre-computed matrices, drill-down queries
3. TemporalMatrix - Time-series data organization
4. DeviationMatrix - Dimensional deviation tracking
5. AnalysisContext - Sticky filter memory, confidence decay, topic shift

These components enable:
- Fetch once, analyze many times pattern
- Token-efficient agent responses
- Conversational context persistence
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import time


class TestSessionManager:
    """Tests for SessionManager singleton and session lifecycle."""
    
    def test_singleton_pattern(self):
        """SessionManager should be a singleton."""
        from pywats_agent.tools.shared.session import SessionManager
        
        manager1 = SessionManager.get_instance()
        manager2 = SessionManager.get_instance()
        
        assert manager1 is manager2
    
    def test_create_session_generates_unique_id(self):
        """Each session should have a unique ID."""
        from pywats_agent.tools.shared.session import SessionManager, SessionType
        
        SessionManager.reset_instance()
        manager = SessionManager.get_instance()
        
        session1 = manager.create_session(
            session_type=SessionType.TREND,
            filter_params={"part_number": "TEST"},
            yield_data=[]
        )
        session2 = manager.create_session(
            session_type=SessionType.DEVIATION,
            filter_params={"part_number": "TEST"},
            yield_data=[]
        )
        
        assert session1.session_id != session2.session_id
        assert "trend" in session1.session_id.lower()
        assert "deviation" in session2.session_id.lower()
    
    def test_get_session_by_id(self):
        """Should retrieve session by ID."""
        from pywats_agent.tools.shared.session import SessionManager, SessionType
        
        SessionManager.reset_instance()
        manager = SessionManager.get_instance()
        
        created = manager.create_session(
            session_type=SessionType.GENERAL,
            filter_params={},
            yield_data=[]
        )
        retrieved = manager.get_session(created.session_id)
        
        assert retrieved is created
    
    def test_get_nonexistent_session_returns_none(self):
        """Should return None for unknown session ID."""
        from pywats_agent.tools.shared.session import SessionManager
        
        manager = SessionManager.get_instance()
        result = manager.get_session("nonexistent_123")
        
        assert result is None
    
    def test_session_ttl_expiration(self):
        """Sessions should expire after TTL."""
        from pywats_agent.tools.shared.session import SessionManager, SessionType
        
        SessionManager.reset_instance()
        manager = SessionManager.get_instance()
        
        # Create session with very short TTL
        session = manager.create_session(
            session_type=SessionType.GENERAL,
            filter_params={},
            yield_data=[],
            ttl_minutes=0
        )
        
        # Force expiration time to past
        session.expires_at = datetime.now() - timedelta(seconds=1)
        
        # Should be expired
        assert session.is_expired
        
        # get_session should return None for expired sessions
        result = manager.get_session(session.session_id)
        assert result is None
    
    def test_cleanup_removes_expired_sessions(self):
        """Cleanup should remove expired sessions."""
        from pywats_agent.tools.shared.session import SessionManager, SessionType
        
        SessionManager.reset_instance()
        manager = SessionManager.get_instance()
        
        # Create session and manually expire it
        session = manager.create_session(
            session_type=SessionType.GENERAL,
            filter_params={},
            yield_data=[]
        )
        session.expires_at = datetime.now() - timedelta(seconds=1)
        
        # Trigger cleanup by creating new session
        manager.create_session(
            session_type=SessionType.GENERAL,
            filter_params={},
            yield_data=[]
        )
        
        # Expired session should be removed
        assert manager.get_session(session.session_id) is None
    
    def test_reset_instance_clears_manager(self):
        """reset_instance should clear the singleton."""
        from pywats_agent.tools.shared.session import SessionManager, SessionType
        
        manager1 = SessionManager.get_instance()
        manager1.create_session(
            session_type=SessionType.GENERAL,
            filter_params={},
            yield_data=[]
        )
        
        SessionManager.reset_instance()
        manager2 = SessionManager.get_instance()
        
        assert manager1 is not manager2
        assert manager2.get_active_session_count() == 0


class TestAnalysisSession:
    """Tests for AnalysisSession data storage and access."""
    
    def test_session_stores_filter_params(self):
        """Session should store original filter parameters."""
        from pywats_agent.tools.shared.session import AnalysisSession, SessionType
        
        filter_params = {"part_number": "TEST-001", "days": 30}
        session = AnalysisSession(
            session_id="test_123",
            session_type=SessionType.TREND,
            filter_params=filter_params,
            yield_data=[],
        )
        
        assert session.filter_params == filter_params
    
    def test_session_touch_updates_last_accessed(self):
        """Touching session should update last_accessed time."""
        from pywats_agent.tools.shared.session import AnalysisSession, SessionType
        
        session = AnalysisSession(
            session_id="test_123",
            session_type=SessionType.GENERAL,
            filter_params={},
            yield_data=[],
        )
        
        old_accessed = session.last_accessed
        time.sleep(0.01)  # Ensure time difference
        session.touch()
        
        assert session.last_accessed > old_accessed
    
    def test_session_expiration_check(self):
        """is_expired should correctly identify expired sessions."""
        from pywats_agent.tools.shared.session import AnalysisSession, SessionType
        
        # Non-expired session
        session = AnalysisSession(
            session_id="test_123",
            session_type=SessionType.GENERAL,
            filter_params={},
            yield_data=[],
            ttl_minutes=5,
        )
        assert not session.is_expired
        
        # Expired session
        session.expires_at = datetime.now() - timedelta(seconds=1)
        assert session.is_expired
    
    def test_session_summary_is_token_efficient(self):
        """Session summary should contain minimal essential info."""
        from pywats_agent.tools.shared.session import AnalysisSession, SessionType
        
        session = AnalysisSession(
            session_id="trend_abc123",
            session_type=SessionType.TREND,
            filter_params={"part_number": "TEST", "station_name": "ST-01", "days": 30},
            yield_data=[Mock() for _ in range(100)],
        )
        
        summary = session.to_summary()
        
        assert "session_id" in summary
        assert "session_type" in summary
        assert "total_records" in summary
        assert summary["total_records"] == 100
        assert "expires_in_minutes" in summary
    
    def test_session_created_at_set_automatically(self):
        """Session should have created_at set automatically."""
        from pywats_agent.tools.shared.session import AnalysisSession, SessionType
        
        before = datetime.now()
        session = AnalysisSession(
            session_id="test_123",
            session_type=SessionType.GENERAL,
            filter_params={},
            yield_data=[],
        )
        after = datetime.now()
        
        assert before <= session.created_at <= after


class TestTemporalMatrix:
    """Tests for pre-computed temporal analysis data."""
    
    def test_temporal_matrix_creation(self):
        """TemporalMatrix should store period data correctly."""
        from pywats_agent.tools.shared.session import TemporalMatrix
        
        matrix = TemporalMatrix(
            periods=["2024-01", "2024-02", "2024-03"],
            yields={"2024-01": 95.0, "2024-02": 93.5, "2024-03": 96.2},
            unit_counts={"2024-01": 100, "2024-02": 120, "2024-03": 110},
            fp_counts={"2024-01": 95, "2024-02": 112, "2024-03": 106},
        )
        
        assert len(matrix.periods) == 3
        assert matrix.yields["2024-02"] == 93.5
    
    def test_get_period_returns_correct_data(self):
        """get_period should return data for specific period."""
        from pywats_agent.tools.shared.session import TemporalMatrix
        
        matrix = TemporalMatrix(
            periods=["2024-01", "2024-02"],
            yields={"2024-01": 95.0, "2024-02": 93.5},
            unit_counts={"2024-01": 100, "2024-02": 120},
            fp_counts={"2024-01": 95, "2024-02": 112},
        )
        
        period_data = matrix.get_period("2024-01")
        
        assert period_data["period"] == "2024-01"
        assert period_data["yield"] == 95.0
        assert period_data["unit_count"] == 100
    
    def test_get_period_nonexistent_returns_none(self):
        """get_period should return None for nonexistent period."""
        from pywats_agent.tools.shared.session import TemporalMatrix
        
        matrix = TemporalMatrix(
            periods=["2024-01"],
            yields={"2024-01": 95.0},
            unit_counts={"2024-01": 100},
            fp_counts={"2024-01": 95},
        )
        
        result = matrix.get_period("2024-12")
        assert result is None
    
    def test_get_range_returns_period_subset(self):
        """get_range should return data for period range."""
        from pywats_agent.tools.shared.session import TemporalMatrix
        
        matrix = TemporalMatrix(
            periods=["2024-01", "2024-02", "2024-03", "2024-04"],
            yields={"2024-01": 95.0, "2024-02": 93.5, "2024-03": 96.2, "2024-04": 94.0},
            unit_counts={"2024-01": 100, "2024-02": 120, "2024-03": 110, "2024-04": 130},
            fp_counts={"2024-01": 95, "2024-02": 112, "2024-03": 106, "2024-04": 122},
        )
        
        range_data = matrix.get_range("2024-02", "2024-03")
        
        assert len(range_data) == 2
        assert range_data[0]["period"] == "2024-02"
        assert range_data[1]["period"] == "2024-03"
    
    def test_temporal_matrix_with_trend_metrics(self):
        """TemporalMatrix should support trend metrics."""
        from pywats_agent.tools.shared.session import TemporalMatrix
        
        matrix = TemporalMatrix(
            periods=["2024-01", "2024-02"],
            yields={"2024-01": 95.0, "2024-02": 93.5},
            unit_counts={"2024-01": 100, "2024-02": 120},
            fp_counts={"2024-01": 95, "2024-02": 112},
            trend_slope=-0.5,
            volatility=1.2,
            change_points=["2024-02"],
        )
        
        assert matrix.trend_slope == -0.5
        assert matrix.volatility == 1.2
        assert "2024-02" in matrix.change_points


class TestDeviationMatrix:
    """Tests for pre-computed deviation analysis data."""
    
    def test_deviation_cell_creation(self):
        """DeviationCell should store deviation data correctly."""
        from pywats_agent.tools.shared.session import DeviationCell
        
        cell = DeviationCell(
            dimension_values={"station_name": "ST-01"},
            yield_value=88.5,
            unit_count=50,
            deviation_from_baseline=-6.5,
            significance="high",
            confidence=0.8,
        )
        
        assert cell.yield_value == 88.5
        assert cell.deviation_from_baseline == -6.5
        assert cell.significance == "high"
        assert cell.dimension_values["station_name"] == "ST-01"
    
    def test_deviation_matrix_stores_ranked_cells(self):
        """DeviationMatrix should store pre-ranked cells."""
        from pywats_agent.tools.shared.session import DeviationMatrix, DeviationCell
        
        critical = DeviationCell(
            dimension_values={"station_name": "ST-01"},
            yield_value=80.0,
            unit_count=100,
            deviation_from_baseline=-15.0,
            significance="critical",
            confidence=0.9,
        )
        
        matrix = DeviationMatrix(
            dimensions=["station_name"],
            baseline_yield=95.0,
            total_units=500,
            cells=[critical],
            critical_cells=[critical],
            high_cells=[],
            moderate_cells=[],
        )
        
        assert len(matrix.critical_cells) == 1
        assert matrix.critical_cells[0].significance == "critical"
    
    def test_get_cell_by_dimension_values(self):
        """get_cell should find cell by dimension values."""
        from pywats_agent.tools.shared.session import DeviationMatrix, DeviationCell
        
        cell1 = DeviationCell(
            dimension_values={"station_name": "ST-01"},
            yield_value=88.5,
            unit_count=50,
            deviation_from_baseline=-6.5,
            significance="high",
            confidence=0.8,
        )
        cell2 = DeviationCell(
            dimension_values={"station_name": "ST-02"},
            yield_value=96.0,
            unit_count=60,
            deviation_from_baseline=1.0,
            significance="none",
            confidence=0.9,
        )
        
        matrix = DeviationMatrix(
            dimensions=["station_name"],
            baseline_yield=95.0,
            total_units=110,
            cells=[cell1, cell2],
        )
        
        found = matrix.get_cell(station_name="ST-01")
        assert found is cell1
    
    def test_deviation_cell_to_dict(self):
        """DeviationCell.to_dict should include all relevant fields."""
        from pywats_agent.tools.shared.session import DeviationCell
        
        cell = DeviationCell(
            dimension_values={"station_name": "ST-01", "test_operation": "FCT"},
            yield_value=88.5,
            unit_count=50,
            deviation_from_baseline=-6.5,
            significance="high",
            confidence=0.8,
        )
        
        result = cell.to_dict()
        
        assert result["station_name"] == "ST-01"
        assert result["test_operation"] == "FCT"
        assert result["yield"] == 88.5
        assert result["deviation"] == -6.5
    
    def test_get_dimension_values(self):
        """get_dimension_values should return unique values for dimension."""
        from pywats_agent.tools.shared.session import DeviationMatrix, DeviationCell
        
        cell1 = DeviationCell(
            dimension_values={"station_name": "ST-01"},
            yield_value=88.5, unit_count=50,
            deviation_from_baseline=-6.5, significance="high", confidence=0.8
        )
        cell2 = DeviationCell(
            dimension_values={"station_name": "ST-02"},
            yield_value=96.0, unit_count=60,
            deviation_from_baseline=1.0, significance="none", confidence=0.9
        )
        
        matrix = DeviationMatrix(
            dimensions=["station_name"],
            baseline_yield=95.0,
            total_units=110,
            cells=[cell1, cell2],
        )
        
        values = matrix.get_dimension_values("station_name")
        assert "ST-01" in values
        assert "ST-02" in values


class TestAnalysisContext:
    """Tests for sticky filter memory and context management."""
    
    def test_context_singleton_pattern(self):
        """AnalysisContext should be a singleton."""
        from pywats_agent.tools.shared.context import AnalysisContext
        
        ctx1 = AnalysisContext.get_instance()
        ctx2 = AnalysisContext.get_instance()
        
        assert ctx1 is ctx2
    
    def test_context_reset_clears_instance(self):
        """reset_instance should allow fresh context."""
        from pywats_agent.tools.shared.context import AnalysisContext
        
        ctx1 = AnalysisContext.get_instance()
        ctx1.update_filter(part_number="TEST-001")
        
        AnalysisContext.reset_instance()
        ctx2 = AnalysisContext.get_instance()
        
        assert ctx1 is not ctx2
    
    def test_update_filter_stores_values(self):
        """update_filter should store filter parameters."""
        from pywats_agent.tools.shared.context import AnalysisContext
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        ctx.update_filter(part_number="WIDGET-001", test_operation="FCT")
        
        # Access filter memory via filter property
        memory = ctx.filter
        assert memory.part_number == "WIDGET-001"
        assert memory.test_operation == "FCT"
    
    def test_filter_persistence_across_calls(self):
        """Filters should persist across multiple calls."""
        from pywats_agent.tools.shared.context import AnalysisContext
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        ctx.update_filter(part_number="WIDGET-001")
        ctx.update_filter(station_name="ST-01")
        
        memory = ctx.filter
        assert memory.part_number == "WIDGET-001"  # Still there
        assert memory.station_name == "ST-01"      # New value
    
    def test_effective_filter_merges_memory_and_explicit(self):
        """get_effective_filter should merge memory with explicit params."""
        from pywats_agent.tools.shared.context import AnalysisContext
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        ctx.update_filter(part_number="WIDGET-001", test_operation="FCT")
        
        effective, _ = ctx.get_effective_filter(
            explicit_params={"station_name": "ST-02"}
        )
        
        assert effective["part_number"] == "WIDGET-001"
        assert effective["test_operation"] == "FCT"
        assert effective["station_name"] == "ST-02"
    
    def test_explicit_params_override_memory(self):
        """Explicit parameters should override memory values."""
        from pywats_agent.tools.shared.context import AnalysisContext
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        ctx.update_filter(part_number="WIDGET-001")
        
        effective, _ = ctx.get_effective_filter(
            explicit_params={"part_number": "OTHER-002"}
        )
        
        assert effective["part_number"] == "OTHER-002"
    
    def test_clear_method(self):
        """clear should reset all context."""
        from pywats_agent.tools.shared.context import AnalysisContext
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        ctx.update_filter(part_number="TEST", station_name="ST-01")
        ctx.clear()
        
        memory = ctx.filter
        assert memory.part_number is None
        assert memory.station_name is None


class TestContextConfidence:
    """Tests for context confidence decay over time."""
    
    def test_high_confidence_for_recent_interaction(self):
        """Confidence should be HIGH immediately after interaction."""
        from pywats_agent.tools.shared.context import AnalysisContext, ContextConfidence
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        ctx.update_filter(part_number="TEST")
        confidence = ctx.confidence  # Property access
        
        assert confidence == ContextConfidence.HIGH
    
    def test_confidence_decay_with_time(self):
        """Confidence should decay as time passes."""
        from pywats_agent.tools.shared.context import AnalysisContext, ContextConfidence
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        ctx.update_filter(part_number="TEST")
        
        # Simulate time passing
        ctx._last_interaction = datetime.now() - timedelta(minutes=3)
        
        confidence = ctx.confidence
        assert confidence in [ContextConfidence.MEDIUM, ContextConfidence.LOW]
    
    def test_expired_confidence_after_long_time(self):
        """Confidence should be EXPIRED after long inactivity."""
        from pywats_agent.tools.shared.context import AnalysisContext, ContextConfidence
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        ctx.update_filter(part_number="TEST")
        
        # Simulate long time passing
        ctx._last_interaction = datetime.now() - timedelta(minutes=10)
        
        confidence = ctx.confidence
        assert confidence == ContextConfidence.EXPIRED


class TestTopicShiftDetection:
    """Tests for detecting topic shifts in conversation."""
    
    def test_topic_shift_clears_old_context(self):
        """Shifting to new topic should clear previous context."""
        from pywats_agent.tools.shared.context import AnalysisContext
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        # Set initial context
        ctx.update_filter(part_number="PRODUCT-A", station_name="ST-01")
        
        # Shift to different product
        ctx.update_filter(part_number="PRODUCT-B")  # Should clear station_name
        
        memory = ctx.filter
        assert memory.part_number == "PRODUCT-B"
        # Old context should be cleared on topic shift
    
    def test_detect_topic_shift_via_internal_method(self):
        """Should detect topic shift when product changes."""
        from pywats_agent.tools.shared.context import AnalysisContext
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        ctx.update_filter(part_number="PRODUCT-A")
        
        # Different product is a topic shift
        is_shift = ctx._detect_topic_shift(part_number="PRODUCT-B")
        assert is_shift
    
    def test_no_shift_when_adding_context(self):
        """Adding more context shouldn't be detected as shift."""
        from pywats_agent.tools.shared.context import AnalysisContext
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        ctx.update_filter(part_number="PRODUCT-A")
        
        # Adding station to same product is not a shift
        is_shift = ctx._detect_topic_shift(station_name="ST-01")
        assert not is_shift
    
    def test_explicit_topic_shift_clears_all(self):
        """shift_topic should explicitly clear all context."""
        from pywats_agent.tools.shared.context import AnalysisContext
        
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        
        ctx.update_filter(
            part_number="PRODUCT-A",
            station_name="ST-01",
            test_operation="FCT"
        )
        
        ctx.shift_topic(part_number="PRODUCT-B")
        
        memory = ctx.filter
        assert memory.part_number == "PRODUCT-B"
        assert memory.station_name is None  # Cleared
        assert memory.test_operation is None  # Cleared


class TestFilterMemory:
    """Tests for FilterMemory field tracking."""
    
    def test_filter_memory_timestamps(self):
        """FilterMemory should track when fields were set."""
        from pywats_agent.tools.shared.context import FilterMemory
        
        memory = FilterMemory()
        memory = memory.update(part_number="TEST-001")
        
        age = memory.get_age("part_number")
        assert age is not None
        assert age.total_seconds() < 1  # Just set
    
    def test_clear_stale_fields(self):
        """clear_stale_fields should remove old entries."""
        from pywats_agent.tools.shared.context import FilterMemory
        
        memory = FilterMemory()
        memory = memory.update(part_number="TEST-001")
        
        # Fake old timestamp
        memory._field_timestamps["part_number"] = datetime.now() - timedelta(minutes=10)
        
        cleared = memory.clear_stale_fields(max_age=timedelta(minutes=5))
        
        assert cleared.part_number is None
    
    def test_to_dict_excludes_none_values(self):
        """to_dict should only include non-None values."""
        from pywats_agent.tools.shared.context import FilterMemory
        
        memory = FilterMemory()
        memory = memory.update(part_number="TEST", station_name="ST-01")
        
        result = memory.to_dict()
        
        assert "part_number" in result
        assert "station_name" in result
        assert "revision" not in result  # Was None
    
    def test_describe_provides_human_readable(self):
        """describe should return human-readable context summary."""
        from pywats_agent.tools.shared.context import FilterMemory
        
        memory = FilterMemory()
        memory = memory.update(
            part_number="WIDGET-001",
            test_operation="FCT"
        )
        
        desc = memory.describe()
        
        assert "WIDGET-001" in desc
        assert "FCT" in desc
    
    def test_has_product_context(self):
        """has_product_context should detect product filters."""
        from pywats_agent.tools.shared.context import FilterMemory
        
        memory = FilterMemory()
        assert not memory.has_product_context()
        
        memory = memory.update(part_number="TEST")
        assert memory.has_product_context()
    
    def test_has_process_context(self):
        """has_process_context should detect process filters."""
        from pywats_agent.tools.shared.context import FilterMemory
        
        memory = FilterMemory()
        assert not memory.has_process_context()
        
        memory = memory.update(test_operation="FCT")
        assert memory.has_process_context()


class TestSessionTypeDetermination:
    """Tests for session type selection logic."""
    
    def test_trend_session_for_temporal_analysis(self):
        """TREND type should be used for time-series analysis."""
        from pywats_agent.tools.shared.session import SessionType
        
        assert SessionType.TREND.value == "trend"
    
    def test_deviation_session_for_dimension_analysis(self):
        """DEVIATION type should be used for dimensional analysis."""
        from pywats_agent.tools.shared.session import SessionType
        
        assert SessionType.DEVIATION.value == "deviation"
    
    def test_general_session_for_general_queries(self):
        """GENERAL type should be available for general queries."""
        from pywats_agent.tools.shared.session import SessionType
        
        assert SessionType.GENERAL.value == "general"


class TestIntegration:
    """Integration tests for session + context workflow."""
    
    def test_context_informs_session_creation(self):
        """Context should inform session filter params."""
        from pywats_agent.tools.shared.context import AnalysisContext
        from pywats_agent.tools.shared.session import SessionManager, SessionType
        
        # Setup context
        AnalysisContext.reset_instance()
        ctx = AnalysisContext.get_instance()
        ctx.update_filter(part_number="WIDGET-001", days=30)
        
        effective, _ = ctx.get_effective_filter()
        
        # Create session with context
        SessionManager.reset_instance()
        manager = SessionManager.get_instance()
        
        session = manager.create_session(
            session_type=SessionType.TREND,
            filter_params=effective,
            yield_data=[],
        )
        
        assert session.filter_params["part_number"] == "WIDGET-001"
        assert session.filter_params["days"] == 30
    
    def test_session_summary_with_matrices(self):
        """Session with data should have computed matrices."""
        from pywats_agent.tools.shared.session import SessionManager, SessionType
        
        # Mock yield data
        mock_data = [
            Mock(period="2024-01", fpy=95.0, unit_count=100, fp_count=95),
            Mock(period="2024-02", fpy=93.5, unit_count=120, fp_count=112),
        ]
        
        SessionManager.reset_instance()
        manager = SessionManager.get_instance()
        
        session = manager.create_session(
            session_type=SessionType.TREND,
            filter_params={"part_number": "TEST"},
            yield_data=mock_data,
        )
        
        # Temporal matrix should be lazily built
        matrix = session.temporal_matrix
        assert matrix is not None
        assert len(matrix.periods) == 2
    
    def test_session_period_detail_drill_down(self):
        """Session should support drill-down by period."""
        from pywats_agent.tools.shared.session import SessionManager, SessionType
        
        mock_data = [
            Mock(period="2024-01", fpy=95.0, unit_count=100, fp_count=95),
            Mock(period="2024-02", fpy=93.5, unit_count=120, fp_count=112),
        ]
        
        SessionManager.reset_instance()
        manager = SessionManager.get_instance()
        
        session = manager.create_session(
            session_type=SessionType.TREND,
            filter_params={},
            yield_data=mock_data,
        )
        
        detail = session.get_period_detail("2024-01")
        assert detail is not None
        assert detail["period"] == "2024-01"
        assert detail["yield"] == 95.0
    
    def test_session_compare_periods(self):
        """Session should support comparing two periods."""
        from pywats_agent.tools.shared.session import SessionManager, SessionType
        
        mock_data = [
            Mock(period="2024-01", fpy=95.0, unit_count=100, fp_count=95),
            Mock(period="2024-02", fpy=93.5, unit_count=120, fp_count=112),
        ]
        
        SessionManager.reset_instance()
        manager = SessionManager.get_instance()
        
        session = manager.create_session(
            session_type=SessionType.TREND,
            filter_params={},
            yield_data=mock_data,
        )
        
        comparison = session.compare_periods("2024-01", "2024-02")
        assert "yield_change" in comparison
        assert comparison["yield_change"] == pytest.approx(-1.5, abs=0.1)


class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""
    
    def test_get_session_manager_function(self):
        """get_session_manager should return singleton."""
        from pywats_agent.tools.shared.session import get_session_manager, SessionManager
        
        manager = get_session_manager()
        assert isinstance(manager, SessionManager)
        assert manager is SessionManager.get_instance()
    
    def test_create_trend_session_function(self):
        """create_trend_session should create TREND type session."""
        from pywats_agent.tools.shared.session import (
            create_trend_session, SessionType, SessionManager
        )
        
        SessionManager.reset_instance()
        session = create_trend_session(
            filter_params={"part_number": "TEST"},
            yield_data=[]
        )
        
        assert session.session_type == SessionType.TREND
    
    def test_create_deviation_session_function(self):
        """create_deviation_session should create DEVIATION type session."""
        from pywats_agent.tools.shared.session import (
            create_deviation_session, SessionType, SessionManager
        )
        
        SessionManager.reset_instance()
        session = create_deviation_session(
            filter_params={"dimensions": "stationName"},
            yield_data=[]
        )
        
        assert session.session_type == SessionType.DEVIATION
    
    def test_get_context_function(self):
        """get_context should return singleton context."""
        from pywats_agent.tools.shared.context import get_context, AnalysisContext
        
        ctx = get_context()
        assert isinstance(ctx, AnalysisContext)
        assert ctx is AnalysisContext.get_instance()
