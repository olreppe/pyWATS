from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSInterfaceModelsMiscInfo")



@_attrs_define
class VirincoWATSInterfaceModelsMiscInfo:
    """ 
        Attributes:
            guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            description (Union[Unset, str]):
            input_mask (Union[Unset, str]):
            valid_regex (Union[Unset, str]):
            status (Union[Unset, int]):
            sort_order (Union[Unset, int]):
            allowed_values (Union[Unset, list[str]]):
     """

    guid: Union[Unset, UUID] = UNSET
    description: Union[Unset, str] = UNSET
    input_mask: Union[Unset, str] = UNSET
    valid_regex: Union[Unset, str] = UNSET
    status: Union[Unset, int] = UNSET
    sort_order: Union[Unset, int] = UNSET
    allowed_values: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        guid: Union[Unset, str] = UNSET
        if not isinstance(self.guid, Unset):
            guid = str(self.guid)

        description = self.description

        input_mask = self.input_mask

        valid_regex = self.valid_regex

        status = self.status

        sort_order = self.sort_order

        allowed_values: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_values, Unset):
            allowed_values = self.allowed_values




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if guid is not UNSET:
            field_dict["GUID"] = guid
        if description is not UNSET:
            field_dict["Description"] = description
        if input_mask is not UNSET:
            field_dict["InputMask"] = input_mask
        if valid_regex is not UNSET:
            field_dict["ValidRegex"] = valid_regex
        if status is not UNSET:
            field_dict["Status"] = status
        if sort_order is not UNSET:
            field_dict["SortOrder"] = sort_order
        if allowed_values is not UNSET:
            field_dict["AllowedValues"] = allowed_values

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _guid = d.pop("GUID", UNSET)
        guid: Union[Unset, UUID]
        if isinstance(_guid,  Unset):
            guid = UNSET
        else:
            guid = UUID(_guid)




        description = d.pop("Description", UNSET)

        input_mask = d.pop("InputMask", UNSET)

        valid_regex = d.pop("ValidRegex", UNSET)

        status = d.pop("Status", UNSET)

        sort_order = d.pop("SortOrder", UNSET)

        allowed_values = cast(list[str], d.pop("AllowedValues", UNSET))


        virinco_wats_interface_models_misc_info = cls(
            guid=guid,
            description=description,
            input_mask=input_mask,
            valid_regex=valid_regex,
            status=status,
            sort_order=sort_order,
            allowed_values=allowed_values,
        )


        virinco_wats_interface_models_misc_info.additional_properties = d
        return virinco_wats_interface_models_misc_info

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
