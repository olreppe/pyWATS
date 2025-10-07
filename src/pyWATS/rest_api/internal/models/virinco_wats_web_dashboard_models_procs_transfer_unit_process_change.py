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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsProcsTransferUnitProcessChange")



@_attrs_define
class VirincoWATSWebDashboardModelsProcsTransferUnitProcessChange:
    """ 
        Attributes:
            sn (Union[Unset, str]):
            pn (Union[Unset, str]):
            change_utc (Union[Unset, datetime.datetime]):
            from_phase (Union[Unset, int]):
            from_process_code (Union[Unset, int]):
            to_phase (Union[Unset, int]):
            to_process_code (Union[Unset, int]):
            operator (Union[Unset, str]):
            station (Union[Unset, str]):
            forced (Union[Unset, bool]):
            detail_level (Union[Unset, int]):
            action_type (Union[Unset, str]):
            info (Union[Unset, str]):
            error_message (Union[Unset, str]):
            report_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            client_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
     """

    sn: Union[Unset, str] = UNSET
    pn: Union[Unset, str] = UNSET
    change_utc: Union[Unset, datetime.datetime] = UNSET
    from_phase: Union[Unset, int] = UNSET
    from_process_code: Union[Unset, int] = UNSET
    to_phase: Union[Unset, int] = UNSET
    to_process_code: Union[Unset, int] = UNSET
    operator: Union[Unset, str] = UNSET
    station: Union[Unset, str] = UNSET
    forced: Union[Unset, bool] = UNSET
    detail_level: Union[Unset, int] = UNSET
    action_type: Union[Unset, str] = UNSET
    info: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    report_id: Union[Unset, UUID] = UNSET
    client_id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        sn = self.sn

        pn = self.pn

        change_utc: Union[Unset, str] = UNSET
        if not isinstance(self.change_utc, Unset):
            change_utc = self.change_utc.isoformat()

        from_phase = self.from_phase

        from_process_code = self.from_process_code

        to_phase = self.to_phase

        to_process_code = self.to_process_code

        operator = self.operator

        station = self.station

        forced = self.forced

        detail_level = self.detail_level

        action_type = self.action_type

        info = self.info

        error_message = self.error_message

        report_id: Union[Unset, str] = UNSET
        if not isinstance(self.report_id, Unset):
            report_id = str(self.report_id)

        client_id: Union[Unset, str] = UNSET
        if not isinstance(self.client_id, Unset):
            client_id = str(self.client_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if sn is not UNSET:
            field_dict["SN"] = sn
        if pn is not UNSET:
            field_dict["PN"] = pn
        if change_utc is not UNSET:
            field_dict["ChangeUtc"] = change_utc
        if from_phase is not UNSET:
            field_dict["FromPhase"] = from_phase
        if from_process_code is not UNSET:
            field_dict["FromProcessCode"] = from_process_code
        if to_phase is not UNSET:
            field_dict["ToPhase"] = to_phase
        if to_process_code is not UNSET:
            field_dict["ToProcessCode"] = to_process_code
        if operator is not UNSET:
            field_dict["Operator"] = operator
        if station is not UNSET:
            field_dict["Station"] = station
        if forced is not UNSET:
            field_dict["Forced"] = forced
        if detail_level is not UNSET:
            field_dict["DetailLevel"] = detail_level
        if action_type is not UNSET:
            field_dict["ActionType"] = action_type
        if info is not UNSET:
            field_dict["Info"] = info
        if error_message is not UNSET:
            field_dict["ErrorMessage"] = error_message
        if report_id is not UNSET:
            field_dict["ReportId"] = report_id
        if client_id is not UNSET:
            field_dict["ClientId"] = client_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sn = d.pop("SN", UNSET)

        pn = d.pop("PN", UNSET)

        _change_utc = d.pop("ChangeUtc", UNSET)
        change_utc: Union[Unset, datetime.datetime]
        if isinstance(_change_utc,  Unset):
            change_utc = UNSET
        else:
            change_utc = isoparse(_change_utc)




        from_phase = d.pop("FromPhase", UNSET)

        from_process_code = d.pop("FromProcessCode", UNSET)

        to_phase = d.pop("ToPhase", UNSET)

        to_process_code = d.pop("ToProcessCode", UNSET)

        operator = d.pop("Operator", UNSET)

        station = d.pop("Station", UNSET)

        forced = d.pop("Forced", UNSET)

        detail_level = d.pop("DetailLevel", UNSET)

        action_type = d.pop("ActionType", UNSET)

        info = d.pop("Info", UNSET)

        error_message = d.pop("ErrorMessage", UNSET)

        _report_id = d.pop("ReportId", UNSET)
        report_id: Union[Unset, UUID]
        if isinstance(_report_id,  Unset):
            report_id = UNSET
        else:
            report_id = UUID(_report_id)




        _client_id = d.pop("ClientId", UNSET)
        client_id: Union[Unset, UUID]
        if isinstance(_client_id,  Unset):
            client_id = UNSET
        else:
            client_id = UUID(_client_id)




        virinco_wats_web_dashboard_models_procs_transfer_unit_process_change = cls(
            sn=sn,
            pn=pn,
            change_utc=change_utc,
            from_phase=from_phase,
            from_process_code=from_process_code,
            to_phase=to_phase,
            to_process_code=to_process_code,
            operator=operator,
            station=station,
            forced=forced,
            detail_level=detail_level,
            action_type=action_type,
            info=info,
            error_message=error_message,
            report_id=report_id,
            client_id=client_id,
        )


        virinco_wats_web_dashboard_models_procs_transfer_unit_process_change.additional_properties = d
        return virinco_wats_web_dashboard_models_procs_transfer_unit_process_change

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
