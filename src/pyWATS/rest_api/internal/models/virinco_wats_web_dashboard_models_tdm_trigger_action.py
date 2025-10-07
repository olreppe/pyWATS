from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_tdm_trigger_action_type import VirincoWATSWebDashboardModelsTdmTriggerActionType
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmTriggerAction")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmTriggerAction:
    """ 
        Attributes:
            id (Union[Unset, int]):
            trigger_id (Union[Unset, int]):
            type_ (Union[Unset, VirincoWATSWebDashboardModelsTdmTriggerActionType]):
            value (Union[Unset, str]):
     """

    id: Union[Unset, int] = UNSET
    trigger_id: Union[Unset, int] = UNSET
    type_: Union[Unset, VirincoWATSWebDashboardModelsTdmTriggerActionType] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        trigger_id = self.trigger_id

        type_: Union[Unset, int] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        value = self.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if trigger_id is not UNSET:
            field_dict["triggerId"] = trigger_id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        trigger_id = d.pop("triggerId", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, VirincoWATSWebDashboardModelsTdmTriggerActionType]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = VirincoWATSWebDashboardModelsTdmTriggerActionType(_type_)




        value = d.pop("value", UNSET)

        virinco_wats_web_dashboard_models_tdm_trigger_action = cls(
            id=id,
            trigger_id=trigger_id,
            type_=type_,
            value=value,
        )


        virinco_wats_web_dashboard_models_tdm_trigger_action.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_trigger_action

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
