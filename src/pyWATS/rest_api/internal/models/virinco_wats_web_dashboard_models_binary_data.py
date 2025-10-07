from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsBinaryData")



@_attrs_define
class VirincoWATSWebDashboardModelsBinaryData:
    """ 
        Attributes:
            compressed (Union[Unset, str]):
            binary_data_guid (Union[Unset, str]):
            content_type (Union[Unset, str]):
            size (Union[Unset, int]):
            size_specified (Union[Unset, bool]):
            file_name (Union[Unset, str]):
            value (Union[Unset, str]):
     """

    compressed: Union[Unset, str] = UNSET
    binary_data_guid: Union[Unset, str] = UNSET
    content_type: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    size_specified: Union[Unset, bool] = UNSET
    file_name: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        compressed = self.compressed

        binary_data_guid = self.binary_data_guid

        content_type = self.content_type

        size = self.size

        size_specified = self.size_specified

        file_name = self.file_name

        value = self.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if compressed is not UNSET:
            field_dict["Compressed"] = compressed
        if binary_data_guid is not UNSET:
            field_dict["BinaryDataGUID"] = binary_data_guid
        if content_type is not UNSET:
            field_dict["ContentType"] = content_type
        if size is not UNSET:
            field_dict["size"] = size
        if size_specified is not UNSET:
            field_dict["sizeSpecified"] = size_specified
        if file_name is not UNSET:
            field_dict["FileName"] = file_name
        if value is not UNSET:
            field_dict["Value"] = value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        compressed = d.pop("Compressed", UNSET)

        binary_data_guid = d.pop("BinaryDataGUID", UNSET)

        content_type = d.pop("ContentType", UNSET)

        size = d.pop("size", UNSET)

        size_specified = d.pop("sizeSpecified", UNSET)

        file_name = d.pop("FileName", UNSET)

        value = d.pop("Value", UNSET)

        virinco_wats_web_dashboard_models_binary_data = cls(
            compressed=compressed,
            binary_data_guid=binary_data_guid,
            content_type=content_type,
            size=size,
            size_specified=size_specified,
            file_name=file_name,
            value=value,
        )


        virinco_wats_web_dashboard_models_binary_data.additional_properties = d
        return virinco_wats_web_dashboard_models_binary_data

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
