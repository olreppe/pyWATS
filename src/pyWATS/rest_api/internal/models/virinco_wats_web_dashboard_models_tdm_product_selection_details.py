from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmProductSelectionDetails")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmProductSelectionDetails:
    """ 
        Attributes:
            id (Union[Unset, int]):
            product_selection_id (Union[Unset, int]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            prod_sel (Union[Unset, int]):
            exclude (Union[Unset, bool]):
            order_no (Union[Unset, int]):
     """

    id: Union[Unset, int] = UNSET
    product_selection_id: Union[Unset, int] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    prod_sel: Union[Unset, int] = UNSET
    exclude: Union[Unset, bool] = UNSET
    order_no: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        product_selection_id = self.product_selection_id

        part_number = self.part_number

        revision = self.revision

        prod_sel = self.prod_sel

        exclude = self.exclude

        order_no = self.order_no


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if product_selection_id is not UNSET:
            field_dict["productSelectionId"] = product_selection_id
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if prod_sel is not UNSET:
            field_dict["prodSel"] = prod_sel
        if exclude is not UNSET:
            field_dict["exclude"] = exclude
        if order_no is not UNSET:
            field_dict["orderNo"] = order_no

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        product_selection_id = d.pop("productSelectionId", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        prod_sel = d.pop("prodSel", UNSET)

        exclude = d.pop("exclude", UNSET)

        order_no = d.pop("orderNo", UNSET)

        virinco_wats_web_dashboard_models_tdm_product_selection_details = cls(
            id=id,
            product_selection_id=product_selection_id,
            part_number=part_number,
            revision=revision,
            prod_sel=prod_sel,
            exclude=exclude,
            order_no=order_no,
        )


        virinco_wats_web_dashboard_models_tdm_product_selection_details.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_product_selection_details

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
