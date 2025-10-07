from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsLoginViewModel")



@_attrs_define
class VirincoWATSWebDashboardModelsLoginViewModel:
    """ 
        Attributes:
            eula_required (Union[Unset, bool]):
            email (Union[Unset, str]):
            two_factor_enabled (Union[Unset, bool]):
            two_factor_code (Union[Unset, str]):
            username (Union[Unset, str]):
            password (Union[Unset, str]):
            remember_me (Union[Unset, bool]):
            return_url (Union[Unset, str]):
            global_2_fa_enabled (Union[Unset, bool]):
            wats_login_enabled (Union[Unset, bool]):
            aad_login_enabled (Union[Unset, bool]):
            local_ad_login_enabled (Union[Unset, bool]):
            custom_sso_login_enabled (Union[Unset, bool]):
            custom_sso_name (Union[Unset, str]):
            request_access_enabled (Union[Unset, bool]):
            reset_password_enabled (Union[Unset, bool]):
            recaptcha (Union[Unset, bool]):
     """

    eula_required: Union[Unset, bool] = UNSET
    email: Union[Unset, str] = UNSET
    two_factor_enabled: Union[Unset, bool] = UNSET
    two_factor_code: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    remember_me: Union[Unset, bool] = UNSET
    return_url: Union[Unset, str] = UNSET
    global_2_fa_enabled: Union[Unset, bool] = UNSET
    wats_login_enabled: Union[Unset, bool] = UNSET
    aad_login_enabled: Union[Unset, bool] = UNSET
    local_ad_login_enabled: Union[Unset, bool] = UNSET
    custom_sso_login_enabled: Union[Unset, bool] = UNSET
    custom_sso_name: Union[Unset, str] = UNSET
    request_access_enabled: Union[Unset, bool] = UNSET
    reset_password_enabled: Union[Unset, bool] = UNSET
    recaptcha: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        eula_required = self.eula_required

        email = self.email

        two_factor_enabled = self.two_factor_enabled

        two_factor_code = self.two_factor_code

        username = self.username

        password = self.password

        remember_me = self.remember_me

        return_url = self.return_url

        global_2_fa_enabled = self.global_2_fa_enabled

        wats_login_enabled = self.wats_login_enabled

        aad_login_enabled = self.aad_login_enabled

        local_ad_login_enabled = self.local_ad_login_enabled

        custom_sso_login_enabled = self.custom_sso_login_enabled

        custom_sso_name = self.custom_sso_name

        request_access_enabled = self.request_access_enabled

        reset_password_enabled = self.reset_password_enabled

        recaptcha = self.recaptcha


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if eula_required is not UNSET:
            field_dict["eulaRequired"] = eula_required
        if email is not UNSET:
            field_dict["email"] = email
        if two_factor_enabled is not UNSET:
            field_dict["twoFactorEnabled"] = two_factor_enabled
        if two_factor_code is not UNSET:
            field_dict["twoFactorCode"] = two_factor_code
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password
        if remember_me is not UNSET:
            field_dict["rememberMe"] = remember_me
        if return_url is not UNSET:
            field_dict["returnUrl"] = return_url
        if global_2_fa_enabled is not UNSET:
            field_dict["global2faEnabled"] = global_2_fa_enabled
        if wats_login_enabled is not UNSET:
            field_dict["watsLoginEnabled"] = wats_login_enabled
        if aad_login_enabled is not UNSET:
            field_dict["aadLoginEnabled"] = aad_login_enabled
        if local_ad_login_enabled is not UNSET:
            field_dict["localAdLoginEnabled"] = local_ad_login_enabled
        if custom_sso_login_enabled is not UNSET:
            field_dict["customSsoLoginEnabled"] = custom_sso_login_enabled
        if custom_sso_name is not UNSET:
            field_dict["customSsoName"] = custom_sso_name
        if request_access_enabled is not UNSET:
            field_dict["requestAccessEnabled"] = request_access_enabled
        if reset_password_enabled is not UNSET:
            field_dict["resetPasswordEnabled"] = reset_password_enabled
        if recaptcha is not UNSET:
            field_dict["recaptcha"] = recaptcha

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        eula_required = d.pop("eulaRequired", UNSET)

        email = d.pop("email", UNSET)

        two_factor_enabled = d.pop("twoFactorEnabled", UNSET)

        two_factor_code = d.pop("twoFactorCode", UNSET)

        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        remember_me = d.pop("rememberMe", UNSET)

        return_url = d.pop("returnUrl", UNSET)

        global_2_fa_enabled = d.pop("global2faEnabled", UNSET)

        wats_login_enabled = d.pop("watsLoginEnabled", UNSET)

        aad_login_enabled = d.pop("aadLoginEnabled", UNSET)

        local_ad_login_enabled = d.pop("localAdLoginEnabled", UNSET)

        custom_sso_login_enabled = d.pop("customSsoLoginEnabled", UNSET)

        custom_sso_name = d.pop("customSsoName", UNSET)

        request_access_enabled = d.pop("requestAccessEnabled", UNSET)

        reset_password_enabled = d.pop("resetPasswordEnabled", UNSET)

        recaptcha = d.pop("recaptcha", UNSET)

        virinco_wats_web_dashboard_models_login_view_model = cls(
            eula_required=eula_required,
            email=email,
            two_factor_enabled=two_factor_enabled,
            two_factor_code=two_factor_code,
            username=username,
            password=password,
            remember_me=remember_me,
            return_url=return_url,
            global_2_fa_enabled=global_2_fa_enabled,
            wats_login_enabled=wats_login_enabled,
            aad_login_enabled=aad_login_enabled,
            local_ad_login_enabled=local_ad_login_enabled,
            custom_sso_login_enabled=custom_sso_login_enabled,
            custom_sso_name=custom_sso_name,
            request_access_enabled=request_access_enabled,
            reset_password_enabled=reset_password_enabled,
            recaptcha=recaptcha,
        )


        virinco_wats_web_dashboard_models_login_view_model.additional_properties = d
        return virinco_wats_web_dashboard_models_login_view_model

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
