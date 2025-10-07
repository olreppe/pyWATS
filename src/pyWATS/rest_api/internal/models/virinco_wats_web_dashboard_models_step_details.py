from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_step_details_grouping import VirincoWATSWebDashboardModelsStepDetailsGrouping
from ..models.virinco_wats_web_dashboard_models_step_details_options import VirincoWATSWebDashboardModelsStepDetailsOptions
from ..models.virinco_wats_web_dashboard_models_step_details_valid_group_by import VirincoWATSWebDashboardModelsStepDetailsValidGroupBy
from ..models.virinco_wats_web_dashboard_models_step_details_valid_group_by_suggestions import VirincoWATSWebDashboardModelsStepDetailsValidGroupBySuggestions
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_control_chart import VirincoWATSWebDashboardModelsControlChart
  from ..models.virinco_wats_web_dashboard_models_step_details_suggestion import VirincoWATSWebDashboardModelsStepDetailsSuggestion
  from ..models.virinco_wats_web_dashboard_models_aggregated_measurement import VirincoWATSWebDashboardModelsAggregatedMeasurement
  from ..models.virinco_wats_web_dashboard_models_measurement_group import VirincoWATSWebDashboardModelsMeasurementGroup





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsStepDetails")



@_attrs_define
class VirincoWATSWebDashboardModelsStepDetails:
    """ 
        Attributes:
            measurement_groups (Union[Unset, list['VirincoWATSWebDashboardModelsMeasurementGroup']]):
            aggregated_measurements (Union[Unset, list['VirincoWATSWebDashboardModelsAggregatedMeasurement']]):
            grouping (Union[Unset, VirincoWATSWebDashboardModelsStepDetailsGrouping]):
            options (Union[Unset, VirincoWATSWebDashboardModelsStepDetailsOptions]):
            plot_from (Union[Unset, float]):
            plot_to (Union[Unset, float]):
            zoom_from (Union[Unset, float]):
            zoom_to (Union[Unset, float]):
            valid_group_by (Union[Unset, VirincoWATSWebDashboardModelsStepDetailsValidGroupBy]):
            valid_group_by_string (Union[Unset, str]):
            valid_group_by_suggestions (Union[Unset, VirincoWATSWebDashboardModelsStepDetailsValidGroupBySuggestions]):
            valid_group_by_suggestions_string (Union[Unset, str]):
            valid_group_by_misc_descriptions (Union[Unset, list[str]]):
            suggestions (Union[Unset, list['VirincoWATSWebDashboardModelsStepDetailsSuggestion']]):
            x_bar (Union[Unset, list['VirincoWATSWebDashboardModelsControlChart']]):
            s_bar (Union[Unset, list['VirincoWATSWebDashboardModelsControlChart']]):
            cpl (Union[Unset, float]):
            cpu (Union[Unset, float]):
            cp (Union[Unset, float]):
            cpk (Union[Unset, float]):
            max_ (Union[Unset, float]):
            min_ (Union[Unset, float]):
            avg (Union[Unset, float]):
            sum_ (Union[Unset, float]):
            sum2 (Union[Unset, float]):
            stdev (Union[Unset, float]):
            sigma_low_3 (Union[Unset, float]):
            sigma_high_3 (Union[Unset, float]):
            var (Union[Unset, float]):
            count (Union[Unset, int]):
            meas_count (Union[Unset, int]):
            median (Union[Unset, float]):
            q1 (Union[Unset, float]):
            q3 (Union[Unset, float]):
            step_time_min (Union[Unset, float]):
            step_time_avg (Union[Unset, float]):
            step_time_max (Union[Unset, float]):
            max_utc_start_time (Union[Unset, datetime.datetime]):
            min_utc_start_time (Union[Unset, datetime.datetime]):
            variabel_limit_1 (Union[Unset, bool]):
            variabel_limit_2 (Union[Unset, bool]):
            limit1 (Union[Unset, float]):
            limit2 (Union[Unset, float]):
            comp_operator (Union[Unset, str]):
            unit (Union[Unset, str]):
            test_status (Union[Unset, str]):
            measure_status (Union[Unset, str]):
            step_status (Union[Unset, str]):
            warning (Union[Unset, bool]):
            m (Union[Unset, str]):
            op (Union[Unset, str]):
            p (Union[Unset, str]):
            r (Union[Unset, str]):
            b (Union[Unset, str]):
            si (Union[Unset, int]):
            f (Union[Unset, str]):
            to (Union[Unset, str]):
            sf (Union[Unset, str]):
            sv (Union[Unset, str]):
     """

    measurement_groups: Union[Unset, list['VirincoWATSWebDashboardModelsMeasurementGroup']] = UNSET
    aggregated_measurements: Union[Unset, list['VirincoWATSWebDashboardModelsAggregatedMeasurement']] = UNSET
    grouping: Union[Unset, VirincoWATSWebDashboardModelsStepDetailsGrouping] = UNSET
    options: Union[Unset, VirincoWATSWebDashboardModelsStepDetailsOptions] = UNSET
    plot_from: Union[Unset, float] = UNSET
    plot_to: Union[Unset, float] = UNSET
    zoom_from: Union[Unset, float] = UNSET
    zoom_to: Union[Unset, float] = UNSET
    valid_group_by: Union[Unset, VirincoWATSWebDashboardModelsStepDetailsValidGroupBy] = UNSET
    valid_group_by_string: Union[Unset, str] = UNSET
    valid_group_by_suggestions: Union[Unset, VirincoWATSWebDashboardModelsStepDetailsValidGroupBySuggestions] = UNSET
    valid_group_by_suggestions_string: Union[Unset, str] = UNSET
    valid_group_by_misc_descriptions: Union[Unset, list[str]] = UNSET
    suggestions: Union[Unset, list['VirincoWATSWebDashboardModelsStepDetailsSuggestion']] = UNSET
    x_bar: Union[Unset, list['VirincoWATSWebDashboardModelsControlChart']] = UNSET
    s_bar: Union[Unset, list['VirincoWATSWebDashboardModelsControlChart']] = UNSET
    cpl: Union[Unset, float] = UNSET
    cpu: Union[Unset, float] = UNSET
    cp: Union[Unset, float] = UNSET
    cpk: Union[Unset, float] = UNSET
    max_: Union[Unset, float] = UNSET
    min_: Union[Unset, float] = UNSET
    avg: Union[Unset, float] = UNSET
    sum_: Union[Unset, float] = UNSET
    sum2: Union[Unset, float] = UNSET
    stdev: Union[Unset, float] = UNSET
    sigma_low_3: Union[Unset, float] = UNSET
    sigma_high_3: Union[Unset, float] = UNSET
    var: Union[Unset, float] = UNSET
    count: Union[Unset, int] = UNSET
    meas_count: Union[Unset, int] = UNSET
    median: Union[Unset, float] = UNSET
    q1: Union[Unset, float] = UNSET
    q3: Union[Unset, float] = UNSET
    step_time_min: Union[Unset, float] = UNSET
    step_time_avg: Union[Unset, float] = UNSET
    step_time_max: Union[Unset, float] = UNSET
    max_utc_start_time: Union[Unset, datetime.datetime] = UNSET
    min_utc_start_time: Union[Unset, datetime.datetime] = UNSET
    variabel_limit_1: Union[Unset, bool] = UNSET
    variabel_limit_2: Union[Unset, bool] = UNSET
    limit1: Union[Unset, float] = UNSET
    limit2: Union[Unset, float] = UNSET
    comp_operator: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    test_status: Union[Unset, str] = UNSET
    measure_status: Union[Unset, str] = UNSET
    step_status: Union[Unset, str] = UNSET
    warning: Union[Unset, bool] = UNSET
    m: Union[Unset, str] = UNSET
    op: Union[Unset, str] = UNSET
    p: Union[Unset, str] = UNSET
    r: Union[Unset, str] = UNSET
    b: Union[Unset, str] = UNSET
    si: Union[Unset, int] = UNSET
    f: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    sf: Union[Unset, str] = UNSET
    sv: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_control_chart import VirincoWATSWebDashboardModelsControlChart
        from ..models.virinco_wats_web_dashboard_models_step_details_suggestion import VirincoWATSWebDashboardModelsStepDetailsSuggestion
        from ..models.virinco_wats_web_dashboard_models_aggregated_measurement import VirincoWATSWebDashboardModelsAggregatedMeasurement
        from ..models.virinco_wats_web_dashboard_models_measurement_group import VirincoWATSWebDashboardModelsMeasurementGroup
        measurement_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.measurement_groups, Unset):
            measurement_groups = []
            for measurement_groups_item_data in self.measurement_groups:
                measurement_groups_item = measurement_groups_item_data.to_dict()
                measurement_groups.append(measurement_groups_item)



        aggregated_measurements: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.aggregated_measurements, Unset):
            aggregated_measurements = []
            for aggregated_measurements_item_data in self.aggregated_measurements:
                aggregated_measurements_item = aggregated_measurements_item_data.to_dict()
                aggregated_measurements.append(aggregated_measurements_item)



        grouping: Union[Unset, int] = UNSET
        if not isinstance(self.grouping, Unset):
            grouping = self.grouping.value


        options: Union[Unset, int] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.value


        plot_from = self.plot_from

        plot_to = self.plot_to

        zoom_from = self.zoom_from

        zoom_to = self.zoom_to

        valid_group_by: Union[Unset, int] = UNSET
        if not isinstance(self.valid_group_by, Unset):
            valid_group_by = self.valid_group_by.value


        valid_group_by_string = self.valid_group_by_string

        valid_group_by_suggestions: Union[Unset, int] = UNSET
        if not isinstance(self.valid_group_by_suggestions, Unset):
            valid_group_by_suggestions = self.valid_group_by_suggestions.value


        valid_group_by_suggestions_string = self.valid_group_by_suggestions_string

        valid_group_by_misc_descriptions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.valid_group_by_misc_descriptions, Unset):
            valid_group_by_misc_descriptions = self.valid_group_by_misc_descriptions



        suggestions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.suggestions, Unset):
            suggestions = []
            for suggestions_item_data in self.suggestions:
                suggestions_item = suggestions_item_data.to_dict()
                suggestions.append(suggestions_item)



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



        cpl = self.cpl

        cpu = self.cpu

        cp = self.cp

        cpk = self.cpk

        max_ = self.max_

        min_ = self.min_

        avg = self.avg

        sum_ = self.sum_

        sum2 = self.sum2

        stdev = self.stdev

        sigma_low_3 = self.sigma_low_3

        sigma_high_3 = self.sigma_high_3

        var = self.var

        count = self.count

        meas_count = self.meas_count

        median = self.median

        q1 = self.q1

        q3 = self.q3

        step_time_min = self.step_time_min

        step_time_avg = self.step_time_avg

        step_time_max = self.step_time_max

        max_utc_start_time: Union[Unset, str] = UNSET
        if not isinstance(self.max_utc_start_time, Unset):
            max_utc_start_time = self.max_utc_start_time.isoformat()

        min_utc_start_time: Union[Unset, str] = UNSET
        if not isinstance(self.min_utc_start_time, Unset):
            min_utc_start_time = self.min_utc_start_time.isoformat()

        variabel_limit_1 = self.variabel_limit_1

        variabel_limit_2 = self.variabel_limit_2

        limit1 = self.limit1

        limit2 = self.limit2

        comp_operator = self.comp_operator

        unit = self.unit

        test_status = self.test_status

        measure_status = self.measure_status

        step_status = self.step_status

        warning = self.warning

        m = self.m

        op = self.op

        p = self.p

        r = self.r

        b = self.b

        si = self.si

        f = self.f

        to = self.to

        sf = self.sf

        sv = self.sv


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if measurement_groups is not UNSET:
            field_dict["measurementGroups"] = measurement_groups
        if aggregated_measurements is not UNSET:
            field_dict["aggregatedMeasurements"] = aggregated_measurements
        if grouping is not UNSET:
            field_dict["grouping"] = grouping
        if options is not UNSET:
            field_dict["options"] = options
        if plot_from is not UNSET:
            field_dict["plotFrom"] = plot_from
        if plot_to is not UNSET:
            field_dict["plotTo"] = plot_to
        if zoom_from is not UNSET:
            field_dict["zoomFrom"] = zoom_from
        if zoom_to is not UNSET:
            field_dict["zoomTo"] = zoom_to
        if valid_group_by is not UNSET:
            field_dict["validGroupBy"] = valid_group_by
        if valid_group_by_string is not UNSET:
            field_dict["validGroupByString"] = valid_group_by_string
        if valid_group_by_suggestions is not UNSET:
            field_dict["validGroupBySuggestions"] = valid_group_by_suggestions
        if valid_group_by_suggestions_string is not UNSET:
            field_dict["validGroupBySuggestionsString"] = valid_group_by_suggestions_string
        if valid_group_by_misc_descriptions is not UNSET:
            field_dict["validGroupByMiscDescriptions"] = valid_group_by_misc_descriptions
        if suggestions is not UNSET:
            field_dict["suggestions"] = suggestions
        if x_bar is not UNSET:
            field_dict["xBar"] = x_bar
        if s_bar is not UNSET:
            field_dict["sBar"] = s_bar
        if cpl is not UNSET:
            field_dict["cpl"] = cpl
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if cp is not UNSET:
            field_dict["cp"] = cp
        if cpk is not UNSET:
            field_dict["cpk"] = cpk
        if max_ is not UNSET:
            field_dict["max"] = max_
        if min_ is not UNSET:
            field_dict["min"] = min_
        if avg is not UNSET:
            field_dict["avg"] = avg
        if sum_ is not UNSET:
            field_dict["sum"] = sum_
        if sum2 is not UNSET:
            field_dict["sum2"] = sum2
        if stdev is not UNSET:
            field_dict["stdev"] = stdev
        if sigma_low_3 is not UNSET:
            field_dict["sigmaLow3"] = sigma_low_3
        if sigma_high_3 is not UNSET:
            field_dict["sigmaHigh3"] = sigma_high_3
        if var is not UNSET:
            field_dict["var"] = var
        if count is not UNSET:
            field_dict["count"] = count
        if meas_count is not UNSET:
            field_dict["measCount"] = meas_count
        if median is not UNSET:
            field_dict["median"] = median
        if q1 is not UNSET:
            field_dict["q1"] = q1
        if q3 is not UNSET:
            field_dict["q3"] = q3
        if step_time_min is not UNSET:
            field_dict["stepTimeMin"] = step_time_min
        if step_time_avg is not UNSET:
            field_dict["stepTimeAvg"] = step_time_avg
        if step_time_max is not UNSET:
            field_dict["stepTimeMax"] = step_time_max
        if max_utc_start_time is not UNSET:
            field_dict["maxUtcStartTime"] = max_utc_start_time
        if min_utc_start_time is not UNSET:
            field_dict["minUtcStartTime"] = min_utc_start_time
        if variabel_limit_1 is not UNSET:
            field_dict["variabelLimit1"] = variabel_limit_1
        if variabel_limit_2 is not UNSET:
            field_dict["variabelLimit2"] = variabel_limit_2
        if limit1 is not UNSET:
            field_dict["limit1"] = limit1
        if limit2 is not UNSET:
            field_dict["limit2"] = limit2
        if comp_operator is not UNSET:
            field_dict["compOperator"] = comp_operator
        if unit is not UNSET:
            field_dict["unit"] = unit
        if test_status is not UNSET:
            field_dict["testStatus"] = test_status
        if measure_status is not UNSET:
            field_dict["measureStatus"] = measure_status
        if step_status is not UNSET:
            field_dict["stepStatus"] = step_status
        if warning is not UNSET:
            field_dict["warning"] = warning
        if m is not UNSET:
            field_dict["m"] = m
        if op is not UNSET:
            field_dict["op"] = op
        if p is not UNSET:
            field_dict["p"] = p
        if r is not UNSET:
            field_dict["r"] = r
        if b is not UNSET:
            field_dict["b"] = b
        if si is not UNSET:
            field_dict["si"] = si
        if f is not UNSET:
            field_dict["f"] = f
        if to is not UNSET:
            field_dict["to"] = to
        if sf is not UNSET:
            field_dict["sf"] = sf
        if sv is not UNSET:
            field_dict["sv"] = sv

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_control_chart import VirincoWATSWebDashboardModelsControlChart
        from ..models.virinco_wats_web_dashboard_models_step_details_suggestion import VirincoWATSWebDashboardModelsStepDetailsSuggestion
        from ..models.virinco_wats_web_dashboard_models_aggregated_measurement import VirincoWATSWebDashboardModelsAggregatedMeasurement
        from ..models.virinco_wats_web_dashboard_models_measurement_group import VirincoWATSWebDashboardModelsMeasurementGroup
        d = dict(src_dict)
        measurement_groups = []
        _measurement_groups = d.pop("measurementGroups", UNSET)
        for measurement_groups_item_data in (_measurement_groups or []):
            measurement_groups_item = VirincoWATSWebDashboardModelsMeasurementGroup.from_dict(measurement_groups_item_data)



            measurement_groups.append(measurement_groups_item)


        aggregated_measurements = []
        _aggregated_measurements = d.pop("aggregatedMeasurements", UNSET)
        for aggregated_measurements_item_data in (_aggregated_measurements or []):
            aggregated_measurements_item = VirincoWATSWebDashboardModelsAggregatedMeasurement.from_dict(aggregated_measurements_item_data)



            aggregated_measurements.append(aggregated_measurements_item)


        _grouping = d.pop("grouping", UNSET)
        grouping: Union[Unset, VirincoWATSWebDashboardModelsStepDetailsGrouping]
        if isinstance(_grouping,  Unset):
            grouping = UNSET
        else:
            grouping = VirincoWATSWebDashboardModelsStepDetailsGrouping(_grouping)




        _options = d.pop("options", UNSET)
        options: Union[Unset, VirincoWATSWebDashboardModelsStepDetailsOptions]
        if isinstance(_options,  Unset):
            options = UNSET
        else:
            options = VirincoWATSWebDashboardModelsStepDetailsOptions(_options)




        plot_from = d.pop("plotFrom", UNSET)

        plot_to = d.pop("plotTo", UNSET)

        zoom_from = d.pop("zoomFrom", UNSET)

        zoom_to = d.pop("zoomTo", UNSET)

        _valid_group_by = d.pop("validGroupBy", UNSET)
        valid_group_by: Union[Unset, VirincoWATSWebDashboardModelsStepDetailsValidGroupBy]
        if isinstance(_valid_group_by,  Unset):
            valid_group_by = UNSET
        else:
            valid_group_by = VirincoWATSWebDashboardModelsStepDetailsValidGroupBy(_valid_group_by)




        valid_group_by_string = d.pop("validGroupByString", UNSET)

        _valid_group_by_suggestions = d.pop("validGroupBySuggestions", UNSET)
        valid_group_by_suggestions: Union[Unset, VirincoWATSWebDashboardModelsStepDetailsValidGroupBySuggestions]
        if isinstance(_valid_group_by_suggestions,  Unset):
            valid_group_by_suggestions = UNSET
        else:
            valid_group_by_suggestions = VirincoWATSWebDashboardModelsStepDetailsValidGroupBySuggestions(_valid_group_by_suggestions)




        valid_group_by_suggestions_string = d.pop("validGroupBySuggestionsString", UNSET)

        valid_group_by_misc_descriptions = cast(list[str], d.pop("validGroupByMiscDescriptions", UNSET))


        suggestions = []
        _suggestions = d.pop("suggestions", UNSET)
        for suggestions_item_data in (_suggestions or []):
            suggestions_item = VirincoWATSWebDashboardModelsStepDetailsSuggestion.from_dict(suggestions_item_data)



            suggestions.append(suggestions_item)


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


        cpl = d.pop("cpl", UNSET)

        cpu = d.pop("cpu", UNSET)

        cp = d.pop("cp", UNSET)

        cpk = d.pop("cpk", UNSET)

        max_ = d.pop("max", UNSET)

        min_ = d.pop("min", UNSET)

        avg = d.pop("avg", UNSET)

        sum_ = d.pop("sum", UNSET)

        sum2 = d.pop("sum2", UNSET)

        stdev = d.pop("stdev", UNSET)

        sigma_low_3 = d.pop("sigmaLow3", UNSET)

        sigma_high_3 = d.pop("sigmaHigh3", UNSET)

        var = d.pop("var", UNSET)

        count = d.pop("count", UNSET)

        meas_count = d.pop("measCount", UNSET)

        median = d.pop("median", UNSET)

        q1 = d.pop("q1", UNSET)

        q3 = d.pop("q3", UNSET)

        step_time_min = d.pop("stepTimeMin", UNSET)

        step_time_avg = d.pop("stepTimeAvg", UNSET)

        step_time_max = d.pop("stepTimeMax", UNSET)

        _max_utc_start_time = d.pop("maxUtcStartTime", UNSET)
        max_utc_start_time: Union[Unset, datetime.datetime]
        if isinstance(_max_utc_start_time,  Unset):
            max_utc_start_time = UNSET
        else:
            max_utc_start_time = isoparse(_max_utc_start_time)




        _min_utc_start_time = d.pop("minUtcStartTime", UNSET)
        min_utc_start_time: Union[Unset, datetime.datetime]
        if isinstance(_min_utc_start_time,  Unset):
            min_utc_start_time = UNSET
        else:
            min_utc_start_time = isoparse(_min_utc_start_time)




        variabel_limit_1 = d.pop("variabelLimit1", UNSET)

        variabel_limit_2 = d.pop("variabelLimit2", UNSET)

        limit1 = d.pop("limit1", UNSET)

        limit2 = d.pop("limit2", UNSET)

        comp_operator = d.pop("compOperator", UNSET)

        unit = d.pop("unit", UNSET)

        test_status = d.pop("testStatus", UNSET)

        measure_status = d.pop("measureStatus", UNSET)

        step_status = d.pop("stepStatus", UNSET)

        warning = d.pop("warning", UNSET)

        m = d.pop("m", UNSET)

        op = d.pop("op", UNSET)

        p = d.pop("p", UNSET)

        r = d.pop("r", UNSET)

        b = d.pop("b", UNSET)

        si = d.pop("si", UNSET)

        f = d.pop("f", UNSET)

        to = d.pop("to", UNSET)

        sf = d.pop("sf", UNSET)

        sv = d.pop("sv", UNSET)

        virinco_wats_web_dashboard_models_step_details = cls(
            measurement_groups=measurement_groups,
            aggregated_measurements=aggregated_measurements,
            grouping=grouping,
            options=options,
            plot_from=plot_from,
            plot_to=plot_to,
            zoom_from=zoom_from,
            zoom_to=zoom_to,
            valid_group_by=valid_group_by,
            valid_group_by_string=valid_group_by_string,
            valid_group_by_suggestions=valid_group_by_suggestions,
            valid_group_by_suggestions_string=valid_group_by_suggestions_string,
            valid_group_by_misc_descriptions=valid_group_by_misc_descriptions,
            suggestions=suggestions,
            x_bar=x_bar,
            s_bar=s_bar,
            cpl=cpl,
            cpu=cpu,
            cp=cp,
            cpk=cpk,
            max_=max_,
            min_=min_,
            avg=avg,
            sum_=sum_,
            sum2=sum2,
            stdev=stdev,
            sigma_low_3=sigma_low_3,
            sigma_high_3=sigma_high_3,
            var=var,
            count=count,
            meas_count=meas_count,
            median=median,
            q1=q1,
            q3=q3,
            step_time_min=step_time_min,
            step_time_avg=step_time_avg,
            step_time_max=step_time_max,
            max_utc_start_time=max_utc_start_time,
            min_utc_start_time=min_utc_start_time,
            variabel_limit_1=variabel_limit_1,
            variabel_limit_2=variabel_limit_2,
            limit1=limit1,
            limit2=limit2,
            comp_operator=comp_operator,
            unit=unit,
            test_status=test_status,
            measure_status=measure_status,
            step_status=step_status,
            warning=warning,
            m=m,
            op=op,
            p=p,
            r=r,
            b=b,
            si=si,
            f=f,
            to=to,
            sf=sf,
            sv=sv,
        )


        virinco_wats_web_dashboard_models_step_details.additional_properties = d
        return virinco_wats_web_dashboard_models_step_details

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
