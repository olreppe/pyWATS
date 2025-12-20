"""
Tests for the visualization payload system.

The viz_payload is an OPTIONAL sidecar that:
- Bypasses LLM context (no token cost)
- Provides explicit chart hints when UI can't infer
- Is NOT needed for simple cases (UI infers from data)
"""

import pytest
from datetime import datetime


# =============================================================================
# Import Tests
# =============================================================================

class TestImports:
    """Test that all visualization types can be imported."""
    
    def test_import_chart_types(self):
        from pywats_agent import ChartType
        assert ChartType.LINE == "line"
        assert ChartType.BAR == "bar"
        assert ChartType.PARETO == "pareto"
        assert ChartType.CONTROL == "control"
    
    def test_import_data_models(self):
        from pywats_agent import (
            DataSeries,
            ReferenceLine,
            Annotation,
            ChartPayload,
            TableColumn,
            TablePayload,
            KPIPayload,
            DrillDownOption,
            VisualizationPayload,
        )
        # All imports should work
        assert DataSeries is not None
        assert VisualizationPayload is not None
    
    def test_import_builder(self):
        from pywats_agent import VizBuilder
        assert hasattr(VizBuilder, 'line_chart')
        assert hasattr(VizBuilder, 'bar_chart')
        assert hasattr(VizBuilder, 'pareto_chart')
    
    def test_import_helpers(self):
        from pywats_agent import merge_visualizations, empty_visualization
        assert callable(merge_visualizations)
        assert callable(empty_visualization)


# =============================================================================
# Data Model Tests
# =============================================================================

class TestDataSeries:
    """Test DataSeries model."""
    
    def test_basic_series(self):
        from pywats_agent import DataSeries
        
        series = DataSeries(name="Yield", values=[94.5, 95.2, 93.8])
        assert series.name == "Yield"
        assert series.values == [94.5, 95.2, 93.8]
        assert series.color is None
    
    def test_series_with_options(self):
        from pywats_agent import DataSeries
        
        series = DataSeries(
            name="Target",
            values=[95, 95, 95],
            color="green",
            type="line",
            y_axis="right"
        )
        assert series.color == "green"
        assert series.type == "line"
        assert series.y_axis == "right"
    
    def test_scatter_series(self):
        from pywats_agent import DataSeries
        
        series = DataSeries(
            name="Correlation",
            values=[1, 2, 3],
            x_values=[10, 20, 30],
            sizes=[5, 10, 15]
        )
        assert series.x_values == [10, 20, 30]
        assert series.sizes == [5, 10, 15]


class TestReferenceLine:
    """Test ReferenceLine model."""
    
    def test_basic_reference_line(self):
        from pywats_agent import ReferenceLine
        
        line = ReferenceLine(value=95, label="Target")
        assert line.value == 95
        assert line.label == "Target"
        assert line.style == "dashed"  # default
    
    def test_styled_reference_line(self):
        from pywats_agent import ReferenceLine
        
        line = ReferenceLine(
            value=90,
            label="Lower Limit",
            color="red",
            style="solid"
        )
        assert line.color == "red"
        assert line.style == "solid"


class TestChartPayload:
    """Test ChartPayload model."""
    
    def test_basic_chart(self):
        from pywats_agent import ChartPayload, ChartType, DataSeries
        
        chart = ChartPayload(
            chart_type=ChartType.LINE,
            title="Yield Trend",
            labels=["Mon", "Tue", "Wed"],
            series=[DataSeries(name="Yield", values=[94, 95, 93])]
        )
        assert chart.chart_type == ChartType.LINE
        assert chart.title == "Yield Trend"
        assert len(chart.series) == 1
    
    def test_control_chart(self):
        from pywats_agent import ChartPayload, ChartType, DataSeries
        
        chart = ChartPayload(
            chart_type=ChartType.CONTROL,
            title="SPC Chart",
            labels=["1", "2", "3"],
            series=[DataSeries(name="Value", values=[10, 11, 9])],
            ucl=12,
            lcl=8,
            target=10
        )
        assert chart.ucl == 12
        assert chart.lcl == 8
        assert chart.target == 10


