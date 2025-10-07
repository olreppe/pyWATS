from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardControllersApiClientControllerClientSettings")



@_attrs_define
class VirincoWATSWebDashboardControllersApiClientControllerClientSettings:
    """ 
        Attributes:
            name (Union[Unset, str]):
            location (Union[Unset, str]):
            purpose (Union[Unset, str]):
            miscinfo (Union[Unset, str]):
            utcoffset (Union[Unset, str]):
     """

    name: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    miscinfo: Union[Unset, str] = UNSET
    utcoffset: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        location = self.location

        purpose = self.purpose

        miscinfo = self.miscinfo

        utcoffset = self.utcoffset


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if location is not UNSET:
            field_dict["location"] = location
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if miscinfo is not UNSET:
            field_dict["miscinfo"] = miscinfo
        if utcoffset is not UNSET:
            field_dict["utcoffset"] = utcoffset

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        location = d.pop("location", UNSET)

        purpose = d.pop("purpose", UNSET)

        miscinfo = d.pop("miscinfo", UNSET)

        utcoffset = d.pop("utcoffset", UNSET)

        virinco_wats_web_dashboard_controllers_api_client_controller_client_settings = cls(
            name=name,
            location=location,
            purpose=purpose,
            miscinfo=miscinfo,
            utcoffset=utcoffset,
        )


        virinco_wats_web_dashboard_controllers_api_client_controller_client_settings.additional_properties = d
        return virinco_wats_web_dashboard_controllers_api_client_controller_client_settings

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
