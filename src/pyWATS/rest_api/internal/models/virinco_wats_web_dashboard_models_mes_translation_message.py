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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesTranslationMessage")



@_attrs_define
class VirincoWATSWebDashboardModelsMesTranslationMessage:
    """ 
        Attributes:
            message_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            english_text (Union[Unset, str]):
            parameters (Union[Unset, int]):
            type_ (Union[Unset, int]):
            created (Union[Unset, datetime.datetime]):
            request_date (Union[Unset, datetime.datetime]):
            request_count (Union[Unset, int]):
            hash_code (Union[Unset, str]):
     """

    message_id: Union[Unset, UUID] = UNSET
    english_text: Union[Unset, str] = UNSET
    parameters: Union[Unset, int] = UNSET
    type_: Union[Unset, int] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    request_date: Union[Unset, datetime.datetime] = UNSET
    request_count: Union[Unset, int] = UNSET
    hash_code: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        message_id: Union[Unset, str] = UNSET
        if not isinstance(self.message_id, Unset):
            message_id = str(self.message_id)

        english_text = self.english_text

        parameters = self.parameters

        type_ = self.type_

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        request_date: Union[Unset, str] = UNSET
        if not isinstance(self.request_date, Unset):
            request_date = self.request_date.isoformat()

        request_count = self.request_count

        hash_code = self.hash_code


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if message_id is not UNSET:
            field_dict["messageId"] = message_id
        if english_text is not UNSET:
            field_dict["englishText"] = english_text
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if type_ is not UNSET:
            field_dict["type"] = type_
        if created is not UNSET:
            field_dict["created"] = created
        if request_date is not UNSET:
            field_dict["requestDate"] = request_date
        if request_count is not UNSET:
            field_dict["requestCount"] = request_count
        if hash_code is not UNSET:
            field_dict["hashCode"] = hash_code

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _message_id = d.pop("messageId", UNSET)
        message_id: Union[Unset, UUID]
        if isinstance(_message_id,  Unset):
            message_id = UNSET
        else:
            message_id = UUID(_message_id)




        english_text = d.pop("englishText", UNSET)

        parameters = d.pop("parameters", UNSET)

        type_ = d.pop("type", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created,  Unset):
            created = UNSET
        else:
            created = isoparse(_created)




        _request_date = d.pop("requestDate", UNSET)
        request_date: Union[Unset, datetime.datetime]
        if isinstance(_request_date,  Unset):
            request_date = UNSET
        else:
            request_date = isoparse(_request_date)




        request_count = d.pop("requestCount", UNSET)

        hash_code = d.pop("hashCode", UNSET)

        virinco_wats_web_dashboard_models_mes_translation_message = cls(
            message_id=message_id,
            english_text=english_text,
            parameters=parameters,
            type_=type_,
            created=created,
            request_date=request_date,
            request_count=request_count,
            hash_code=hash_code,
        )


        virinco_wats_web_dashboard_models_mes_translation_message.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_translation_message

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
