from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMiscInfo")



@_attrs_define
class VirincoWATSWebDashboardModelsMiscInfo:
    """ 
        Attributes:
            sn (Union[Unset, str]):
            process_code (Union[Unset, int]):
            report_id (Union[Unset, int]):
            misc_description (Union[Unset, str]):
            misc_value (Union[Unset, str]):
            guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            report_type (Union[Unset, str]):
     """

    sn: Union[Unset, str] = UNSET
    process_code: Union[Unset, int] = UNSET
    report_id: Union[Unset, int] = UNSET
    misc_description: Union[Unset, str] = UNSET
    misc_value: Union[Unset, str] = UNSET
    guid: Union[Unset, UUID] = UNSET
    report_type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        sn = self.sn

        process_code = self.process_code

        report_id = self.report_id

        misc_description = self.misc_description

        misc_value = self.misc_value

        guid: Union[Unset, str] = UNSET
        if not isinstance(self.guid, Unset):
            guid = str(self.guid)

        report_type = self.report_type


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if sn is not UNSET:
            field_dict["SN"] = sn
        if process_code is not UNSET:
            field_dict["ProcessCode"] = process_code
        if report_id is not UNSET:
            field_dict["ReportId"] = report_id
        if misc_description is not UNSET:
            field_dict["MiscDescription"] = misc_description
        if misc_value is not UNSET:
            field_dict["MiscValue"] = misc_value
        if guid is not UNSET:
            field_dict["GUID"] = guid
        if report_type is not UNSET:
            field_dict["ReportType"] = report_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sn = d.pop("SN", UNSET)

        process_code = d.pop("ProcessCode", UNSET)

        report_id = d.pop("ReportId", UNSET)

        misc_description = d.pop("MiscDescription", UNSET)

        misc_value = d.pop("MiscValue", UNSET)

        _guid = d.pop("GUID", UNSET)
        guid: Union[Unset, UUID]
        if isinstance(_guid,  Unset):
            guid = UNSET
        else:
            guid = UUID(_guid)




        report_type = d.pop("ReportType", UNSET)

        virinco_wats_web_dashboard_models_misc_info = cls(
            sn=sn,
            process_code=process_code,
            report_id=report_id,
            misc_description=misc_description,
            misc_value=misc_value,
            guid=guid,
            report_type=report_type,
        )


        virinco_wats_web_dashboard_models_misc_info.additional_properties = d
        return virinco_wats_web_dashboard_models_misc_info

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
