"""
TDM Models

Data models for TDM operations, providing structures for statistical analysis,
trend data, and analytical results.
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field
from enum import IntEnum


class TrendDataPoint(BaseModel):
    """Single data point in a trend analysis."""
    timestamp: datetime
    value: Union[int, float]
    count: Optional[int] = None
    status: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True


class TrendData(BaseModel):
    """Trend analysis data model."""
    part_number: str = Field(..., alias="partNumber")
    operation_key: str = Field(..., alias="operationKey")
    data_points: List[TrendDataPoint] = Field([], alias="dataPoints")
    total_count: int = Field(0, alias="totalCount")
    start_date: Optional[datetime] = Field(None, alias="startDate")
    end_date: Optional[datetime] = Field(None, alias="endDate")
    
    class Config:
        allow_population_by_field_name = True


class LastResultData(BaseModel):
    """Last test result data model."""
    part_number: str = Field(..., alias="partNumber")
    operation_key: str = Field(..., alias="operationKey")
    result: Optional[str] = None
    timestamp: Optional[datetime] = None
    value: Optional[Union[int, float]] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True


class AlertLevels(BaseModel):
    """Alert level configuration model."""
    part_number: str = Field(..., alias="partNumber")
    warning_level: float = Field(..., alias="warningLevel")
    critical_level: float = Field(..., alias="criticalLevel")
    total_count: int = Field(..., alias="totalCount")
    last_count: int = Field(..., alias="lastCount")
    
    class Config:
        allow_population_by_field_name = True


class MeasurementData(BaseModel):
    """Measurement data point model."""
    measurement_name: str = Field(..., alias="measurementName")
    value: Union[int, float]
    unit: Optional[str] = None
    timestamp: datetime
    serial_number: Optional[str] = Field(None, alias="serialNumber")
    part_number: Optional[str] = Field(None, alias="partNumber")
    
    class Config:
        allow_population_by_field_name = True


class AggregatedMeasurement(BaseModel):
    """Aggregated measurement statistics model."""
    measurement_name: str = Field(..., alias="measurementName")
    count: int = 0
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    average: Optional[float] = None
    median: Optional[float] = None
    std_deviation: Optional[float] = Field(None, alias="stdDeviation")
    unit: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True


class StepStatus(BaseModel):
    """Step status information model."""
    step_name: str = Field(..., alias="stepName")
    passed_count: int = Field(0, alias="passedCount")
    failed_count: int = Field(0, alias="failedCount")
    total_count: int = Field(0, alias="totalCount")
    pass_rate: float = Field(0.0, alias="passRate")
    
    class Config:
        allow_population_by_field_name = True


class TopFailedStep(BaseModel):
    """Top failed step model."""
    step_name: str = Field(..., alias="stepName")
    failure_count: int = Field(..., alias="failureCount")
    total_count: int = Field(..., alias="totalCount")
    failure_rate: float = Field(..., alias="failureRate")
    part_number: Optional[str] = Field(None, alias="partNumber")
    process_code: Optional[str] = Field(None, alias="processCode")
    
    class Config:
        allow_population_by_field_name = True


class YieldData(BaseModel):
    """Yield analysis data model."""
    part_number: Optional[str] = Field(None, alias="partNumber")
    process_code: Optional[str] = Field(None, alias="processCode")
    total_units: int = Field(0, alias="totalUnits")
    passed_units: int = Field(0, alias="passedUnits")
    failed_units: int = Field(0, alias="failedUnits")
    yield_percentage: float = Field(0.0, alias="yieldPercentage")
    date_range: Optional[str] = Field(None, alias="dateRange")
    
    class Config:
        allow_population_by_field_name = True


class StatisticsFilter(BaseModel):
    """Filter for statistics queries."""
    part_number: Optional[str] = Field(None, alias="partNumber")
    process_code: Optional[str] = Field(None, alias="processCode")
    start_date: Optional[datetime] = Field(None, alias="startDate")
    end_date: Optional[datetime] = Field(None, alias="endDate")
    days: Optional[int] = None
    station_name: Optional[str] = Field(None, alias="stationName")
    operator: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True


class AnalyticsResult(BaseModel):
    """Generic analytics result model."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        allow_population_by_field_name = True