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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmMessage")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmMessage:
    """ 
        Attributes:
            message_id (Union[Unset, int]):
            syslog_id (Union[Unset, int]):
            created_by (Union[Unset, str]):
            created_date (Union[Unset, datetime.datetime]):
            created_date_formatted (Union[Unset, str]):
            schedule_start (Union[Unset, datetime.datetime]):
            schedule_end (Union[Unset, datetime.datetime]):
            description (Union[Unset, str]):
            text (Union[Unset, str]):
            url (Union[Unset, str]):
            category (Union[Unset, int]):
            severity (Union[Unset, int]):
            group (Union[Unset, str]):
            active (Union[Unset, bool]):
            responses (Union[Unset, str]):
            priority (Union[Unset, int]):
            ui_type (Union[Unset, int]): default = 0, popUp = 1, startPage = 2
            is_dismissable (Union[Unset, bool]):
     """

    message_id: Union[Unset, int] = UNSET
    syslog_id: Union[Unset, int] = UNSET
    created_by: Union[Unset, str] = UNSET
    created_date: Union[Unset, datetime.datetime] = UNSET
    created_date_formatted: Union[Unset, str] = UNSET
    schedule_start: Union[Unset, datetime.datetime] = UNSET
    schedule_end: Union[Unset, datetime.datetime] = UNSET
    description: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    category: Union[Unset, int] = UNSET
    severity: Union[Unset, int] = UNSET
    group: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    responses: Union[Unset, str] = UNSET
    priority: Union[Unset, int] = UNSET
    ui_type: Union[Unset, int] = UNSET
    is_dismissable: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        message_id = self.message_id

        syslog_id = self.syslog_id

        created_by = self.created_by

        created_date: Union[Unset, str] = UNSET
        if not isinstance(self.created_date, Unset):
            created_date = self.created_date.isoformat()

        created_date_formatted = self.created_date_formatted

        schedule_start: Union[Unset, str] = UNSET
        if not isinstance(self.schedule_start, Unset):
            schedule_start = self.schedule_start.isoformat()

        schedule_end: Union[Unset, str] = UNSET
        if not isinstance(self.schedule_end, Unset):
            schedule_end = self.schedule_end.isoformat()

        description = self.description

        text = self.text

        url = self.url

        category = self.category

        severity = self.severity

        group = self.group

        active = self.active

        responses = self.responses

        priority = self.priority

        ui_type = self.ui_type

        is_dismissable = self.is_dismissable


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if message_id is not UNSET:
            field_dict["messageId"] = message_id
        if syslog_id is not UNSET:
            field_dict["syslogId"] = syslog_id
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if created_date_formatted is not UNSET:
            field_dict["createdDateFormatted"] = created_date_formatted
        if schedule_start is not UNSET:
            field_dict["scheduleStart"] = schedule_start
        if schedule_end is not UNSET:
            field_dict["scheduleEnd"] = schedule_end
        if description is not UNSET:
            field_dict["description"] = description
        if text is not UNSET:
            field_dict["text"] = text
        if url is not UNSET:
            field_dict["url"] = url
        if category is not UNSET:
            field_dict["category"] = category
        if severity is not UNSET:
            field_dict["severity"] = severity
        if group is not UNSET:
            field_dict["group"] = group
        if active is not UNSET:
            field_dict["active"] = active
        if responses is not UNSET:
            field_dict["responses"] = responses
        if priority is not UNSET:
            field_dict["priority"] = priority
        if ui_type is not UNSET:
            field_dict["uiType"] = ui_type
        if is_dismissable is not UNSET:
            field_dict["isDismissable"] = is_dismissable

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message_id = d.pop("messageId", UNSET)

        syslog_id = d.pop("syslogId", UNSET)

        created_by = d.pop("createdBy", UNSET)

        _created_date = d.pop("createdDate", UNSET)
        created_date: Union[Unset, datetime.datetime]
        if isinstance(_created_date,  Unset):
            created_date = UNSET
        else:
            created_date = isoparse(_created_date)




        created_date_formatted = d.pop("createdDateFormatted", UNSET)

        _schedule_start = d.pop("scheduleStart", UNSET)
        schedule_start: Union[Unset, datetime.datetime]
        if isinstance(_schedule_start,  Unset):
            schedule_start = UNSET
        else:
            schedule_start = isoparse(_schedule_start)




        _schedule_end = d.pop("scheduleEnd", UNSET)
        schedule_end: Union[Unset, datetime.datetime]
        if isinstance(_schedule_end,  Unset):
            schedule_end = UNSET
        else:
            schedule_end = isoparse(_schedule_end)




        description = d.pop("description", UNSET)

        text = d.pop("text", UNSET)

        url = d.pop("url", UNSET)

        category = d.pop("category", UNSET)

        severity = d.pop("severity", UNSET)

        group = d.pop("group", UNSET)

        active = d.pop("active", UNSET)

        responses = d.pop("responses", UNSET)

        priority = d.pop("priority", UNSET)

        ui_type = d.pop("uiType", UNSET)

        is_dismissable = d.pop("isDismissable", UNSET)

        virinco_wats_web_dashboard_models_tdm_message = cls(
            message_id=message_id,
            syslog_id=syslog_id,
            created_by=created_by,
            created_date=created_date,
            created_date_formatted=created_date_formatted,
            schedule_start=schedule_start,
            schedule_end=schedule_end,
            description=description,
            text=text,
            url=url,
            category=category,
            severity=severity,
            group=group,
            active=active,
            responses=responses,
            priority=priority,
            ui_type=ui_type,
            is_dismissable=is_dismissable,
        )


        virinco_wats_web_dashboard_models_tdm_message.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_message

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
