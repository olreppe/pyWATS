from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsSequenceSelection")



@_attrs_define
class VirincoWATSWebDashboardModelsSequenceSelection:
    """ 
        Attributes:
            process_name (Union[Unset, str]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            sw_filename (Union[Unset, str]):
            sw_version (Union[Unset, str]):
     """

    process_name: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    sw_filename: Union[Unset, str] = UNSET
    sw_version: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        process_name = self.process_name

        part_number = self.part_number

        revision = self.revision

        sw_filename = self.sw_filename

        sw_version = self.sw_version


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if process_name is not UNSET:
            field_dict["processName"] = process_name
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if sw_filename is not UNSET:
            field_dict["swFilename"] = sw_filename
        if sw_version is not UNSET:
            field_dict["swVersion"] = sw_version

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_name = d.pop("processName", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        sw_filename = d.pop("swFilename", UNSET)

        sw_version = d.pop("swVersion", UNSET)

        virinco_wats_web_dashboard_models_sequence_selection = cls(
            process_name=process_name,
            part_number=part_number,
            revision=revision,
            sw_filename=sw_filename,
            sw_version=sw_version,
        )


        virinco_wats_web_dashboard_models_sequence_selection.additional_properties = d
        return virinco_wats_web_dashboard_models_sequence_selection

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
