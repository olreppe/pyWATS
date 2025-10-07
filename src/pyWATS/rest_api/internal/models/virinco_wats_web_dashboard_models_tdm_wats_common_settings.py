from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmWatsCommonSettings")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmWatsCommonSettings:
    """ 
        Attributes:
            type_ (Union[Unset, str]):
            tab_target (Union[Unset, str]): Open links in context/action menu in new or current tab
            date_column_grouping_type (Union[Unset, int]): Defines the grid date column grouping type (hour, day, month
                etc..)
     """

    type_: Union[Unset, str] = UNSET
    tab_target: Union[Unset, str] = UNSET
    date_column_grouping_type: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        tab_target = self.tab_target

        date_column_grouping_type = self.date_column_grouping_type


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["type"] = type_
        if tab_target is not UNSET:
            field_dict["tabTarget"] = tab_target
        if date_column_grouping_type is not UNSET:
            field_dict["dateColumnGroupingType"] = date_column_grouping_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        tab_target = d.pop("tabTarget", UNSET)

        date_column_grouping_type = d.pop("dateColumnGroupingType", UNSET)

        virinco_wats_web_dashboard_models_tdm_wats_common_settings = cls(
            type_=type_,
            tab_target=tab_target,
            date_column_grouping_type=date_column_grouping_type,
        )


        virinco_wats_web_dashboard_models_tdm_wats_common_settings.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_wats_common_settings

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
