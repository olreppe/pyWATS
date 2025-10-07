from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_public_unit_verification import VirincoWATSWebDashboardModelsPublicUnitVerification





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsPublicUnitVerificationGrade")



@_attrs_define
class VirincoWATSWebDashboardModelsPublicUnitVerificationGrade:
    """ 
        Attributes:
            status (Union[Unset, str]): Unit status.
            grade (Union[Unset, str]): Unit grade.
            all_processes_executed_in_correct_order (Union[Unset, bool]): Unit was tested in correct process order according
                to process index.
            all_processes_passed_first_run (Union[Unset, bool]): Unit passed in each process first time.
            all_processes_passed_any_run (Union[Unset, bool]): Unit passed at some point in each process, maybe after or
                before fail and repair.
            all_processes_passed_last_run (Union[Unset, bool]): Unit eventually passed in each process, maybe after fail and
                repair. See {Virinco.WATS.Web.Dashboard.Models.PublicUnitVerification.NonPassedCount} and
                {Virinco.WATS.Web.Dashboard.Models.PublicUnitVerification.RepairCount} per process.
            no_repairs (Union[Unset, bool]): Unit never needed repair.
            results (Union[Unset, list['VirincoWATSWebDashboardModelsPublicUnitVerification']]): Unit results per process in
                verification rule.
     """

    status: Union[Unset, str] = UNSET
    grade: Union[Unset, str] = UNSET
    all_processes_executed_in_correct_order: Union[Unset, bool] = UNSET
    all_processes_passed_first_run: Union[Unset, bool] = UNSET
    all_processes_passed_any_run: Union[Unset, bool] = UNSET
    all_processes_passed_last_run: Union[Unset, bool] = UNSET
    no_repairs: Union[Unset, bool] = UNSET
    results: Union[Unset, list['VirincoWATSWebDashboardModelsPublicUnitVerification']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_public_unit_verification import VirincoWATSWebDashboardModelsPublicUnitVerification
        status = self.status

        grade = self.grade

        all_processes_executed_in_correct_order = self.all_processes_executed_in_correct_order

        all_processes_passed_first_run = self.all_processes_passed_first_run

        all_processes_passed_any_run = self.all_processes_passed_any_run

        all_processes_passed_last_run = self.all_processes_passed_last_run

        no_repairs = self.no_repairs

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
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_public_unit_verification import VirincoWATSWebDashboardModelsPublicUnitVerification
        d = dict(src_dict)
        status = d.pop("status", UNSET)

        grade = d.pop("grade", UNSET)

        all_processes_executed_in_correct_order = d.pop("allProcessesExecutedInCorrectOrder", UNSET)

        all_processes_passed_first_run = d.pop("allProcessesPassedFirstRun", UNSET)

        all_processes_passed_any_run = d.pop("allProcessesPassedAnyRun", UNSET)

        all_processes_passed_last_run = d.pop("allProcessesPassedLastRun", UNSET)

        no_repairs = d.pop("noRepairs", UNSET)

        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in (_results or []):
            results_item = VirincoWATSWebDashboardModelsPublicUnitVerification.from_dict(results_item_data)



            results.append(results_item)


        virinco_wats_web_dashboard_models_public_unit_verification_grade = cls(
            status=status,
            grade=grade,
            all_processes_executed_in_correct_order=all_processes_executed_in_correct_order,
            all_processes_passed_first_run=all_processes_passed_first_run,
            all_processes_passed_any_run=all_processes_passed_any_run,
            all_processes_passed_last_run=all_processes_passed_last_run,
            no_repairs=no_repairs,
            results=results,
        )


        virinco_wats_web_dashboard_models_public_unit_verification_grade.additional_properties = d
        return virinco_wats_web_dashboard_models_public_unit_verification_grade

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
