from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductPart")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductPart:
    """ 
        Attributes:
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            name (Union[Unset, str]):
            category (Union[Unset, str]):
            action (Union[Unset, str]):
     """

    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    action: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        part_number = self.part_number

        revision = self.revision

        name = self.name

        category = self.category

        action = self.action


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if name is not UNSET:
            field_dict["name"] = name
        if category is not UNSET:
            field_dict["category"] = category
        if action is not UNSET:
            field_dict["action"] = action

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        name = d.pop("name", UNSET)

        category = d.pop("category", UNSET)

        action = d.pop("action", UNSET)

        virinco_wats_web_dashboard_models_mes_product_part = cls(
            part_number=part_number,
            revision=revision,
            name=name,
            category=category,
            action=action,
        )


        virinco_wats_web_dashboard_models_mes_product_part.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_product_part

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
