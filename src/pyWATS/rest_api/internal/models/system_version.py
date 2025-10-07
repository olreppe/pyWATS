from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="SystemVersion")



@_attrs_define
class SystemVersion:
    """ 
        Attributes:
            major (Union[Unset, int]):
            minor (Union[Unset, int]):
            build (Union[Unset, int]):
            revision (Union[Unset, int]):
            major_revision (Union[Unset, int]):
            minor_revision (Union[Unset, int]):
     """

    major: Union[Unset, int] = UNSET
    minor: Union[Unset, int] = UNSET
    build: Union[Unset, int] = UNSET
    revision: Union[Unset, int] = UNSET
    major_revision: Union[Unset, int] = UNSET
    minor_revision: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        major = self.major

        minor = self.minor

        build = self.build

        revision = self.revision

        major_revision = self.major_revision

        minor_revision = self.minor_revision


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if major is not UNSET:
            field_dict["Major"] = major
        if minor is not UNSET:
            field_dict["Minor"] = minor
        if build is not UNSET:
            field_dict["Build"] = build
        if revision is not UNSET:
            field_dict["Revision"] = revision
        if major_revision is not UNSET:
            field_dict["MajorRevision"] = major_revision
        if minor_revision is not UNSET:
            field_dict["MinorRevision"] = minor_revision

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        major = d.pop("Major", UNSET)

        minor = d.pop("Minor", UNSET)

        build = d.pop("Build", UNSET)

        revision = d.pop("Revision", UNSET)

        major_revision = d.pop("MajorRevision", UNSET)

        minor_revision = d.pop("MinorRevision", UNSET)

        system_version = cls(
            major=major,
            minor=minor,
            build=build,
            revision=revision,
            major_revision=major_revision,
            minor_revision=minor_revision,
        )


        system_version.additional_properties = d
        return system_version

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
