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
  from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_process_relation import VirincoWATSWebDashboardModelsMesMITestSequenceProcessRelation
  from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_site_relation import VirincoWATSWebDashboardModelsMesMITestSequenceSiteRelation





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesMITestSequenceRelation")



@_attrs_define
class VirincoWATSWebDashboardModelsMesMITestSequenceRelation:
    """ 
        Attributes:
            test_sequence_relation_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            test_sequence_definition_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            entity_schema (Union[Unset, str]):
            entity_name (Union[Unset, str]):
            entity_key (Union[Unset, str]):
            entity_value (Union[Unset, str]):
            status (Union[Unset, int]):
            test_sequence_site_relations (Union[Unset, list['VirincoWATSWebDashboardModelsMesMITestSequenceSiteRelation']]):
            test_sequence_process_relations (Union[Unset,
                list['VirincoWATSWebDashboardModelsMesMITestSequenceProcessRelation']]):
            product_name (Union[Unset, str]):
     """

    test_sequence_relation_id: Union[Unset, UUID] = UNSET
    test_sequence_definition_id: Union[Unset, UUID] = UNSET
    entity_schema: Union[Unset, str] = UNSET
    entity_name: Union[Unset, str] = UNSET
    entity_key: Union[Unset, str] = UNSET
    entity_value: Union[Unset, str] = UNSET
    status: Union[Unset, int] = UNSET
    test_sequence_site_relations: Union[Unset, list['VirincoWATSWebDashboardModelsMesMITestSequenceSiteRelation']] = UNSET
    test_sequence_process_relations: Union[Unset, list['VirincoWATSWebDashboardModelsMesMITestSequenceProcessRelation']] = UNSET
    product_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_process_relation import VirincoWATSWebDashboardModelsMesMITestSequenceProcessRelation
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_site_relation import VirincoWATSWebDashboardModelsMesMITestSequenceSiteRelation
        test_sequence_relation_id: Union[Unset, str] = UNSET
        if not isinstance(self.test_sequence_relation_id, Unset):
            test_sequence_relation_id = str(self.test_sequence_relation_id)

        test_sequence_definition_id: Union[Unset, str] = UNSET
        if not isinstance(self.test_sequence_definition_id, Unset):
            test_sequence_definition_id = str(self.test_sequence_definition_id)

        entity_schema = self.entity_schema

        entity_name = self.entity_name

        entity_key = self.entity_key

        entity_value = self.entity_value

        status = self.status

        test_sequence_site_relations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.test_sequence_site_relations, Unset):
            test_sequence_site_relations = []
            for test_sequence_site_relations_item_data in self.test_sequence_site_relations:
                test_sequence_site_relations_item = test_sequence_site_relations_item_data.to_dict()
                test_sequence_site_relations.append(test_sequence_site_relations_item)



        test_sequence_process_relations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.test_sequence_process_relations, Unset):
            test_sequence_process_relations = []
            for test_sequence_process_relations_item_data in self.test_sequence_process_relations:
                test_sequence_process_relations_item = test_sequence_process_relations_item_data.to_dict()
                test_sequence_process_relations.append(test_sequence_process_relations_item)



        product_name = self.product_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if test_sequence_relation_id is not UNSET:
            field_dict["TestSequenceRelationId"] = test_sequence_relation_id
        if test_sequence_definition_id is not UNSET:
            field_dict["TestSequenceDefinitionId"] = test_sequence_definition_id
        if entity_schema is not UNSET:
            field_dict["EntitySchema"] = entity_schema
        if entity_name is not UNSET:
            field_dict["EntityName"] = entity_name
        if entity_key is not UNSET:
            field_dict["EntityKey"] = entity_key
        if entity_value is not UNSET:
            field_dict["EntityValue"] = entity_value
        if status is not UNSET:
            field_dict["Status"] = status
        if test_sequence_site_relations is not UNSET:
            field_dict["TestSequenceSiteRelations"] = test_sequence_site_relations
        if test_sequence_process_relations is not UNSET:
            field_dict["TestSequenceProcessRelations"] = test_sequence_process_relations
        if product_name is not UNSET:
            field_dict["ProductName"] = product_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_process_relation import VirincoWATSWebDashboardModelsMesMITestSequenceProcessRelation
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_site_relation import VirincoWATSWebDashboardModelsMesMITestSequenceSiteRelation
        d = dict(src_dict)
        _test_sequence_relation_id = d.pop("TestSequenceRelationId", UNSET)
        test_sequence_relation_id: Union[Unset, UUID]
        if isinstance(_test_sequence_relation_id,  Unset):
            test_sequence_relation_id = UNSET
        else:
            test_sequence_relation_id = UUID(_test_sequence_relation_id)




        _test_sequence_definition_id = d.pop("TestSequenceDefinitionId", UNSET)
        test_sequence_definition_id: Union[Unset, UUID]
        if isinstance(_test_sequence_definition_id,  Unset):
            test_sequence_definition_id = UNSET
        else:
            test_sequence_definition_id = UUID(_test_sequence_definition_id)




        entity_schema = d.pop("EntitySchema", UNSET)

        entity_name = d.pop("EntityName", UNSET)

        entity_key = d.pop("EntityKey", UNSET)

        entity_value = d.pop("EntityValue", UNSET)

        status = d.pop("Status", UNSET)

        test_sequence_site_relations = []
        _test_sequence_site_relations = d.pop("TestSequenceSiteRelations", UNSET)
        for test_sequence_site_relations_item_data in (_test_sequence_site_relations or []):
            test_sequence_site_relations_item = VirincoWATSWebDashboardModelsMesMITestSequenceSiteRelation.from_dict(test_sequence_site_relations_item_data)



            test_sequence_site_relations.append(test_sequence_site_relations_item)


        test_sequence_process_relations = []
        _test_sequence_process_relations = d.pop("TestSequenceProcessRelations", UNSET)
        for test_sequence_process_relations_item_data in (_test_sequence_process_relations or []):
            test_sequence_process_relations_item = VirincoWATSWebDashboardModelsMesMITestSequenceProcessRelation.from_dict(test_sequence_process_relations_item_data)



            test_sequence_process_relations.append(test_sequence_process_relations_item)


        product_name = d.pop("ProductName", UNSET)

        virinco_wats_web_dashboard_models_mes_mi_test_sequence_relation = cls(
            test_sequence_relation_id=test_sequence_relation_id,
            test_sequence_definition_id=test_sequence_definition_id,
            entity_schema=entity_schema,
            entity_name=entity_name,
            entity_key=entity_key,
            entity_value=entity_value,
            status=status,
            test_sequence_site_relations=test_sequence_site_relations,
            test_sequence_process_relations=test_sequence_process_relations,
            product_name=product_name,
        )


        virinco_wats_web_dashboard_models_mes_mi_test_sequence_relation.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_mi_test_sequence_relation

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
