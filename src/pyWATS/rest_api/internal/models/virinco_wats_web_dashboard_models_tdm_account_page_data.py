from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_account_subscription_plan import VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlan
  from ..models.virinco_wats_web_dashboard_models_tdm_account_server_overview import VirincoWATSWebDashboardModelsTdmAccountServerOverview
  from ..models.virinco_wats_web_dashboard_models_tdm_account_security_settings import VirincoWATSWebDashboardModelsTdmAccountSecuritySettings
  from ..models.virinco_wats_web_dashboard_models_tdm_account_admin_settings import VirincoWATSWebDashboardModelsTdmAccountAdminSettings
  from ..models.virinco_wats_web_dashboard_models_tdm_system_settings import VirincoWATSWebDashboardModelsTdmSystemSettings





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmAccountPageData")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmAccountPageData:
    """ 
        Attributes:
            subscription_plan (Union[Unset, VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlan]):
            server_overview (Union[Unset, VirincoWATSWebDashboardModelsTdmAccountServerOverview]):
            security_settings (Union[Unset, VirincoWATSWebDashboardModelsTdmAccountSecuritySettings]):
            admin_settings (Union[Unset, VirincoWATSWebDashboardModelsTdmAccountAdminSettings]):
            system_settings (Union[Unset, VirincoWATSWebDashboardModelsTdmSystemSettings]):
     """

    subscription_plan: Union[Unset, 'VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlan'] = UNSET
    server_overview: Union[Unset, 'VirincoWATSWebDashboardModelsTdmAccountServerOverview'] = UNSET
    security_settings: Union[Unset, 'VirincoWATSWebDashboardModelsTdmAccountSecuritySettings'] = UNSET
    admin_settings: Union[Unset, 'VirincoWATSWebDashboardModelsTdmAccountAdminSettings'] = UNSET
    system_settings: Union[Unset, 'VirincoWATSWebDashboardModelsTdmSystemSettings'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_account_subscription_plan import VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlan
        from ..models.virinco_wats_web_dashboard_models_tdm_account_server_overview import VirincoWATSWebDashboardModelsTdmAccountServerOverview
        from ..models.virinco_wats_web_dashboard_models_tdm_account_security_settings import VirincoWATSWebDashboardModelsTdmAccountSecuritySettings
        from ..models.virinco_wats_web_dashboard_models_tdm_account_admin_settings import VirincoWATSWebDashboardModelsTdmAccountAdminSettings
        from ..models.virinco_wats_web_dashboard_models_tdm_system_settings import VirincoWATSWebDashboardModelsTdmSystemSettings
        subscription_plan: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.subscription_plan, Unset):
            subscription_plan = self.subscription_plan.to_dict()

        server_overview: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.server_overview, Unset):
            server_overview = self.server_overview.to_dict()

        security_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.security_settings, Unset):
            security_settings = self.security_settings.to_dict()

        admin_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.admin_settings, Unset):
            admin_settings = self.admin_settings.to_dict()

        system_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.system_settings, Unset):
            system_settings = self.system_settings.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if subscription_plan is not UNSET:
            field_dict["subscriptionPlan"] = subscription_plan
        if server_overview is not UNSET:
            field_dict["serverOverview"] = server_overview
        if security_settings is not UNSET:
            field_dict["securitySettings"] = security_settings
        if admin_settings is not UNSET:
            field_dict["adminSettings"] = admin_settings
        if system_settings is not UNSET:
            field_dict["systemSettings"] = system_settings

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_account_subscription_plan import VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlan
        from ..models.virinco_wats_web_dashboard_models_tdm_account_server_overview import VirincoWATSWebDashboardModelsTdmAccountServerOverview
        from ..models.virinco_wats_web_dashboard_models_tdm_account_security_settings import VirincoWATSWebDashboardModelsTdmAccountSecuritySettings
        from ..models.virinco_wats_web_dashboard_models_tdm_account_admin_settings import VirincoWATSWebDashboardModelsTdmAccountAdminSettings
        from ..models.virinco_wats_web_dashboard_models_tdm_system_settings import VirincoWATSWebDashboardModelsTdmSystemSettings
        d = dict(src_dict)
        _subscription_plan = d.pop("subscriptionPlan", UNSET)
        subscription_plan: Union[Unset, VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlan]
        if isinstance(_subscription_plan,  Unset):
            subscription_plan = UNSET
        else:
            subscription_plan = VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlan.from_dict(_subscription_plan)




        _server_overview = d.pop("serverOverview", UNSET)
        server_overview: Union[Unset, VirincoWATSWebDashboardModelsTdmAccountServerOverview]
        if isinstance(_server_overview,  Unset):
            server_overview = UNSET
        else:
            server_overview = VirincoWATSWebDashboardModelsTdmAccountServerOverview.from_dict(_server_overview)




        _security_settings = d.pop("securitySettings", UNSET)
        security_settings: Union[Unset, VirincoWATSWebDashboardModelsTdmAccountSecuritySettings]
        if isinstance(_security_settings,  Unset):
            security_settings = UNSET
        else:
            security_settings = VirincoWATSWebDashboardModelsTdmAccountSecuritySettings.from_dict(_security_settings)




        _admin_settings = d.pop("adminSettings", UNSET)
        admin_settings: Union[Unset, VirincoWATSWebDashboardModelsTdmAccountAdminSettings]
        if isinstance(_admin_settings,  Unset):
            admin_settings = UNSET
        else:
            admin_settings = VirincoWATSWebDashboardModelsTdmAccountAdminSettings.from_dict(_admin_settings)




        _system_settings = d.pop("systemSettings", UNSET)
        system_settings: Union[Unset, VirincoWATSWebDashboardModelsTdmSystemSettings]
        if isinstance(_system_settings,  Unset):
            system_settings = UNSET
        else:
            system_settings = VirincoWATSWebDashboardModelsTdmSystemSettings.from_dict(_system_settings)




        virinco_wats_web_dashboard_models_tdm_account_page_data = cls(
            subscription_plan=subscription_plan,
            server_overview=server_overview,
            security_settings=security_settings,
            admin_settings=admin_settings,
            system_settings=system_settings,
        )


        virinco_wats_web_dashboard_models_tdm_account_page_data.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_account_page_data

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
