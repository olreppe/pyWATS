from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_production_public_serial_number_type_identifier import VirincoWATSWebDashboardModelsMesProductionPublicSerialNumberTypeIdentifier
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductionPublicSerialNumberType")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductionPublicSerialNumberType:
    """ 
        Attributes:
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            format_ (Union[Unset, str]):
            reg_ex (Union[Unset, str]):
            identifier (Union[Unset, VirincoWATSWebDashboardModelsMesProductionPublicSerialNumberTypeIdentifier]):
            identifier_name (Union[Unset, str]):
     """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    format_: Union[Unset, str] = UNSET
    reg_ex: Union[Unset, str] = UNSET
    identifier: Union[Unset, VirincoWATSWebDashboardModelsMesProductionPublicSerialNumberTypeIdentifier] = UNSET
    identifier_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        format_ = self.format_

        reg_ex = self.reg_ex

        identifier: Union[Unset, int] = UNSET
        if not isinstance(self.identifier, Unset):
            identifier = self.identifier.value


        identifier_name = self.identifier_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if format_ is not UNSET:
            field_dict["format"] = format_
        if reg_ex is not UNSET:
            field_dict["regEx"] = reg_ex
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if identifier_name is not UNSET:
            field_dict["identifierName"] = identifier_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        format_ = d.pop("format", UNSET)

        reg_ex = d.pop("regEx", UNSET)

        _identifier = d.pop("identifier", UNSET)
        identifier: Union[Unset, VirincoWATSWebDashboardModelsMesProductionPublicSerialNumberTypeIdentifier]
        if isinstance(_identifier,  Unset):
            identifier = UNSET
        else:
            identifier = VirincoWATSWebDashboardModelsMesProductionPublicSerialNumberTypeIdentifier(_identifier)




        identifier_name = d.pop("identifierName", UNSET)

        virinco_wats_web_dashboard_models_mes_production_public_serial_number_type = cls(
            name=name,
            description=description,
            format_=format_,
            reg_ex=reg_ex,
            identifier=identifier,
            identifier_name=identifier_name,
        )


        virinco_wats_web_dashboard_models_mes_production_public_serial_number_type.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_production_public_serial_number_type

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
