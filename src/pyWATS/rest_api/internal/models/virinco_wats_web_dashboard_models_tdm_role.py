from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmRole")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmRole:
    """ 
        Attributes:
            id (Union[Unset, str]):
            name (Union[Unset, str]):
            quantity (Union[Unset, int]):
            headless (Union[Unset, bool]):
     """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    quantity: Union[Unset, int] = UNSET
    headless: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        quantity = self.quantity

        headless = self.headless


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["Id"] = id
        if name is not UNSET:
            field_dict["Name"] = name
        if quantity is not UNSET:
            field_dict["Quantity"] = quantity
        if headless is not UNSET:
            field_dict["Headless"] = headless

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("Id", UNSET)

        name = d.pop("Name", UNSET)

        quantity = d.pop("Quantity", UNSET)

        headless = d.pop("Headless", UNSET)

        virinco_wats_web_dashboard_models_tdm_role = cls(
            id=id,
            name=name,
            quantity=quantity,
            headless=headless,
        )


        virinco_wats_web_dashboard_models_tdm_role.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_role

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
