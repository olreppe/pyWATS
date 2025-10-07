from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_chart_plot import VirincoWATSWebDashboardModelsChartPlot





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsChartData")



@_attrs_define
class VirincoWATSWebDashboardModelsChartData:
    """ 
        Attributes:
            loaded_reports (Union[Unset, int]):
            total_reports (Union[Unset, int]):
            chart_label (Union[Unset, str]):
            x_label (Union[Unset, str]):
            x_unit (Union[Unset, str]):
            y_label (Union[Unset, str]):
            y_unit (Union[Unset, str]):
            chart_type (Union[Unset, str]):
            plots (Union[Unset, list['VirincoWATSWebDashboardModelsChartPlot']]):
            report_uuids (Union[Unset, list[UUID]]):
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

    loaded_reports: Union[Unset, int] = UNSET
    total_reports: Union[Unset, int] = UNSET
    chart_label: Union[Unset, str] = UNSET
    x_label: Union[Unset, str] = UNSET
    x_unit: Union[Unset, str] = UNSET
    y_label: Union[Unset, str] = UNSET
    y_unit: Union[Unset, str] = UNSET
    chart_type: Union[Unset, str] = UNSET
    plots: Union[Unset, list['VirincoWATSWebDashboardModelsChartPlot']] = UNSET
    report_uuids: Union[Unset, list[UUID]] = UNSET
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
        from ..models.virinco_wats_web_dashboard_models_chart_plot import VirincoWATSWebDashboardModelsChartPlot
        loaded_reports = self.loaded_reports

        total_reports = self.total_reports

        chart_label = self.chart_label

        x_label = self.x_label

        x_unit = self.x_unit

        y_label = self.y_label

        y_unit = self.y_unit

        chart_type = self.chart_type

        plots: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.plots, Unset):
            plots = []
            for plots_item_data in self.plots:
                plots_item = plots_item_data.to_dict()
                plots.append(plots_item)



        report_uuids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.report_uuids, Unset):
            report_uuids = []
            for report_uuids_item_data in self.report_uuids:
                report_uuids_item = str(report_uuids_item_data)
                report_uuids.append(report_uuids_item)



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
        if loaded_reports is not UNSET:
            field_dict["loadedReports"] = loaded_reports
        if total_reports is not UNSET:
            field_dict["totalReports"] = total_reports
        if chart_label is not UNSET:
            field_dict["chartLabel"] = chart_label
        if x_label is not UNSET:
            field_dict["xLabel"] = x_label
        if x_unit is not UNSET:
            field_dict["xUnit"] = x_unit
        if y_label is not UNSET:
            field_dict["yLabel"] = y_label
        if y_unit is not UNSET:
            field_dict["yUnit"] = y_unit
        if chart_type is not UNSET:
            field_dict["chartType"] = chart_type
        if plots is not UNSET:
            field_dict["plots"] = plots
        if report_uuids is not UNSET:
            field_dict["reportUuids"] = report_uuids
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
        from ..models.virinco_wats_web_dashboard_models_chart_plot import VirincoWATSWebDashboardModelsChartPlot
        d = dict(src_dict)
        loaded_reports = d.pop("loadedReports", UNSET)

        total_reports = d.pop("totalReports", UNSET)

        chart_label = d.pop("chartLabel", UNSET)

        x_label = d.pop("xLabel", UNSET)

        x_unit = d.pop("xUnit", UNSET)

        y_label = d.pop("yLabel", UNSET)

        y_unit = d.pop("yUnit", UNSET)

        chart_type = d.pop("chartType", UNSET)

        plots = []
        _plots = d.pop("plots", UNSET)
        for plots_item_data in (_plots or []):
            plots_item = VirincoWATSWebDashboardModelsChartPlot.from_dict(plots_item_data)



            plots.append(plots_item)


        report_uuids = []
        _report_uuids = d.pop("reportUuids", UNSET)
        for report_uuids_item_data in (_report_uuids or []):
            report_uuids_item = UUID(report_uuids_item_data)



            report_uuids.append(report_uuids_item)


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

        virinco_wats_web_dashboard_models_chart_data = cls(
            loaded_reports=loaded_reports,
            total_reports=total_reports,
            chart_label=chart_label,
            x_label=x_label,
            x_unit=x_unit,
            y_label=y_label,
            y_unit=y_unit,
            chart_type=chart_type,
            plots=plots,
            report_uuids=report_uuids,
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


        virinco_wats_web_dashboard_models_chart_data.additional_properties = d
        return virinco_wats_web_dashboard_models_chart_data

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
