from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_chart_data import VirincoWATSWebDashboardModelsChartData
  from ..models.virinco_wats_web_dashboard_models_step_details import VirincoWATSWebDashboardModelsStepDetails





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsSequenceStep")



@_attrs_define
class VirincoWATSWebDashboardModelsSequenceStep:
    """ 
        Attributes:
            step_name (Union[Unset, str]):
            measure_name (Union[Unset, str]):
            step_type (Union[Unset, str]):
            step_type_enum (Union[Unset, int]):
            step_path (Union[Unset, str]):
            sequence_step_ids (Union[Unset, list[int]]):
            h_level (Union[Unset, int]):
            row_no (Union[Unset, int]):
            step_group (Union[Unset, str]):
            step_total_count (Union[Unset, int]):
            step_pass_count (Union[Unset, int]):
            step_done_count (Union[Unset, int]):
            step_skipped_count (Union[Unset, int]):
            step_terminated_count (Union[Unset, int]):
            step_fail_count (Union[Unset, int]):
            step_error_count (Union[Unset, int]):
            step_other_count (Union[Unset, int]):
            step_non_success_count (Union[Unset, int]):
            step_caused_uut_fail (Union[Unset, int]):
            step_caused_uut_fail_terminated (Union[Unset, int]):
            step_caused_uut_fail_failed (Union[Unset, int]):
            step_caused_uut_fail_error (Union[Unset, int]):
            step_time_min (Union[Unset, float]):
            step_time_avg (Union[Unset, float]):
            step_time_max (Union[Unset, float]):
            comp_operator (Union[Unset, str]):
            meas_count (Union[Unset, int]):
            limit1 (Union[Unset, float]):
            limit2 (Union[Unset, float]):
            meas_count_wof (Union[Unset, int]):
            limit_1_wof (Union[Unset, float]):
            limit_2_wof (Union[Unset, float]):
            min_ (Union[Unset, float]):
            max_ (Union[Unset, float]):
            avg (Union[Unset, float]):
            stdev (Union[Unset, float]):
            var (Union[Unset, float]):
            cpk (Union[Unset, float]):
            cp (Union[Unset, float]):
            cp_upper (Union[Unset, float]):
            cp_lower (Union[Unset, float]):
            min_wof (Union[Unset, float]):
            max_wof (Union[Unset, float]):
            avg_wof (Union[Unset, float]):
            stdev_wof (Union[Unset, float]):
            var_wof (Union[Unset, float]):
            cpk_wof (Union[Unset, float]):
            cp_wof (Union[Unset, float]):
            cp_upper_wof (Union[Unset, float]):
            cp_lower_wof (Union[Unset, float]):
            sigma_low_3 (Union[Unset, float]):
            sigma_high_3 (Union[Unset, float]):
            sigma_low_3_wof (Union[Unset, float]):
            sigma_high_3_wof (Union[Unset, float]):
            warning (Union[Unset, bool]): May contain outliers - investigate data
            warning_wof (Union[Unset, bool]): May contain outliers - investigate data
            details (Union[Unset, VirincoWATSWebDashboardModelsStepDetails]):
            chart (Union[Unset, VirincoWATSWebDashboardModelsChartData]):
     """

    step_name: Union[Unset, str] = UNSET
    measure_name: Union[Unset, str] = UNSET
    step_type: Union[Unset, str] = UNSET
    step_type_enum: Union[Unset, int] = UNSET
    step_path: Union[Unset, str] = UNSET
    sequence_step_ids: Union[Unset, list[int]] = UNSET
    h_level: Union[Unset, int] = UNSET
    row_no: Union[Unset, int] = UNSET
    step_group: Union[Unset, str] = UNSET
    step_total_count: Union[Unset, int] = UNSET
    step_pass_count: Union[Unset, int] = UNSET
    step_done_count: Union[Unset, int] = UNSET
    step_skipped_count: Union[Unset, int] = UNSET
    step_terminated_count: Union[Unset, int] = UNSET
    step_fail_count: Union[Unset, int] = UNSET
    step_error_count: Union[Unset, int] = UNSET
    step_other_count: Union[Unset, int] = UNSET
    step_non_success_count: Union[Unset, int] = UNSET
    step_caused_uut_fail: Union[Unset, int] = UNSET
    step_caused_uut_fail_terminated: Union[Unset, int] = UNSET
    step_caused_uut_fail_failed: Union[Unset, int] = UNSET
    step_caused_uut_fail_error: Union[Unset, int] = UNSET
    step_time_min: Union[Unset, float] = UNSET
    step_time_avg: Union[Unset, float] = UNSET
    step_time_max: Union[Unset, float] = UNSET
    comp_operator: Union[Unset, str] = UNSET
    meas_count: Union[Unset, int] = UNSET
    limit1: Union[Unset, float] = UNSET
    limit2: Union[Unset, float] = UNSET
    meas_count_wof: Union[Unset, int] = UNSET
    limit_1_wof: Union[Unset, float] = UNSET
    limit_2_wof: Union[Unset, float] = UNSET
    min_: Union[Unset, float] = UNSET
    max_: Union[Unset, float] = UNSET
    avg: Union[Unset, float] = UNSET
    stdev: Union[Unset, float] = UNSET
    var: Union[Unset, float] = UNSET
    cpk: Union[Unset, float] = UNSET
    cp: Union[Unset, float] = UNSET
    cp_upper: Union[Unset, float] = UNSET
    cp_lower: Union[Unset, float] = UNSET
    min_wof: Union[Unset, float] = UNSET
    max_wof: Union[Unset, float] = UNSET
    avg_wof: Union[Unset, float] = UNSET
    stdev_wof: Union[Unset, float] = UNSET
    var_wof: Union[Unset, float] = UNSET
    cpk_wof: Union[Unset, float] = UNSET
    cp_wof: Union[Unset, float] = UNSET
    cp_upper_wof: Union[Unset, float] = UNSET
    cp_lower_wof: Union[Unset, float] = UNSET
    sigma_low_3: Union[Unset, float] = UNSET
    sigma_high_3: Union[Unset, float] = UNSET
    sigma_low_3_wof: Union[Unset, float] = UNSET
    sigma_high_3_wof: Union[Unset, float] = UNSET
    warning: Union[Unset, bool] = UNSET
    warning_wof: Union[Unset, bool] = UNSET
    details: Union[Unset, 'VirincoWATSWebDashboardModelsStepDetails'] = UNSET
    chart: Union[Unset, 'VirincoWATSWebDashboardModelsChartData'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_chart_data import VirincoWATSWebDashboardModelsChartData
        from ..models.virinco_wats_web_dashboard_models_step_details import VirincoWATSWebDashboardModelsStepDetails
        step_name = self.step_name

        measure_name = self.measure_name

        step_type = self.step_type

        step_type_enum = self.step_type_enum

        step_path = self.step_path

        sequence_step_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.sequence_step_ids, Unset):
            sequence_step_ids = self.sequence_step_ids



        h_level = self.h_level

        row_no = self.row_no

        step_group = self.step_group

        step_total_count = self.step_total_count

        step_pass_count = self.step_pass_count

        step_done_count = self.step_done_count

        step_skipped_count = self.step_skipped_count

        step_terminated_count = self.step_terminated_count

        step_fail_count = self.step_fail_count

        step_error_count = self.step_error_count

        step_other_count = self.step_other_count

        step_non_success_count = self.step_non_success_count

        step_caused_uut_fail = self.step_caused_uut_fail

        step_caused_uut_fail_terminated = self.step_caused_uut_fail_terminated

        step_caused_uut_fail_failed = self.step_caused_uut_fail_failed

        step_caused_uut_fail_error = self.step_caused_uut_fail_error

        step_time_min = self.step_time_min

        step_time_avg = self.step_time_avg

        step_time_max = self.step_time_max

        comp_operator = self.comp_operator

        meas_count = self.meas_count

        limit1 = self.limit1

        limit2 = self.limit2

        meas_count_wof = self.meas_count_wof

        limit_1_wof = self.limit_1_wof

        limit_2_wof = self.limit_2_wof

        min_ = self.min_

        max_ = self.max_

        avg = self.avg

        stdev = self.stdev

        var = self.var

        cpk = self.cpk

        cp = self.cp

        cp_upper = self.cp_upper

        cp_lower = self.cp_lower

        min_wof = self.min_wof

        max_wof = self.max_wof

        avg_wof = self.avg_wof

        stdev_wof = self.stdev_wof

        var_wof = self.var_wof

        cpk_wof = self.cpk_wof

        cp_wof = self.cp_wof

        cp_upper_wof = self.cp_upper_wof

        cp_lower_wof = self.cp_lower_wof

        sigma_low_3 = self.sigma_low_3

        sigma_high_3 = self.sigma_high_3

        sigma_low_3_wof = self.sigma_low_3_wof

        sigma_high_3_wof = self.sigma_high_3_wof

        warning = self.warning

        warning_wof = self.warning_wof

        details: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        chart: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.chart, Unset):
            chart = self.chart.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if step_name is not UNSET:
            field_dict["stepName"] = step_name
        if measure_name is not UNSET:
            field_dict["measureName"] = measure_name
        if step_type is not UNSET:
            field_dict["stepType"] = step_type
        if step_type_enum is not UNSET:
            field_dict["stepTypeEnum"] = step_type_enum
        if step_path is not UNSET:
            field_dict["stepPath"] = step_path
        if sequence_step_ids is not UNSET:
            field_dict["sequenceStepIds"] = sequence_step_ids
        if h_level is not UNSET:
            field_dict["hLevel"] = h_level
        if row_no is not UNSET:
            field_dict["rowNo"] = row_no
        if step_group is not UNSET:
            field_dict["stepGroup"] = step_group
        if step_total_count is not UNSET:
            field_dict["stepTotalCount"] = step_total_count
        if step_pass_count is not UNSET:
            field_dict["stepPassCount"] = step_pass_count
        if step_done_count is not UNSET:
            field_dict["stepDoneCount"] = step_done_count
        if step_skipped_count is not UNSET:
            field_dict["stepSkippedCount"] = step_skipped_count
        if step_terminated_count is not UNSET:
            field_dict["stepTerminatedCount"] = step_terminated_count
        if step_fail_count is not UNSET:
            field_dict["stepFailCount"] = step_fail_count
        if step_error_count is not UNSET:
            field_dict["stepErrorCount"] = step_error_count
        if step_other_count is not UNSET:
            field_dict["stepOtherCount"] = step_other_count
        if step_non_success_count is not UNSET:
            field_dict["stepNonSuccessCount"] = step_non_success_count
        if step_caused_uut_fail is not UNSET:
            field_dict["stepCausedUutFail"] = step_caused_uut_fail
        if step_caused_uut_fail_terminated is not UNSET:
            field_dict["stepCausedUutFailTerminated"] = step_caused_uut_fail_terminated
        if step_caused_uut_fail_failed is not UNSET:
            field_dict["stepCausedUutFailFailed"] = step_caused_uut_fail_failed
        if step_caused_uut_fail_error is not UNSET:
            field_dict["stepCausedUutFailError"] = step_caused_uut_fail_error
        if step_time_min is not UNSET:
            field_dict["stepTimeMin"] = step_time_min
        if step_time_avg is not UNSET:
            field_dict["stepTimeAvg"] = step_time_avg
        if step_time_max is not UNSET:
            field_dict["stepTimeMax"] = step_time_max
        if comp_operator is not UNSET:
            field_dict["compOperator"] = comp_operator
        if meas_count is not UNSET:
            field_dict["measCount"] = meas_count
        if limit1 is not UNSET:
            field_dict["limit1"] = limit1
        if limit2 is not UNSET:
            field_dict["limit2"] = limit2
        if meas_count_wof is not UNSET:
            field_dict["measCountWof"] = meas_count_wof
        if limit_1_wof is not UNSET:
            field_dict["limit1Wof"] = limit_1_wof
        if limit_2_wof is not UNSET:
            field_dict["limit2Wof"] = limit_2_wof
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_
        if avg is not UNSET:
            field_dict["avg"] = avg
        if stdev is not UNSET:
            field_dict["stdev"] = stdev
        if var is not UNSET:
            field_dict["var"] = var
        if cpk is not UNSET:
            field_dict["cpk"] = cpk
        if cp is not UNSET:
            field_dict["cp"] = cp
        if cp_upper is not UNSET:
            field_dict["cpUpper"] = cp_upper
        if cp_lower is not UNSET:
            field_dict["cpLower"] = cp_lower
        if min_wof is not UNSET:
            field_dict["minWof"] = min_wof
        if max_wof is not UNSET:
            field_dict["maxWof"] = max_wof
        if avg_wof is not UNSET:
            field_dict["avgWof"] = avg_wof
        if stdev_wof is not UNSET:
            field_dict["stdevWof"] = stdev_wof
        if var_wof is not UNSET:
            field_dict["varWof"] = var_wof
        if cpk_wof is not UNSET:
            field_dict["cpkWof"] = cpk_wof
        if cp_wof is not UNSET:
            field_dict["cpWof"] = cp_wof
        if cp_upper_wof is not UNSET:
            field_dict["cpUpperWof"] = cp_upper_wof
        if cp_lower_wof is not UNSET:
            field_dict["cpLowerWof"] = cp_lower_wof
        if sigma_low_3 is not UNSET:
            field_dict["sigmaLow3"] = sigma_low_3
        if sigma_high_3 is not UNSET:
            field_dict["sigmaHigh3"] = sigma_high_3
        if sigma_low_3_wof is not UNSET:
            field_dict["sigmaLow3Wof"] = sigma_low_3_wof
        if sigma_high_3_wof is not UNSET:
            field_dict["sigmaHigh3Wof"] = sigma_high_3_wof
        if warning is not UNSET:
            field_dict["warning"] = warning
        if warning_wof is not UNSET:
            field_dict["warningWof"] = warning_wof
        if details is not UNSET:
            field_dict["details"] = details
        if chart is not UNSET:
            field_dict["chart"] = chart

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_chart_data import VirincoWATSWebDashboardModelsChartData
        from ..models.virinco_wats_web_dashboard_models_step_details import VirincoWATSWebDashboardModelsStepDetails
        d = dict(src_dict)
        step_name = d.pop("stepName", UNSET)

        measure_name = d.pop("measureName", UNSET)

        step_type = d.pop("stepType", UNSET)

        step_type_enum = d.pop("stepTypeEnum", UNSET)

        step_path = d.pop("stepPath", UNSET)

        sequence_step_ids = cast(list[int], d.pop("sequenceStepIds", UNSET))


        h_level = d.pop("hLevel", UNSET)

        row_no = d.pop("rowNo", UNSET)

        step_group = d.pop("stepGroup", UNSET)

        step_total_count = d.pop("stepTotalCount", UNSET)

        step_pass_count = d.pop("stepPassCount", UNSET)

        step_done_count = d.pop("stepDoneCount", UNSET)

        step_skipped_count = d.pop("stepSkippedCount", UNSET)

        step_terminated_count = d.pop("stepTerminatedCount", UNSET)

        step_fail_count = d.pop("stepFailCount", UNSET)

        step_error_count = d.pop("stepErrorCount", UNSET)

        step_other_count = d.pop("stepOtherCount", UNSET)

        step_non_success_count = d.pop("stepNonSuccessCount", UNSET)

        step_caused_uut_fail = d.pop("stepCausedUutFail", UNSET)

        step_caused_uut_fail_terminated = d.pop("stepCausedUutFailTerminated", UNSET)

        step_caused_uut_fail_failed = d.pop("stepCausedUutFailFailed", UNSET)

        step_caused_uut_fail_error = d.pop("stepCausedUutFailError", UNSET)

        step_time_min = d.pop("stepTimeMin", UNSET)

        step_time_avg = d.pop("stepTimeAvg", UNSET)

        step_time_max = d.pop("stepTimeMax", UNSET)

        comp_operator = d.pop("compOperator", UNSET)

        meas_count = d.pop("measCount", UNSET)

        limit1 = d.pop("limit1", UNSET)

        limit2 = d.pop("limit2", UNSET)

        meas_count_wof = d.pop("measCountWof", UNSET)

        limit_1_wof = d.pop("limit1Wof", UNSET)

        limit_2_wof = d.pop("limit2Wof", UNSET)

        min_ = d.pop("min", UNSET)

        max_ = d.pop("max", UNSET)

        avg = d.pop("avg", UNSET)

        stdev = d.pop("stdev", UNSET)

        var = d.pop("var", UNSET)

        cpk = d.pop("cpk", UNSET)

        cp = d.pop("cp", UNSET)

        cp_upper = d.pop("cpUpper", UNSET)

        cp_lower = d.pop("cpLower", UNSET)

        min_wof = d.pop("minWof", UNSET)

        max_wof = d.pop("maxWof", UNSET)

        avg_wof = d.pop("avgWof", UNSET)

        stdev_wof = d.pop("stdevWof", UNSET)

        var_wof = d.pop("varWof", UNSET)

        cpk_wof = d.pop("cpkWof", UNSET)

        cp_wof = d.pop("cpWof", UNSET)

        cp_upper_wof = d.pop("cpUpperWof", UNSET)

        cp_lower_wof = d.pop("cpLowerWof", UNSET)

        sigma_low_3 = d.pop("sigmaLow3", UNSET)

        sigma_high_3 = d.pop("sigmaHigh3", UNSET)

        sigma_low_3_wof = d.pop("sigmaLow3Wof", UNSET)

        sigma_high_3_wof = d.pop("sigmaHigh3Wof", UNSET)

        warning = d.pop("warning", UNSET)

        warning_wof = d.pop("warningWof", UNSET)

        _details = d.pop("details", UNSET)
        details: Union[Unset, VirincoWATSWebDashboardModelsStepDetails]
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = VirincoWATSWebDashboardModelsStepDetails.from_dict(_details)




        _chart = d.pop("chart", UNSET)
        chart: Union[Unset, VirincoWATSWebDashboardModelsChartData]
        if isinstance(_chart,  Unset):
            chart = UNSET
        else:
            chart = VirincoWATSWebDashboardModelsChartData.from_dict(_chart)




        virinco_wats_web_dashboard_models_sequence_step = cls(
            step_name=step_name,
            measure_name=measure_name,
            step_type=step_type,
            step_type_enum=step_type_enum,
            step_path=step_path,
            sequence_step_ids=sequence_step_ids,
            h_level=h_level,
            row_no=row_no,
            step_group=step_group,
            step_total_count=step_total_count,
            step_pass_count=step_pass_count,
            step_done_count=step_done_count,
            step_skipped_count=step_skipped_count,
            step_terminated_count=step_terminated_count,
            step_fail_count=step_fail_count,
            step_error_count=step_error_count,
            step_other_count=step_other_count,
            step_non_success_count=step_non_success_count,
            step_caused_uut_fail=step_caused_uut_fail,
            step_caused_uut_fail_terminated=step_caused_uut_fail_terminated,
            step_caused_uut_fail_failed=step_caused_uut_fail_failed,
            step_caused_uut_fail_error=step_caused_uut_fail_error,
            step_time_min=step_time_min,
            step_time_avg=step_time_avg,
            step_time_max=step_time_max,
            comp_operator=comp_operator,
            meas_count=meas_count,
            limit1=limit1,
            limit2=limit2,
            meas_count_wof=meas_count_wof,
            limit_1_wof=limit_1_wof,
            limit_2_wof=limit_2_wof,
            min_=min_,
            max_=max_,
            avg=avg,
            stdev=stdev,
            var=var,
            cpk=cpk,
            cp=cp,
            cp_upper=cp_upper,
            cp_lower=cp_lower,
            min_wof=min_wof,
            max_wof=max_wof,
            avg_wof=avg_wof,
            stdev_wof=stdev_wof,
            var_wof=var_wof,
            cpk_wof=cpk_wof,
            cp_wof=cp_wof,
            cp_upper_wof=cp_upper_wof,
            cp_lower_wof=cp_lower_wof,
            sigma_low_3=sigma_low_3,
            sigma_high_3=sigma_high_3,
            sigma_low_3_wof=sigma_low_3_wof,
            sigma_high_3_wof=sigma_high_3_wof,
            warning=warning,
            warning_wof=warning_wof,
            details=details,
            chart=chart,
        )


        virinco_wats_web_dashboard_models_sequence_step.additional_properties = d
        return virinco_wats_web_dashboard_models_sequence_step

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
