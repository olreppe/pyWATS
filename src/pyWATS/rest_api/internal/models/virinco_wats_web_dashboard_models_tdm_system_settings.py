from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmSystemSettings")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmSystemSettings:
    """ 
        Attributes:
            prompt_version_on_file_upload (Union[Unset, bool]):
            auto_sync_products (Union[Unset, bool]):
            keep_uut_measures_for_num_months (Union[Unset, int]):
            keep_dw_measures_for_num_months (Union[Unset, int]):
     """

    prompt_version_on_file_upload: Union[Unset, bool] = UNSET
    auto_sync_products: Union[Unset, bool] = UNSET
    keep_uut_measures_for_num_months: Union[Unset, int] = UNSET
    keep_dw_measures_for_num_months: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        prompt_version_on_file_upload = self.prompt_version_on_file_upload

        auto_sync_products = self.auto_sync_products

        keep_uut_measures_for_num_months = self.keep_uut_measures_for_num_months

        keep_dw_measures_for_num_months = self.keep_dw_measures_for_num_months


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if prompt_version_on_file_upload is not UNSET:
            field_dict["promptVersionOnFileUpload"] = prompt_version_on_file_upload
        if auto_sync_products is not UNSET:
            field_dict["autoSyncProducts"] = auto_sync_products
        if keep_uut_measures_for_num_months is not UNSET:
            field_dict["keepUutMeasuresForNumMonths"] = keep_uut_measures_for_num_months
        if keep_dw_measures_for_num_months is not UNSET:
            field_dict["keepDwMeasuresForNumMonths"] = keep_dw_measures_for_num_months

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        prompt_version_on_file_upload = d.pop("promptVersionOnFileUpload", UNSET)

        auto_sync_products = d.pop("autoSyncProducts", UNSET)

        keep_uut_measures_for_num_months = d.pop("keepUutMeasuresForNumMonths", UNSET)

        keep_dw_measures_for_num_months = d.pop("keepDwMeasuresForNumMonths", UNSET)

        virinco_wats_web_dashboard_models_tdm_system_settings = cls(
            prompt_version_on_file_upload=prompt_version_on_file_upload,
            auto_sync_products=auto_sync_products,
            keep_uut_measures_for_num_months=keep_uut_measures_for_num_months,
            keep_dw_measures_for_num_months=keep_dw_measures_for_num_months,
        )


        virinco_wats_web_dashboard_models_tdm_system_settings.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_system_settings

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
