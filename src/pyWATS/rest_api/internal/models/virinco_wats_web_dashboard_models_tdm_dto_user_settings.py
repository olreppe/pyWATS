from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmDtoUserSettings")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmDtoUserSettings:
    """ DTO - UserSettings (data transfer object)

        Attributes:
            culture_code (Union[Unset, str]):
            default_from_date_ticks (Union[Unset, int]):
     """

    culture_code: Union[Unset, str] = UNSET
    default_from_date_ticks: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        culture_code = self.culture_code

        default_from_date_ticks = self.default_from_date_ticks


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if culture_code is not UNSET:
            field_dict["CultureCode"] = culture_code
        if default_from_date_ticks is not UNSET:
            field_dict["DefaultFromDateTicks"] = default_from_date_ticks

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        culture_code = d.pop("CultureCode", UNSET)

        default_from_date_ticks = d.pop("DefaultFromDateTicks", UNSET)

        virinco_wats_web_dashboard_models_tdm_dto_user_settings = cls(
            culture_code=culture_code,
            default_from_date_ticks=default_from_date_ticks,
        )


        virinco_wats_web_dashboard_models_tdm_dto_user_settings.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_dto_user_settings

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
