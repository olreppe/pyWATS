from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_relation_site_relation import VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelationSiteRelation





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation")



@_attrs_define
class VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation:
    """ 
        Attributes:
            workflow_relation_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            workflow_definition_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            entity_schema (Union[Unset, str]):
            entity_name (Union[Unset, str]):
            entity_key_name (Union[Unset, str]):
            entity_value (Union[Unset, str]):
            status (Union[Unset, int]):
            workflow_relation_site_relations (Union[Unset,
                list['VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelationSiteRelation']]):
            product_name (Union[Unset, str]):
     """

    workflow_relation_id: Union[Unset, UUID] = UNSET
    workflow_definition_id: Union[Unset, UUID] = UNSET
    entity_schema: Union[Unset, str] = UNSET
    entity_name: Union[Unset, str] = UNSET
    entity_key_name: Union[Unset, str] = UNSET
    entity_value: Union[Unset, str] = UNSET
    status: Union[Unset, int] = UNSET
    workflow_relation_site_relations: Union[Unset, list['VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelationSiteRelation']] = UNSET
    product_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_relation_site_relation import VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelationSiteRelation
        workflow_relation_id: Union[Unset, str] = UNSET
        if not isinstance(self.workflow_relation_id, Unset):
            workflow_relation_id = str(self.workflow_relation_id)

        workflow_definition_id: Union[Unset, str] = UNSET
        if not isinstance(self.workflow_definition_id, Unset):
            workflow_definition_id = str(self.workflow_definition_id)

        entity_schema = self.entity_schema

        entity_name = self.entity_name

        entity_key_name = self.entity_key_name

        entity_value = self.entity_value

        status = self.status

        workflow_relation_site_relations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.workflow_relation_site_relations, Unset):
            workflow_relation_site_relations = []
            for workflow_relation_site_relations_item_data in self.workflow_relation_site_relations:
                workflow_relation_site_relations_item = workflow_relation_site_relations_item_data.to_dict()
                workflow_relation_site_relations.append(workflow_relation_site_relations_item)



        product_name = self.product_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if workflow_relation_id is not UNSET:
            field_dict["WorkflowRelationId"] = workflow_relation_id
        if workflow_definition_id is not UNSET:
            field_dict["WorkflowDefinitionId"] = workflow_definition_id
        if entity_schema is not UNSET:
            field_dict["EntitySchema"] = entity_schema
        if entity_name is not UNSET:
            field_dict["EntityName"] = entity_name
        if entity_key_name is not UNSET:
            field_dict["EntityKeyName"] = entity_key_name
        if entity_value is not UNSET:
            field_dict["EntityValue"] = entity_value
        if status is not UNSET:
            field_dict["Status"] = status
        if workflow_relation_site_relations is not UNSET:
            field_dict["WorkflowRelationSiteRelations"] = workflow_relation_site_relations
        if product_name is not UNSET:
            field_dict["ProductName"] = product_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_relation_site_relation import VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelationSiteRelation
        d = dict(src_dict)
        _workflow_relation_id = d.pop("WorkflowRelationId", UNSET)
        workflow_relation_id: Union[Unset, UUID]
        if isinstance(_workflow_relation_id,  Unset):
            workflow_relation_id = UNSET
        else:
            workflow_relation_id = UUID(_workflow_relation_id)




        _workflow_definition_id = d.pop("WorkflowDefinitionId", UNSET)
        workflow_definition_id: Union[Unset, UUID]
        if isinstance(_workflow_definition_id,  Unset):
            workflow_definition_id = UNSET
        else:
            workflow_definition_id = UUID(_workflow_definition_id)




        entity_schema = d.pop("EntitySchema", UNSET)

        entity_name = d.pop("EntityName", UNSET)

        entity_key_name = d.pop("EntityKeyName", UNSET)

        entity_value = d.pop("EntityValue", UNSET)

        status = d.pop("Status", UNSET)

        workflow_relation_site_relations = []
        _workflow_relation_site_relations = d.pop("WorkflowRelationSiteRelations", UNSET)
        for workflow_relation_site_relations_item_data in (_workflow_relation_site_relations or []):
            workflow_relation_site_relations_item = VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelationSiteRelation.from_dict(workflow_relation_site_relations_item_data)



            workflow_relation_site_relations.append(workflow_relation_site_relations_item)


        product_name = d.pop("ProductName", UNSET)

        virinco_wats_web_dashboard_models_mes_workflow_workflow_relation = cls(
            workflow_relation_id=workflow_relation_id,
            workflow_definition_id=workflow_definition_id,
            entity_schema=entity_schema,
            entity_name=entity_name,
            entity_key_name=entity_key_name,
            entity_value=entity_value,
            status=status,
            workflow_relation_site_relations=workflow_relation_site_relations,
            product_name=product_name,
        )


        virinco_wats_web_dashboard_models_mes_workflow_workflow_relation.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_workflow_workflow_relation

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
