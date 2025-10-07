from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmStorageUsageHistory")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmStorageUsageHistory:
    """ 
        Attributes:
            period (Union[Unset, str]):
            receive_size (Union[Unset, int]):
            raw_report_size (Union[Unset, int]):
            raw_binary_size (Union[Unset, int]):
     """

    period: Union[Unset, str] = UNSET
    receive_size: Union[Unset, int] = UNSET
    raw_report_size: Union[Unset, int] = UNSET
    raw_binary_size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        period = self.period

        receive_size = self.receive_size

        raw_report_size = self.raw_report_size

        raw_binary_size = self.raw_binary_size


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if period is not UNSET:
            field_dict["period"] = period
        if receive_size is not UNSET:
            field_dict["receiveSize"] = receive_size
        if raw_report_size is not UNSET:
            field_dict["rawReportSize"] = raw_report_size
        if raw_binary_size is not UNSET:
            field_dict["rawBinarySize"] = raw_binary_size

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period = d.pop("period", UNSET)

        receive_size = d.pop("receiveSize", UNSET)

        raw_report_size = d.pop("rawReportSize", UNSET)

        raw_binary_size = d.pop("rawBinarySize", UNSET)

        virinco_wats_web_dashboard_models_tdm_storage_usage_history = cls(
            period=period,
            receive_size=receive_size,
            raw_report_size=raw_report_size,
            raw_binary_size=raw_binary_size,
        )


        virinco_wats_web_dashboard_models_tdm_storage_usage_history.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_storage_usage_history

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
