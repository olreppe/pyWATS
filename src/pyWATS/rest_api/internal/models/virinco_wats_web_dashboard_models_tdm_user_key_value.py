from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_application_user import VirincoWATSWebDashboardModelsTdmApplicationUser





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmUserKeyValue")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmUserKeyValue:
    """ 
        Attributes:
            user (Union[Unset, VirincoWATSWebDashboardModelsTdmApplicationUser]):
            user_id (Union[Unset, str]):
            key (Union[Unset, str]):
            value (Union[Unset, str]):
            last_updated (Union[Unset, datetime.datetime]):
     """

    user: Union[Unset, 'VirincoWATSWebDashboardModelsTdmApplicationUser'] = UNSET
    user_id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    last_updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_application_user import VirincoWATSWebDashboardModelsTdmApplicationUser
        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        user_id = self.user_id

        key = self.key

        value = self.value

        last_updated: Union[Unset, str] = UNSET
        if not isinstance(self.last_updated, Unset):
            last_updated = self.last_updated.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if user is not UNSET:
            field_dict["User"] = user
        if user_id is not UNSET:
            field_dict["UserId"] = user_id
        if key is not UNSET:
            field_dict["Key"] = key
        if value is not UNSET:
            field_dict["Value"] = value
        if last_updated is not UNSET:
            field_dict["LastUpdated"] = last_updated

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_application_user import VirincoWATSWebDashboardModelsTdmApplicationUser
        d = dict(src_dict)
        _user = d.pop("User", UNSET)
        user: Union[Unset, VirincoWATSWebDashboardModelsTdmApplicationUser]
        if isinstance(_user,  Unset):
            user = UNSET
        else:
            user = VirincoWATSWebDashboardModelsTdmApplicationUser.from_dict(_user)




        user_id = d.pop("UserId", UNSET)

        key = d.pop("Key", UNSET)

        value = d.pop("Value", UNSET)

        _last_updated = d.pop("LastUpdated", UNSET)
        last_updated: Union[Unset, datetime.datetime]
        if isinstance(_last_updated,  Unset):
            last_updated = UNSET
        else:
            last_updated = isoparse(_last_updated)




        virinco_wats_web_dashboard_models_tdm_user_key_value = cls(
            user=user,
            user_id=user_id,
            key=key,
            value=value,
            last_updated=last_updated,
        )


        virinco_wats_web_dashboard_models_tdm_user_key_value.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_user_key_value

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
