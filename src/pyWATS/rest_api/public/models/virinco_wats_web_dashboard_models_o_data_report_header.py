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

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_o_data_miscinfo import VirincoWATSWebDashboardModelsODataMiscinfo
  from ..models.virinco_wats_web_dashboard_models_o_data_uur_attachment import VirincoWATSWebDashboardModelsODataUURAttachment
  from ..models.virinco_wats_web_dashboard_models_o_data_asset import VirincoWATSWebDashboardModelsODataAsset
  from ..models.virinco_wats_web_dashboard_models_o_data_uur_miscinfo import VirincoWATSWebDashboardModelsODataUURMiscinfo
  from ..models.virinco_wats_web_dashboard_models_o_data_uur_subunit import VirincoWATSWebDashboardModelsODataUURSubunit
  from ..models.virinco_wats_web_dashboard_models_o_data_subunit import VirincoWATSWebDashboardModelsODataSubunit
  from ..models.virinco_wats_web_dashboard_models_o_data_attachment import VirincoWATSWebDashboardModelsODataAttachment





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsODataReportHeader")



@_attrs_define
class VirincoWATSWebDashboardModelsODataReportHeader:
    """ 
        Attributes:
            uuid (Union[Unset, UUID]): Report id. Can be used in order by Example: 00000000-0000-0000-0000-000000000000.
            serial_number (Union[Unset, str]): Report serial number. Can be using in order by
            part_number (Union[Unset, str]): Report part number
            report_type (Union[Unset, str]): Report type.T = UUT, R = UUR
            start (Union[Unset, datetime.datetime]): Report start time. In format yyyy-MM-ddTHH:mm:ssZ. Default order by
                descending
            revision (Union[Unset, str]): Report revision
            result (Union[Unset, str]): Report result. Passed, Failed, Error, or Terminated
            batch_number (Union[Unset, str]): Report batch number
            user_name (Union[Unset, str]): Report operator
            station_name (Union[Unset, str]): Test station name.
            location (Union[Unset, str]): Test station location
            purpose (Union[Unset, str]): Test station purpose.
            measures_deleted (Union[Unset, bool]):
            time_stamp (Union[Unset, int]): Report processing order. Does not represent time, instead is an incrementing
                number used as processing order. Can be used in order by
            process_code (Union[Unset, int]): Report test/repair operation code
            process_name (Union[Unset, str]): Report test/repair operation name
            comment (Union[Unset, str]): Report comment
            execution_time (Union[Unset, float]): Report execution time
            sw_filename (Union[Unset, str]): Report test software filename
            sw_version (Union[Unset, str]): Report test software version
            test_socket_index (Union[Unset, int]): Report test socket index
            fixture_id (Union[Unset, str]): Report fixture id
            error_code (Union[Unset, int]): Report error code
            error_message (Union[Unset, str]): Report error message
            run (Union[Unset, int]): Report test run number (same serial number in same test operation)
            receive_count (Union[Unset, int]): Report receive count
            report_size (Union[Unset, int]): Report size in KB
            caused_uut_failure (Union[Unset, str]): Step name that caused the report to fail
            caused_uut_failure_path (Union[Unset, str]): Step path that caused the report to fail
            passed_in_run (Union[Unset, int]): Run number the report first passed in
            referenced_uut (Union[Unset, UUID]): Repair report referencing a test report Example:
                00000000-0000-0000-0000-000000000000.
            sub_units (Union[Unset, list['VirincoWATSWebDashboardModelsODataSubunit']]): UUT sub units. Must be expanded
            misc_info (Union[Unset, list['VirincoWATSWebDashboardModelsODataMiscinfo']]): UUT miscellaneous info. Must be
                expanded
            assets (Union[Unset, list['VirincoWATSWebDashboardModelsODataAsset']]): UUT asset info. Must be expanded
            attachments (Union[Unset, list['VirincoWATSWebDashboardModelsODataAttachment']]): UUT attachments. Must be
                expanded
            uur_sub_units (Union[Unset, list['VirincoWATSWebDashboardModelsODataUURSubunit']]): UUR sub units. Must be
                expanded
            uur_misc_info (Union[Unset, list['VirincoWATSWebDashboardModelsODataUURMiscinfo']]): UUR miscellaneous info.
                Must be expanded
            uur_attachments (Union[Unset, list['VirincoWATSWebDashboardModelsODataUURAttachment']]): UUR attachments. Must
                be expanded
     """

    uuid: Union[Unset, UUID] = UNSET
    serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    report_type: Union[Unset, str] = UNSET
    start: Union[Unset, datetime.datetime] = UNSET
    revision: Union[Unset, str] = UNSET
    result: Union[Unset, str] = UNSET
    batch_number: Union[Unset, str] = UNSET
    user_name: Union[Unset, str] = UNSET
    station_name: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    measures_deleted: Union[Unset, bool] = UNSET
    time_stamp: Union[Unset, int] = UNSET
    process_code: Union[Unset, int] = UNSET
    process_name: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    execution_time: Union[Unset, float] = UNSET
    sw_filename: Union[Unset, str] = UNSET
    sw_version: Union[Unset, str] = UNSET
    test_socket_index: Union[Unset, int] = UNSET
    fixture_id: Union[Unset, str] = UNSET
    error_code: Union[Unset, int] = UNSET
    error_message: Union[Unset, str] = UNSET
    run: Union[Unset, int] = UNSET
    receive_count: Union[Unset, int] = UNSET
    report_size: Union[Unset, int] = UNSET
    caused_uut_failure: Union[Unset, str] = UNSET
    caused_uut_failure_path: Union[Unset, str] = UNSET
    passed_in_run: Union[Unset, int] = UNSET
    referenced_uut: Union[Unset, UUID] = UNSET
    sub_units: Union[Unset, list['VirincoWATSWebDashboardModelsODataSubunit']] = UNSET
    misc_info: Union[Unset, list['VirincoWATSWebDashboardModelsODataMiscinfo']] = UNSET
    assets: Union[Unset, list['VirincoWATSWebDashboardModelsODataAsset']] = UNSET
    attachments: Union[Unset, list['VirincoWATSWebDashboardModelsODataAttachment']] = UNSET
    uur_sub_units: Union[Unset, list['VirincoWATSWebDashboardModelsODataUURSubunit']] = UNSET
    uur_misc_info: Union[Unset, list['VirincoWATSWebDashboardModelsODataUURMiscinfo']] = UNSET
    uur_attachments: Union[Unset, list['VirincoWATSWebDashboardModelsODataUURAttachment']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_o_data_miscinfo import VirincoWATSWebDashboardModelsODataMiscinfo
        from ..models.virinco_wats_web_dashboard_models_o_data_uur_attachment import VirincoWATSWebDashboardModelsODataUURAttachment
        from ..models.virinco_wats_web_dashboard_models_o_data_asset import VirincoWATSWebDashboardModelsODataAsset
        from ..models.virinco_wats_web_dashboard_models_o_data_uur_miscinfo import VirincoWATSWebDashboardModelsODataUURMiscinfo
        from ..models.virinco_wats_web_dashboard_models_o_data_uur_subunit import VirincoWATSWebDashboardModelsODataUURSubunit
        from ..models.virinco_wats_web_dashboard_models_o_data_subunit import VirincoWATSWebDashboardModelsODataSubunit
        from ..models.virinco_wats_web_dashboard_models_o_data_attachment import VirincoWATSWebDashboardModelsODataAttachment
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        serial_number = self.serial_number

        part_number = self.part_number

        report_type = self.report_type

        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        revision = self.revision

        result = self.result

        batch_number = self.batch_number

        user_name = self.user_name

        station_name = self.station_name

        location = self.location

        purpose = self.purpose

        measures_deleted = self.measures_deleted

        time_stamp = self.time_stamp

        process_code = self.process_code

        process_name = self.process_name

        comment = self.comment

        execution_time = self.execution_time

        sw_filename = self.sw_filename

        sw_version = self.sw_version

        test_socket_index = self.test_socket_index

        fixture_id = self.fixture_id

        error_code = self.error_code

        error_message = self.error_message

        run = self.run

        receive_count = self.receive_count

        report_size = self.report_size

        caused_uut_failure = self.caused_uut_failure

        caused_uut_failure_path = self.caused_uut_failure_path

        passed_in_run = self.passed_in_run

        referenced_uut: Union[Unset, str] = UNSET
        if not isinstance(self.referenced_uut, Unset):
            referenced_uut = str(self.referenced_uut)

        sub_units: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sub_units, Unset):
            sub_units = []
            for sub_units_item_data in self.sub_units:
                sub_units_item = sub_units_item_data.to_dict()
                sub_units.append(sub_units_item)



        misc_info: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.misc_info, Unset):
            misc_info = []
            for misc_info_item_data in self.misc_info:
                misc_info_item = misc_info_item_data.to_dict()
                misc_info.append(misc_info_item)



        assets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.assets, Unset):
            assets = []
            for assets_item_data in self.assets:
                assets_item = assets_item_data.to_dict()
                assets.append(assets_item)



        attachments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = []
            for attachments_item_data in self.attachments:
                attachments_item = attachments_item_data.to_dict()
                attachments.append(attachments_item)



        uur_sub_units: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.uur_sub_units, Unset):
            uur_sub_units = []
            for uur_sub_units_item_data in self.uur_sub_units:
                uur_sub_units_item = uur_sub_units_item_data.to_dict()
                uur_sub_units.append(uur_sub_units_item)



        uur_misc_info: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.uur_misc_info, Unset):
            uur_misc_info = []
            for uur_misc_info_item_data in self.uur_misc_info:
                uur_misc_info_item = uur_misc_info_item_data.to_dict()
                uur_misc_info.append(uur_misc_info_item)



        uur_attachments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.uur_attachments, Unset):
            uur_attachments = []
            for uur_attachments_item_data in self.uur_attachments:
                uur_attachments_item = uur_attachments_item_data.to_dict()
                uur_attachments.append(uur_attachments_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if report_type is not UNSET:
            field_dict["reportType"] = report_type
        if start is not UNSET:
            field_dict["start"] = start
        if revision is not UNSET:
            field_dict["revision"] = revision
        if result is not UNSET:
            field_dict["result"] = result
        if batch_number is not UNSET:
            field_dict["batchNumber"] = batch_number
        if user_name is not UNSET:
            field_dict["userName"] = user_name
        if station_name is not UNSET:
            field_dict["stationName"] = station_name
        if location is not UNSET:
            field_dict["location"] = location
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if measures_deleted is not UNSET:
            field_dict["measuresDeleted"] = measures_deleted
        if time_stamp is not UNSET:
            field_dict["timeStamp"] = time_stamp
        if process_code is not UNSET:
            field_dict["processCode"] = process_code
        if process_name is not UNSET:
            field_dict["processName"] = process_name
        if comment is not UNSET:
            field_dict["comment"] = comment
        if execution_time is not UNSET:
            field_dict["executionTime"] = execution_time
        if sw_filename is not UNSET:
            field_dict["swFilename"] = sw_filename
        if sw_version is not UNSET:
            field_dict["swVersion"] = sw_version
        if test_socket_index is not UNSET:
            field_dict["testSocketIndex"] = test_socket_index
        if fixture_id is not UNSET:
            field_dict["fixtureId"] = fixture_id
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if run is not UNSET:
            field_dict["run"] = run
        if receive_count is not UNSET:
            field_dict["receiveCount"] = receive_count
        if report_size is not UNSET:
            field_dict["reportSize"] = report_size
        if caused_uut_failure is not UNSET:
            field_dict["causedUutFailure"] = caused_uut_failure
        if caused_uut_failure_path is not UNSET:
            field_dict["causedUutFailurePath"] = caused_uut_failure_path
        if passed_in_run is not UNSET:
            field_dict["passedInRun"] = passed_in_run
        if referenced_uut is not UNSET:
            field_dict["referencedUut"] = referenced_uut
        if sub_units is not UNSET:
            field_dict["subUnits"] = sub_units
        if misc_info is not UNSET:
            field_dict["miscInfo"] = misc_info
        if assets is not UNSET:
            field_dict["assets"] = assets
        if attachments is not UNSET:
            field_dict["attachments"] = attachments
        if uur_sub_units is not UNSET:
            field_dict["uurSubUnits"] = uur_sub_units
        if uur_misc_info is not UNSET:
            field_dict["uurMiscInfo"] = uur_misc_info
        if uur_attachments is not UNSET:
            field_dict["uurAttachments"] = uur_attachments

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_o_data_miscinfo import VirincoWATSWebDashboardModelsODataMiscinfo
        from ..models.virinco_wats_web_dashboard_models_o_data_uur_attachment import VirincoWATSWebDashboardModelsODataUURAttachment
        from ..models.virinco_wats_web_dashboard_models_o_data_asset import VirincoWATSWebDashboardModelsODataAsset
        from ..models.virinco_wats_web_dashboard_models_o_data_uur_miscinfo import VirincoWATSWebDashboardModelsODataUURMiscinfo
        from ..models.virinco_wats_web_dashboard_models_o_data_uur_subunit import VirincoWATSWebDashboardModelsODataUURSubunit
        from ..models.virinco_wats_web_dashboard_models_o_data_subunit import VirincoWATSWebDashboardModelsODataSubunit
        from ..models.virinco_wats_web_dashboard_models_o_data_attachment import VirincoWATSWebDashboardModelsODataAttachment
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid,  Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)




        serial_number = d.pop("serialNumber", UNSET)

        part_number = d.pop("partNumber", UNSET)

        report_type = d.pop("reportType", UNSET)

        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.datetime]
        if isinstance(_start,  Unset):
            start = UNSET
        else:
            start = isoparse(_start)




        revision = d.pop("revision", UNSET)

        result = d.pop("result", UNSET)

        batch_number = d.pop("batchNumber", UNSET)

        user_name = d.pop("userName", UNSET)

        station_name = d.pop("stationName", UNSET)

        location = d.pop("location", UNSET)

        purpose = d.pop("purpose", UNSET)

        measures_deleted = d.pop("measuresDeleted", UNSET)

        time_stamp = d.pop("timeStamp", UNSET)

        process_code = d.pop("processCode", UNSET)

        process_name = d.pop("processName", UNSET)

        comment = d.pop("comment", UNSET)

        execution_time = d.pop("executionTime", UNSET)

        sw_filename = d.pop("swFilename", UNSET)

        sw_version = d.pop("swVersion", UNSET)

        test_socket_index = d.pop("testSocketIndex", UNSET)

        fixture_id = d.pop("fixtureId", UNSET)

        error_code = d.pop("errorCode", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        run = d.pop("run", UNSET)

        receive_count = d.pop("receiveCount", UNSET)

        report_size = d.pop("reportSize", UNSET)

        caused_uut_failure = d.pop("causedUutFailure", UNSET)

        caused_uut_failure_path = d.pop("causedUutFailurePath", UNSET)

        passed_in_run = d.pop("passedInRun", UNSET)

        _referenced_uut = d.pop("referencedUut", UNSET)
        referenced_uut: Union[Unset, UUID]
        if isinstance(_referenced_uut,  Unset):
            referenced_uut = UNSET
        else:
            referenced_uut = UUID(_referenced_uut)




        sub_units = []
        _sub_units = d.pop("subUnits", UNSET)
        for sub_units_item_data in (_sub_units or []):
            sub_units_item = VirincoWATSWebDashboardModelsODataSubunit.from_dict(sub_units_item_data)



            sub_units.append(sub_units_item)


        misc_info = []
        _misc_info = d.pop("miscInfo", UNSET)
        for misc_info_item_data in (_misc_info or []):
            misc_info_item = VirincoWATSWebDashboardModelsODataMiscinfo.from_dict(misc_info_item_data)



            misc_info.append(misc_info_item)


        assets = []
        _assets = d.pop("assets", UNSET)
        for assets_item_data in (_assets or []):
            assets_item = VirincoWATSWebDashboardModelsODataAsset.from_dict(assets_item_data)



            assets.append(assets_item)


        attachments = []
        _attachments = d.pop("attachments", UNSET)
        for attachments_item_data in (_attachments or []):
            attachments_item = VirincoWATSWebDashboardModelsODataAttachment.from_dict(attachments_item_data)



            attachments.append(attachments_item)


        uur_sub_units = []
        _uur_sub_units = d.pop("uurSubUnits", UNSET)
        for uur_sub_units_item_data in (_uur_sub_units or []):
            uur_sub_units_item = VirincoWATSWebDashboardModelsODataUURSubunit.from_dict(uur_sub_units_item_data)



            uur_sub_units.append(uur_sub_units_item)


        uur_misc_info = []
        _uur_misc_info = d.pop("uurMiscInfo", UNSET)
        for uur_misc_info_item_data in (_uur_misc_info or []):
            uur_misc_info_item = VirincoWATSWebDashboardModelsODataUURMiscinfo.from_dict(uur_misc_info_item_data)



            uur_misc_info.append(uur_misc_info_item)


        uur_attachments = []
        _uur_attachments = d.pop("uurAttachments", UNSET)
        for uur_attachments_item_data in (_uur_attachments or []):
            uur_attachments_item = VirincoWATSWebDashboardModelsODataUURAttachment.from_dict(uur_attachments_item_data)



            uur_attachments.append(uur_attachments_item)


        virinco_wats_web_dashboard_models_o_data_report_header = cls(
            uuid=uuid,
            serial_number=serial_number,
            part_number=part_number,
            report_type=report_type,
            start=start,
            revision=revision,
            result=result,
            batch_number=batch_number,
            user_name=user_name,
            station_name=station_name,
            location=location,
            purpose=purpose,
            measures_deleted=measures_deleted,
            time_stamp=time_stamp,
            process_code=process_code,
            process_name=process_name,
            comment=comment,
            execution_time=execution_time,
            sw_filename=sw_filename,
            sw_version=sw_version,
            test_socket_index=test_socket_index,
            fixture_id=fixture_id,
            error_code=error_code,
            error_message=error_message,
            run=run,
            receive_count=receive_count,
            report_size=report_size,
            caused_uut_failure=caused_uut_failure,
            caused_uut_failure_path=caused_uut_failure_path,
            passed_in_run=passed_in_run,
            referenced_uut=referenced_uut,
            sub_units=sub_units,
            misc_info=misc_info,
            assets=assets,
            attachments=attachments,
            uur_sub_units=uur_sub_units,
            uur_misc_info=uur_misc_info,
            uur_attachments=uur_attachments,
        )


        virinco_wats_web_dashboard_models_o_data_report_header.additional_properties = d
        return virinco_wats_web_dashboard_models_o_data_report_header

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
