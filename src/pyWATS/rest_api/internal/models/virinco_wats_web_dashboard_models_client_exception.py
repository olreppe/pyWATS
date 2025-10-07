from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_client_exception_category import VirincoWATSWebDashboardModelsClientExceptionCategory
from ..models.virinco_wats_web_dashboard_models_client_exception_client_type import VirincoWATSWebDashboardModelsClientExceptionClientType
from ..models.virinco_wats_web_dashboard_models_client_exception_severity import VirincoWATSWebDashboardModelsClientExceptionSeverity
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsClientException")



@_attrs_define
class VirincoWATSWebDashboardModelsClientException:
    """ 
        Attributes:
            client_id (Union[Unset, int]):
            log_id (Union[Unset, int]):
            name (Union[Unset, str]):
            location (Union[Unset, str]):
            purpose (Union[Unset, str]):
            client_type (Union[Unset, VirincoWATSWebDashboardModelsClientExceptionClientType]):
            category (Union[Unset, VirincoWATSWebDashboardModelsClientExceptionCategory]):
            severity (Union[Unset, VirincoWATSWebDashboardModelsClientExceptionSeverity]):
            severity_text (Union[Unset, str]):
            log_date (Union[Unset, datetime.datetime]):
            description (Union[Unset, str]):
            exception_details (Union[Unset, str]):
            comment (Union[Unset, str]):
            item_guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
     """

    client_id: Union[Unset, int] = UNSET
    log_id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    client_type: Union[Unset, VirincoWATSWebDashboardModelsClientExceptionClientType] = UNSET
    category: Union[Unset, VirincoWATSWebDashboardModelsClientExceptionCategory] = UNSET
    severity: Union[Unset, VirincoWATSWebDashboardModelsClientExceptionSeverity] = UNSET
    severity_text: Union[Unset, str] = UNSET
    log_date: Union[Unset, datetime.datetime] = UNSET
    description: Union[Unset, str] = UNSET
    exception_details: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    item_guid: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        log_id = self.log_id

        name = self.name

        location = self.location

        purpose = self.purpose

        client_type: Union[Unset, int] = UNSET
        if not isinstance(self.client_type, Unset):
            client_type = self.client_type.value


        category: Union[Unset, int] = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.value


        severity: Union[Unset, int] = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value


        severity_text = self.severity_text

        log_date: Union[Unset, str] = UNSET
        if not isinstance(self.log_date, Unset):
            log_date = self.log_date.isoformat()

        description = self.description

        exception_details = self.exception_details

        comment = self.comment

        item_guid: Union[Unset, str] = UNSET
        if not isinstance(self.item_guid, Unset):
            item_guid = str(self.item_guid)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if client_id is not UNSET:
            field_dict["clientId"] = client_id
        if log_id is not UNSET:
            field_dict["logId"] = log_id
        if name is not UNSET:
            field_dict["name"] = name
        if location is not UNSET:
            field_dict["location"] = location
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if client_type is not UNSET:
            field_dict["clientType"] = client_type
        if category is not UNSET:
            field_dict["category"] = category
        if severity is not UNSET:
            field_dict["severity"] = severity
        if severity_text is not UNSET:
            field_dict["severityText"] = severity_text
        if log_date is not UNSET:
            field_dict["logDate"] = log_date
        if description is not UNSET:
            field_dict["description"] = description
        if exception_details is not UNSET:
            field_dict["exceptionDetails"] = exception_details
        if comment is not UNSET:
            field_dict["comment"] = comment
        if item_guid is not UNSET:
            field_dict["itemGuid"] = item_guid

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_id = d.pop("clientId", UNSET)

        log_id = d.pop("logId", UNSET)

        name = d.pop("name", UNSET)

        location = d.pop("location", UNSET)

        purpose = d.pop("purpose", UNSET)

        _client_type = d.pop("clientType", UNSET)
        client_type: Union[Unset, VirincoWATSWebDashboardModelsClientExceptionClientType]
        if isinstance(_client_type,  Unset):
            client_type = UNSET
        else:
            client_type = VirincoWATSWebDashboardModelsClientExceptionClientType(_client_type)




        _category = d.pop("category", UNSET)
        category: Union[Unset, VirincoWATSWebDashboardModelsClientExceptionCategory]
        if isinstance(_category,  Unset):
            category = UNSET
        else:
            category = VirincoWATSWebDashboardModelsClientExceptionCategory(_category)




        _severity = d.pop("severity", UNSET)
        severity: Union[Unset, VirincoWATSWebDashboardModelsClientExceptionSeverity]
        if isinstance(_severity,  Unset):
            severity = UNSET
        else:
            severity = VirincoWATSWebDashboardModelsClientExceptionSeverity(_severity)




        severity_text = d.pop("severityText", UNSET)

        _log_date = d.pop("logDate", UNSET)
        log_date: Union[Unset, datetime.datetime]
        if isinstance(_log_date,  Unset):
            log_date = UNSET
        else:
            log_date = isoparse(_log_date)




        description = d.pop("description", UNSET)

        exception_details = d.pop("exceptionDetails", UNSET)

        comment = d.pop("comment", UNSET)

        _item_guid = d.pop("itemGuid", UNSET)
        item_guid: Union[Unset, UUID]
        if isinstance(_item_guid,  Unset):
            item_guid = UNSET
        else:
            item_guid = UUID(_item_guid)




        virinco_wats_web_dashboard_models_client_exception = cls(
            client_id=client_id,
            log_id=log_id,
            name=name,
            location=location,
            purpose=purpose,
            client_type=client_type,
            category=category,
            severity=severity,
            severity_text=severity_text,
            log_date=log_date,
            description=description,
            exception_details=exception_details,
            comment=comment,
            item_guid=item_guid,
        )


        virinco_wats_web_dashboard_models_client_exception.additional_properties = d
        return virinco_wats_web_dashboard_models_client_exception

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
