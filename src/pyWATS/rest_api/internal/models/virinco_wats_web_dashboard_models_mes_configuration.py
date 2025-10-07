from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_configuration_manual_inspection_status import VirincoWATSWebDashboardModelsMesConfigurationManualInspectionStatus
from ..models.virinco_wats_web_dashboard_models_mes_configuration_workflow_status import VirincoWATSWebDashboardModelsMesConfigurationWorkflowStatus
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesConfiguration")



@_attrs_define
class VirincoWATSWebDashboardModelsMesConfiguration:
    """ 
        Attributes:
            manual_inspection_enabled (Union[Unset, bool]):
            manual_inspection_status (Union[Unset, VirincoWATSWebDashboardModelsMesConfigurationManualInspectionStatus]):
            manual_inspection_log_operator (Union[Unset, bool]):
            manual_inspection_log_description (Union[Unset, bool]):
            product_enabled (Union[Unset, bool]):
            production_enabled (Union[Unset, bool]):
            production_add_units (Union[Unset, bool]):
            production_sn_unique (Union[Unset, bool]):
            workflow_enabled (Union[Unset, bool]):
            workflow_status (Union[Unset, VirincoWATSWebDashboardModelsMesConfigurationWorkflowStatus]):
            workflow_auto_initialize (Union[Unset, bool]):
     """

    manual_inspection_enabled: Union[Unset, bool] = UNSET
    manual_inspection_status: Union[Unset, VirincoWATSWebDashboardModelsMesConfigurationManualInspectionStatus] = UNSET
    manual_inspection_log_operator: Union[Unset, bool] = UNSET
    manual_inspection_log_description: Union[Unset, bool] = UNSET
    product_enabled: Union[Unset, bool] = UNSET
    production_enabled: Union[Unset, bool] = UNSET
    production_add_units: Union[Unset, bool] = UNSET
    production_sn_unique: Union[Unset, bool] = UNSET
    workflow_enabled: Union[Unset, bool] = UNSET
    workflow_status: Union[Unset, VirincoWATSWebDashboardModelsMesConfigurationWorkflowStatus] = UNSET
    workflow_auto_initialize: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        manual_inspection_enabled = self.manual_inspection_enabled

        manual_inspection_status: Union[Unset, int] = UNSET
        if not isinstance(self.manual_inspection_status, Unset):
            manual_inspection_status = self.manual_inspection_status.value


        manual_inspection_log_operator = self.manual_inspection_log_operator

        manual_inspection_log_description = self.manual_inspection_log_description

        product_enabled = self.product_enabled

        production_enabled = self.production_enabled

        production_add_units = self.production_add_units

        production_sn_unique = self.production_sn_unique

        workflow_enabled = self.workflow_enabled

        workflow_status: Union[Unset, int] = UNSET
        if not isinstance(self.workflow_status, Unset):
            workflow_status = self.workflow_status.value


        workflow_auto_initialize = self.workflow_auto_initialize


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if manual_inspection_enabled is not UNSET:
            field_dict["ManualInspectionEnabled"] = manual_inspection_enabled
        if manual_inspection_status is not UNSET:
            field_dict["ManualInspectionStatus"] = manual_inspection_status
        if manual_inspection_log_operator is not UNSET:
            field_dict["ManualInspectionLogOperator"] = manual_inspection_log_operator
        if manual_inspection_log_description is not UNSET:
            field_dict["ManualInspectionLogDescription"] = manual_inspection_log_description
        if product_enabled is not UNSET:
            field_dict["ProductEnabled"] = product_enabled
        if production_enabled is not UNSET:
            field_dict["ProductionEnabled"] = production_enabled
        if production_add_units is not UNSET:
            field_dict["ProductionAddUnits"] = production_add_units
        if production_sn_unique is not UNSET:
            field_dict["ProductionSNUnique"] = production_sn_unique
        if workflow_enabled is not UNSET:
            field_dict["WorkflowEnabled"] = workflow_enabled
        if workflow_status is not UNSET:
            field_dict["WorkflowStatus"] = workflow_status
        if workflow_auto_initialize is not UNSET:
            field_dict["WorkflowAutoInitialize"] = workflow_auto_initialize

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        manual_inspection_enabled = d.pop("ManualInspectionEnabled", UNSET)

        _manual_inspection_status = d.pop("ManualInspectionStatus", UNSET)
        manual_inspection_status: Union[Unset, VirincoWATSWebDashboardModelsMesConfigurationManualInspectionStatus]
        if isinstance(_manual_inspection_status,  Unset):
            manual_inspection_status = UNSET
        else:
            manual_inspection_status = VirincoWATSWebDashboardModelsMesConfigurationManualInspectionStatus(_manual_inspection_status)




        manual_inspection_log_operator = d.pop("ManualInspectionLogOperator", UNSET)

        manual_inspection_log_description = d.pop("ManualInspectionLogDescription", UNSET)

        product_enabled = d.pop("ProductEnabled", UNSET)

        production_enabled = d.pop("ProductionEnabled", UNSET)

        production_add_units = d.pop("ProductionAddUnits", UNSET)

        production_sn_unique = d.pop("ProductionSNUnique", UNSET)

        workflow_enabled = d.pop("WorkflowEnabled", UNSET)

        _workflow_status = d.pop("WorkflowStatus", UNSET)
        workflow_status: Union[Unset, VirincoWATSWebDashboardModelsMesConfigurationWorkflowStatus]
        if isinstance(_workflow_status,  Unset):
            workflow_status = UNSET
        else:
            workflow_status = VirincoWATSWebDashboardModelsMesConfigurationWorkflowStatus(_workflow_status)




        workflow_auto_initialize = d.pop("WorkflowAutoInitialize", UNSET)

        virinco_wats_web_dashboard_models_mes_configuration = cls(
            manual_inspection_enabled=manual_inspection_enabled,
            manual_inspection_status=manual_inspection_status,
            manual_inspection_log_operator=manual_inspection_log_operator,
            manual_inspection_log_description=manual_inspection_log_description,
            product_enabled=product_enabled,
            production_enabled=production_enabled,
            production_add_units=production_add_units,
            production_sn_unique=production_sn_unique,
            workflow_enabled=workflow_enabled,
            workflow_status=workflow_status,
            workflow_auto_initialize=workflow_auto_initialize,
        )


        virinco_wats_web_dashboard_models_mes_configuration.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_configuration

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
