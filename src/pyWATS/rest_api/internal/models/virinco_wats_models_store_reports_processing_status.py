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






T = TypeVar("T", bound="VirincoWATSModelsStoreReportsProcessingStatus")



@_attrs_define
class VirincoWATSModelsStoreReportsProcessingStatus:
    """ 
        Attributes:
            uuid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            state (Union[Unset, str]):
            process_at_utc (Union[Unset, datetime.datetime]):
            receive_date (Union[Unset, datetime.datetime]):
            receive_count (Union[Unset, int]):
            last_attempt (Union[Unset, datetime.datetime]):
            attempts (Union[Unset, int]):
     """

    uuid: Union[Unset, UUID] = UNSET
    state: Union[Unset, str] = UNSET
    process_at_utc: Union[Unset, datetime.datetime] = UNSET
    receive_date: Union[Unset, datetime.datetime] = UNSET
    receive_count: Union[Unset, int] = UNSET
    last_attempt: Union[Unset, datetime.datetime] = UNSET
    attempts: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        state = self.state

        process_at_utc: Union[Unset, str] = UNSET
        if not isinstance(self.process_at_utc, Unset):
            process_at_utc = self.process_at_utc.isoformat()

        receive_date: Union[Unset, str] = UNSET
        if not isinstance(self.receive_date, Unset):
            receive_date = self.receive_date.isoformat()

        receive_count = self.receive_count

        last_attempt: Union[Unset, str] = UNSET
        if not isinstance(self.last_attempt, Unset):
            last_attempt = self.last_attempt.isoformat()

        attempts = self.attempts


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if state is not UNSET:
            field_dict["State"] = state
        if process_at_utc is not UNSET:
            field_dict["ProcessAtUtc"] = process_at_utc
        if receive_date is not UNSET:
            field_dict["ReceiveDate"] = receive_date
        if receive_count is not UNSET:
            field_dict["ReceiveCount"] = receive_count
        if last_attempt is not UNSET:
            field_dict["LastAttempt"] = last_attempt
        if attempts is not UNSET:
            field_dict["Attempts"] = attempts

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid,  Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)




        state = d.pop("State", UNSET)

        _process_at_utc = d.pop("ProcessAtUtc", UNSET)
        process_at_utc: Union[Unset, datetime.datetime]
        if isinstance(_process_at_utc,  Unset):
            process_at_utc = UNSET
        else:
            process_at_utc = isoparse(_process_at_utc)




        _receive_date = d.pop("ReceiveDate", UNSET)
        receive_date: Union[Unset, datetime.datetime]
        if isinstance(_receive_date,  Unset):
            receive_date = UNSET
        else:
            receive_date = isoparse(_receive_date)




        receive_count = d.pop("ReceiveCount", UNSET)

        _last_attempt = d.pop("LastAttempt", UNSET)
        last_attempt: Union[Unset, datetime.datetime]
        if isinstance(_last_attempt,  Unset):
            last_attempt = UNSET
        else:
            last_attempt = isoparse(_last_attempt)




        attempts = d.pop("Attempts", UNSET)

        virinco_wats_models_store_reports_processing_status = cls(
            uuid=uuid,
            state=state,
            process_at_utc=process_at_utc,
            receive_date=receive_date,
            receive_count=receive_count,
            last_attempt=last_attempt,
            attempts=attempts,
        )


        virinco_wats_models_store_reports_processing_status.additional_properties = d
        return virinco_wats_models_store_reports_processing_status

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
