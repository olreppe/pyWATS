from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_role_permission_permission import VirincoWATSWebDashboardModelsRolePermissionPermission
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsRolePermission")



@_attrs_define
class VirincoWATSWebDashboardModelsRolePermission:
    """ 
        Attributes:
            permission (Union[Unset, VirincoWATSWebDashboardModelsRolePermissionPermission]):
            parent_permission (Union[Unset, int]):
            enabled (Union[Unset, bool]):
            description (Union[Unset, str]):
            allow (Union[Unset, bool]):
            deny (Union[Unset, bool]):
            explanation (Union[Unset, str]):
            permission_string (Union[Unset, str]):
     """

    permission: Union[Unset, VirincoWATSWebDashboardModelsRolePermissionPermission] = UNSET
    parent_permission: Union[Unset, int] = UNSET
    enabled: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    allow: Union[Unset, bool] = UNSET
    deny: Union[Unset, bool] = UNSET
    explanation: Union[Unset, str] = UNSET
    permission_string: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        permission: Union[Unset, int] = UNSET
        if not isinstance(self.permission, Unset):
            permission = self.permission.value


        parent_permission = self.parent_permission

        enabled = self.enabled

        description = self.description

        allow = self.allow

        deny = self.deny

        explanation = self.explanation

        permission_string = self.permission_string


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if permission is not UNSET:
            field_dict["permission"] = permission
        if parent_permission is not UNSET:
            field_dict["parentPermission"] = parent_permission
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if description is not UNSET:
            field_dict["description"] = description
        if allow is not UNSET:
            field_dict["allow"] = allow
        if deny is not UNSET:
            field_dict["deny"] = deny
        if explanation is not UNSET:
            field_dict["explanation"] = explanation
        if permission_string is not UNSET:
            field_dict["permissionString"] = permission_string

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _permission = d.pop("permission", UNSET)
        permission: Union[Unset, VirincoWATSWebDashboardModelsRolePermissionPermission]
        if isinstance(_permission,  Unset):
            permission = UNSET
        else:
            permission = VirincoWATSWebDashboardModelsRolePermissionPermission(_permission)




        parent_permission = d.pop("parentPermission", UNSET)

        enabled = d.pop("enabled", UNSET)

        description = d.pop("description", UNSET)

        allow = d.pop("allow", UNSET)

        deny = d.pop("deny", UNSET)

        explanation = d.pop("explanation", UNSET)

        permission_string = d.pop("permissionString", UNSET)

        virinco_wats_web_dashboard_models_role_permission = cls(
            permission=permission,
            parent_permission=parent_permission,
            enabled=enabled,
            description=description,
            allow=allow,
            deny=deny,
            explanation=explanation,
            permission_string=permission_string,
        )


        virinco_wats_web_dashboard_models_role_permission.additional_properties = d
        return virinco_wats_web_dashboard_models_role_permission

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
