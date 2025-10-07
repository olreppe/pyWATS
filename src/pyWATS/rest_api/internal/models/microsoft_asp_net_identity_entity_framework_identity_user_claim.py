from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MicrosoftAspNetIdentityEntityFrameworkIdentityUserClaim")



@_attrs_define
class MicrosoftAspNetIdentityEntityFrameworkIdentityUserClaim:
    """ 
        Attributes:
            id (Union[Unset, int]):
            user_id (Union[Unset, str]):
            claim_type (Union[Unset, str]):
            claim_value (Union[Unset, str]):
     """

    id: Union[Unset, int] = UNSET
    user_id: Union[Unset, str] = UNSET
    claim_type: Union[Unset, str] = UNSET
    claim_value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        user_id = self.user_id

        claim_type = self.claim_type

        claim_value = self.claim_value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["Id"] = id
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if claim_type is not UNSET:
            field_dict["ClaimType"] = claim_type
        if claim_value is not UNSET:
            field_dict["ClaimValue"] = claim_value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("Id", UNSET)

        user_id = d.pop("UserId", UNSET)

        claim_type = d.pop("ClaimType", UNSET)

        claim_value = d.pop("ClaimValue", UNSET)

        microsoft_asp_net_identity_entity_framework_identity_user_claim = cls(
            id=id,
            user_id=user_id,
            claim_type=claim_type,
            claim_value=claim_value,
        )


        microsoft_asp_net_identity_entity_framework_identity_user_claim.additional_properties = d
        return microsoft_asp_net_identity_entity_framework_identity_user_claim

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
