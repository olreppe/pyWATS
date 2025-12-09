"""App domain models.

Statistics and KPI data models.
"""
from typing import Optional
from pydantic import Field

from ...shared.base_model import PyWATSModel


class YieldData(PyWATSModel):
    """
    Represents yield statistics data.

    Attributes:
        part_number: Product part number
        revision: Product revision
        product_name: Product name
        product_group: Product group
        station_name: Test station name
        test_operation: Test operation
        period: Time period
        unit_count: Total unit count
        fp_count: First pass count
        sp_count: Second pass count
        tp_count: Third pass count
        lp_count: Last pass count
        fpy: First pass yield
        spy: Second pass yield
        tpy: Third pass yield
        lpy: Last pass yield
    """

    part_number: Optional[str] = Field(default=None, alias="partNumber")
    revision: Optional[str] = Field(default=None, alias="revision")
    product_name: Optional[str] = Field(default=None, alias="productName")
    product_group: Optional[str] = Field(default=None, alias="productGroup")
    station_name: Optional[str] = Field(default=None, alias="stationName")
    test_operation: Optional[str] = Field(default=None, alias="testOperation")
    period: Optional[str] = Field(default=None, alias="period")
    unit_count: Optional[int] = Field(default=None, alias="unitCount")
    fp_count: Optional[int] = Field(default=None, alias="fpCount")
    sp_count: Optional[int] = Field(default=None, alias="spCount")
    tp_count: Optional[int] = Field(default=None, alias="tpCount")
    lp_count: Optional[int] = Field(default=None, alias="lpCount")
    fpy: Optional[float] = Field(default=None, alias="fpy")
    spy: Optional[float] = Field(default=None, alias="spy")
    tpy: Optional[float] = Field(default=None, alias="tpy")
    lpy: Optional[float] = Field(default=None, alias="lpy")


class ProcessInfo(PyWATSModel):
    """
    Represents process/test operation information.

    Attributes:
        process_code: Process code
        process_name: Process name
        process_index: Process order index
    """

    process_code: Optional[int] = Field(default=None, alias="processCode")
    process_name: Optional[str] = Field(default=None, alias="processName")
    process_index: Optional[int] = Field(default=None, alias="processIndex")


class LevelInfo(PyWATSModel):
    """
    Represents production level information.

    Attributes:
        level_id: Level ID
        level_name: Level name
    """

    level_id: Optional[int] = Field(default=None, alias="levelId")
    level_name: Optional[str] = Field(default=None, alias="levelName")


class ProductGroup(PyWATSModel):
    """
    Represents a product group.

    Attributes:
        product_group_id: Product group ID
        product_group_name: Product group name
    """

    product_group_id: Optional[int] = Field(
        default=None, alias="productGroupId"
    )
    product_group_name: Optional[str] = Field(
        default=None, alias="productGroupName"
    )
