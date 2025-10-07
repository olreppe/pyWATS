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
  from ..models.virinco_wats_web_dashboard_models_chart_data_point import VirincoWATSWebDashboardModelsChartDataPoint





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsChartPlotSerie")



@_attrs_define
class VirincoWATSWebDashboardModelsChartPlotSerie:
    """ 
        Attributes:
            serial_number (Union[Unset, str]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            batch_number (Union[Unset, str]):
            operator (Union[Unset, str]):
            fixture_id (Union[Unset, str]):
            socket_index (Union[Unset, int]):
            process_code (Union[Unset, int]):
            process_name (Union[Unset, str]):
            station_name (Union[Unset, str]):
            sw_filename (Union[Unset, str]):
            sw_version (Union[Unset, str]):
            start_utc (Union[Unset, datetime.datetime]):
            label (Union[Unset, str]):
            step_order_number (Union[Unset, int]):
            guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            status (Union[Unset, str]):
            data_points (Union[Unset, list['VirincoWATSWebDashboardModelsChartDataPoint']]):
            warning (Union[Unset, bool]):
            stdev_y (Union[Unset, float]):
            avg_y (Union[Unset, float]):
            stdev_3_low_y (Union[Unset, float]):
            stdev_3_high_y (Union[Unset, float]):
            max_y_guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            max_ystep_order_number (Union[Unset, int]):
            max_y (Union[Unset, float]):
            min_y_guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            min_ystep_order_number (Union[Unset, int]):
            min_y (Union[Unset, float]):
            range_y (Union[Unset, float]):
            sum_y (Union[Unset, float]):
            sum_2y (Union[Unset, float]):
            count (Union[Unset, float]):
            x_0_removed (Union[Unset, bool]):
            y_0_removed (Union[Unset, bool]):
            x_has_nan_or_inf_values (Union[Unset, bool]):
            y_has_nan_or_inf_values (Union[Unset, bool]):
     """

    serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    batch_number: Union[Unset, str] = UNSET
    operator: Union[Unset, str] = UNSET
    fixture_id: Union[Unset, str] = UNSET
    socket_index: Union[Unset, int] = UNSET
    process_code: Union[Unset, int] = UNSET
    process_name: Union[Unset, str] = UNSET
    station_name: Union[Unset, str] = UNSET
    sw_filename: Union[Unset, str] = UNSET
    sw_version: Union[Unset, str] = UNSET
    start_utc: Union[Unset, datetime.datetime] = UNSET
    label: Union[Unset, str] = UNSET
    step_order_number: Union[Unset, int] = UNSET
    guid: Union[Unset, UUID] = UNSET
    status: Union[Unset, str] = UNSET
    data_points: Union[Unset, list['VirincoWATSWebDashboardModelsChartDataPoint']] = UNSET
    warning: Union[Unset, bool] = UNSET
    stdev_y: Union[Unset, float] = UNSET
    avg_y: Union[Unset, float] = UNSET
    stdev_3_low_y: Union[Unset, float] = UNSET
    stdev_3_high_y: Union[Unset, float] = UNSET
    max_y_guid: Union[Unset, UUID] = UNSET
    max_ystep_order_number: Union[Unset, int] = UNSET
    max_y: Union[Unset, float] = UNSET
    min_y_guid: Union[Unset, UUID] = UNSET
    min_ystep_order_number: Union[Unset, int] = UNSET
    min_y: Union[Unset, float] = UNSET
    range_y: Union[Unset, float] = UNSET
    sum_y: Union[Unset, float] = UNSET
    sum_2y: Union[Unset, float] = UNSET
    count: Union[Unset, float] = UNSET
    x_0_removed: Union[Unset, bool] = UNSET
    y_0_removed: Union[Unset, bool] = UNSET
    x_has_nan_or_inf_values: Union[Unset, bool] = UNSET
    y_has_nan_or_inf_values: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_chart_data_point import VirincoWATSWebDashboardModelsChartDataPoint
        serial_number = self.serial_number

        part_number = self.part_number

        revision = self.revision

        batch_number = self.batch_number

        operator = self.operator

        fixture_id = self.fixture_id

        socket_index = self.socket_index

        process_code = self.process_code

        process_name = self.process_name

        station_name = self.station_name

        sw_filename = self.sw_filename

        sw_version = self.sw_version

        start_utc: Union[Unset, str] = UNSET
        if not isinstance(self.start_utc, Unset):
            start_utc = self.start_utc.isoformat()

        label = self.label

        step_order_number = self.step_order_number

        guid: Union[Unset, str] = UNSET
        if not isinstance(self.guid, Unset):
            guid = str(self.guid)

        status = self.status

        data_points: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data_points, Unset):
            data_points = []
            for data_points_item_data in self.data_points:
                data_points_item = data_points_item_data.to_dict()
                data_points.append(data_points_item)



        warning = self.warning

        stdev_y = self.stdev_y

        avg_y = self.avg_y

        stdev_3_low_y = self.stdev_3_low_y

        stdev_3_high_y = self.stdev_3_high_y

        max_y_guid: Union[Unset, str] = UNSET
        if not isinstance(self.max_y_guid, Unset):
            max_y_guid = str(self.max_y_guid)

        max_ystep_order_number = self.max_ystep_order_number

        max_y = self.max_y

        min_y_guid: Union[Unset, str] = UNSET
        if not isinstance(self.min_y_guid, Unset):
            min_y_guid = str(self.min_y_guid)

        min_ystep_order_number = self.min_ystep_order_number

        min_y = self.min_y

        range_y = self.range_y

        sum_y = self.sum_y

        sum_2y = self.sum_2y

        count = self.count

        x_0_removed = self.x_0_removed

        y_0_removed = self.y_0_removed

        x_has_nan_or_inf_values = self.x_has_nan_or_inf_values

        y_has_nan_or_inf_values = self.y_has_nan_or_inf_values


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
        if batch_number is not UNSET:
            field_dict["batchNumber"] = batch_number
        if operator is not UNSET:
            field_dict["operator"] = operator
        if fixture_id is not UNSET:
            field_dict["fixtureId"] = fixture_id
        if socket_index is not UNSET:
            field_dict["socketIndex"] = socket_index
        if process_code is not UNSET:
            field_dict["processCode"] = process_code
        if process_name is not UNSET:
            field_dict["processName"] = process_name
        if station_name is not UNSET:
            field_dict["stationName"] = station_name
        if sw_filename is not UNSET:
            field_dict["swFilename"] = sw_filename
        if sw_version is not UNSET:
            field_dict["swVersion"] = sw_version
        if start_utc is not UNSET:
            field_dict["startUtc"] = start_utc
        if label is not UNSET:
            field_dict["label"] = label
        if step_order_number is not UNSET:
            field_dict["stepOrderNumber"] = step_order_number
        if guid is not UNSET:
            field_dict["guid"] = guid
        if status is not UNSET:
            field_dict["status"] = status
        if data_points is not UNSET:
            field_dict["dataPoints"] = data_points
        if warning is not UNSET:
            field_dict["warning"] = warning
        if stdev_y is not UNSET:
            field_dict["stdevY"] = stdev_y
        if avg_y is not UNSET:
            field_dict["avgY"] = avg_y
        if stdev_3_low_y is not UNSET:
            field_dict["stdev3LowY"] = stdev_3_low_y
        if stdev_3_high_y is not UNSET:
            field_dict["stdev3HighY"] = stdev_3_high_y
        if max_y_guid is not UNSET:
            field_dict["maxYGuid"] = max_y_guid
        if max_ystep_order_number is not UNSET:
            field_dict["maxYstepOrderNumber"] = max_ystep_order_number
        if max_y is not UNSET:
            field_dict["maxY"] = max_y
        if min_y_guid is not UNSET:
            field_dict["minYGuid"] = min_y_guid
        if min_ystep_order_number is not UNSET:
            field_dict["minYstepOrderNumber"] = min_ystep_order_number
        if min_y is not UNSET:
            field_dict["minY"] = min_y
        if range_y is not UNSET:
            field_dict["rangeY"] = range_y
        if sum_y is not UNSET:
            field_dict["sumY"] = sum_y
        if sum_2y is not UNSET:
            field_dict["sum2Y"] = sum_2y
        if count is not UNSET:
            field_dict["count"] = count
        if x_0_removed is not UNSET:
            field_dict["x0Removed"] = x_0_removed
        if y_0_removed is not UNSET:
            field_dict["y0Removed"] = y_0_removed
        if x_has_nan_or_inf_values is not UNSET:
            field_dict["xHasNanOrInfValues"] = x_has_nan_or_inf_values
        if y_has_nan_or_inf_values is not UNSET:
            field_dict["yHasNanOrInfValues"] = y_has_nan_or_inf_values

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_chart_data_point import VirincoWATSWebDashboardModelsChartDataPoint
        d = dict(src_dict)
        serial_number = d.pop("serialNumber", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        batch_number = d.pop("batchNumber", UNSET)

        operator = d.pop("operator", UNSET)

        fixture_id = d.pop("fixtureId", UNSET)

        socket_index = d.pop("socketIndex", UNSET)

        process_code = d.pop("processCode", UNSET)

        process_name = d.pop("processName", UNSET)

        station_name = d.pop("stationName", UNSET)

        sw_filename = d.pop("swFilename", UNSET)

        sw_version = d.pop("swVersion", UNSET)

        _start_utc = d.pop("startUtc", UNSET)
        start_utc: Union[Unset, datetime.datetime]
        if isinstance(_start_utc,  Unset):
            start_utc = UNSET
        else:
            start_utc = isoparse(_start_utc)




        label = d.pop("label", UNSET)

        step_order_number = d.pop("stepOrderNumber", UNSET)

        _guid = d.pop("guid", UNSET)
        guid: Union[Unset, UUID]
        if isinstance(_guid,  Unset):
            guid = UNSET
        else:
            guid = UUID(_guid)




        status = d.pop("status", UNSET)

        data_points = []
        _data_points = d.pop("dataPoints", UNSET)
        for data_points_item_data in (_data_points or []):
            data_points_item = VirincoWATSWebDashboardModelsChartDataPoint.from_dict(data_points_item_data)



            data_points.append(data_points_item)


        warning = d.pop("warning", UNSET)

        stdev_y = d.pop("stdevY", UNSET)

        avg_y = d.pop("avgY", UNSET)

        stdev_3_low_y = d.pop("stdev3LowY", UNSET)

        stdev_3_high_y = d.pop("stdev3HighY", UNSET)

        _max_y_guid = d.pop("maxYGuid", UNSET)
        max_y_guid: Union[Unset, UUID]
        if isinstance(_max_y_guid,  Unset):
            max_y_guid = UNSET
        else:
            max_y_guid = UUID(_max_y_guid)




        max_ystep_order_number = d.pop("maxYstepOrderNumber", UNSET)

        max_y = d.pop("maxY", UNSET)

        _min_y_guid = d.pop("minYGuid", UNSET)
        min_y_guid: Union[Unset, UUID]
        if isinstance(_min_y_guid,  Unset):
            min_y_guid = UNSET
        else:
            min_y_guid = UUID(_min_y_guid)




        min_ystep_order_number = d.pop("minYstepOrderNumber", UNSET)

        min_y = d.pop("minY", UNSET)

        range_y = d.pop("rangeY", UNSET)

        sum_y = d.pop("sumY", UNSET)

        sum_2y = d.pop("sum2Y", UNSET)

        count = d.pop("count", UNSET)

        x_0_removed = d.pop("x0Removed", UNSET)

        y_0_removed = d.pop("y0Removed", UNSET)

        x_has_nan_or_inf_values = d.pop("xHasNanOrInfValues", UNSET)

        y_has_nan_or_inf_values = d.pop("yHasNanOrInfValues", UNSET)

        virinco_wats_web_dashboard_models_chart_plot_serie = cls(
            serial_number=serial_number,
            part_number=part_number,
            revision=revision,
            batch_number=batch_number,
            operator=operator,
            fixture_id=fixture_id,
            socket_index=socket_index,
            process_code=process_code,
            process_name=process_name,
            station_name=station_name,
            sw_filename=sw_filename,
            sw_version=sw_version,
            start_utc=start_utc,
            label=label,
            step_order_number=step_order_number,
            guid=guid,
            status=status,
            data_points=data_points,
            warning=warning,
            stdev_y=stdev_y,
            avg_y=avg_y,
            stdev_3_low_y=stdev_3_low_y,
            stdev_3_high_y=stdev_3_high_y,
            max_y_guid=max_y_guid,
            max_ystep_order_number=max_ystep_order_number,
            max_y=max_y,
            min_y_guid=min_y_guid,
            min_ystep_order_number=min_ystep_order_number,
            min_y=min_y,
            range_y=range_y,
            sum_y=sum_y,
            sum_2y=sum_2y,
            count=count,
            x_0_removed=x_0_removed,
            y_0_removed=y_0_removed,
            x_has_nan_or_inf_values=x_has_nan_or_inf_values,
            y_has_nan_or_inf_values=y_has_nan_or_inf_values,
        )


        virinco_wats_web_dashboard_models_chart_plot_serie.additional_properties = d
        return virinco_wats_web_dashboard_models_chart_plot_serie

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
