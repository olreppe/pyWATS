from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_tsa_filter_measure_status import VirincoWATSWebDashboardModelsTSAFilterMeasureStatus
from ..models.virinco_wats_web_dashboard_models_tsa_filter_step_details_grouping import VirincoWATSWebDashboardModelsTSAFilterStepDetailsGrouping
from ..models.virinco_wats_web_dashboard_models_tsa_filter_step_details_options import VirincoWATSWebDashboardModelsTSAFilterStepDetailsOptions
from ..models.virinco_wats_web_dashboard_models_tsa_filter_step_grouping import VirincoWATSWebDashboardModelsTSAFilterStepGrouping
from ..models.virinco_wats_web_dashboard_models_tsa_filter_step_status import VirincoWATSWebDashboardModelsTSAFilterStepStatus
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_sequence_step import VirincoWATSWebDashboardModelsSequenceStep
  from ..models.virinco_wats_web_dashboard_models_sequence_selection import VirincoWATSWebDashboardModelsSequenceSelection
  from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTSAFilter")



@_attrs_define
class VirincoWATSWebDashboardModelsTSAFilter:
    """ 
        Attributes:
            wats_filter (Union[Unset, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter]): Wats filter exposed in
                rest API
            selection_filter (Union[Unset, list['VirincoWATSWebDashboardModelsSequenceSelection']]):
            sequence_steps (Union[Unset, list['VirincoWATSWebDashboardModelsSequenceStep']]):
            step_grouping (Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepGrouping]):
            period_from (Union[Unset, str]):
            period_to (Union[Unset, str]):
            force_refresh (Union[Unset, bool]):
            loop_index (Union[Unset, int]):
            step_details_options (Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepDetailsOptions]):
            step_details_grouping (Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepDetailsGrouping]):
            filter_failed_measures (Union[Unset, bool]):
            measure_status (Union[Unset, VirincoWATSWebDashboardModelsTSAFilterMeasureStatus]):
            step_status (Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepStatus]):
            include_earlier_runs (Union[Unset, bool]):
            filter_measure_high (Union[Unset, float]):
            filter_measure_low (Union[Unset, float]):
            high_test_limit (Union[Unset, float]):
            low_test_limit (Union[Unset, float]):
            number_of_measurements (Union[Unset, int]):
            group_by_misc_descriptions (Union[Unset, list[str]]):
     """

    wats_filter: Union[Unset, 'VirincoWATSWebDashboardControllersApiAppPublicWatsFilter'] = UNSET
    selection_filter: Union[Unset, list['VirincoWATSWebDashboardModelsSequenceSelection']] = UNSET
    sequence_steps: Union[Unset, list['VirincoWATSWebDashboardModelsSequenceStep']] = UNSET
    step_grouping: Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepGrouping] = UNSET
    period_from: Union[Unset, str] = UNSET
    period_to: Union[Unset, str] = UNSET
    force_refresh: Union[Unset, bool] = UNSET
    loop_index: Union[Unset, int] = UNSET
    step_details_options: Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepDetailsOptions] = UNSET
    step_details_grouping: Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepDetailsGrouping] = UNSET
    filter_failed_measures: Union[Unset, bool] = UNSET
    measure_status: Union[Unset, VirincoWATSWebDashboardModelsTSAFilterMeasureStatus] = UNSET
    step_status: Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepStatus] = UNSET
    include_earlier_runs: Union[Unset, bool] = UNSET
    filter_measure_high: Union[Unset, float] = UNSET
    filter_measure_low: Union[Unset, float] = UNSET
    high_test_limit: Union[Unset, float] = UNSET
    low_test_limit: Union[Unset, float] = UNSET
    number_of_measurements: Union[Unset, int] = UNSET
    group_by_misc_descriptions: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_sequence_step import VirincoWATSWebDashboardModelsSequenceStep
        from ..models.virinco_wats_web_dashboard_models_sequence_selection import VirincoWATSWebDashboardModelsSequenceSelection
        from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter
        wats_filter: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.wats_filter, Unset):
            wats_filter = self.wats_filter.to_dict()

        selection_filter: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.selection_filter, Unset):
            selection_filter = []
            for selection_filter_item_data in self.selection_filter:
                selection_filter_item = selection_filter_item_data.to_dict()
                selection_filter.append(selection_filter_item)



        sequence_steps: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sequence_steps, Unset):
            sequence_steps = []
            for sequence_steps_item_data in self.sequence_steps:
                sequence_steps_item = sequence_steps_item_data.to_dict()
                sequence_steps.append(sequence_steps_item)



        step_grouping: Union[Unset, int] = UNSET
        if not isinstance(self.step_grouping, Unset):
            step_grouping = self.step_grouping.value


        period_from = self.period_from

        period_to = self.period_to

        force_refresh = self.force_refresh

        loop_index = self.loop_index

        step_details_options: Union[Unset, int] = UNSET
        if not isinstance(self.step_details_options, Unset):
            step_details_options = self.step_details_options.value


        step_details_grouping: Union[Unset, int] = UNSET
        if not isinstance(self.step_details_grouping, Unset):
            step_details_grouping = self.step_details_grouping.value


        filter_failed_measures = self.filter_failed_measures

        measure_status: Union[Unset, int] = UNSET
        if not isinstance(self.measure_status, Unset):
            measure_status = self.measure_status.value


        step_status: Union[Unset, int] = UNSET
        if not isinstance(self.step_status, Unset):
            step_status = self.step_status.value


        include_earlier_runs = self.include_earlier_runs

        filter_measure_high = self.filter_measure_high

        filter_measure_low = self.filter_measure_low

        high_test_limit = self.high_test_limit

        low_test_limit = self.low_test_limit

        number_of_measurements = self.number_of_measurements

        group_by_misc_descriptions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.group_by_misc_descriptions, Unset):
            group_by_misc_descriptions = self.group_by_misc_descriptions




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if wats_filter is not UNSET:
            field_dict["watsFilter"] = wats_filter
        if selection_filter is not UNSET:
            field_dict["selectionFilter"] = selection_filter
        if sequence_steps is not UNSET:
            field_dict["sequenceSteps"] = sequence_steps
        if step_grouping is not UNSET:
            field_dict["stepGrouping"] = step_grouping
        if period_from is not UNSET:
            field_dict["periodFrom"] = period_from
        if period_to is not UNSET:
            field_dict["periodTo"] = period_to
        if force_refresh is not UNSET:
            field_dict["forceRefresh"] = force_refresh
        if loop_index is not UNSET:
            field_dict["loopIndex"] = loop_index
        if step_details_options is not UNSET:
            field_dict["stepDetailsOptions"] = step_details_options
        if step_details_grouping is not UNSET:
            field_dict["stepDetailsGrouping"] = step_details_grouping
        if filter_failed_measures is not UNSET:
            field_dict["filterFailedMeasures"] = filter_failed_measures
        if measure_status is not UNSET:
            field_dict["measureStatus"] = measure_status
        if step_status is not UNSET:
            field_dict["stepStatus"] = step_status
        if include_earlier_runs is not UNSET:
            field_dict["includeEarlierRuns"] = include_earlier_runs
        if filter_measure_high is not UNSET:
            field_dict["filterMeasureHigh"] = filter_measure_high
        if filter_measure_low is not UNSET:
            field_dict["filterMeasureLow"] = filter_measure_low
        if high_test_limit is not UNSET:
            field_dict["highTestLimit"] = high_test_limit
        if low_test_limit is not UNSET:
            field_dict["lowTestLimit"] = low_test_limit
        if number_of_measurements is not UNSET:
            field_dict["numberOfMeasurements"] = number_of_measurements
        if group_by_misc_descriptions is not UNSET:
            field_dict["groupByMiscDescriptions"] = group_by_misc_descriptions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_sequence_step import VirincoWATSWebDashboardModelsSequenceStep
        from ..models.virinco_wats_web_dashboard_models_sequence_selection import VirincoWATSWebDashboardModelsSequenceSelection
        from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter
        d = dict(src_dict)
        _wats_filter = d.pop("watsFilter", UNSET)
        wats_filter: Union[Unset, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter]
        if isinstance(_wats_filter,  Unset):
            wats_filter = UNSET
        else:
            wats_filter = VirincoWATSWebDashboardControllersApiAppPublicWatsFilter.from_dict(_wats_filter)




        selection_filter = []
        _selection_filter = d.pop("selectionFilter", UNSET)
        for selection_filter_item_data in (_selection_filter or []):
            selection_filter_item = VirincoWATSWebDashboardModelsSequenceSelection.from_dict(selection_filter_item_data)



            selection_filter.append(selection_filter_item)


        sequence_steps = []
        _sequence_steps = d.pop("sequenceSteps", UNSET)
        for sequence_steps_item_data in (_sequence_steps or []):
            sequence_steps_item = VirincoWATSWebDashboardModelsSequenceStep.from_dict(sequence_steps_item_data)



            sequence_steps.append(sequence_steps_item)


        _step_grouping = d.pop("stepGrouping", UNSET)
        step_grouping: Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepGrouping]
        if isinstance(_step_grouping,  Unset):
            step_grouping = UNSET
        else:
            step_grouping = VirincoWATSWebDashboardModelsTSAFilterStepGrouping(_step_grouping)




        period_from = d.pop("periodFrom", UNSET)

        period_to = d.pop("periodTo", UNSET)

        force_refresh = d.pop("forceRefresh", UNSET)

        loop_index = d.pop("loopIndex", UNSET)

        _step_details_options = d.pop("stepDetailsOptions", UNSET)
        step_details_options: Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepDetailsOptions]
        if isinstance(_step_details_options,  Unset):
            step_details_options = UNSET
        else:
            step_details_options = VirincoWATSWebDashboardModelsTSAFilterStepDetailsOptions(_step_details_options)




        _step_details_grouping = d.pop("stepDetailsGrouping", UNSET)
        step_details_grouping: Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepDetailsGrouping]
        if isinstance(_step_details_grouping,  Unset):
            step_details_grouping = UNSET
        else:
            step_details_grouping = VirincoWATSWebDashboardModelsTSAFilterStepDetailsGrouping(_step_details_grouping)




        filter_failed_measures = d.pop("filterFailedMeasures", UNSET)

        _measure_status = d.pop("measureStatus", UNSET)
        measure_status: Union[Unset, VirincoWATSWebDashboardModelsTSAFilterMeasureStatus]
        if isinstance(_measure_status,  Unset):
            measure_status = UNSET
        else:
            measure_status = VirincoWATSWebDashboardModelsTSAFilterMeasureStatus(_measure_status)




        _step_status = d.pop("stepStatus", UNSET)
        step_status: Union[Unset, VirincoWATSWebDashboardModelsTSAFilterStepStatus]
        if isinstance(_step_status,  Unset):
            step_status = UNSET
        else:
            step_status = VirincoWATSWebDashboardModelsTSAFilterStepStatus(_step_status)




        include_earlier_runs = d.pop("includeEarlierRuns", UNSET)

        filter_measure_high = d.pop("filterMeasureHigh", UNSET)

        filter_measure_low = d.pop("filterMeasureLow", UNSET)

        high_test_limit = d.pop("highTestLimit", UNSET)

        low_test_limit = d.pop("lowTestLimit", UNSET)

        number_of_measurements = d.pop("numberOfMeasurements", UNSET)

        group_by_misc_descriptions = cast(list[str], d.pop("groupByMiscDescriptions", UNSET))


        virinco_wats_web_dashboard_models_tsa_filter = cls(
            wats_filter=wats_filter,
            selection_filter=selection_filter,
            sequence_steps=sequence_steps,
            step_grouping=step_grouping,
            period_from=period_from,
            period_to=period_to,
            force_refresh=force_refresh,
            loop_index=loop_index,
            step_details_options=step_details_options,
            step_details_grouping=step_details_grouping,
            filter_failed_measures=filter_failed_measures,
            measure_status=measure_status,
            step_status=step_status,
            include_earlier_runs=include_earlier_runs,
            filter_measure_high=filter_measure_high,
            filter_measure_low=filter_measure_low,
            high_test_limit=high_test_limit,
            low_test_limit=low_test_limit,
            number_of_measurements=number_of_measurements,
            group_by_misc_descriptions=group_by_misc_descriptions,
        )


        virinco_wats_web_dashboard_models_tsa_filter.additional_properties = d
        return virinco_wats_web_dashboard_models_tsa_filter

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
