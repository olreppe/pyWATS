"""
WATS Filter Models

Common filter and request models used across the API.
"""

from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import IntEnum


class DateGrouping(IntEnum):
    """Date grouping enumeration for filters."""
    NONE = 0
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    QUARTERLY = 4
    YEARLY = 5
    AUTO = -1


class PublicWatsFilter(BaseModel):
    """
    Public WATS filter for API requests.
    
    This is the primary filter model used across many endpoints.
    """
    
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True
    )
    
    serial_number: Optional[str] = Field(None, alias="serialNumber")
    part_number: Optional[str] = Field(None, alias="partNumber")
    revision: Optional[str] = None
    batch_number: Optional[str] = Field(None, alias="batchNumber")
    station_name: Optional[str] = Field(None, alias="stationName")
    test_operation: Optional[str] = Field(None, alias="testOperation")
    status: Optional[str] = None
    yield_filter: Optional[int] = Field(None, alias="yield")
    misc_description: Optional[str] = Field(None, alias="miscDescription")
    misc_value: Optional[str] = Field(None, alias="miscValue")
    product_group: Optional[str] = Field(None, alias="productGroup")
    level: Optional[str] = None
    sw_filename: Optional[str] = Field(None, alias="swFilename")
    sw_version: Optional[str] = Field(None, alias="swVersion")
    socket: Optional[str] = None
    date_from: Optional[datetime] = Field(None, alias="dateFrom")
    date_to: Optional[datetime] = Field(None, alias="dateTo")
    date_grouping: Optional[DateGrouping] = Field(None, alias="dateGrouping")
    period_count: Optional[int] = Field(None, alias="periodCount")
    include_current_period: Optional[bool] = Field(None, alias="includeCurrentPeriod")
    max_count: Optional[int] = Field(None, alias="maxCount")
    min_count: Optional[int] = Field(None, alias="minCount")
    top_count: Optional[int] = Field(None, alias="topCount")
    dimensions: Optional[str] = None


class CommonUserSettings(BaseModel):
    """Common user settings response model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    full_name: Optional[str] = Field(None, alias="fullName")
    culture_code: Optional[str] = Field(None, alias="cultureCode")
    email: Optional[str] = None
    roles: Optional[list[str]] = []
    levels: Optional[list[str]] = []
    product_groups: Optional[list[str]] = Field([], alias="productGroups")