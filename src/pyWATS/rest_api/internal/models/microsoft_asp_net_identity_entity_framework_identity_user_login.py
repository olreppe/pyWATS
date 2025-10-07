from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MicrosoftAspNetIdentityEntityFrameworkIdentityUserLogin")



@_attrs_define
class MicrosoftAspNetIdentityEntityFrameworkIdentityUserLogin:
    """ 
        Attributes:
            login_provider (Union[Unset, str]):
            provider_key (Union[Unset, str]):
            user_id (Union[Unset, str]):
     """

    login_provider: Union[Unset, str] = UNSET
    provider_key: Union[Unset, str] = UNSET
    user_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        login_provider = self.login_provider

        provider_key = self.provider_key

        user_id = self.user_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if login_provider is not UNSET:
            field_dict["LoginProvider"] = login_provider
        if provider_key is not UNSET:
            field_dict["ProviderKey"] = provider_key
        if user_id is not UNSET:
            field_dict["UserId"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        login_provider = d.pop("LoginProvider", UNSET)

        provider_key = d.pop("ProviderKey", UNSET)

        user_id = d.pop("UserId", UNSET)

        microsoft_asp_net_identity_entity_framework_identity_user_login = cls(
            login_provider=login_provider,
            provider_key=provider_key,
            user_id=user_id,
        )


        microsoft_asp_net_identity_entity_framework_identity_user_login.additional_properties = d
        return microsoft_asp_net_identity_entity_framework_identity_user_login

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
