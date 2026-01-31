"""
Chart Classes - v3 Implementation

Support for chart visualization in steps.
"""
from __future__ import annotations

from typing import Optional, List, Literal

from .common_types import (
    WATSBase,
    Field,
    ChartType,
)


class ChartSeries(WATSBase):
    """
    A single data series in a chart.
    
    Contains the X and Y data points plus metadata about the series.
    """
    
    # Data type identifier
    data_type: str = Field(
        ...,
        max_length=50,
        validation_alias="dataType",
        serialization_alias="dataType",
        description="Type of data in this series."
    )
    
    # Series name
    name: str = Field(
        ...,
        max_length=100,
        min_length=1,
        description="Name of the data series."
    )
    
    # X-axis data points
    x_data: List[float] = Field(
        ...,
        validation_alias="xData",
        serialization_alias="xData",
        description="X-axis values."
    )
    
    # Y-axis data points
    y_data: List[float] = Field(
        ...,
        validation_alias="yData",
        serialization_alias="yData",
        description="Y-axis values."
    )


class Chart(WATSBase):
    """
    Chart configuration and data for visualization.
    
    Charts can be attached to steps to provide visual representation
    of measurement data like waveforms, histograms, etc.
    """
    
    # Chart type
    chart_type: ChartType = Field(
        default=ChartType.LineChart,
        validation_alias="chartType",
        serialization_alias="chartType",
        description="Type of chart visualization."
    )
    
    # Chart label/title
    label: str = Field(
        default="Chart",
        max_length=100,
        description="Chart title/label."
    )
    
    # X-axis configuration
    x_label: str = Field(
        default="X",
        max_length=100,
        validation_alias="xLabel",
        serialization_alias="xLabel",
        description="X-axis label."
    )
    
    x_unit: str = Field(
        default="",
        max_length=50,
        validation_alias="xUnit",
        serialization_alias="xUnit",
        description="X-axis unit."
    )
    
    # Y-axis configuration
    y_label: str = Field(
        default="Y",
        max_length=100,
        validation_alias="yLabel",
        serialization_alias="yLabel",
        description="Y-axis label."
    )
    
    y_unit: str = Field(
        default="",
        max_length=50,
        validation_alias="yUnit",
        serialization_alias="yUnit",
        description="Y-axis unit."
    )
    
    # Data series
    series: List[ChartSeries] = Field(
        default_factory=list,
        description="List of data series in the chart."
    )
    
    def add_series(
        self,
        name: str,
        x_data: List[float],
        y_data: List[float],
        data_type: str = "float"
    ) -> ChartSeries:
        """
        Add a data series to the chart.
        
        Args:
            name: Name of the series
            x_data: X-axis values
            y_data: Y-axis values  
            data_type: Type identifier for the data
            
        Returns:
            The created ChartSeries object
        """
        series = ChartSeries(
            data_type=data_type,
            name=name,
            x_data=x_data,
            y_data=y_data
        )
        self.series.append(series)
        return series
