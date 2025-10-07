from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_chart_plot_grouping import VirincoWATSWebDashboardModelsChartPlotGrouping
from ..models.virinco_wats_web_dashboard_models_chart_plot_valid_group_by import VirincoWATSWebDashboardModelsChartPlotValidGroupBy
from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_control_chart import VirincoWATSWebDashboardModelsControlChart
  from ..models.virinco_wats_web_dashboard_models_chart_data_suggestion import VirincoWATSWebDashboardModelsChartDataSuggestion
  from ..models.virinco_wats_web_dashboard_models_chart_plot_serie import VirincoWATSWebDashboardModelsChartPlotSerie





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsChartPlot")



@_attrs_define
class VirincoWATSWebDashboardModelsChartPlot:
    """ 
        Attributes:
            plot_name (Union[Unset, str]):
            plot_index (Union[Unset, int]):
            plot_group (Union[Unset, str]):
            grouping (Union[Unset, VirincoWATSWebDashboardModelsChartPlotGrouping]):
            series (Union[Unset, list['VirincoWATSWebDashboardModelsChartPlotSerie']]):
            avg_y_at_x (Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]):
            range_y_at_x (Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]):
            stdev_y_at_x (Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]):
            min_y_at_x (Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]):
            max_y_at_x (Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]):
            stdev_3_high_y_at_x (Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]):
            stdev_3_low_y_at_x (Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]):
            x_bar (Union[Unset, list['VirincoWATSWebDashboardModelsControlChart']]):
            s_bar (Union[Unset, list['VirincoWATSWebDashboardModelsControlChart']]):
            suggestions (Union[Unset, list['VirincoWATSWebDashboardModelsChartDataSuggestion']]):
            valid_group_by (Union[Unset, VirincoWATSWebDashboardModelsChartPlotValidGroupBy]):
            valid_group_by_string (Union[Unset, str]):
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

    plot_name: Union[Unset, str] = UNSET
    plot_index: Union[Unset, int] = UNSET
    plot_group: Union[Unset, str] = UNSET
    grouping: Union[Unset, VirincoWATSWebDashboardModelsChartPlotGrouping] = UNSET
    series: Union[Unset, list['VirincoWATSWebDashboardModelsChartPlotSerie']] = UNSET
    avg_y_at_x: Union[Unset, 'VirincoWATSWebDashboardModelsChartPlotSerie'] = UNSET
    range_y_at_x: Union[Unset, 'VirincoWATSWebDashboardModelsChartPlotSerie'] = UNSET
    stdev_y_at_x: Union[Unset, 'VirincoWATSWebDashboardModelsChartPlotSerie'] = UNSET
    min_y_at_x: Union[Unset, 'VirincoWATSWebDashboardModelsChartPlotSerie'] = UNSET
    max_y_at_x: Union[Unset, 'VirincoWATSWebDashboardModelsChartPlotSerie'] = UNSET
    stdev_3_high_y_at_x: Union[Unset, 'VirincoWATSWebDashboardModelsChartPlotSerie'] = UNSET
    stdev_3_low_y_at_x: Union[Unset, 'VirincoWATSWebDashboardModelsChartPlotSerie'] = UNSET
    x_bar: Union[Unset, list['VirincoWATSWebDashboardModelsControlChart']] = UNSET
    s_bar: Union[Unset, list['VirincoWATSWebDashboardModelsControlChart']] = UNSET
    suggestions: Union[Unset, list['VirincoWATSWebDashboardModelsChartDataSuggestion']] = UNSET
    valid_group_by: Union[Unset, VirincoWATSWebDashboardModelsChartPlotValidGroupBy] = UNSET
    valid_group_by_string: Union[Unset, str] = UNSET
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
        from ..models.virinco_wats_web_dashboard_models_control_chart import VirincoWATSWebDashboardModelsControlChart
        from ..models.virinco_wats_web_dashboard_models_chart_data_suggestion import VirincoWATSWebDashboardModelsChartDataSuggestion
        from ..models.virinco_wats_web_dashboard_models_chart_plot_serie import VirincoWATSWebDashboardModelsChartPlotSerie
        plot_name = self.plot_name

        plot_index = self.plot_index

        plot_group = self.plot_group

        grouping: Union[Unset, int] = UNSET
        if not isinstance(self.grouping, Unset):
            grouping = self.grouping.value


        series: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.series, Unset):
            series = []
            for series_item_data in self.series:
                series_item = series_item_data.to_dict()
                series.append(series_item)



        avg_y_at_x: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.avg_y_at_x, Unset):
            avg_y_at_x = self.avg_y_at_x.to_dict()

        range_y_at_x: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.range_y_at_x, Unset):
            range_y_at_x = self.range_y_at_x.to_dict()

        stdev_y_at_x: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.stdev_y_at_x, Unset):
            stdev_y_at_x = self.stdev_y_at_x.to_dict()

        min_y_at_x: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.min_y_at_x, Unset):
            min_y_at_x = self.min_y_at_x.to_dict()

        max_y_at_x: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.max_y_at_x, Unset):
            max_y_at_x = self.max_y_at_x.to_dict()

        stdev_3_high_y_at_x: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.stdev_3_high_y_at_x, Unset):
            stdev_3_high_y_at_x = self.stdev_3_high_y_at_x.to_dict()

        stdev_3_low_y_at_x: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.stdev_3_low_y_at_x, Unset):
            stdev_3_low_y_at_x = self.stdev_3_low_y_at_x.to_dict()

        x_bar: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.x_bar, Unset):
            x_bar = []
            for x_bar_item_data in self.x_bar:
                x_bar_item = x_bar_item_data.to_dict()
                x_bar.append(x_bar_item)



        s_bar: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.s_bar, Unset):
            s_bar = []
            for s_bar_item_data in self.s_bar:
                s_bar_item = s_bar_item_data.to_dict()
                s_bar.append(s_bar_item)



        suggestions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.suggestions, Unset):
            suggestions = []
            for suggestions_item_data in self.suggestions:
                suggestions_item = suggestions_item_data.to_dict()
                suggestions.append(suggestions_item)



        valid_group_by: Union[Unset, int] = UNSET
        if not isinstance(self.valid_group_by, Unset):
            valid_group_by = self.valid_group_by.value


        valid_group_by_string = self.valid_group_by_string

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
        if plot_name is not UNSET:
            field_dict["plotName"] = plot_name
        if plot_index is not UNSET:
            field_dict["plotIndex"] = plot_index
        if plot_group is not UNSET:
            field_dict["plotGroup"] = plot_group
        if grouping is not UNSET:
            field_dict["grouping"] = grouping
        if series is not UNSET:
            field_dict["series"] = series
        if avg_y_at_x is not UNSET:
            field_dict["avgYAtX"] = avg_y_at_x
        if range_y_at_x is not UNSET:
            field_dict["rangeYAtX"] = range_y_at_x
        if stdev_y_at_x is not UNSET:
            field_dict["stdevYAtX"] = stdev_y_at_x
        if min_y_at_x is not UNSET:
            field_dict["minYAtX"] = min_y_at_x
        if max_y_at_x is not UNSET:
            field_dict["maxYAtX"] = max_y_at_x
        if stdev_3_high_y_at_x is not UNSET:
            field_dict["stdev3HighYAtX"] = stdev_3_high_y_at_x
        if stdev_3_low_y_at_x is not UNSET:
            field_dict["stdev3LowYAtX"] = stdev_3_low_y_at_x
        if x_bar is not UNSET:
            field_dict["xBar"] = x_bar
        if s_bar is not UNSET:
            field_dict["sBar"] = s_bar
        if suggestions is not UNSET:
            field_dict["suggestions"] = suggestions
        if valid_group_by is not UNSET:
            field_dict["validGroupBy"] = valid_group_by
        if valid_group_by_string is not UNSET:
            field_dict["validGroupByString"] = valid_group_by_string
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
        from ..models.virinco_wats_web_dashboard_models_control_chart import VirincoWATSWebDashboardModelsControlChart
        from ..models.virinco_wats_web_dashboard_models_chart_data_suggestion import VirincoWATSWebDashboardModelsChartDataSuggestion
        from ..models.virinco_wats_web_dashboard_models_chart_plot_serie import VirincoWATSWebDashboardModelsChartPlotSerie
        d = dict(src_dict)
        plot_name = d.pop("plotName", UNSET)

        plot_index = d.pop("plotIndex", UNSET)

        plot_group = d.pop("plotGroup", UNSET)

        _grouping = d.pop("grouping", UNSET)
        grouping: Union[Unset, VirincoWATSWebDashboardModelsChartPlotGrouping]
        if isinstance(_grouping,  Unset):
            grouping = UNSET
        else:
            grouping = VirincoWATSWebDashboardModelsChartPlotGrouping(_grouping)




        series = []
        _series = d.pop("series", UNSET)
        for series_item_data in (_series or []):
            series_item = VirincoWATSWebDashboardModelsChartPlotSerie.from_dict(series_item_data)



            series.append(series_item)


        _avg_y_at_x = d.pop("avgYAtX", UNSET)
        avg_y_at_x: Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]
        if isinstance(_avg_y_at_x,  Unset):
            avg_y_at_x = UNSET
        else:
            avg_y_at_x = VirincoWATSWebDashboardModelsChartPlotSerie.from_dict(_avg_y_at_x)




        _range_y_at_x = d.pop("rangeYAtX", UNSET)
        range_y_at_x: Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]
        if isinstance(_range_y_at_x,  Unset):
            range_y_at_x = UNSET
        else:
            range_y_at_x = VirincoWATSWebDashboardModelsChartPlotSerie.from_dict(_range_y_at_x)




        _stdev_y_at_x = d.pop("stdevYAtX", UNSET)
        stdev_y_at_x: Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]
        if isinstance(_stdev_y_at_x,  Unset):
            stdev_y_at_x = UNSET
        else:
            stdev_y_at_x = VirincoWATSWebDashboardModelsChartPlotSerie.from_dict(_stdev_y_at_x)




        _min_y_at_x = d.pop("minYAtX", UNSET)
        min_y_at_x: Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]
        if isinstance(_min_y_at_x,  Unset):
            min_y_at_x = UNSET
        else:
            min_y_at_x = VirincoWATSWebDashboardModelsChartPlotSerie.from_dict(_min_y_at_x)




        _max_y_at_x = d.pop("maxYAtX", UNSET)
        max_y_at_x: Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]
        if isinstance(_max_y_at_x,  Unset):
            max_y_at_x = UNSET
        else:
            max_y_at_x = VirincoWATSWebDashboardModelsChartPlotSerie.from_dict(_max_y_at_x)




        _stdev_3_high_y_at_x = d.pop("stdev3HighYAtX", UNSET)
        stdev_3_high_y_at_x: Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]
        if isinstance(_stdev_3_high_y_at_x,  Unset):
            stdev_3_high_y_at_x = UNSET
        else:
            stdev_3_high_y_at_x = VirincoWATSWebDashboardModelsChartPlotSerie.from_dict(_stdev_3_high_y_at_x)




        _stdev_3_low_y_at_x = d.pop("stdev3LowYAtX", UNSET)
        stdev_3_low_y_at_x: Union[Unset, VirincoWATSWebDashboardModelsChartPlotSerie]
        if isinstance(_stdev_3_low_y_at_x,  Unset):
            stdev_3_low_y_at_x = UNSET
        else:
            stdev_3_low_y_at_x = VirincoWATSWebDashboardModelsChartPlotSerie.from_dict(_stdev_3_low_y_at_x)




        x_bar = []
        _x_bar = d.pop("xBar", UNSET)
        for x_bar_item_data in (_x_bar or []):
            x_bar_item = VirincoWATSWebDashboardModelsControlChart.from_dict(x_bar_item_data)



            x_bar.append(x_bar_item)


        s_bar = []
        _s_bar = d.pop("sBar", UNSET)
        for s_bar_item_data in (_s_bar or []):
            s_bar_item = VirincoWATSWebDashboardModelsControlChart.from_dict(s_bar_item_data)



            s_bar.append(s_bar_item)


        suggestions = []
        _suggestions = d.pop("suggestions", UNSET)
        for suggestions_item_data in (_suggestions or []):
            suggestions_item = VirincoWATSWebDashboardModelsChartDataSuggestion.from_dict(suggestions_item_data)



            suggestions.append(suggestions_item)


        _valid_group_by = d.pop("validGroupBy", UNSET)
        valid_group_by: Union[Unset, VirincoWATSWebDashboardModelsChartPlotValidGroupBy]
        if isinstance(_valid_group_by,  Unset):
            valid_group_by = UNSET
        else:
            valid_group_by = VirincoWATSWebDashboardModelsChartPlotValidGroupBy(_valid_group_by)




        valid_group_by_string = d.pop("validGroupByString", UNSET)

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

        virinco_wats_web_dashboard_models_chart_plot = cls(
            plot_name=plot_name,
            plot_index=plot_index,
            plot_group=plot_group,
            grouping=grouping,
            series=series,
            avg_y_at_x=avg_y_at_x,
            range_y_at_x=range_y_at_x,
            stdev_y_at_x=stdev_y_at_x,
            min_y_at_x=min_y_at_x,
            max_y_at_x=max_y_at_x,
            stdev_3_high_y_at_x=stdev_3_high_y_at_x,
            stdev_3_low_y_at_x=stdev_3_low_y_at_x,
            x_bar=x_bar,
            s_bar=s_bar,
            suggestions=suggestions,
            valid_group_by=valid_group_by,
            valid_group_by_string=valid_group_by_string,
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


        virinco_wats_web_dashboard_models_chart_plot.additional_properties = d
        return virinco_wats_web_dashboard_models_chart_plot

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
