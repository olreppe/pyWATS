from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_user import VirincoWATSWebDashboardModelsTdmUser
  from ..models.virinco_wats_web_dashboard_models_tdm_dto_user_settings import VirincoWATSWebDashboardModelsTdmDtoUserSettings
  from ..models.virinco_wats_web_dashboard_models_tdm_reporting_common_settings import VirincoWATSWebDashboardModelsTdmReportingCommonSettings
  from ..models.virinco_wats_web_dashboard_models_tdm_system_language import VirincoWATSWebDashboardModelsTdmSystemLanguage
  from ..models.virinco_wats_web_dashboard_models_tdm_wats_common_settings import VirincoWATSWebDashboardModelsTdmWatsCommonSettings
  from ..models.virinco_wats_web_dashboard_models_binary_data import VirincoWATSWebDashboardModelsBinaryData





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmMySettingsUser")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmMySettingsUser:
    """ Wrapper model used for updating user settings, used in conjunction with My Settings

        Attributes:
            signature_binary_data (Union[Unset, VirincoWATSWebDashboardModelsBinaryData]):
            user_theme (Union[Unset, int]):
            user (Union[Unset, VirincoWATSWebDashboardModelsTdmUser]): DTO - User (data transfer object)
            user_settings (Union[Unset, VirincoWATSWebDashboardModelsTdmDtoUserSettings]): DTO - UserSettings (data transfer
                object)
            wats_common_settings (Union[Unset, VirincoWATSWebDashboardModelsTdmWatsCommonSettings]):
            reporting_common_settings (Union[Unset, VirincoWATSWebDashboardModelsTdmReportingCommonSettings]):
            language (Union[Unset, VirincoWATSWebDashboardModelsTdmSystemLanguage]):
     """

    signature_binary_data: Union[Unset, 'VirincoWATSWebDashboardModelsBinaryData'] = UNSET
    user_theme: Union[Unset, int] = UNSET
    user: Union[Unset, 'VirincoWATSWebDashboardModelsTdmUser'] = UNSET
    user_settings: Union[Unset, 'VirincoWATSWebDashboardModelsTdmDtoUserSettings'] = UNSET
    wats_common_settings: Union[Unset, 'VirincoWATSWebDashboardModelsTdmWatsCommonSettings'] = UNSET
    reporting_common_settings: Union[Unset, 'VirincoWATSWebDashboardModelsTdmReportingCommonSettings'] = UNSET
    language: Union[Unset, 'VirincoWATSWebDashboardModelsTdmSystemLanguage'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_user import VirincoWATSWebDashboardModelsTdmUser
        from ..models.virinco_wats_web_dashboard_models_tdm_dto_user_settings import VirincoWATSWebDashboardModelsTdmDtoUserSettings
        from ..models.virinco_wats_web_dashboard_models_tdm_reporting_common_settings import VirincoWATSWebDashboardModelsTdmReportingCommonSettings
        from ..models.virinco_wats_web_dashboard_models_tdm_system_language import VirincoWATSWebDashboardModelsTdmSystemLanguage
        from ..models.virinco_wats_web_dashboard_models_tdm_wats_common_settings import VirincoWATSWebDashboardModelsTdmWatsCommonSettings
        from ..models.virinco_wats_web_dashboard_models_binary_data import VirincoWATSWebDashboardModelsBinaryData
        signature_binary_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.signature_binary_data, Unset):
            signature_binary_data = self.signature_binary_data.to_dict()

        user_theme = self.user_theme

        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        user_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_settings, Unset):
            user_settings = self.user_settings.to_dict()

        wats_common_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.wats_common_settings, Unset):
            wats_common_settings = self.wats_common_settings.to_dict()

        reporting_common_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.reporting_common_settings, Unset):
            reporting_common_settings = self.reporting_common_settings.to_dict()

        language: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.language, Unset):
            language = self.language.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if signature_binary_data is not UNSET:
            field_dict["SignatureBinaryData"] = signature_binary_data
        if user_theme is not UNSET:
            field_dict["UserTheme"] = user_theme
        if user is not UNSET:
            field_dict["User"] = user
        if user_settings is not UNSET:
            field_dict["UserSettings"] = user_settings
        if wats_common_settings is not UNSET:
            field_dict["WatsCommonSettings"] = wats_common_settings
        if reporting_common_settings is not UNSET:
            field_dict["ReportingCommonSettings"] = reporting_common_settings
        if language is not UNSET:
            field_dict["Language"] = language

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_user import VirincoWATSWebDashboardModelsTdmUser
        from ..models.virinco_wats_web_dashboard_models_tdm_dto_user_settings import VirincoWATSWebDashboardModelsTdmDtoUserSettings
        from ..models.virinco_wats_web_dashboard_models_tdm_reporting_common_settings import VirincoWATSWebDashboardModelsTdmReportingCommonSettings
        from ..models.virinco_wats_web_dashboard_models_tdm_system_language import VirincoWATSWebDashboardModelsTdmSystemLanguage
        from ..models.virinco_wats_web_dashboard_models_tdm_wats_common_settings import VirincoWATSWebDashboardModelsTdmWatsCommonSettings
        from ..models.virinco_wats_web_dashboard_models_binary_data import VirincoWATSWebDashboardModelsBinaryData
        d = dict(src_dict)
        _signature_binary_data = d.pop("SignatureBinaryData", UNSET)
        signature_binary_data: Union[Unset, VirincoWATSWebDashboardModelsBinaryData]
        if isinstance(_signature_binary_data,  Unset):
            signature_binary_data = UNSET
        else:
            signature_binary_data = VirincoWATSWebDashboardModelsBinaryData.from_dict(_signature_binary_data)




        user_theme = d.pop("UserTheme", UNSET)

        _user = d.pop("User", UNSET)
        user: Union[Unset, VirincoWATSWebDashboardModelsTdmUser]
        if isinstance(_user,  Unset):
            user = UNSET
        else:
            user = VirincoWATSWebDashboardModelsTdmUser.from_dict(_user)




        _user_settings = d.pop("UserSettings", UNSET)
        user_settings: Union[Unset, VirincoWATSWebDashboardModelsTdmDtoUserSettings]
        if isinstance(_user_settings,  Unset):
            user_settings = UNSET
        else:
            user_settings = VirincoWATSWebDashboardModelsTdmDtoUserSettings.from_dict(_user_settings)




        _wats_common_settings = d.pop("WatsCommonSettings", UNSET)
        wats_common_settings: Union[Unset, VirincoWATSWebDashboardModelsTdmWatsCommonSettings]
        if isinstance(_wats_common_settings,  Unset):
            wats_common_settings = UNSET
        else:
            wats_common_settings = VirincoWATSWebDashboardModelsTdmWatsCommonSettings.from_dict(_wats_common_settings)




        _reporting_common_settings = d.pop("ReportingCommonSettings", UNSET)
        reporting_common_settings: Union[Unset, VirincoWATSWebDashboardModelsTdmReportingCommonSettings]
        if isinstance(_reporting_common_settings,  Unset):
            reporting_common_settings = UNSET
        else:
            reporting_common_settings = VirincoWATSWebDashboardModelsTdmReportingCommonSettings.from_dict(_reporting_common_settings)




        _language = d.pop("Language", UNSET)
        language: Union[Unset, VirincoWATSWebDashboardModelsTdmSystemLanguage]
        if isinstance(_language,  Unset):
            language = UNSET
        else:
            language = VirincoWATSWebDashboardModelsTdmSystemLanguage.from_dict(_language)




        virinco_wats_web_dashboard_models_tdm_my_settings_user = cls(
            signature_binary_data=signature_binary_data,
            user_theme=user_theme,
            user=user,
            user_settings=user_settings,
            wats_common_settings=wats_common_settings,
            reporting_common_settings=reporting_common_settings,
            language=language,
        )


        virinco_wats_web_dashboard_models_tdm_my_settings_user.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_my_settings_user

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
