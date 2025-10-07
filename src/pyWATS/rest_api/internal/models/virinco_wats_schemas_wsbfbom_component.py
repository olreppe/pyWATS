from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSSchemasWSBFBOMComponent")



@_attrs_define
class VirincoWATSSchemasWSBFBOMComponent:
    """ 
        Attributes:
            number (Union[Unset, str]):
            rev (Union[Unset, str]):
            qty (Union[Unset, int]):
            qty_specified (Union[Unset, bool]):
            desc (Union[Unset, str]):
            ref (Union[Unset, str]):
            function_block (Union[Unset, str]):
     """

    number: Union[Unset, str] = UNSET
    rev: Union[Unset, str] = UNSET
    qty: Union[Unset, int] = UNSET
    qty_specified: Union[Unset, bool] = UNSET
    desc: Union[Unset, str] = UNSET
    ref: Union[Unset, str] = UNSET
    function_block: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        number = self.number

        rev = self.rev

        qty = self.qty

        qty_specified = self.qty_specified

        desc = self.desc

        ref = self.ref

        function_block = self.function_block


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if number is not UNSET:
            field_dict["Number"] = number
        if rev is not UNSET:
            field_dict["Rev"] = rev
        if qty is not UNSET:
            field_dict["Qty"] = qty
        if qty_specified is not UNSET:
            field_dict["QtySpecified"] = qty_specified
        if desc is not UNSET:
            field_dict["Desc"] = desc
        if ref is not UNSET:
            field_dict["Ref"] = ref
        if function_block is not UNSET:
            field_dict["FunctionBlock"] = function_block

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        number = d.pop("Number", UNSET)

        rev = d.pop("Rev", UNSET)

        qty = d.pop("Qty", UNSET)

        qty_specified = d.pop("QtySpecified", UNSET)

        desc = d.pop("Desc", UNSET)

        ref = d.pop("Ref", UNSET)

        function_block = d.pop("FunctionBlock", UNSET)

        virinco_wats_schemas_wsbfbom_component = cls(
            number=number,
            rev=rev,
            qty=qty,
            qty_specified=qty_specified,
            desc=desc,
            ref=ref,
            function_block=function_block,
        )


        virinco_wats_schemas_wsbfbom_component.additional_properties = d
        return virinco_wats_schemas_wsbfbom_component

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
