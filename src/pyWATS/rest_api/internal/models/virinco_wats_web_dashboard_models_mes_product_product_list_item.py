from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductProductListItem")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductProductListItem:
    """ 
        Attributes:
            pn (Union[Unset, str]):
            name (Union[Unset, str]):
            desc (Union[Unset, str]):
            state (Union[Unset, int]):
            category (Union[Unset, str]):
     """

    pn: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    desc: Union[Unset, str] = UNSET
    state: Union[Unset, int] = UNSET
    category: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        pn = self.pn

        name = self.name

        desc = self.desc

        state = self.state

        category = self.category


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if pn is not UNSET:
            field_dict["PN"] = pn
        if name is not UNSET:
            field_dict["Name"] = name
        if desc is not UNSET:
            field_dict["Desc"] = desc
        if state is not UNSET:
            field_dict["State"] = state
        if category is not UNSET:
            field_dict["Category"] = category

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pn = d.pop("PN", UNSET)

        name = d.pop("Name", UNSET)

        desc = d.pop("Desc", UNSET)

        state = d.pop("State", UNSET)

        category = d.pop("Category", UNSET)

        virinco_wats_web_dashboard_models_mes_product_product_list_item = cls(
            pn=pn,
            name=name,
            desc=desc,
            state=state,
            category=category,
        )


        virinco_wats_web_dashboard_models_mes_product_product_list_item.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_product_product_list_item

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
