from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsChartDataSuggestion")



@_attrs_define
class VirincoWATSWebDashboardModelsChartDataSuggestion:
    """ 
        Attributes:
            description (Union[Unset, str]):
            values (Union[Unset, list[str]]):
            keys (Union[Unset, list[str]]):
     """

    description: Union[Unset, str] = UNSET
    values: Union[Unset, list[str]] = UNSET
    keys: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        values: Union[Unset, list[str]] = UNSET
        if not isinstance(self.values, Unset):
            values = self.values



        keys: Union[Unset, list[str]] = UNSET
        if not isinstance(self.keys, Unset):
            keys = self.keys




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if description is not UNSET:
            field_dict["description"] = description
        if values is not UNSET:
            field_dict["values"] = values
        if keys is not UNSET:
            field_dict["keys"] = keys

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        values = cast(list[str], d.pop("values", UNSET))


        keys = cast(list[str], d.pop("keys", UNSET))


        virinco_wats_web_dashboard_models_chart_data_suggestion = cls(
            description=description,
            values=values,
            keys=keys,
        )


        virinco_wats_web_dashboard_models_chart_data_suggestion.additional_properties = d
        return virinco_wats_web_dashboard_models_chart_data_suggestion

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
