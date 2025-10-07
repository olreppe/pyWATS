from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSSchemasWSJFMiscInfo")



@_attrs_define
class VirincoWATSSchemasWSJFMiscInfo:
    """ 
        Attributes:
            description (Union[Unset, str]): Description of misc info.
            typedef (Union[Unset, str]): Type definition (deprecated?).
            text (Union[Unset, str]): Textual value of misc info.
            numeric (Union[Unset, int]): Numeric value of misc info.
            numeric_format (Union[Unset, str]): Numeric format of numeric.
            id (Union[Unset, UUID]): Id of misc info (only valid for repair). Example: 00000000-0000-0000-0000-000000000000.
     """

    description: Union[Unset, str] = UNSET
    typedef: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    numeric: Union[Unset, int] = UNSET
    numeric_format: Union[Unset, str] = UNSET
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        typedef = self.typedef

        text = self.text

        numeric = self.numeric

        numeric_format = self.numeric_format

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if description is not UNSET:
            field_dict["description"] = description
        if typedef is not UNSET:
            field_dict["typedef"] = typedef
        if text is not UNSET:
            field_dict["text"] = text
        if numeric is not UNSET:
            field_dict["numeric"] = numeric
        if numeric_format is not UNSET:
            field_dict["numericFormat"] = numeric_format
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        typedef = d.pop("typedef", UNSET)

        text = d.pop("text", UNSET)

        numeric = d.pop("numeric", UNSET)

        numeric_format = d.pop("numericFormat", UNSET)

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        virinco_wats_schemas_wsjf_misc_info = cls(
            description=description,
            typedef=typedef,
            text=text,
            numeric=numeric,
            numeric_format=numeric_format,
            id=id,
        )


        virinco_wats_schemas_wsjf_misc_info.additional_properties = d
        return virinco_wats_schemas_wsjf_misc_info

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
