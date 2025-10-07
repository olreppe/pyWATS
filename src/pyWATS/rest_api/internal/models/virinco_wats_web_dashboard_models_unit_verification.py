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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsUnitVerification")



@_attrs_define
class VirincoWATSWebDashboardModelsUnitVerification:
    """ 
        Attributes:
            process_id (Union[Unset, int]):
            process_name (Union[Unset, str]):
            process_index (Union[Unset, int]):
            status (Union[Unset, str]):
            start_utc (Union[Unset, datetime.datetime]):
            station_name (Union[Unset, str]):
            total_count (Union[Unset, int]):
            fail_count (Union[Unset, int]):
            repair_count (Union[Unset, int]):
     """

    process_id: Union[Unset, int] = UNSET
    process_name: Union[Unset, str] = UNSET
    process_index: Union[Unset, int] = UNSET
    status: Union[Unset, str] = UNSET
    start_utc: Union[Unset, datetime.datetime] = UNSET
    station_name: Union[Unset, str] = UNSET
    total_count: Union[Unset, int] = UNSET
    fail_count: Union[Unset, int] = UNSET
    repair_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        process_id = self.process_id

        process_name = self.process_name

        process_index = self.process_index

        status = self.status

        start_utc: Union[Unset, str] = UNSET
        if not isinstance(self.start_utc, Unset):
            start_utc = self.start_utc.isoformat()

        station_name = self.station_name

        total_count = self.total_count

        fail_count = self.fail_count

        repair_count = self.repair_count


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if process_id is not UNSET:
            field_dict["processID"] = process_id
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
        if fail_count is not UNSET:
            field_dict["failCount"] = fail_count
        if repair_count is not UNSET:
            field_dict["repairCount"] = repair_count

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_id = d.pop("processID", UNSET)

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

        fail_count = d.pop("failCount", UNSET)

        repair_count = d.pop("repairCount", UNSET)

        virinco_wats_web_dashboard_models_unit_verification = cls(
            process_id=process_id,
            process_name=process_name,
            process_index=process_index,
            status=status,
            start_utc=start_utc,
            station_name=station_name,
            total_count=total_count,
            fail_count=fail_count,
            repair_count=repair_count,
        )


        virinco_wats_web_dashboard_models_unit_verification.additional_properties = d
        return virinco_wats_web_dashboard_models_unit_verification

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
