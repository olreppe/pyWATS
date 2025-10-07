from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmClientGroupEx")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmClientGroupEx:
    """ 
        Attributes:
            path (Union[Unset, str]):
            indented_name (Union[Unset, str]):
            child_client_groups (Union[Unset, list['VirincoWATSWebDashboardModelsTdmClientGroupEx']]):
            client_group_id (Union[Unset, int]):
            name (Union[Unset, str]):
            parent_id (Union[Unset, int]):
            type_ (Union[Unset, str]):
            gps (Union[Unset, str]):
     """

    path: Union[Unset, str] = UNSET
    indented_name: Union[Unset, str] = UNSET
    child_client_groups: Union[Unset, list['VirincoWATSWebDashboardModelsTdmClientGroupEx']] = UNSET
    client_group_id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    parent_id: Union[Unset, int] = UNSET
    type_: Union[Unset, str] = UNSET
    gps: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        path = self.path

        indented_name = self.indented_name

        child_client_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.child_client_groups, Unset):
            child_client_groups = []
            for child_client_groups_item_data in self.child_client_groups:
                child_client_groups_item = child_client_groups_item_data.to_dict()
                child_client_groups.append(child_client_groups_item)



        client_group_id = self.client_group_id

        name = self.name

        parent_id = self.parent_id

        type_ = self.type_

        gps = self.gps


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if path is not UNSET:
            field_dict["path"] = path
        if indented_name is not UNSET:
            field_dict["indentedName"] = indented_name
        if child_client_groups is not UNSET:
            field_dict["childClientGroups"] = child_client_groups
        if client_group_id is not UNSET:
            field_dict["clientGroupId"] = client_group_id
        if name is not UNSET:
            field_dict["name"] = name
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if gps is not UNSET:
            field_dict["gps"] = gps

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path", UNSET)

        indented_name = d.pop("indentedName", UNSET)

        child_client_groups = []
        _child_client_groups = d.pop("childClientGroups", UNSET)
        for child_client_groups_item_data in (_child_client_groups or []):
            child_client_groups_item = VirincoWATSWebDashboardModelsTdmClientGroupEx.from_dict(child_client_groups_item_data)



            child_client_groups.append(child_client_groups_item)


        client_group_id = d.pop("clientGroupId", UNSET)

        name = d.pop("name", UNSET)

        parent_id = d.pop("parentId", UNSET)

        type_ = d.pop("type", UNSET)

        gps = d.pop("gps", UNSET)

        virinco_wats_web_dashboard_models_tdm_client_group_ex = cls(
            path=path,
            indented_name=indented_name,
            child_client_groups=child_client_groups,
            client_group_id=client_group_id,
            name=name,
            parent_id=parent_id,
            type_=type_,
            gps=gps,
        )


        virinco_wats_web_dashboard_models_tdm_client_group_ex.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_client_group_ex

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
