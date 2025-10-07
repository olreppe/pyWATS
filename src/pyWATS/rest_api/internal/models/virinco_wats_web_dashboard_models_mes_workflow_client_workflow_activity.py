from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_workflow_client_workflow_activity_method import VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivityMethod
from ..models.virinco_wats_web_dashboard_models_mes_workflow_client_workflow_activity_test_result import VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivityTestResult
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivity")



@_attrs_define
class VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivity:
    """ 
        Attributes:
            name (Union[Unset, str]):
            method (Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivityMethod]):
            forced (Union[Unset, bool]):
            test_result (Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivityTestResult]):
            string_result (Union[Unset, str]):
     """

    name: Union[Unset, str] = UNSET
    method: Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivityMethod] = UNSET
    forced: Union[Unset, bool] = UNSET
    test_result: Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivityTestResult] = UNSET
    string_result: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        method: Union[Unset, int] = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.value


        forced = self.forced

        test_result: Union[Unset, int] = UNSET
        if not isinstance(self.test_result, Unset):
            test_result = self.test_result.value


        string_result = self.string_result


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if method is not UNSET:
            field_dict["method"] = method
        if forced is not UNSET:
            field_dict["forced"] = forced
        if test_result is not UNSET:
            field_dict["testResult"] = test_result
        if string_result is not UNSET:
            field_dict["stringResult"] = string_result

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _method = d.pop("method", UNSET)
        method: Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivityMethod]
        if isinstance(_method,  Unset):
            method = UNSET
        else:
            method = VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivityMethod(_method)




        forced = d.pop("forced", UNSET)

        _test_result = d.pop("testResult", UNSET)
        test_result: Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivityTestResult]
        if isinstance(_test_result,  Unset):
            test_result = UNSET
        else:
            test_result = VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivityTestResult(_test_result)




        string_result = d.pop("stringResult", UNSET)

        virinco_wats_web_dashboard_models_mes_workflow_client_workflow_activity = cls(
            name=name,
            method=method,
            forced=forced,
            test_result=test_result,
            string_result=string_result,
        )


        virinco_wats_web_dashboard_models_mes_workflow_client_workflow_activity.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_workflow_client_workflow_activity

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
