from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_authentication_options import VirincoWATSWebDashboardModelsTdmAuthenticationOptions





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmAccountSecuritySettings")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmAccountSecuritySettings:
    """ 
        Attributes:
            strict_password (Union[Unset, bool]):
            authentication_options (Union[Unset, list['VirincoWATSWebDashboardModelsTdmAuthenticationOptions']]):
            global_2fa_enabled (Union[Unset, bool]):
     """

    strict_password: Union[Unset, bool] = UNSET
    authentication_options: Union[Unset, list['VirincoWATSWebDashboardModelsTdmAuthenticationOptions']] = UNSET
    global_2fa_enabled: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_authentication_options import VirincoWATSWebDashboardModelsTdmAuthenticationOptions
        strict_password = self.strict_password

        authentication_options: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.authentication_options, Unset):
            authentication_options = []
            for authentication_options_item_data in self.authentication_options:
                authentication_options_item = authentication_options_item_data.to_dict()
                authentication_options.append(authentication_options_item)



        global_2fa_enabled = self.global_2fa_enabled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if strict_password is not UNSET:
            field_dict["strictPassword"] = strict_password
        if authentication_options is not UNSET:
            field_dict["authenticationOptions"] = authentication_options
        if global_2fa_enabled is not UNSET:
            field_dict["global2FAEnabled"] = global_2fa_enabled

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_authentication_options import VirincoWATSWebDashboardModelsTdmAuthenticationOptions
        d = dict(src_dict)
        strict_password = d.pop("strictPassword", UNSET)

        authentication_options = []
        _authentication_options = d.pop("authenticationOptions", UNSET)
        for authentication_options_item_data in (_authentication_options or []):
            authentication_options_item = VirincoWATSWebDashboardModelsTdmAuthenticationOptions.from_dict(authentication_options_item_data)



            authentication_options.append(authentication_options_item)


        global_2fa_enabled = d.pop("global2FAEnabled", UNSET)

        virinco_wats_web_dashboard_models_tdm_account_security_settings = cls(
            strict_password=strict_password,
            authentication_options=authentication_options,
            global_2fa_enabled=global_2fa_enabled,
        )


        virinco_wats_web_dashboard_models_tdm_account_security_settings.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_account_security_settings

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
