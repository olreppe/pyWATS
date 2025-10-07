from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_workflow_client_workflow_request_settings_status import VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettingsStatus
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettings")



@_attrs_define
class VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettings:
    """ 
        Attributes:
            status (Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettingsStatus]):
            auto_initialize (Union[Unset, bool]):
            culture_code (Union[Unset, str]):
            locked_processes (Union[Unset, list[str]]):
     """

    status: Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettingsStatus] = UNSET
    auto_initialize: Union[Unset, bool] = UNSET
    culture_code: Union[Unset, str] = UNSET
    locked_processes: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value


        auto_initialize = self.auto_initialize

        culture_code = self.culture_code

        locked_processes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.locked_processes, Unset):
            locked_processes = self.locked_processes




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if status is not UNSET:
            field_dict["status"] = status
        if auto_initialize is not UNSET:
            field_dict["autoInitialize"] = auto_initialize
        if culture_code is not UNSET:
            field_dict["cultureCode"] = culture_code
        if locked_processes is not UNSET:
            field_dict["lockedProcesses"] = locked_processes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _status = d.pop("status", UNSET)
        status: Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettingsStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettingsStatus(_status)




        auto_initialize = d.pop("autoInitialize", UNSET)

        culture_code = d.pop("cultureCode", UNSET)

        locked_processes = cast(list[str], d.pop("lockedProcesses", UNSET))


        virinco_wats_web_dashboard_models_mes_workflow_client_workflow_request_settings = cls(
            status=status,
            auto_initialize=auto_initialize,
            culture_code=culture_code,
            locked_processes=locked_processes,
        )


        virinco_wats_web_dashboard_models_mes_workflow_client_workflow_request_settings.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_workflow_client_workflow_request_settings

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
