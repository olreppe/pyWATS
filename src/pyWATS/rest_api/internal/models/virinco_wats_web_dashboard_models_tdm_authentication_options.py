from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_tdm_authentication_options_authentication_type import VirincoWATSWebDashboardModelsTdmAuthenticationOptionsAuthenticationType
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmAuthenticationOptions")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmAuthenticationOptions:
    """ 
        Attributes:
            active (Union[Unset, bool]):
            is_default_authentication (Union[Unset, bool]):
            authentication_type_name (Union[Unset, str]):
            authentication_type_description (Union[Unset, str]):
            authentication_type (Union[Unset, VirincoWATSWebDashboardModelsTdmAuthenticationOptionsAuthenticationType]):
     """

    active: Union[Unset, bool] = UNSET
    is_default_authentication: Union[Unset, bool] = UNSET
    authentication_type_name: Union[Unset, str] = UNSET
    authentication_type_description: Union[Unset, str] = UNSET
    authentication_type: Union[Unset, VirincoWATSWebDashboardModelsTdmAuthenticationOptionsAuthenticationType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        active = self.active

        is_default_authentication = self.is_default_authentication

        authentication_type_name = self.authentication_type_name

        authentication_type_description = self.authentication_type_description

        authentication_type: Union[Unset, int] = UNSET
        if not isinstance(self.authentication_type, Unset):
            authentication_type = self.authentication_type.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if active is not UNSET:
            field_dict["active"] = active
        if is_default_authentication is not UNSET:
            field_dict["isDefaultAuthentication"] = is_default_authentication
        if authentication_type_name is not UNSET:
            field_dict["authenticationTypeName"] = authentication_type_name
        if authentication_type_description is not UNSET:
            field_dict["authenticationTypeDescription"] = authentication_type_description
        if authentication_type is not UNSET:
            field_dict["authenticationType"] = authentication_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active = d.pop("active", UNSET)

        is_default_authentication = d.pop("isDefaultAuthentication", UNSET)

        authentication_type_name = d.pop("authenticationTypeName", UNSET)

        authentication_type_description = d.pop("authenticationTypeDescription", UNSET)

        _authentication_type = d.pop("authenticationType", UNSET)
        authentication_type: Union[Unset, VirincoWATSWebDashboardModelsTdmAuthenticationOptionsAuthenticationType]
        if isinstance(_authentication_type,  Unset):
            authentication_type = UNSET
        else:
            authentication_type = VirincoWATSWebDashboardModelsTdmAuthenticationOptionsAuthenticationType(_authentication_type)




        virinco_wats_web_dashboard_models_tdm_authentication_options = cls(
            active=active,
            is_default_authentication=is_default_authentication,
            authentication_type_name=authentication_type_name,
            authentication_type_description=authentication_type_description,
            authentication_type=authentication_type,
        )


        virinco_wats_web_dashboard_models_tdm_authentication_options.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_authentication_options

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
