"""
Report Base Classes
-
-
-
-
"""
from report.common_types import *

from .report_info import ReportInfo
from .misc_info import MiscInfo
from .additional_data import AdditionalData, AdditionalDataProperty
from .binary_data import BinaryData
from .asset import Asset, AssetStats
from .chart import Chart
from .sub_unit import SubUnit

class ReportStatus(Enum):
    """
    P = Passed
    F = Failed
    S = Skipped
    * Consider replacing with Eunm
    """
    Passed = 'P'
    Failed = 'F'
    Skipped = 'S'

class Report(BaseModel):
    """
    Class: Report
    Purpose: Base class for UUTReport and UURReport.
    """
    id: UUID  = Field(default_factory=uuid4, 
                      description="A UUID identifying the report. Submitting a report witn an existing id will overwrite the existing report. Generates new guid when UUTReport object is created.")
    type: str = Field(default="T", max_length=1, min_length=1, pattern='^[TR]$',
                      description="The type of report. 'T'=TestReport(UUT) 'R'=RepairReport(UUR)")
    pn: str   = Field(..., max_length=100, min_length=1,
                      description="The part number of the unit tested or repaired.")
    sn: str   = Field(..., max_length=100, min_length=1, description="The serial number of the unit tested or repaired.")
    rev: str  = Field(..., max_length=100, min_length=1, description="The revision of the unit(part number) tested or repaired.")
 
    process_code: int = Field(..., deserialization_alias="processCode", serialization_alias="processCode")
    
    #info: ReportInfo | None = None
    info: Optional[ReportInfo] = None

    # Report result
    result: str = Field(default="P", max_length=1, min_length=1, pattern='^[PFDET]$')
    
    # Station info
    station_name: str = Field(..., max_length=100, min_length=1, deserialization_alias="machineName", serialization_alias="machineName")
    location: str = Field(..., max_length=100, min_length=1)
    purpose: str = Field(..., max_length=100, min_length=1)

    start: datetime = Field(default_factory=lambda: datetime.now().astimezone(), examples=["2019-09-12T12:26:16.977+01:00"])
    # Do not use the UTC-time
    start_utc: Optional[datetime] = Field(default=None, examples=['2019-09-12T12:26:16.977Z'], deserialization_alias="startUTC", serialization_alias="startUTC", exclude=True)
   
    # Miscelaneous information
    misc_infos: Optional[list[MiscInfo]] = Field(default_factory=list, deserialization_alias="miscInfos",serialization_alias="miscInfos")
    def add_misc_info(self, description: str, value: Any) -> MiscInfo:
        str_val = str(value)
        mi = MiscInfo(description=description, string_value=str_val)
        self.misc_infos.append(mi)
        return mi

    # -------------------------------------------------------------------------
    # SubUnits
    sub_units: Optional[list[SubUnit]] = Field(default_factory=list, deserialization_alias="subUnits",serialization_alias="subUnits")
    def add_sub_unit(self, part_type:str, sn:str, pn:str, rev:str) -> SubUnit:
        su = SubUnit(partType=part_type, sn=sn, pn=pn, rev=rev)
        self.sub_units.append(su)
        return su

    # -------------------------------------------------------------------------
    # Assets
    assets: Optional[list[Asset]] = Field(default_factory=list)
    asset_stats: Optional[list[AssetStats]] = Field(default=None, exclude=True, deserialization_alias="assetStats", serialization_alias="assetStats")
    def add_asset(self, sn:str, usage_count:int) -> Asset:
        asset = Asset(assetSN=sn, usage_count=usage_count)
        self.assets.append(asset)
        return asset

    # -------------------------------------------------------------------------
    # NB: NOT IMPLEMENTED!
    # BiunaryData
    binary_data: Optional[list[BinaryData]] = Field(default_factory=list, deserialization_alias="binaryData", serialization_alias="binaryData")
    # AdditionalData
    additional_data: Optional[list[Optional[AdditionalData]]]= Field(default_factory=list, deserialization_alias="additionalData", serialization_alias="additionalData")

    def add_additional_data(self, props: List[AdditionalDataProperty]) -> AdditionalData:
        ad = AdditionalData()
        ad.props = props
        self.additional_data.append(ad)
        return ad
   
    def add_additional_data(self, json_dict: dict) -> List[AdditionalData]:
        self.additional_data = [AdditionalDataProperty.from_dict(name, data) for name, data in json_dict.items()]
        return self.additional_data

    # Output only properties
    origin:       Optional[str] = Field(default=None, max_length=100, min_length=0,exclude=True)
    product_name: Optional[str] = Field(default=None, max_length=100, min_length=0,exclude=True, deserialization_alias="productName", serialization_alias="productName")
    process_name: Optional[str] = Field(default=None, max_length=100, min_length=0,exclude=True, deserialization_alias="processName", serialization_alias="processName")

    # -------------------------------------------------------------------
    # Model validator
    # Inject defaults for missing requirements when deserializing - to support legacy reports
    @model_validator(mode="before")
    @classmethod
    def replace_none_during_deserialization(cls, data, info):
        # Check if deserialization context is set
        if info.context.get("is_deserialization", False):
            for key in ["pn", "sn", "rev", "machineName", "location", "purpose"]:
                if data.get(key) in (None, ""):
                    data[key] = def_MissingString
        return data

    # -------------------------------------------------------------------
    # Model Config
    # Make sure json is deserialized to alias names
    model_config = {
        "allow_populate_by_name": True  # Allows deserialization using alias}
    }