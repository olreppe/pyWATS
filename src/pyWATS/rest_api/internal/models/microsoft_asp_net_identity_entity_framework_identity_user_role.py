from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MicrosoftAspNetIdentityEntityFrameworkIdentityUserRole")



@_attrs_define
class MicrosoftAspNetIdentityEntityFrameworkIdentityUserRole:
    """ 
        Attributes:
            user_id (Union[Unset, str]):
            role_id (Union[Unset, str]):
     """

    user_id: Union[Unset, str] = UNSET
    role_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        role_id = self.role_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if role_id is not UNSET:
            field_dict["RoleId"] = role_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = d.pop("UserId", UNSET)

        role_id = d.pop("RoleId", UNSET)

        microsoft_asp_net_identity_entity_framework_identity_user_role = cls(
            user_id=user_id,
            role_id=role_id,
        )


        microsoft_asp_net_identity_entity_framework_identity_user_role.additional_properties = d
        return microsoft_asp_net_identity_entity_framework_identity_user_role

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