class TestTablePayload:
    """Test TablePayload model."""
    
    def test_basic_table(self):
        from pywats_agent import TablePayload, TableColumn
        
        table = TablePayload(
            title="Stations",
            columns=[
                TableColumn(key="name", label="Station Name"),
                TableColumn(key="yield", label="Yield %", type="percent"),
            ],
            rows=[
                {"name": "Station A", "yield": 94.5},
                {"name": "Station B", "yield": 96.2},
            ]
        )
        assert table.title == "Stations"
        assert len(table.columns) == 2
        assert len(table.rows) == 2
        assert table.exportable == True  # default


class TestKPIPayload:
    """Test KPIPayload model."""
    
    def test_basic_kpi(self):
        from pywats_agent import KPIPayload
        
        kpi = KPIPayload(
            title="Overall Yield",
            value=94.5,
            unit="%"
        )
        assert kpi.title == "Overall Yield"
        assert kpi.value == 94.5
        assert kpi.unit == "%"
    
    def test_kpi_with_trend(self):
        from pywats_agent import KPIPayload
        
        kpi = KPIPayload(
            title="Weekly Yield",
            value=94.5,
            trend="down",
            trend_value=-1.2,
            trend_period="vs last week",
            trend_is_good=False
        )
        assert kpi.trend == "down"
        assert kpi.trend_is_good == False
    
    def test_kpi_with_thresholds(self):
        from pywats_agent import KPIPayload
        
        kpi = KPIPayload(
            title="Defect Rate",
            value=2.5,
            thresholds={"good": 1, "warn": 3},
            invert_thresholds=True  # lower is better
        )
        assert kpi.thresholds == {"good": 1, "warn": 3}
        assert kpi.invert_thresholds == True


# =============================================================================
# VizBuilder Tests
# =============================================================================

