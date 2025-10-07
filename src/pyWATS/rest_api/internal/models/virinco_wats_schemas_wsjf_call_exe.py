from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSSchemasWSJFCallExe")



@_attrs_define
class VirincoWATSSchemasWSJFCallExe:
    """ 
        Attributes:
            exit_code (Union[Unset, float]): Exit code of called exe.
            exit_code_format (Union[Unset, str]): Numeric format of exit code.
     """

    exit_code: Union[Unset, float] = UNSET
    exit_code_format: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        exit_code = self.exit_code

        exit_code_format = self.exit_code_format


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if exit_code is not UNSET:
            field_dict["exitCode"] = exit_code
        if exit_code_format is not UNSET:
            field_dict["exitCodeFormat"] = exit_code_format

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        exit_code = d.pop("exitCode", UNSET)

        exit_code_format = d.pop("exitCodeFormat", UNSET)

        virinco_wats_schemas_wsjf_call_exe = cls(
            exit_code=exit_code,
            exit_code_format=exit_code_format,
        )


        virinco_wats_schemas_wsjf_call_exe.additional_properties = d
        return virinco_wats_schemas_wsjf_call_exe

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
