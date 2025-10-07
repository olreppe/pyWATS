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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsSnHistoryReport")



@_attrs_define
class VirincoWATSWebDashboardModelsSnHistoryReport:
    """ 
        Attributes:
            serial_number (Union[Unset, str]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            parent_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            product_name (Union[Unset, str]):
            batch_number (Union[Unset, str]):
            start (Union[Unset, datetime.datetime]):
            start_local (Union[Unset, datetime.datetime]):
            start_utc (Union[Unset, datetime.datetime]):
            operator (Union[Unset, str]):
            execution_time (Union[Unset, float]):
            fixture_id (Union[Unset, str]):
            process (Union[Unset, str]):
            phase (Union[Unset, str]):
            comment (Union[Unset, str]):
            report_type (Union[Unset, str]):
            entity (Union[Unset, str]):
            uuid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            error_message (Union[Unset, str]):
            location (Union[Unset, str]):
            purpose (Union[Unset, str]):
            status (Union[Unset, str]):
            station_name (Union[Unset, str]):
            sw_filename (Union[Unset, str]):
            sw_version (Union[Unset, str]):
            sub_sn (Union[Unset, str]):
            sub_pn (Union[Unset, str]):
            sub_product_name (Union[Unset, str]):
            sub_rev (Union[Unset, str]):
            test_process (Union[Unset, str]):
            finalize_date_utc (Union[Unset, datetime.datetime]):
            finalize_date_local (Union[Unset, datetime.datetime]):
            forced (Union[Unset, bool]):
            action_type (Union[Unset, str]):
            report_type_text (Union[Unset, str]):
            ticket_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            caused_uut_failure (Union[Unset, str]):
            caused_uut_failure_path (Union[Unset, str]):
     """

    serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    parent_id: Union[Unset, UUID] = UNSET
    product_name: Union[Unset, str] = UNSET
    batch_number: Union[Unset, str] = UNSET
    start: Union[Unset, datetime.datetime] = UNSET
    start_local: Union[Unset, datetime.datetime] = UNSET
    start_utc: Union[Unset, datetime.datetime] = UNSET
    operator: Union[Unset, str] = UNSET
    execution_time: Union[Unset, float] = UNSET
    fixture_id: Union[Unset, str] = UNSET
    process: Union[Unset, str] = UNSET
    phase: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    report_type: Union[Unset, str] = UNSET
    entity: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    error_message: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    station_name: Union[Unset, str] = UNSET
    sw_filename: Union[Unset, str] = UNSET
    sw_version: Union[Unset, str] = UNSET
    sub_sn: Union[Unset, str] = UNSET
    sub_pn: Union[Unset, str] = UNSET
    sub_product_name: Union[Unset, str] = UNSET
    sub_rev: Union[Unset, str] = UNSET
    test_process: Union[Unset, str] = UNSET
    finalize_date_utc: Union[Unset, datetime.datetime] = UNSET
    finalize_date_local: Union[Unset, datetime.datetime] = UNSET
    forced: Union[Unset, bool] = UNSET
    action_type: Union[Unset, str] = UNSET
    report_type_text: Union[Unset, str] = UNSET
    ticket_id: Union[Unset, UUID] = UNSET
    caused_uut_failure: Union[Unset, str] = UNSET
    caused_uut_failure_path: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        serial_number = self.serial_number

        part_number = self.part_number

        revision = self.revision

        parent_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_id, Unset):
            parent_id = str(self.parent_id)

        product_name = self.product_name

        batch_number = self.batch_number

        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        start_local: Union[Unset, str] = UNSET
        if not isinstance(self.start_local, Unset):
            start_local = self.start_local.isoformat()

        start_utc: Union[Unset, str] = UNSET
        if not isinstance(self.start_utc, Unset):
            start_utc = self.start_utc.isoformat()

        operator = self.operator

        execution_time = self.execution_time

        fixture_id = self.fixture_id

        process = self.process

        phase = self.phase

        comment = self.comment

        report_type = self.report_type

        entity = self.entity

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        error_message = self.error_message

        location = self.location

        purpose = self.purpose

        status = self.status

        station_name = self.station_name

        sw_filename = self.sw_filename

        sw_version = self.sw_version

        sub_sn = self.sub_sn

        sub_pn = self.sub_pn

        sub_product_name = self.sub_product_name

        sub_rev = self.sub_rev

        test_process = self.test_process

        finalize_date_utc: Union[Unset, str] = UNSET
        if not isinstance(self.finalize_date_utc, Unset):
            finalize_date_utc = self.finalize_date_utc.isoformat()

        finalize_date_local: Union[Unset, str] = UNSET
        if not isinstance(self.finalize_date_local, Unset):
            finalize_date_local = self.finalize_date_local.isoformat()

        forced = self.forced

        action_type = self.action_type

        report_type_text = self.report_type_text

        ticket_id: Union[Unset, str] = UNSET
        if not isinstance(self.ticket_id, Unset):
            ticket_id = str(self.ticket_id)

        caused_uut_failure = self.caused_uut_failure

        caused_uut_failure_path = self.caused_uut_failure_path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if product_name is not UNSET:
            field_dict["productName"] = product_name
        if batch_number is not UNSET:
            field_dict["batchNumber"] = batch_number
        if start is not UNSET:
            field_dict["start"] = start
        if start_local is not UNSET:
            field_dict["startLocal"] = start_local
        if start_utc is not UNSET:
            field_dict["startUtc"] = start_utc
        if operator is not UNSET:
            field_dict["operator"] = operator
        if execution_time is not UNSET:
            field_dict["executionTime"] = execution_time
        if fixture_id is not UNSET:
            field_dict["fixtureId"] = fixture_id
        if process is not UNSET:
            field_dict["process"] = process
        if phase is not UNSET:
            field_dict["phase"] = phase
        if comment is not UNSET:
            field_dict["comment"] = comment
        if report_type is not UNSET:
            field_dict["reportType"] = report_type
        if entity is not UNSET:
            field_dict["entity"] = entity
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if location is not UNSET:
            field_dict["location"] = location
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if status is not UNSET:
            field_dict["status"] = status
        if station_name is not UNSET:
            field_dict["stationName"] = station_name
        if sw_filename is not UNSET:
            field_dict["swFilename"] = sw_filename
        if sw_version is not UNSET:
            field_dict["swVersion"] = sw_version
        if sub_sn is not UNSET:
            field_dict["subSn"] = sub_sn
        if sub_pn is not UNSET:
            field_dict["subPn"] = sub_pn
        if sub_product_name is not UNSET:
            field_dict["subProductName"] = sub_product_name
        if sub_rev is not UNSET:
            field_dict["subRev"] = sub_rev
        if test_process is not UNSET:
            field_dict["testProcess"] = test_process
        if finalize_date_utc is not UNSET:
            field_dict["finalizeDateUtc"] = finalize_date_utc
        if finalize_date_local is not UNSET:
            field_dict["finalizeDateLocal"] = finalize_date_local
        if forced is not UNSET:
            field_dict["forced"] = forced
        if action_type is not UNSET:
            field_dict["actionType"] = action_type
        if report_type_text is not UNSET:
            field_dict["reportTypeText"] = report_type_text
        if ticket_id is not UNSET:
            field_dict["ticketId"] = ticket_id
        if caused_uut_failure is not UNSET:
            field_dict["causedUutFailure"] = caused_uut_failure
        if caused_uut_failure_path is not UNSET:
            field_dict["causedUutFailurePath"] = caused_uut_failure_path

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        serial_number = d.pop("serialNumber", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        _parent_id = d.pop("parentId", UNSET)
        parent_id: Union[Unset, UUID]
        if isinstance(_parent_id,  Unset):
            parent_id = UNSET
        else:
            parent_id = UUID(_parent_id)




        product_name = d.pop("productName", UNSET)

        batch_number = d.pop("batchNumber", UNSET)

        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.datetime]
        if isinstance(_start,  Unset):
            start = UNSET
        else:
            start = isoparse(_start)




        _start_local = d.pop("startLocal", UNSET)
        start_local: Union[Unset, datetime.datetime]
        if isinstance(_start_local,  Unset):
            start_local = UNSET
        else:
            start_local = isoparse(_start_local)




        _start_utc = d.pop("startUtc", UNSET)
        start_utc: Union[Unset, datetime.datetime]
        if isinstance(_start_utc,  Unset):
            start_utc = UNSET
        else:
            start_utc = isoparse(_start_utc)




        operator = d.pop("operator", UNSET)

        execution_time = d.pop("executionTime", UNSET)

        fixture_id = d.pop("fixtureId", UNSET)

        process = d.pop("process", UNSET)

        phase = d.pop("phase", UNSET)

        comment = d.pop("comment", UNSET)

        report_type = d.pop("reportType", UNSET)

        entity = d.pop("entity", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid,  Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)




        error_message = d.pop("errorMessage", UNSET)

        location = d.pop("location", UNSET)

        purpose = d.pop("purpose", UNSET)

        status = d.pop("status", UNSET)

        station_name = d.pop("stationName", UNSET)

        sw_filename = d.pop("swFilename", UNSET)

        sw_version = d.pop("swVersion", UNSET)

        sub_sn = d.pop("subSn", UNSET)

        sub_pn = d.pop("subPn", UNSET)

        sub_product_name = d.pop("subProductName", UNSET)

        sub_rev = d.pop("subRev", UNSET)

        test_process = d.pop("testProcess", UNSET)

        _finalize_date_utc = d.pop("finalizeDateUtc", UNSET)
        finalize_date_utc: Union[Unset, datetime.datetime]
        if isinstance(_finalize_date_utc,  Unset):
            finalize_date_utc = UNSET
        else:
            finalize_date_utc = isoparse(_finalize_date_utc)




        _finalize_date_local = d.pop("finalizeDateLocal", UNSET)
        finalize_date_local: Union[Unset, datetime.datetime]
        if isinstance(_finalize_date_local,  Unset):
            finalize_date_local = UNSET
        else:
            finalize_date_local = isoparse(_finalize_date_local)




        forced = d.pop("forced", UNSET)

        action_type = d.pop("actionType", UNSET)

        report_type_text = d.pop("reportTypeText", UNSET)

        _ticket_id = d.pop("ticketId", UNSET)
        ticket_id: Union[Unset, UUID]
        if isinstance(_ticket_id,  Unset):
            ticket_id = UNSET
        else:
            ticket_id = UUID(_ticket_id)




        caused_uut_failure = d.pop("causedUutFailure", UNSET)

        caused_uut_failure_path = d.pop("causedUutFailurePath", UNSET)

        virinco_wats_web_dashboard_models_sn_history_report = cls(
            serial_number=serial_number,
            part_number=part_number,
            revision=revision,
            parent_id=parent_id,
            product_name=product_name,
            batch_number=batch_number,
            start=start,
            start_local=start_local,
            start_utc=start_utc,
            operator=operator,
            execution_time=execution_time,
            fixture_id=fixture_id,
            process=process,
            phase=phase,
            comment=comment,
            report_type=report_type,
            entity=entity,
            uuid=uuid,
            error_message=error_message,
            location=location,
            purpose=purpose,
            status=status,
            station_name=station_name,
            sw_filename=sw_filename,
            sw_version=sw_version,
            sub_sn=sub_sn,
            sub_pn=sub_pn,
            sub_product_name=sub_product_name,
            sub_rev=sub_rev,
            test_process=test_process,
            finalize_date_utc=finalize_date_utc,
            finalize_date_local=finalize_date_local,
            forced=forced,
            action_type=action_type,
            report_type_text=report_type_text,
            ticket_id=ticket_id,
            caused_uut_failure=caused_uut_failure,
            caused_uut_failure_path=caused_uut_failure_path,
        )


        virinco_wats_web_dashboard_models_sn_history_report.additional_properties = d
        return virinco_wats_web_dashboard_models_sn_history_report

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
