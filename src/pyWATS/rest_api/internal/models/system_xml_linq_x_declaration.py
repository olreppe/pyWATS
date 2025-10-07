from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="SystemXmlLinqXDeclaration")



@_attrs_define
class SystemXmlLinqXDeclaration:
    """ 
        Attributes:
            encoding (Union[Unset, str]):
            standalone (Union[Unset, str]):
            version (Union[Unset, str]):
     """

    encoding: Union[Unset, str] = UNSET
    standalone: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        encoding = self.encoding

        standalone = self.standalone

        version = self.version


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if encoding is not UNSET:
            field_dict["Encoding"] = encoding
        if standalone is not UNSET:
            field_dict["Standalone"] = standalone
        if version is not UNSET:
            field_dict["Version"] = version

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        encoding = d.pop("Encoding", UNSET)

        standalone = d.pop("Standalone", UNSET)

        version = d.pop("Version", UNSET)

        system_xml_linq_x_declaration = cls(
            encoding=encoding,
            standalone=standalone,
            version=version,
        )


        system_xml_linq_x_declaration.additional_properties = d
        return system_xml_linq_x_declaration

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
