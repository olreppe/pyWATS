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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsProcsTransferClientLog")



@_attrs_define
class VirincoWATSWebDashboardModelsProcsTransferClientLog:
    """ 
        Attributes:
            client_id (Union[Unset, int]):
            log_id (Union[Unset, int]):
            category (Union[Unset, int]):
            severity (Union[Unset, int]):
            log_date (Union[Unset, datetime.datetime]):
            item_type (Union[Unset, int]):
            item_guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            total_time (Union[Unset, float]):
            module_time (Union[Unset, float]):
            external_time (Union[Unset, float]):
            description (Union[Unset, str]):
            exception_details (Union[Unset, str]):
            comment (Union[Unset, str]):
     """

    client_id: Union[Unset, int] = UNSET
    log_id: Union[Unset, int] = UNSET
    category: Union[Unset, int] = UNSET
    severity: Union[Unset, int] = UNSET
    log_date: Union[Unset, datetime.datetime] = UNSET
    item_type: Union[Unset, int] = UNSET
    item_guid: Union[Unset, UUID] = UNSET
    total_time: Union[Unset, float] = UNSET
    module_time: Union[Unset, float] = UNSET
    external_time: Union[Unset, float] = UNSET
    description: Union[Unset, str] = UNSET
    exception_details: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        log_id = self.log_id

        category = self.category

        severity = self.severity

        log_date: Union[Unset, str] = UNSET
        if not isinstance(self.log_date, Unset):
            log_date = self.log_date.isoformat()

        item_type = self.item_type

        item_guid: Union[Unset, str] = UNSET
        if not isinstance(self.item_guid, Unset):
            item_guid = str(self.item_guid)

        total_time = self.total_time

        module_time = self.module_time

        external_time = self.external_time

        description = self.description

        exception_details = self.exception_details

        comment = self.comment


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if client_id is not UNSET:
            field_dict["ClientId"] = client_id
        if log_id is not UNSET:
            field_dict["LogId"] = log_id
        if category is not UNSET:
            field_dict["Category"] = category
        if severity is not UNSET:
            field_dict["Severity"] = severity
        if log_date is not UNSET:
            field_dict["LogDate"] = log_date
        if item_type is not UNSET:
            field_dict["ItemType"] = item_type
        if item_guid is not UNSET:
            field_dict["ItemGuid"] = item_guid
        if total_time is not UNSET:
            field_dict["TotalTime"] = total_time
        if module_time is not UNSET:
            field_dict["ModuleTime"] = module_time
        if external_time is not UNSET:
            field_dict["ExternalTime"] = external_time
        if description is not UNSET:
            field_dict["Description"] = description
        if exception_details is not UNSET:
            field_dict["ExceptionDetails"] = exception_details
        if comment is not UNSET:
            field_dict["Comment"] = comment

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_id = d.pop("ClientId", UNSET)

        log_id = d.pop("LogId", UNSET)

        category = d.pop("Category", UNSET)

        severity = d.pop("Severity", UNSET)

        _log_date = d.pop("LogDate", UNSET)
        log_date: Union[Unset, datetime.datetime]
        if isinstance(_log_date,  Unset):
            log_date = UNSET
        else:
            log_date = isoparse(_log_date)




        item_type = d.pop("ItemType", UNSET)

        _item_guid = d.pop("ItemGuid", UNSET)
        item_guid: Union[Unset, UUID]
        if isinstance(_item_guid,  Unset):
            item_guid = UNSET
        else:
            item_guid = UUID(_item_guid)




        total_time = d.pop("TotalTime", UNSET)

        module_time = d.pop("ModuleTime", UNSET)

        external_time = d.pop("ExternalTime", UNSET)

        description = d.pop("Description", UNSET)

        exception_details = d.pop("ExceptionDetails", UNSET)

        comment = d.pop("Comment", UNSET)

        virinco_wats_web_dashboard_models_procs_transfer_client_log = cls(
            client_id=client_id,
            log_id=log_id,
            category=category,
            severity=severity,
            log_date=log_date,
            item_type=item_type,
            item_guid=item_guid,
            total_time=total_time,
            module_time=module_time,
            external_time=external_time,
            description=description,
            exception_details=exception_details,
            comment=comment,
        )


        virinco_wats_web_dashboard_models_procs_transfer_client_log.additional_properties = d
        return virinco_wats_web_dashboard_models_procs_transfer_client_log

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
