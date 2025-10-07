from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmArchiveFilterProcess")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmArchiveFilterProcess:
    """ 
        Attributes:
            filter_process_id (Union[Unset, int]):
            filter_id (Union[Unset, int]):
            process_code (Union[Unset, int]):
     """

    filter_process_id: Union[Unset, int] = UNSET
    filter_id: Union[Unset, int] = UNSET
    process_code: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        filter_process_id = self.filter_process_id

        filter_id = self.filter_id

        process_code = self.process_code


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if filter_process_id is not UNSET:
            field_dict["FilterProcessId"] = filter_process_id
        if filter_id is not UNSET:
            field_dict["FilterId"] = filter_id
        if process_code is not UNSET:
            field_dict["ProcessCode"] = process_code

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filter_process_id = d.pop("FilterProcessId", UNSET)

        filter_id = d.pop("FilterId", UNSET)

        process_code = d.pop("ProcessCode", UNSET)

        virinco_wats_web_dashboard_models_tdm_archive_filter_process = cls(
            filter_process_id=filter_process_id,
            filter_id=filter_id,
            process_code=process_code,
        )


        virinco_wats_web_dashboard_models_tdm_archive_filter_process.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_archive_filter_process

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
