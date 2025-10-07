from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmSite")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmSite:
    """ 
        Attributes:
            client_group_id (Union[Unset, int]):
            name (Union[Unset, str]):
            code (Union[Unset, str]):
            gps (Union[Unset, str]):
     """

    client_group_id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    gps: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        client_group_id = self.client_group_id

        name = self.name

        code = self.code

        gps = self.gps


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if client_group_id is not UNSET:
            field_dict["ClientGroupId"] = client_group_id
        if name is not UNSET:
            field_dict["Name"] = name
        if code is not UNSET:
            field_dict["Code"] = code
        if gps is not UNSET:
            field_dict["Gps"] = gps

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_group_id = d.pop("ClientGroupId", UNSET)

        name = d.pop("Name", UNSET)

        code = d.pop("Code", UNSET)

        gps = d.pop("Gps", UNSET)

        virinco_wats_web_dashboard_models_tdm_site = cls(
            client_group_id=client_group_id,
            name=name,
            code=code,
            gps=gps,
        )


        virinco_wats_web_dashboard_models_tdm_site.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_site

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
