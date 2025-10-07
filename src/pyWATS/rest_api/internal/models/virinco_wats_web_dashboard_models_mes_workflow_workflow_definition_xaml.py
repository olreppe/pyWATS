from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinitionXaml")



@_attrs_define
class VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinitionXaml:
    """ 
        Attributes:
            workflow_definition_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            definition (Union[Unset, str]):
     """

    workflow_definition_id: Union[Unset, UUID] = UNSET
    definition: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        workflow_definition_id: Union[Unset, str] = UNSET
        if not isinstance(self.workflow_definition_id, Unset):
            workflow_definition_id = str(self.workflow_definition_id)

        definition = self.definition


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if workflow_definition_id is not UNSET:
            field_dict["WorkflowDefinitionId"] = workflow_definition_id
        if definition is not UNSET:
            field_dict["Definition"] = definition

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _workflow_definition_id = d.pop("WorkflowDefinitionId", UNSET)
        workflow_definition_id: Union[Unset, UUID]
        if isinstance(_workflow_definition_id,  Unset):
            workflow_definition_id = UNSET
        else:
            workflow_definition_id = UUID(_workflow_definition_id)




        definition = d.pop("Definition", UNSET)

        virinco_wats_web_dashboard_models_mes_workflow_workflow_definition_xaml = cls(
            workflow_definition_id=workflow_definition_id,
            definition=definition,
        )


        virinco_wats_web_dashboard_models_mes_workflow_workflow_definition_xaml.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_workflow_workflow_definition_xaml

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
