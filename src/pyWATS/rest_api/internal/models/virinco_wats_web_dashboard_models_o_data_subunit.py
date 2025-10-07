from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsODataSubunit")



@_attrs_define
class VirincoWATSWebDashboardModelsODataSubunit:
    """ 
        Attributes:
            part_type (Union[Unset, str]): Sub unit part type
            serial_number (Union[Unset, str]): Sub unit serial number
            part_number (Union[Unset, str]): Sub unit part number
            revision (Union[Unset, str]): Sub unit revision
     """

    part_type: Union[Unset, str] = UNSET
    serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        part_type = self.part_type

        serial_number = self.serial_number

        part_number = self.part_number

        revision = self.revision


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if part_type is not UNSET:
            field_dict["partType"] = part_type
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        part_type = d.pop("partType", UNSET)

        serial_number = d.pop("serialNumber", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        virinco_wats_web_dashboard_models_o_data_subunit = cls(
            part_type=part_type,
            serial_number=serial_number,
            part_number=part_number,
            revision=revision,
        )


        virinco_wats_web_dashboard_models_o_data_subunit.additional_properties = d
        return virinco_wats_web_dashboard_models_o_data_subunit

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
