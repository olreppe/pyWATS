from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="QuarantineRetryQuarantinedReportsWithNewDateDataBody")



@_attrs_define
class QuarantineRetryQuarantinedReportsWithNewDateDataBody:
    """ 
     """

    additional_properties: dict[str, datetime.datetime] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.isoformat()


        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        quarantine_retry_quarantined_reports_with_new_date_data_body = cls(
        )


        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = isoparse(prop_dict)



            additional_properties[prop_name] = additional_property

        quarantine_retry_quarantined_reports_with_new_date_data_body.additional_properties = additional_properties
        return quarantine_retry_quarantined_reports_with_new_date_data_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> datetime.datetime:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: datetime.datetime) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
