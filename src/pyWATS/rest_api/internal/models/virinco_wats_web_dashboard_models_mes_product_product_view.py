from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductProductView")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductProductView:
    """ 
        Attributes:
            part_number (Union[Unset, str]):
            name (Union[Unset, str]):
            category (Union[Unset, str]):
            non_serial (Union[Unset, bool]):
            state (Union[Unset, int]):
     """

    part_number: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    non_serial: Union[Unset, bool] = UNSET
    state: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        part_number = self.part_number

        name = self.name

        category = self.category

        non_serial = self.non_serial

        state = self.state


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if name is not UNSET:
            field_dict["name"] = name
        if category is not UNSET:
            field_dict["category"] = category
        if non_serial is not UNSET:
            field_dict["nonSerial"] = non_serial
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        part_number = d.pop("partNumber", UNSET)

        name = d.pop("name", UNSET)

        category = d.pop("category", UNSET)

        non_serial = d.pop("nonSerial", UNSET)

        state = d.pop("state", UNSET)

        virinco_wats_web_dashboard_models_mes_product_product_view = cls(
            part_number=part_number,
            name=name,
            category=category,
            non_serial=non_serial,
            state=state,
        )


        virinco_wats_web_dashboard_models_mes_product_product_view.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_product_product_view

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
