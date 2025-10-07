from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="VirincoWATSConfigurationCommonUserSettings")



@_attrs_define
class VirincoWATSConfigurationCommonUserSettings:
    """ 
        Attributes:
            full_name (Union[Unset, str]):
            culture_code (Union[Unset, str]):
            email (Union[Unset, str]):
            roles (Union[Unset, list[str]]):
            levels (Union[Unset, list[str]]):
            product_groups (Union[Unset, list[str]]):
     """

    full_name: Union[Unset, str] = UNSET
    culture_code: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    roles: Union[Unset, list[str]] = UNSET
    levels: Union[Unset, list[str]] = UNSET
    product_groups: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        full_name = self.full_name

        culture_code = self.culture_code

        email = self.email

        roles: Union[Unset, list[str]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles



        levels: Union[Unset, list[str]] = UNSET
        if not isinstance(self.levels, Unset):
            levels = self.levels



        product_groups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.product_groups, Unset):
            product_groups = self.product_groups




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if full_name is not UNSET:
            field_dict["fullName"] = full_name
        if culture_code is not UNSET:
            field_dict["cultureCode"] = culture_code
        if email is not UNSET:
            field_dict["email"] = email
        if roles is not UNSET:
            field_dict["roles"] = roles
        if levels is not UNSET:
            field_dict["levels"] = levels
        if product_groups is not UNSET:
            field_dict["productGroups"] = product_groups

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        full_name = d.pop("fullName", UNSET)

        culture_code = d.pop("cultureCode", UNSET)

        email = d.pop("email", UNSET)

        roles = cast(list[str], d.pop("roles", UNSET))


        levels = cast(list[str], d.pop("levels", UNSET))


        product_groups = cast(list[str], d.pop("productGroups", UNSET))


        virinco_wats_configuration_common_user_settings = cls(
            full_name=full_name,
            culture_code=culture_code,
            email=email,
            roles=roles,
            levels=levels,
            product_groups=product_groups,
        )


        virinco_wats_configuration_common_user_settings.additional_properties = d
        return virinco_wats_configuration_common_user_settings

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
