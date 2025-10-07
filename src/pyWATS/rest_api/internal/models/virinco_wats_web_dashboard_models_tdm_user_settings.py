from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_application_user import VirincoWATSWebDashboardModelsTdmApplicationUser





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmUserSettings")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmUserSettings:
    """ 
        Attributes:
            user_id (Union[Unset, str]):
            user (Union[Unset, VirincoWATSWebDashboardModelsTdmApplicationUser]):
            culture_code (Union[Unset, str]):
            default_from_date (Union[Unset, str]):
            default_from_date_ticks (Union[Unset, int]):
            signature_binary_data_guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
     """

    user_id: Union[Unset, str] = UNSET
    user: Union[Unset, 'VirincoWATSWebDashboardModelsTdmApplicationUser'] = UNSET
    culture_code: Union[Unset, str] = UNSET
    default_from_date: Union[Unset, str] = UNSET
    default_from_date_ticks: Union[Unset, int] = UNSET
    signature_binary_data_guid: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_application_user import VirincoWATSWebDashboardModelsTdmApplicationUser
        user_id = self.user_id

        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        culture_code = self.culture_code

        default_from_date = self.default_from_date

        default_from_date_ticks = self.default_from_date_ticks

        signature_binary_data_guid: Union[Unset, str] = UNSET
        if not isinstance(self.signature_binary_data_guid, Unset):
            signature_binary_data_guid = str(self.signature_binary_data_guid)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if user is not UNSET:
            field_dict["User"] = user
        if culture_code is not UNSET:
            field_dict["CultureCode"] = culture_code
        if default_from_date is not UNSET:
            field_dict["DefaultFromDate"] = default_from_date
        if default_from_date_ticks is not UNSET:
            field_dict["DefaultFromDateTicks"] = default_from_date_ticks
        if signature_binary_data_guid is not UNSET:
            field_dict["SignatureBinaryDataGUID"] = signature_binary_data_guid

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_application_user import VirincoWATSWebDashboardModelsTdmApplicationUser
        d = dict(src_dict)
        user_id = d.pop("UserId", UNSET)

        _user = d.pop("User", UNSET)
        user: Union[Unset, VirincoWATSWebDashboardModelsTdmApplicationUser]
        if isinstance(_user,  Unset):
            user = UNSET
        else:
            user = VirincoWATSWebDashboardModelsTdmApplicationUser.from_dict(_user)




        culture_code = d.pop("CultureCode", UNSET)

        default_from_date = d.pop("DefaultFromDate", UNSET)

        default_from_date_ticks = d.pop("DefaultFromDateTicks", UNSET)

        _signature_binary_data_guid = d.pop("SignatureBinaryDataGUID", UNSET)
        signature_binary_data_guid: Union[Unset, UUID]
        if isinstance(_signature_binary_data_guid,  Unset):
            signature_binary_data_guid = UNSET
        else:
            signature_binary_data_guid = UUID(_signature_binary_data_guid)




        virinco_wats_web_dashboard_models_tdm_user_settings = cls(
            user_id=user_id,
            user=user,
            culture_code=culture_code,
            default_from_date=default_from_date,
            default_from_date_ticks=default_from_date_ticks,
            signature_binary_data_guid=signature_binary_data_guid,
        )


        virinco_wats_web_dashboard_models_tdm_user_settings.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_user_settings

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
