from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmMessageUser")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmMessageUser:
    """ 
        Attributes:
            user_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            message_id (Union[Unset, int]):
            postponed_until (Union[Unset, datetime.datetime]):
            hidden (Union[Unset, bool]):
     """

    user_id: Union[Unset, UUID] = UNSET
    message_id: Union[Unset, int] = UNSET
    postponed_until: Union[Unset, datetime.datetime] = UNSET
    hidden: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        user_id: Union[Unset, str] = UNSET
        if not isinstance(self.user_id, Unset):
            user_id = str(self.user_id)

        message_id = self.message_id

        postponed_until: Union[Unset, str] = UNSET
        if not isinstance(self.postponed_until, Unset):
            postponed_until = self.postponed_until.isoformat()

        hidden = self.hidden


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if message_id is not UNSET:
            field_dict["messageId"] = message_id
        if postponed_until is not UNSET:
            field_dict["postponedUntil"] = postponed_until
        if hidden is not UNSET:
            field_dict["hidden"] = hidden

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _user_id = d.pop("userId", UNSET)
        user_id: Union[Unset, UUID]
        if isinstance(_user_id,  Unset):
            user_id = UNSET
        else:
            user_id = UUID(_user_id)




        message_id = d.pop("messageId", UNSET)

        _postponed_until = d.pop("postponedUntil", UNSET)
        postponed_until: Union[Unset, datetime.datetime]
        if isinstance(_postponed_until,  Unset):
            postponed_until = UNSET
        else:
            postponed_until = isoparse(_postponed_until)




        hidden = d.pop("hidden", UNSET)

        virinco_wats_web_dashboard_models_tdm_message_user = cls(
            user_id=user_id,
            message_id=message_id,
            postponed_until=postponed_until,
            hidden=hidden,
        )


        virinco_wats_web_dashboard_models_tdm_message_user.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_message_user

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
