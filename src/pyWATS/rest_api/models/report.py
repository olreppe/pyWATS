"""
Report Models

Models for report-related endpoints.
"""

from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

from .common import PublicWatsFilter


class ReportHeader(BaseModel):
    """Report header model for OData queries."""
    
    uuid: Optional[UUID] = None
    serial_number: Optional[str] = Field(None, alias="serialNumber")
    part_number: Optional[str] = Field(None, alias="partNumber")
    revision: Optional[str] = None
    batch_number: Optional[str] = Field(None, alias="batchNumber")
    station_name: Optional[str] = Field(None, alias="stationName")
    test_operation: Optional[str] = Field(None, alias="testOperation")
    status: Optional[str] = None
    start: Optional[datetime] = None
    timestamp: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""
        allow_population_by_field_name = True


class InsertReportResult(BaseModel):
    """Result model for report insertion operations."""
    
    success: Optional[bool] = None
    report_id: Optional[UUID] = Field(None, alias="reportId")
    message: Optional[str] = None
    errors: Optional[List[str]] = []

    class Config:
        """Pydantic configuration."""
        allow_population_by_field_name = True


class UUTResult(BaseModel):
    """UUT result model for report queries."""
    
    # This would contain the specific fields from the UUT result
    # Based on the API documentation, this appears to be a complex model
    # that would need more detailed specification
    id: Optional[UUID] = None
    serial_number: Optional[str] = Field(None, alias="serialNumber")
    part_number: Optional[str] = Field(None, alias="partNumber")
    # Additional fields would be added based on actual API response structure

    class Config:
        """Pydantic configuration."""
        allow_population_by_field_name = True