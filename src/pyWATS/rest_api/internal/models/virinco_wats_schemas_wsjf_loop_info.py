from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSSchemasWSJFLoopInfo")



@_attrs_define
class VirincoWATSSchemasWSJFLoopInfo:
    """ 
        Attributes:
            idx (Union[Unset, int]): Index (iteration) of loop (iteration only).
            num (Union[Unset, int]): Number of iterations in loop.
            ending_index (Union[Unset, int]): Last index of loop.
            passed (Union[Unset, int]): Number of iterations passed.
            failed (Union[Unset, int]): Number of iterations failed.
     """

    idx: Union[Unset, int] = UNSET
    num: Union[Unset, int] = UNSET
    ending_index: Union[Unset, int] = UNSET
    passed: Union[Unset, int] = UNSET
    failed: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        idx = self.idx

        num = self.num

        ending_index = self.ending_index

        passed = self.passed

        failed = self.failed


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if idx is not UNSET:
            field_dict["idx"] = idx
        if num is not UNSET:
            field_dict["num"] = num
        if ending_index is not UNSET:
            field_dict["endingIndex"] = ending_index
        if passed is not UNSET:
            field_dict["passed"] = passed
        if failed is not UNSET:
            field_dict["failed"] = failed

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        idx = d.pop("idx", UNSET)

        num = d.pop("num", UNSET)

        ending_index = d.pop("endingIndex", UNSET)

        passed = d.pop("passed", UNSET)

        failed = d.pop("failed", UNSET)

        virinco_wats_schemas_wsjf_loop_info = cls(
            idx=idx,
            num=num,
            ending_index=ending_index,
            passed=passed,
            failed=failed,
        )


        virinco_wats_schemas_wsjf_loop_info.additional_properties = d
        return virinco_wats_schemas_wsjf_loop_info

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
