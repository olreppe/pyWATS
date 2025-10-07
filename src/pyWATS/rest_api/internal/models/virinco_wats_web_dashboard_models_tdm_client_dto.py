from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmClientDto")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmClientDto:
    """ Client DTO

        Attributes:
            client_id (int):
            name (Union[Unset, str]):
            display_name (Union[Unset, str]):
            location (Union[Unset, str]):
            purpose (Union[Unset, str]):
            type_ (Union[Unset, int]):
            client_group_id (Union[Unset, int]):
     """

    client_id: int
    name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    type_: Union[Unset, int] = UNSET
    client_group_id: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        name = self.name

        display_name = self.display_name

        location = self.location

        purpose = self.purpose

        type_ = self.type_

        client_group_id = self.client_group_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "clientId": client_id,
        })
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if location is not UNSET:
            field_dict["location"] = location
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if type_ is not UNSET:
            field_dict["type"] = type_
        if client_group_id is not UNSET:
            field_dict["clientGroupId"] = client_group_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_id = d.pop("clientId")

        name = d.pop("name", UNSET)

        display_name = d.pop("displayName", UNSET)

        location = d.pop("location", UNSET)

        purpose = d.pop("purpose", UNSET)

        type_ = d.pop("type", UNSET)

        client_group_id = d.pop("clientGroupId", UNSET)

        virinco_wats_web_dashboard_models_tdm_client_dto = cls(
            client_id=client_id,
            name=name,
            display_name=display_name,
            location=location,
            purpose=purpose,
            type_=type_,
            client_group_id=client_group_id,
        )


        virinco_wats_web_dashboard_models_tdm_client_dto.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_client_dto

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
