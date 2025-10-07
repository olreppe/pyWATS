from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_step_details_suggestion_step_details_grouping import VirincoWATSWebDashboardModelsStepDetailsSuggestionStepDetailsGrouping
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsStepDetailsSuggestion")



@_attrs_define
class VirincoWATSWebDashboardModelsStepDetailsSuggestion:
    """ 
        Attributes:
            step_details_grouping (Union[Unset, VirincoWATSWebDashboardModelsStepDetailsSuggestionStepDetailsGrouping]):
            key (Union[Unset, str]):
            value (Union[Unset, str]):
            z_score_xbar (Union[Unset, float]):
            z_score_sbar (Union[Unset, float]):
            values (Union[Unset, list[str]]):
            keys (Union[Unset, list[str]]):
            misc_descriptions (Union[Unset, list[str]]):
            is_abnormal_high_fail_rate (Union[Unset, bool]):
            fail_rate (Union[Unset, float]):
     """

    step_details_grouping: Union[Unset, VirincoWATSWebDashboardModelsStepDetailsSuggestionStepDetailsGrouping] = UNSET
    key: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    z_score_xbar: Union[Unset, float] = UNSET
    z_score_sbar: Union[Unset, float] = UNSET
    values: Union[Unset, list[str]] = UNSET
    keys: Union[Unset, list[str]] = UNSET
    misc_descriptions: Union[Unset, list[str]] = UNSET
    is_abnormal_high_fail_rate: Union[Unset, bool] = UNSET
    fail_rate: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        step_details_grouping: Union[Unset, int] = UNSET
        if not isinstance(self.step_details_grouping, Unset):
            step_details_grouping = self.step_details_grouping.value


        key = self.key

        value = self.value

        z_score_xbar = self.z_score_xbar

        z_score_sbar = self.z_score_sbar

        values: Union[Unset, list[str]] = UNSET
        if not isinstance(self.values, Unset):
            values = self.values



        keys: Union[Unset, list[str]] = UNSET
        if not isinstance(self.keys, Unset):
            keys = self.keys



        misc_descriptions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.misc_descriptions, Unset):
            misc_descriptions = self.misc_descriptions



        is_abnormal_high_fail_rate = self.is_abnormal_high_fail_rate

        fail_rate = self.fail_rate


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if step_details_grouping is not UNSET:
            field_dict["stepDetailsGrouping"] = step_details_grouping
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value
        if z_score_xbar is not UNSET:
            field_dict["zScoreXbar"] = z_score_xbar
        if z_score_sbar is not UNSET:
            field_dict["zScoreSbar"] = z_score_sbar
        if values is not UNSET:
            field_dict["values"] = values
        if keys is not UNSET:
            field_dict["keys"] = keys
        if misc_descriptions is not UNSET:
            field_dict["miscDescriptions"] = misc_descriptions
        if is_abnormal_high_fail_rate is not UNSET:
            field_dict["isAbnormalHighFailRate"] = is_abnormal_high_fail_rate
        if fail_rate is not UNSET:
            field_dict["failRate"] = fail_rate

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _step_details_grouping = d.pop("stepDetailsGrouping", UNSET)
        step_details_grouping: Union[Unset, VirincoWATSWebDashboardModelsStepDetailsSuggestionStepDetailsGrouping]
        if isinstance(_step_details_grouping,  Unset):
            step_details_grouping = UNSET
        else:
            step_details_grouping = VirincoWATSWebDashboardModelsStepDetailsSuggestionStepDetailsGrouping(_step_details_grouping)




        key = d.pop("key", UNSET)

        value = d.pop("value", UNSET)

        z_score_xbar = d.pop("zScoreXbar", UNSET)

        z_score_sbar = d.pop("zScoreSbar", UNSET)

        values = cast(list[str], d.pop("values", UNSET))


        keys = cast(list[str], d.pop("keys", UNSET))


        misc_descriptions = cast(list[str], d.pop("miscDescriptions", UNSET))


        is_abnormal_high_fail_rate = d.pop("isAbnormalHighFailRate", UNSET)

        fail_rate = d.pop("failRate", UNSET)

        virinco_wats_web_dashboard_models_step_details_suggestion = cls(
            step_details_grouping=step_details_grouping,
            key=key,
            value=value,
            z_score_xbar=z_score_xbar,
            z_score_sbar=z_score_sbar,
            values=values,
            keys=keys,
            misc_descriptions=misc_descriptions,
            is_abnormal_high_fail_rate=is_abnormal_high_fail_rate,
            fail_rate=fail_rate,
        )


        virinco_wats_web_dashboard_models_step_details_suggestion.additional_properties = d
        return virinco_wats_web_dashboard_models_step_details_suggestion

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
