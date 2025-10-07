from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_manager_filter_states_item import VirincoWATSWebDashboardModelsMesAssetAssetManagerFilterStatesItem
from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_manager_filter_statuses_item import VirincoWATSWebDashboardModelsMesAssetAssetManagerFilterStatusesItem
from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter")



@_attrs_define
class VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter:
    """ 
        Attributes:
            types (Union[Unset, list[UUID]]):
            states (Union[Unset, list[VirincoWATSWebDashboardModelsMesAssetAssetManagerFilterStatesItem]]):
            statuses (Union[Unset, list[VirincoWATSWebDashboardModelsMesAssetAssetManagerFilterStatusesItem]]):
            search_string (Union[Unset, str]):
     """

    types: Union[Unset, list[UUID]] = UNSET
    states: Union[Unset, list[VirincoWATSWebDashboardModelsMesAssetAssetManagerFilterStatesItem]] = UNSET
    statuses: Union[Unset, list[VirincoWATSWebDashboardModelsMesAssetAssetManagerFilterStatusesItem]] = UNSET
    search_string: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.types, Unset):
            types = []
            for types_item_data in self.types:
                types_item = str(types_item_data)
                types.append(types_item)



        states: Union[Unset, list[int]] = UNSET
        if not isinstance(self.states, Unset):
            states = []
            for states_item_data in self.states:
                states_item = states_item_data.value
                states.append(states_item)



        statuses: Union[Unset, list[int]] = UNSET
        if not isinstance(self.statuses, Unset):
            statuses = []
            for statuses_item_data in self.statuses:
                statuses_item = statuses_item_data.value
                statuses.append(statuses_item)



        search_string = self.search_string


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if types is not UNSET:
            field_dict["types"] = types
        if states is not UNSET:
            field_dict["states"] = states
        if statuses is not UNSET:
            field_dict["statuses"] = statuses
        if search_string is not UNSET:
            field_dict["searchString"] = search_string

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        types = []
        _types = d.pop("types", UNSET)
        for types_item_data in (_types or []):
            types_item = UUID(types_item_data)



            types.append(types_item)


        states = []
        _states = d.pop("states", UNSET)
        for states_item_data in (_states or []):
            states_item = VirincoWATSWebDashboardModelsMesAssetAssetManagerFilterStatesItem(states_item_data)



            states.append(states_item)


        statuses = []
        _statuses = d.pop("statuses", UNSET)
        for statuses_item_data in (_statuses or []):
            statuses_item = VirincoWATSWebDashboardModelsMesAssetAssetManagerFilterStatusesItem(statuses_item_data)



            statuses.append(statuses_item)


        search_string = d.pop("searchString", UNSET)

        virinco_wats_web_dashboard_models_mes_asset_asset_manager_filter = cls(
            types=types,
            states=states,
            statuses=statuses,
            search_string=search_string,
        )


        virinco_wats_web_dashboard_models_mes_asset_asset_manager_filter.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_asset_asset_manager_filter

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
