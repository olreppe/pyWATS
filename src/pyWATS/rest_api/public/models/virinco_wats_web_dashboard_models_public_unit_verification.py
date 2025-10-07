from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsPublicUnitVerification")



@_attrs_define
class VirincoWATSWebDashboardModelsPublicUnitVerification:
    """ 
        Attributes:
            process_code (Union[Unset, int]): Test operation code.
            process_name (Union[Unset, str]): Test operation name.
            process_index (Union[Unset, int]): Test operation order index.
            status (Union[Unset, str]): Unit test status in this process.
            start_utc (Union[Unset, datetime.datetime]): Test start date and time, or null if
                {Virinco.WATS.Web.Dashboard.Models.PublicUnitVerification.StatusText} is 'Unknown'.
            station_name (Union[Unset, str]): Name of test station.
            total_count (Union[Unset, int]): How many times the unit was tested.
            non_passed_count (Union[Unset, int]): How many times the unit didn't pass the test.
            repair_count (Union[Unset, int]): How many times the unit was repaired.
     """

    process_code: Union[Unset, int] = UNSET
    process_name: Union[Unset, str] = UNSET
    process_index: Union[Unset, int] = UNSET
    status: Union[Unset, str] = UNSET
    start_utc: Union[Unset, datetime.datetime] = UNSET
    station_name: Union[Unset, str] = UNSET
    total_count: Union[Unset, int] = UNSET
    non_passed_count: Union[Unset, int] = UNSET
    repair_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        process_code = self.process_code

        process_name = self.process_name

        process_index = self.process_index

        status = self.status

        start_utc: Union[Unset, str] = UNSET
        if not isinstance(self.start_utc, Unset):
            start_utc = self.start_utc.isoformat()

        station_name = self.station_name

        total_count = self.total_count

        non_passed_count = self.non_passed_count

        repair_count = self.repair_count


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if process_code is not UNSET:
            field_dict["processCode"] = process_code
        if process_name is not UNSET:
            field_dict["processName"] = process_name
        if process_index is not UNSET:
            field_dict["processIndex"] = process_index
        if status is not UNSET:
            field_dict["status"] = status
        if start_utc is not UNSET:
            field_dict["startUtc"] = start_utc
        if station_name is not UNSET:
            field_dict["stationName"] = station_name
        if total_count is not UNSET:
            field_dict["totalCount"] = total_count
        if non_passed_count is not UNSET:
            field_dict["nonPassedCount"] = non_passed_count
        if repair_count is not UNSET:
            field_dict["repairCount"] = repair_count

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_code = d.pop("processCode", UNSET)

        process_name = d.pop("processName", UNSET)

        process_index = d.pop("processIndex", UNSET)

        status = d.pop("status", UNSET)

        _start_utc = d.pop("startUtc", UNSET)
        start_utc: Union[Unset, datetime.datetime]
        if isinstance(_start_utc,  Unset):
            start_utc = UNSET
        else:
            start_utc = isoparse(_start_utc)




        station_name = d.pop("stationName", UNSET)

        total_count = d.pop("totalCount", UNSET)

        non_passed_count = d.pop("nonPassedCount", UNSET)

        repair_count = d.pop("repairCount", UNSET)

        virinco_wats_web_dashboard_models_public_unit_verification = cls(
            process_code=process_code,
            process_name=process_name,
            process_index=process_index,
            status=status,
            start_utc=start_utc,
            station_name=station_name,
            total_count=total_count,
            non_passed_count=non_passed_count,
            repair_count=repair_count,
        )


        virinco_wats_web_dashboard_models_public_unit_verification.additional_properties = d
        return virinco_wats_web_dashboard_models_public_unit_verification

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
