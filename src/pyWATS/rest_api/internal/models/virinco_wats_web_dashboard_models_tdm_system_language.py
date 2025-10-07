from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmSystemLanguage")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmSystemLanguage:
    """ 
        Attributes:
            wats_system_language (Union[Unset, str]):
     """

    wats_system_language: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        wats_system_language = self.wats_system_language


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if wats_system_language is not UNSET:
            field_dict["WatsSystemLanguage"] = wats_system_language

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        wats_system_language = d.pop("WatsSystemLanguage", UNSET)

        virinco_wats_web_dashboard_models_tdm_system_language = cls(
            wats_system_language=wats_system_language,
        )


        virinco_wats_web_dashboard_models_tdm_system_language.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_system_language

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
