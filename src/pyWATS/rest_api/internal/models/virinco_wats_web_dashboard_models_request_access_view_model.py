from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsRequestAccessViewModel")



@_attrs_define
class VirincoWATSWebDashboardModelsRequestAccessViewModel:
    """ 
        Attributes:
            email (Union[Unset, str]):
            full_name (Union[Unset, str]):
            comment (Union[Unset, str]):
            recaptcha_token (Union[Unset, str]):
     """

    email: Union[Unset, str] = UNSET
    full_name: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    recaptcha_token: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        email = self.email

        full_name = self.full_name

        comment = self.comment

        recaptcha_token = self.recaptcha_token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if email is not UNSET:
            field_dict["email"] = email
        if full_name is not UNSET:
            field_dict["fullName"] = full_name
        if comment is not UNSET:
            field_dict["comment"] = comment
        if recaptcha_token is not UNSET:
            field_dict["recaptchaToken"] = recaptcha_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email", UNSET)

        full_name = d.pop("fullName", UNSET)

        comment = d.pop("comment", UNSET)

        recaptcha_token = d.pop("recaptchaToken", UNSET)

        virinco_wats_web_dashboard_models_request_access_view_model = cls(
            email=email,
            full_name=full_name,
            comment=comment,
            recaptcha_token=recaptcha_token,
        )


        virinco_wats_web_dashboard_models_request_access_view_model.additional_properties = d
        return virinco_wats_web_dashboard_models_request_access_view_model

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
