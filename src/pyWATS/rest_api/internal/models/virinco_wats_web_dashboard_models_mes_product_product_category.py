from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductProductCategory")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductProductCategory:
    """ 
        Attributes:
            product_category_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            description (Union[Unset, str]):
     """

    product_category_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        product_category_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_category_id, Unset):
            product_category_id = str(self.product_category_id)

        name = self.name

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if product_category_id is not UNSET:
            field_dict["ProductCategoryId"] = product_category_id
        if name is not UNSET:
            field_dict["Name"] = name
        if description is not UNSET:
            field_dict["Description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _product_category_id = d.pop("ProductCategoryId", UNSET)
        product_category_id: Union[Unset, UUID]
        if isinstance(_product_category_id,  Unset):
            product_category_id = UNSET
        else:
            product_category_id = UUID(_product_category_id)




        name = d.pop("Name", UNSET)

        description = d.pop("Description", UNSET)

        virinco_wats_web_dashboard_models_mes_product_product_category = cls(
            product_category_id=product_category_id,
            name=name,
            description=description,
        )


        virinco_wats_web_dashboard_models_mes_product_product_category.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_product_product_category

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
