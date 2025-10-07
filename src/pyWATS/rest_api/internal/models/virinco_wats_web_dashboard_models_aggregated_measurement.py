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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsAggregatedMeasurement")



@_attrs_define
class VirincoWATSWebDashboardModelsAggregatedMeasurement:
    """ 
        Attributes:
            period (Union[Unset, str]):
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
            cpl_wof (Union[Unset, float]):
            cpu_wof (Union[Unset, float]):
            cp_wof (Union[Unset, float]):
            cpk_wof (Union[Unset, float]):
            max_wof (Union[Unset, float]):
            min_wof (Union[Unset, float]):
            avg_wof (Union[Unset, float]):
            sum_wof (Union[Unset, float]):
            sum_2_wof (Union[Unset, float]):
            stdev_wof (Union[Unset, float]):
            sigma_low_3_wof (Union[Unset, float]):
            sigma_high_3_wof (Union[Unset, float]):
            var_wof (Union[Unset, float]):
            count_wof (Union[Unset, int]):
            meas_count_wof (Union[Unset, int]):
            median_wof (Union[Unset, float]):
            q_1_wof (Union[Unset, float]):
            q_3_wof (Union[Unset, float]):
            step_time_min_wof (Union[Unset, float]):
            step_time_avg_wof (Union[Unset, float]):
            step_time_max_wof (Union[Unset, float]):
            max_utc_start_time_wof (Union[Unset, datetime.datetime]):
            min_utc_start_time_wof (Union[Unset, datetime.datetime]):
            variabel_limit_1_wof (Union[Unset, bool]):
            variabel_limit_2_wof (Union[Unset, bool]):
            limit_1_wof (Union[Unset, float]):
            limit_2_wof (Union[Unset, float]):
            comp_operator_wof (Union[Unset, str]):
            unit_wof (Union[Unset, str]):
            warning_wof (Union[Unset, bool]):
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

    period: Union[Unset, str] = UNSET
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
    cpl_wof: Union[Unset, float] = UNSET
    cpu_wof: Union[Unset, float] = UNSET
    cp_wof: Union[Unset, float] = UNSET
    cpk_wof: Union[Unset, float] = UNSET
    max_wof: Union[Unset, float] = UNSET
    min_wof: Union[Unset, float] = UNSET
    avg_wof: Union[Unset, float] = UNSET
    sum_wof: Union[Unset, float] = UNSET
    sum_2_wof: Union[Unset, float] = UNSET
    stdev_wof: Union[Unset, float] = UNSET
    sigma_low_3_wof: Union[Unset, float] = UNSET
    sigma_high_3_wof: Union[Unset, float] = UNSET
    var_wof: Union[Unset, float] = UNSET
    count_wof: Union[Unset, int] = UNSET
    meas_count_wof: Union[Unset, int] = UNSET
    median_wof: Union[Unset, float] = UNSET
    q_1_wof: Union[Unset, float] = UNSET
    q_3_wof: Union[Unset, float] = UNSET
    step_time_min_wof: Union[Unset, float] = UNSET
    step_time_avg_wof: Union[Unset, float] = UNSET
    step_time_max_wof: Union[Unset, float] = UNSET
    max_utc_start_time_wof: Union[Unset, datetime.datetime] = UNSET
    min_utc_start_time_wof: Union[Unset, datetime.datetime] = UNSET
    variabel_limit_1_wof: Union[Unset, bool] = UNSET
    variabel_limit_2_wof: Union[Unset, bool] = UNSET
    limit_1_wof: Union[Unset, float] = UNSET
    limit_2_wof: Union[Unset, float] = UNSET
    comp_operator_wof: Union[Unset, str] = UNSET
    unit_wof: Union[Unset, str] = UNSET
    warning_wof: Union[Unset, bool] = UNSET
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
        period = self.period

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

        cpl_wof = self.cpl_wof

        cpu_wof = self.cpu_wof

        cp_wof = self.cp_wof

        cpk_wof = self.cpk_wof

        max_wof = self.max_wof

        min_wof = self.min_wof

        avg_wof = self.avg_wof

        sum_wof = self.sum_wof

        sum_2_wof = self.sum_2_wof

        stdev_wof = self.stdev_wof

        sigma_low_3_wof = self.sigma_low_3_wof

        sigma_high_3_wof = self.sigma_high_3_wof

        var_wof = self.var_wof

        count_wof = self.count_wof

        meas_count_wof = self.meas_count_wof

        median_wof = self.median_wof

        q_1_wof = self.q_1_wof

        q_3_wof = self.q_3_wof

        step_time_min_wof = self.step_time_min_wof

        step_time_avg_wof = self.step_time_avg_wof

        step_time_max_wof = self.step_time_max_wof

        max_utc_start_time_wof: Union[Unset, str] = UNSET
        if not isinstance(self.max_utc_start_time_wof, Unset):
            max_utc_start_time_wof = self.max_utc_start_time_wof.isoformat()

        min_utc_start_time_wof: Union[Unset, str] = UNSET
        if not isinstance(self.min_utc_start_time_wof, Unset):
            min_utc_start_time_wof = self.min_utc_start_time_wof.isoformat()

        variabel_limit_1_wof = self.variabel_limit_1_wof

        variabel_limit_2_wof = self.variabel_limit_2_wof

        limit_1_wof = self.limit_1_wof

        limit_2_wof = self.limit_2_wof

        comp_operator_wof = self.comp_operator_wof

        unit_wof = self.unit_wof

        warning_wof = self.warning_wof

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
        if period is not UNSET:
            field_dict["period"] = period
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
        if cpl_wof is not UNSET:
            field_dict["cplWof"] = cpl_wof
        if cpu_wof is not UNSET:
            field_dict["cpuWof"] = cpu_wof
        if cp_wof is not UNSET:
            field_dict["cpWof"] = cp_wof
        if cpk_wof is not UNSET:
            field_dict["cpkWof"] = cpk_wof
        if max_wof is not UNSET:
            field_dict["maxWof"] = max_wof
        if min_wof is not UNSET:
            field_dict["minWof"] = min_wof
        if avg_wof is not UNSET:
            field_dict["avgWof"] = avg_wof
        if sum_wof is not UNSET:
            field_dict["sumWof"] = sum_wof
        if sum_2_wof is not UNSET:
            field_dict["sum2Wof"] = sum_2_wof
        if stdev_wof is not UNSET:
            field_dict["stdevWof"] = stdev_wof
        if sigma_low_3_wof is not UNSET:
            field_dict["sigmaLow3Wof"] = sigma_low_3_wof
        if sigma_high_3_wof is not UNSET:
            field_dict["sigmaHigh3Wof"] = sigma_high_3_wof
        if var_wof is not UNSET:
            field_dict["varWof"] = var_wof
        if count_wof is not UNSET:
            field_dict["countWof"] = count_wof
        if meas_count_wof is not UNSET:
            field_dict["measCountWof"] = meas_count_wof
        if median_wof is not UNSET:
            field_dict["medianWof"] = median_wof
        if q_1_wof is not UNSET:
            field_dict["q1Wof"] = q_1_wof
        if q_3_wof is not UNSET:
            field_dict["q3Wof"] = q_3_wof
        if step_time_min_wof is not UNSET:
            field_dict["stepTimeMinWof"] = step_time_min_wof
        if step_time_avg_wof is not UNSET:
            field_dict["stepTimeAvgWof"] = step_time_avg_wof
        if step_time_max_wof is not UNSET:
            field_dict["stepTimeMaxWof"] = step_time_max_wof
        if max_utc_start_time_wof is not UNSET:
            field_dict["maxUtcStartTimeWof"] = max_utc_start_time_wof
        if min_utc_start_time_wof is not UNSET:
            field_dict["minUtcStartTimeWof"] = min_utc_start_time_wof
        if variabel_limit_1_wof is not UNSET:
            field_dict["variabelLimit1Wof"] = variabel_limit_1_wof
        if variabel_limit_2_wof is not UNSET:
            field_dict["variabelLimit2Wof"] = variabel_limit_2_wof
        if limit_1_wof is not UNSET:
            field_dict["limit1Wof"] = limit_1_wof
        if limit_2_wof is not UNSET:
            field_dict["limit2Wof"] = limit_2_wof
        if comp_operator_wof is not UNSET:
            field_dict["compOperatorWof"] = comp_operator_wof
        if unit_wof is not UNSET:
            field_dict["unitWof"] = unit_wof
        if warning_wof is not UNSET:
            field_dict["warningWof"] = warning_wof
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
        d = dict(src_dict)
        period = d.pop("period", UNSET)

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

        cpl_wof = d.pop("cplWof", UNSET)

        cpu_wof = d.pop("cpuWof", UNSET)

        cp_wof = d.pop("cpWof", UNSET)

        cpk_wof = d.pop("cpkWof", UNSET)

        max_wof = d.pop("maxWof", UNSET)

        min_wof = d.pop("minWof", UNSET)

        avg_wof = d.pop("avgWof", UNSET)

        sum_wof = d.pop("sumWof", UNSET)

        sum_2_wof = d.pop("sum2Wof", UNSET)

        stdev_wof = d.pop("stdevWof", UNSET)

        sigma_low_3_wof = d.pop("sigmaLow3Wof", UNSET)

        sigma_high_3_wof = d.pop("sigmaHigh3Wof", UNSET)

        var_wof = d.pop("varWof", UNSET)

        count_wof = d.pop("countWof", UNSET)

        meas_count_wof = d.pop("measCountWof", UNSET)

        median_wof = d.pop("medianWof", UNSET)

        q_1_wof = d.pop("q1Wof", UNSET)

        q_3_wof = d.pop("q3Wof", UNSET)

        step_time_min_wof = d.pop("stepTimeMinWof", UNSET)

        step_time_avg_wof = d.pop("stepTimeAvgWof", UNSET)

        step_time_max_wof = d.pop("stepTimeMaxWof", UNSET)

        _max_utc_start_time_wof = d.pop("maxUtcStartTimeWof", UNSET)
        max_utc_start_time_wof: Union[Unset, datetime.datetime]
        if isinstance(_max_utc_start_time_wof,  Unset):
            max_utc_start_time_wof = UNSET
        else:
            max_utc_start_time_wof = isoparse(_max_utc_start_time_wof)




        _min_utc_start_time_wof = d.pop("minUtcStartTimeWof", UNSET)
        min_utc_start_time_wof: Union[Unset, datetime.datetime]
        if isinstance(_min_utc_start_time_wof,  Unset):
            min_utc_start_time_wof = UNSET
        else:
            min_utc_start_time_wof = isoparse(_min_utc_start_time_wof)




        variabel_limit_1_wof = d.pop("variabelLimit1Wof", UNSET)

        variabel_limit_2_wof = d.pop("variabelLimit2Wof", UNSET)

        limit_1_wof = d.pop("limit1Wof", UNSET)

        limit_2_wof = d.pop("limit2Wof", UNSET)

        comp_operator_wof = d.pop("compOperatorWof", UNSET)

        unit_wof = d.pop("unitWof", UNSET)

        warning_wof = d.pop("warningWof", UNSET)

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

        virinco_wats_web_dashboard_models_aggregated_measurement = cls(
            period=period,
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
            cpl_wof=cpl_wof,
            cpu_wof=cpu_wof,
            cp_wof=cp_wof,
            cpk_wof=cpk_wof,
            max_wof=max_wof,
            min_wof=min_wof,
            avg_wof=avg_wof,
            sum_wof=sum_wof,
            sum_2_wof=sum_2_wof,
            stdev_wof=stdev_wof,
            sigma_low_3_wof=sigma_low_3_wof,
            sigma_high_3_wof=sigma_high_3_wof,
            var_wof=var_wof,
            count_wof=count_wof,
            meas_count_wof=meas_count_wof,
            median_wof=median_wof,
            q_1_wof=q_1_wof,
            q_3_wof=q_3_wof,
            step_time_min_wof=step_time_min_wof,
            step_time_avg_wof=step_time_avg_wof,
            step_time_max_wof=step_time_max_wof,
            max_utc_start_time_wof=max_utc_start_time_wof,
            min_utc_start_time_wof=min_utc_start_time_wof,
            variabel_limit_1_wof=variabel_limit_1_wof,
            variabel_limit_2_wof=variabel_limit_2_wof,
            limit_1_wof=limit_1_wof,
            limit_2_wof=limit_2_wof,
            comp_operator_wof=comp_operator_wof,
            unit_wof=unit_wof,
            warning_wof=warning_wof,
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


        virinco_wats_web_dashboard_models_aggregated_measurement.additional_properties = d
        return virinco_wats_web_dashboard_models_aggregated_measurement

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
