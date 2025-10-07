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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmClientLog")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmClientLog:
    """ 
        Attributes:
            client_log_id (Union[Unset, int]):
            client_id (Union[Unset, int]):
            log_date (Union[Unset, datetime.datetime]):
            user_name (Union[Unset, str]):
            text (Union[Unset, str]):
     """

    client_log_id: Union[Unset, int] = UNSET
    client_id: Union[Unset, int] = UNSET
    log_date: Union[Unset, datetime.datetime] = UNSET
    user_name: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        client_log_id = self.client_log_id

        client_id = self.client_id

        log_date: Union[Unset, str] = UNSET
        if not isinstance(self.log_date, Unset):
            log_date = self.log_date.isoformat()

        user_name = self.user_name

        text = self.text


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if client_log_id is not UNSET:
            field_dict["clientLogId"] = client_log_id
        if client_id is not UNSET:
            field_dict["clientId"] = client_id
        if log_date is not UNSET:
            field_dict["logDate"] = log_date
        if user_name is not UNSET:
            field_dict["userName"] = user_name
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_log_id = d.pop("clientLogId", UNSET)

        client_id = d.pop("clientId", UNSET)

        _log_date = d.pop("logDate", UNSET)
        log_date: Union[Unset, datetime.datetime]
        if isinstance(_log_date,  Unset):
            log_date = UNSET
        else:
            log_date = isoparse(_log_date)




        user_name = d.pop("userName", UNSET)

        text = d.pop("text", UNSET)

        virinco_wats_web_dashboard_models_tdm_client_log = cls(
            client_log_id=client_log_id,
            client_id=client_id,
            log_date=log_date,
            user_name=user_name,
            text=text,
        )


        virinco_wats_web_dashboard_models_tdm_client_log.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_client_log

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