class TestVizBuilderLineChart:
    """Test VizBuilder.line_chart()"""
    
    def test_simple_line_chart(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.line_chart(
            title="Yield Trend",
            labels=["Mon", "Tue", "Wed"],
            series=[{"name": "Yield", "values": [94, 95, 93]}]
        )
        
        assert payload.viz_type == "chart"
        assert payload.chart is not None
        assert payload.chart.chart_type == "line"
        assert payload.chart.title == "Yield Trend"
        assert len(payload.chart.series) == 1
    
    def test_line_chart_with_reference(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.line_chart(
            title="Yield vs Target",
            labels=["Mon", "Tue", "Wed"],
            series=[{"name": "Yield", "values": [94, 95, 93]}],
            reference_lines=[{"value": 95, "label": "Target", "color": "green"}]
        )
        
        assert len(payload.chart.reference_lines) == 1
        assert payload.chart.reference_lines[0].value == 95


class TestVizBuilderBarChart:
    """Test VizBuilder.bar_chart()"""
    
    def test_simple_bar_chart(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.bar_chart(
            title="Yield by Station",
            labels=["Station A", "Station B", "Station C"],
            series=[{"name": "Yield", "values": [94, 96, 92]}]
        )
        
        assert payload.chart.chart_type == "bar"
    
    def test_horizontal_bar_chart(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.bar_chart(
            title="Yield by Station",
            labels=["Station A", "Station B"],
            series=[{"name": "Yield", "values": [94, 96]}],
            horizontal=True
        )
        
        assert payload.chart.chart_type == "horizontal_bar"
    
    def test_stacked_bar_chart(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.bar_chart(
            title="Results by Station",
            labels=["Station A", "Station B"],
            series=[
                {"name": "Passed", "values": [90, 95]},
                {"name": "Failed", "values": [10, 5]},
            ],
            stacked=True
        )
        
        assert payload.chart.chart_type == "stacked_bar"


class TestVizBuilderParetoChart:
    """Test VizBuilder.pareto_chart()"""
    
    def test_pareto_chart_sorts_descending(self):
        from pywats_agent import VizBuilder
        
        # Input not sorted
        payload = VizBuilder.pareto_chart(
            title="Failure Pareto",
            labels=["Error A", "Error B", "Error C"],
            values=[10, 50, 20]  # Not sorted
        )
        
        # Should be sorted descending
        assert payload.chart.labels == ["Error B", "Error C", "Error A"]
        assert payload.chart.series[0].values == [50, 20, 10]
    
    def test_pareto_chart_has_cumulative(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.pareto_chart(
            title="Failure Pareto",
            labels=["A", "B", "C"],
            values=[50, 30, 20]  # Already sorted, total=100
        )
        
        # Should have cumulative line
        assert len(payload.chart.series) == 2
        assert payload.chart.series[1].name == "Cumulative %"
        # Cumulative: 50%, 80%, 100%
        assert payload.chart.series[1].values == [50.0, 80.0, 100.0]


class TestVizBuilderControlChart:
    """Test VizBuilder.control_chart()"""
    
    def test_control_chart_with_limits(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.control_chart(
            title="Process Control",
            labels=["1", "2", "3", "4", "5"],
            values=[10.1, 9.8, 10.5, 9.9, 10.2],
            ucl=11.0,
            lcl=9.0,
            target=10.0
        )
        
        assert payload.chart.chart_type == "control"
        assert payload.chart.ucl == 11.0
        assert payload.chart.lcl == 9.0
        assert payload.chart.target == 10.0
        
        # Should have reference lines
        assert len(payload.chart.reference_lines) == 3


class TestVizBuilderTable:
    """Test VizBuilder.table()"""
    
    def test_simple_table(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.table(
            columns=[
                {"key": "station", "label": "Station"},
                {"key": "yield", "label": "Yield %", "type": "percent"},
            ],
            rows=[
                {"station": "A", "yield": 94.5},
                {"station": "B", "yield": 96.2},
            ],
            title="Station Summary"
        )
        
        assert payload.viz_type == "table"
        assert payload.table is not None
        assert payload.table.title == "Station Summary"
        assert len(payload.table.rows) == 2


class TestVizBuilderKPI:
    """Test VizBuilder.kpi() and kpi_row()"""
    
    def test_single_kpi(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.kpi(
            title="Overall Yield",
            value=94.5,
            unit="%",
            thresholds={"good": 95, "warn": 90},
            trend="down",
            trend_value=-0.5
        )
        
        assert payload.viz_type == "kpi"
        assert payload.kpi.title == "Overall Yield"
        assert payload.kpi.value == 94.5
    
    def test_kpi_row(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.kpi_row([
            {"title": "Yield", "value": 94.5, "unit": "%"},
            {"title": "Volume", "value": 1234, "unit": "units"},
            {"title": "FPY", "value": 88.2, "unit": "%"},
        ])
        
        assert payload.viz_type == "multi"
        assert len(payload.kpis) == 3
        assert payload.layout == "horizontal"


class TestVizBuilderDashboard:
    """Test VizBuilder.dashboard()"""
    
    def test_dashboard_with_kpis_and_chart(self):
        from pywats_agent import VizBuilder, ChartPayload, ChartType, DataSeries
        
        payload = VizBuilder.dashboard(
            kpis=[
                {"title": "Yield", "value": 94.5},
                {"title": "Volume", "value": 1000},
            ],
            charts=[
                ChartPayload(
                    chart_type=ChartType.LINE,
                    title="Trend",
                    labels=["Mon", "Tue"],
                    series=[DataSeries(name="Y", values=[94, 95])]
                )
            ]
        )
        
        assert payload.viz_type == "dashboard"
        assert len(payload.kpis) == 2
        assert len(payload.charts) == 1


class TestVizBuilderDrillDown:
    """Test drill-down functionality."""
    
    def test_add_drill_down(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.bar_chart(
            title="Yield by Station",
            labels=["A", "B"],
            series=[{"name": "Yield", "values": [94, 96]}]
        )
        
        payload = VizBuilder.with_drill_down(payload, [
            {"label": "Analyze Station A", "action": "analyze_yield", "params": {"station": "A"}},
            {"label": "Analyze Station B", "action": "analyze_yield", "params": {"station": "B"}},
        ])
        
        assert len(payload.drill_down_options) == 2
        assert payload.chart.enable_drill_down == True


# =============================================================================
# AgentResult Integration Tests
# =============================================================================

class TestAgentResultWithVisualization:
    """Test AgentResult with viz_payload."""
    
    def test_result_without_viz(self):
        from pywats_agent import AgentResult
        
        result = AgentResult.ok(
            data=[{"station": "A", "yield": 94.5}],
            summary="Yield is 94.5%"
        )
        
        assert result.viz_payload is None
        assert result.has_visualization() == False
    
    def test_result_with_viz(self):
        from pywats_agent import AgentResult, VizBuilder
        
        result = AgentResult.ok(
            data=[{"station": "A", "yield": 94.5}],
            summary="Yield is 94.5%",
            viz_payload=VizBuilder.bar_chart(
                title="Yield",
                labels=["A"],
                series=[{"name": "Yield", "values": [94.5]}]
            )
        )
        
        assert result.viz_payload is not None
        assert result.has_visualization() == True
    
    def test_to_openai_excludes_viz(self):
        """Verify viz_payload is NOT in LLM response."""
        from pywats_agent import AgentResult, VizBuilder
        import json
        
        result = AgentResult.ok(
            summary="Yield is 94.5%",
            viz_payload=VizBuilder.kpi(title="Yield", value=94.5)
        )
        
        llm_response = json.loads(result.to_openai_response())
        
        # viz_payload should NOT be in LLM response
        assert "viz_payload" not in llm_response
        assert llm_response["summary"] == "Yield is 94.5%"
    
    def test_to_ui_includes_viz(self):
        """Verify viz_payload IS in UI response."""
        from pywats_agent import AgentResult, VizBuilder
        
        result = AgentResult.ok(
            summary="Yield is 94.5%",
            viz_payload=VizBuilder.kpi(title="Yield", value=94.5)
        )
        
        ui_response = result.to_ui_response()
        
        # viz_payload SHOULD be in UI response
        assert "viz_payload" in ui_response
        assert ui_response["viz_payload"]["kpi"]["title"] == "Yield"


# =============================================================================
# Merge and Helper Tests
# =============================================================================

class TestMergeVisualizations:
    """Test merge_visualizations helper."""
    
    def test_merge_two_charts(self):
        from pywats_agent import VizBuilder, merge_visualizations
        
        chart1 = VizBuilder.line_chart(
            title="Trend",
            labels=["Mon", "Tue"],
            series=[{"name": "Y", "values": [94, 95]}]
        )
        
        chart2 = VizBuilder.bar_chart(
            title="Comparison",
            labels=["A", "B"],
            series=[{"name": "Y", "values": [94, 96]}]
        )
        
        merged = merge_visualizations(chart1, chart2)
        
        assert merged.viz_type == "dashboard"
        assert len(merged.charts) == 2
    
    def test_merge_mixed_types(self):
        from pywats_agent import VizBuilder, merge_visualizations
        
        kpi = VizBuilder.kpi(title="Yield", value=94.5)
        chart = VizBuilder.line_chart(
            title="Trend",
            labels=["Mon"],
            series=[{"name": "Y", "values": [94]}]
        )
        table = VizBuilder.table(
            columns=[{"key": "a", "label": "A"}],
            rows=[{"a": 1}]
        )
        
        merged = merge_visualizations(kpi, chart, table)
        
        assert len(merged.kpis) == 1
        assert len(merged.charts) == 1
        assert len(merged.tables) == 1


class TestEmptyVisualization:
    """Test empty_visualization helper."""
    
    def test_empty_viz(self):
        from pywats_agent import empty_visualization
        
        viz = empty_visualization()
        
        assert viz.viz_type == "chart"
        assert viz.chart is None
        assert viz.table is None


# =============================================================================
# Serialization Tests
# =============================================================================

class TestVisualizationSerialization:
    """Test that visualizations serialize correctly."""
    
    def test_chart_to_dict(self):
        from pywats_agent import VizBuilder
        
        payload = VizBuilder.line_chart(
            title="Test",
            labels=["A", "B"],
            series=[{"name": "S", "values": [1, 2]}]
        )
        
        data = payload.model_dump()
        
        assert data["viz_type"] == "chart"
        assert data["chart"]["title"] == "Test"
        assert data["chart"]["chart_type"] == "line"
    
    def test_to_json(self):
        from pywats_agent import VizBuilder
        import json
        
        payload = VizBuilder.kpi(title="Yield", value=94.5)
        
        # Should serialize without errors
        json_str = payload.model_dump_json()
        parsed = json.loads(json_str)
        
        assert parsed["kpi"]["title"] == "Yield"
