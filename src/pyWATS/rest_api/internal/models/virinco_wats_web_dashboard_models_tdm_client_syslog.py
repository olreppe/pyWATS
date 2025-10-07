from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_tdm_client_syslog_category import VirincoWATSWebDashboardModelsTdmClientSyslogCategory
from ..models.virinco_wats_web_dashboard_models_tdm_client_syslog_severity import VirincoWATSWebDashboardModelsTdmClientSyslogSeverity
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmClientSyslog")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmClientSyslog:
    """ 
        Attributes:
            log_id (Union[Unset, int]):
            category (Union[Unset, VirincoWATSWebDashboardModelsTdmClientSyslogCategory]):
            severity (Union[Unset, VirincoWATSWebDashboardModelsTdmClientSyslogSeverity]):
            date (Union[Unset, datetime.datetime]):
            description (Union[Unset, str]):
            exception (Union[Unset, str]):
            comment (Union[Unset, str]):
     """

    log_id: Union[Unset, int] = UNSET
    category: Union[Unset, VirincoWATSWebDashboardModelsTdmClientSyslogCategory] = UNSET
    severity: Union[Unset, VirincoWATSWebDashboardModelsTdmClientSyslogSeverity] = UNSET
    date: Union[Unset, datetime.datetime] = UNSET
    description: Union[Unset, str] = UNSET
    exception: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        log_id = self.log_id

        category: Union[Unset, int] = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.value


        severity: Union[Unset, int] = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value


        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        description = self.description

        exception = self.exception

        comment = self.comment


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if log_id is not UNSET:
            field_dict["logId"] = log_id
        if category is not UNSET:
            field_dict["category"] = category
        if severity is not UNSET:
            field_dict["severity"] = severity
        if date is not UNSET:
            field_dict["date"] = date
        if description is not UNSET:
            field_dict["description"] = description
        if exception is not UNSET:
            field_dict["exception"] = exception
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        log_id = d.pop("logId", UNSET)

        _category = d.pop("category", UNSET)
        category: Union[Unset, VirincoWATSWebDashboardModelsTdmClientSyslogCategory]
        if isinstance(_category,  Unset):
            category = UNSET
        else:
            category = VirincoWATSWebDashboardModelsTdmClientSyslogCategory(_category)




        _severity = d.pop("severity", UNSET)
        severity: Union[Unset, VirincoWATSWebDashboardModelsTdmClientSyslogSeverity]
        if isinstance(_severity,  Unset):
            severity = UNSET
        else:
            severity = VirincoWATSWebDashboardModelsTdmClientSyslogSeverity(_severity)




        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date,  Unset):
            date = UNSET
        else:
            date = isoparse(_date)




        description = d.pop("description", UNSET)

        exception = d.pop("exception", UNSET)

        comment = d.pop("comment", UNSET)

        virinco_wats_web_dashboard_models_tdm_client_syslog = cls(
            log_id=log_id,
            category=category,
            severity=severity,
            date=date,
            description=description,
            exception=exception,
            comment=comment,
        )


        virinco_wats_web_dashboard_models_tdm_client_syslog.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_client_syslog

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
