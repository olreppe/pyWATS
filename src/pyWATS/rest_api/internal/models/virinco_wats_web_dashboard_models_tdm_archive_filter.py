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

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_archive_filter_process import VirincoWATSWebDashboardModelsTdmArchiveFilterProcess





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmArchiveFilter")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmArchiveFilter:
    """ 
        Attributes:
            filter_id (Union[Unset, int]):
            name (Union[Unset, str]):
            delete_measurement (Union[Unset, bool]):
            delete_header (Union[Unset, bool]):
            from_date (Union[Unset, datetime.datetime]):
            to_date (Union[Unset, datetime.datetime]):
            date_offset (Union[Unset, int]):
            date_part (Union[Unset, str]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            max_count (Union[Unset, int]):
            last_run (Union[Unset, datetime.datetime]):
            last_affected (Union[Unset, int]):
            total_run (Union[Unset, int]):
            total_reports (Union[Unset, int]):
            last_duration (Union[Unset, str]):
            config_id (Union[Unset, int]):
            filter_processes (Union[Unset, list['VirincoWATSWebDashboardModelsTdmArchiveFilterProcess']]):
     """

    filter_id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    delete_measurement: Union[Unset, bool] = UNSET
    delete_header: Union[Unset, bool] = UNSET
    from_date: Union[Unset, datetime.datetime] = UNSET
    to_date: Union[Unset, datetime.datetime] = UNSET
    date_offset: Union[Unset, int] = UNSET
    date_part: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    max_count: Union[Unset, int] = UNSET
    last_run: Union[Unset, datetime.datetime] = UNSET
    last_affected: Union[Unset, int] = UNSET
    total_run: Union[Unset, int] = UNSET
    total_reports: Union[Unset, int] = UNSET
    last_duration: Union[Unset, str] = UNSET
    config_id: Union[Unset, int] = UNSET
    filter_processes: Union[Unset, list['VirincoWATSWebDashboardModelsTdmArchiveFilterProcess']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_archive_filter_process import VirincoWATSWebDashboardModelsTdmArchiveFilterProcess
        filter_id = self.filter_id

        name = self.name

        delete_measurement = self.delete_measurement

        delete_header = self.delete_header

        from_date: Union[Unset, str] = UNSET
        if not isinstance(self.from_date, Unset):
            from_date = self.from_date.isoformat()

        to_date: Union[Unset, str] = UNSET
        if not isinstance(self.to_date, Unset):
            to_date = self.to_date.isoformat()

        date_offset = self.date_offset

        date_part = self.date_part

        part_number = self.part_number

        revision = self.revision

        max_count = self.max_count

        last_run: Union[Unset, str] = UNSET
        if not isinstance(self.last_run, Unset):
            last_run = self.last_run.isoformat()

        last_affected = self.last_affected

        total_run = self.total_run

        total_reports = self.total_reports

        last_duration = self.last_duration

        config_id = self.config_id

        filter_processes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filter_processes, Unset):
            filter_processes = []
            for filter_processes_item_data in self.filter_processes:
                filter_processes_item = filter_processes_item_data.to_dict()
                filter_processes.append(filter_processes_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if filter_id is not UNSET:
            field_dict["FilterId"] = filter_id
        if name is not UNSET:
            field_dict["Name"] = name
        if delete_measurement is not UNSET:
            field_dict["DeleteMeasurement"] = delete_measurement
        if delete_header is not UNSET:
            field_dict["DeleteHeader"] = delete_header
        if from_date is not UNSET:
            field_dict["FromDate"] = from_date
        if to_date is not UNSET:
            field_dict["ToDate"] = to_date
        if date_offset is not UNSET:
            field_dict["DateOffset"] = date_offset
        if date_part is not UNSET:
            field_dict["DatePart"] = date_part
        if part_number is not UNSET:
            field_dict["PartNumber"] = part_number
        if revision is not UNSET:
            field_dict["Revision"] = revision
        if max_count is not UNSET:
            field_dict["MaxCount"] = max_count
        if last_run is not UNSET:
            field_dict["LastRun"] = last_run
        if last_affected is not UNSET:
            field_dict["LastAffected"] = last_affected
        if total_run is not UNSET:
            field_dict["TotalRun"] = total_run
        if total_reports is not UNSET:
            field_dict["TotalReports"] = total_reports
        if last_duration is not UNSET:
            field_dict["LastDuration"] = last_duration
        if config_id is not UNSET:
            field_dict["ConfigId"] = config_id
        if filter_processes is not UNSET:
            field_dict["FilterProcesses"] = filter_processes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_archive_filter_process import VirincoWATSWebDashboardModelsTdmArchiveFilterProcess
        d = dict(src_dict)
        filter_id = d.pop("FilterId", UNSET)

        name = d.pop("Name", UNSET)

        delete_measurement = d.pop("DeleteMeasurement", UNSET)

        delete_header = d.pop("DeleteHeader", UNSET)

        _from_date = d.pop("FromDate", UNSET)
        from_date: Union[Unset, datetime.datetime]
        if isinstance(_from_date,  Unset):
            from_date = UNSET
        else:
            from_date = isoparse(_from_date)




        _to_date = d.pop("ToDate", UNSET)
        to_date: Union[Unset, datetime.datetime]
        if isinstance(_to_date,  Unset):
            to_date = UNSET
        else:
            to_date = isoparse(_to_date)




        date_offset = d.pop("DateOffset", UNSET)

        date_part = d.pop("DatePart", UNSET)

        part_number = d.pop("PartNumber", UNSET)

        revision = d.pop("Revision", UNSET)

        max_count = d.pop("MaxCount", UNSET)

        _last_run = d.pop("LastRun", UNSET)
        last_run: Union[Unset, datetime.datetime]
        if isinstance(_last_run,  Unset):
            last_run = UNSET
        else:
            last_run = isoparse(_last_run)




        last_affected = d.pop("LastAffected", UNSET)

        total_run = d.pop("TotalRun", UNSET)

        total_reports = d.pop("TotalReports", UNSET)

        last_duration = d.pop("LastDuration", UNSET)

        config_id = d.pop("ConfigId", UNSET)

        filter_processes = []
        _filter_processes = d.pop("FilterProcesses", UNSET)
        for filter_processes_item_data in (_filter_processes or []):
            filter_processes_item = VirincoWATSWebDashboardModelsTdmArchiveFilterProcess.from_dict(filter_processes_item_data)



            filter_processes.append(filter_processes_item)


        virinco_wats_web_dashboard_models_tdm_archive_filter = cls(
            filter_id=filter_id,
            name=name,
            delete_measurement=delete_measurement,
            delete_header=delete_header,
            from_date=from_date,
            to_date=to_date,
            date_offset=date_offset,
            date_part=date_part,
            part_number=part_number,
            revision=revision,
            max_count=max_count,
            last_run=last_run,
            last_affected=last_affected,
            total_run=total_run,
            total_reports=total_reports,
            last_duration=last_duration,
            config_id=config_id,
            filter_processes=filter_processes,
        )


        virinco_wats_web_dashboard_models_tdm_archive_filter.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_archive_filter

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
