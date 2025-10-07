from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_unit_verification import VirincoWATSWebDashboardModelsUnitVerification





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsUnitVerificationGrade")



@_attrs_define
class VirincoWATSWebDashboardModelsUnitVerificationGrade:
    """ 
        Attributes:
            status (Union[Unset, str]):
            grade (Union[Unset, str]):
            all_processes_executed_in_correct_order (Union[Unset, bool]):
            all_processes_passed_first_run (Union[Unset, bool]):
            all_processes_passed_any_run (Union[Unset, bool]):
            all_processes_passed_last_run (Union[Unset, bool]):
            no_repairs (Union[Unset, bool]):
            process_ids (Union[Unset, list[int]]):
            results (Union[Unset, list['VirincoWATSWebDashboardModelsUnitVerification']]):
     """

    status: Union[Unset, str] = UNSET
    grade: Union[Unset, str] = UNSET
    all_processes_executed_in_correct_order: Union[Unset, bool] = UNSET
    all_processes_passed_first_run: Union[Unset, bool] = UNSET
    all_processes_passed_any_run: Union[Unset, bool] = UNSET
    all_processes_passed_last_run: Union[Unset, bool] = UNSET
    no_repairs: Union[Unset, bool] = UNSET
    process_ids: Union[Unset, list[int]] = UNSET
    results: Union[Unset, list['VirincoWATSWebDashboardModelsUnitVerification']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_unit_verification import VirincoWATSWebDashboardModelsUnitVerification
        status = self.status

        grade = self.grade

        all_processes_executed_in_correct_order = self.all_processes_executed_in_correct_order

        all_processes_passed_first_run = self.all_processes_passed_first_run

        all_processes_passed_any_run = self.all_processes_passed_any_run

        all_processes_passed_last_run = self.all_processes_passed_last_run

        no_repairs = self.no_repairs

        process_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.process_ids, Unset):
            process_ids = self.process_ids



        results: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()
                results.append(results_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if status is not UNSET:
            field_dict["status"] = status
        if grade is not UNSET:
            field_dict["grade"] = grade
        if all_processes_executed_in_correct_order is not UNSET:
            field_dict["allProcessesExecutedInCorrectOrder"] = all_processes_executed_in_correct_order
        if all_processes_passed_first_run is not UNSET:
            field_dict["allProcessesPassedFirstRun"] = all_processes_passed_first_run
        if all_processes_passed_any_run is not UNSET:
            field_dict["allProcessesPassedAnyRun"] = all_processes_passed_any_run
        if all_processes_passed_last_run is not UNSET:
            field_dict["allProcessesPassedLastRun"] = all_processes_passed_last_run
        if no_repairs is not UNSET:
            field_dict["noRepairs"] = no_repairs
        if process_ids is not UNSET:
            field_dict["processIds"] = process_ids
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_unit_verification import VirincoWATSWebDashboardModelsUnitVerification
        d = dict(src_dict)
        status = d.pop("status", UNSET)

        grade = d.pop("grade", UNSET)

        all_processes_executed_in_correct_order = d.pop("allProcessesExecutedInCorrectOrder", UNSET)

        all_processes_passed_first_run = d.pop("allProcessesPassedFirstRun", UNSET)

        all_processes_passed_any_run = d.pop("allProcessesPassedAnyRun", UNSET)

        all_processes_passed_last_run = d.pop("allProcessesPassedLastRun", UNSET)

        no_repairs = d.pop("noRepairs", UNSET)

        process_ids = cast(list[int], d.pop("processIds", UNSET))


        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in (_results or []):
            results_item = VirincoWATSWebDashboardModelsUnitVerification.from_dict(results_item_data)



            results.append(results_item)


        virinco_wats_web_dashboard_models_unit_verification_grade = cls(
            status=status,
            grade=grade,
            all_processes_executed_in_correct_order=all_processes_executed_in_correct_order,
            all_processes_passed_first_run=all_processes_passed_first_run,
            all_processes_passed_any_run=all_processes_passed_any_run,
            all_processes_passed_last_run=all_processes_passed_last_run,
            no_repairs=no_repairs,
            process_ids=process_ids,
            results=results,
        )


        virinco_wats_web_dashboard_models_unit_verification_grade.additional_properties = d
        return virinco_wats_web_dashboard_models_unit_verification_grade

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
