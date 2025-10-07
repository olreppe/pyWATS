from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_entity_container import MicrosoftODataEdmIEdmEntityContainer
  from ..models.microsoft_o_data_edm_vocabularies_i_edm_vocabulary_annotation import MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotation
  from ..models.microsoft_o_data_edm_i_edm_schema_element import MicrosoftODataEdmIEdmSchemaElement
  from ..models.microsoft_o_data_edm_vocabularies_i_edm_direct_value_annotations_manager import MicrosoftODataEdmVocabulariesIEdmDirectValueAnnotationsManager





T = TypeVar("T", bound="MicrosoftODataEdmIEdmModel")



@_attrs_define
class MicrosoftODataEdmIEdmModel:
    """ 
        Attributes:
            schema_elements (Union[Unset, list['MicrosoftODataEdmIEdmSchemaElement']]):
            vocabulary_annotations (Union[Unset, list['MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotation']]):
            referenced_models (Union[Unset, list['MicrosoftODataEdmIEdmModel']]):
            declared_namespaces (Union[Unset, list[str]]):
            direct_value_annotations_manager (Union[Unset, MicrosoftODataEdmVocabulariesIEdmDirectValueAnnotationsManager]):
            entity_container (Union[Unset, MicrosoftODataEdmIEdmEntityContainer]):
     """

    schema_elements: Union[Unset, list['MicrosoftODataEdmIEdmSchemaElement']] = UNSET
    vocabulary_annotations: Union[Unset, list['MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotation']] = UNSET
    referenced_models: Union[Unset, list['MicrosoftODataEdmIEdmModel']] = UNSET
    declared_namespaces: Union[Unset, list[str]] = UNSET
    direct_value_annotations_manager: Union[Unset, 'MicrosoftODataEdmVocabulariesIEdmDirectValueAnnotationsManager'] = UNSET
    entity_container: Union[Unset, 'MicrosoftODataEdmIEdmEntityContainer'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_entity_container import MicrosoftODataEdmIEdmEntityContainer
        from ..models.microsoft_o_data_edm_vocabularies_i_edm_vocabulary_annotation import MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotation
        from ..models.microsoft_o_data_edm_i_edm_schema_element import MicrosoftODataEdmIEdmSchemaElement
        from ..models.microsoft_o_data_edm_vocabularies_i_edm_direct_value_annotations_manager import MicrosoftODataEdmVocabulariesIEdmDirectValueAnnotationsManager
        schema_elements: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.schema_elements, Unset):
            schema_elements = []
            for schema_elements_item_data in self.schema_elements:
                schema_elements_item = schema_elements_item_data.to_dict()
                schema_elements.append(schema_elements_item)



        vocabulary_annotations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.vocabulary_annotations, Unset):
            vocabulary_annotations = []
            for vocabulary_annotations_item_data in self.vocabulary_annotations:
                vocabulary_annotations_item = vocabulary_annotations_item_data.to_dict()
                vocabulary_annotations.append(vocabulary_annotations_item)



        referenced_models: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.referenced_models, Unset):
            referenced_models = []
            for referenced_models_item_data in self.referenced_models:
                referenced_models_item = referenced_models_item_data.to_dict()
                referenced_models.append(referenced_models_item)



        declared_namespaces: Union[Unset, list[str]] = UNSET
        if not isinstance(self.declared_namespaces, Unset):
            declared_namespaces = self.declared_namespaces



        direct_value_annotations_manager: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.direct_value_annotations_manager, Unset):
            direct_value_annotations_manager = self.direct_value_annotations_manager.to_dict()

        entity_container: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.entity_container, Unset):
            entity_container = self.entity_container.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if schema_elements is not UNSET:
            field_dict["SchemaElements"] = schema_elements
        if vocabulary_annotations is not UNSET:
            field_dict["VocabularyAnnotations"] = vocabulary_annotations
        if referenced_models is not UNSET:
            field_dict["ReferencedModels"] = referenced_models
        if declared_namespaces is not UNSET:
            field_dict["DeclaredNamespaces"] = declared_namespaces
        if direct_value_annotations_manager is not UNSET:
            field_dict["DirectValueAnnotationsManager"] = direct_value_annotations_manager
        if entity_container is not UNSET:
            field_dict["EntityContainer"] = entity_container

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_entity_container import MicrosoftODataEdmIEdmEntityContainer
        from ..models.microsoft_o_data_edm_vocabularies_i_edm_vocabulary_annotation import MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotation
        from ..models.microsoft_o_data_edm_i_edm_schema_element import MicrosoftODataEdmIEdmSchemaElement
        from ..models.microsoft_o_data_edm_vocabularies_i_edm_direct_value_annotations_manager import MicrosoftODataEdmVocabulariesIEdmDirectValueAnnotationsManager
        d = dict(src_dict)
        schema_elements = []
        _schema_elements = d.pop("SchemaElements", UNSET)
        for schema_elements_item_data in (_schema_elements or []):
            schema_elements_item = MicrosoftODataEdmIEdmSchemaElement.from_dict(schema_elements_item_data)



            schema_elements.append(schema_elements_item)


        vocabulary_annotations = []
        _vocabulary_annotations = d.pop("VocabularyAnnotations", UNSET)
        for vocabulary_annotations_item_data in (_vocabulary_annotations or []):
            vocabulary_annotations_item = MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotation.from_dict(vocabulary_annotations_item_data)



            vocabulary_annotations.append(vocabulary_annotations_item)


        referenced_models = []
        _referenced_models = d.pop("ReferencedModels", UNSET)
        for referenced_models_item_data in (_referenced_models or []):
            referenced_models_item = MicrosoftODataEdmIEdmModel.from_dict(referenced_models_item_data)



            referenced_models.append(referenced_models_item)


        declared_namespaces = cast(list[str], d.pop("DeclaredNamespaces", UNSET))


        _direct_value_annotations_manager = d.pop("DirectValueAnnotationsManager", UNSET)
        direct_value_annotations_manager: Union[Unset, MicrosoftODataEdmVocabulariesIEdmDirectValueAnnotationsManager]
        if isinstance(_direct_value_annotations_manager,  Unset):
            direct_value_annotations_manager = UNSET
        else:
            direct_value_annotations_manager = MicrosoftODataEdmVocabulariesIEdmDirectValueAnnotationsManager.from_dict(_direct_value_annotations_manager)




        _entity_container = d.pop("EntityContainer", UNSET)
        entity_container: Union[Unset, MicrosoftODataEdmIEdmEntityContainer]
        if isinstance(_entity_container,  Unset):
            entity_container = UNSET
        else:
            entity_container = MicrosoftODataEdmIEdmEntityContainer.from_dict(_entity_container)




        microsoft_o_data_edm_i_edm_model = cls(
            schema_elements=schema_elements,
            vocabulary_annotations=vocabulary_annotations,
            referenced_models=referenced_models,
            declared_namespaces=declared_namespaces,
            direct_value_annotations_manager=direct_value_annotations_manager,
            entity_container=entity_container,
        )


        microsoft_o_data_edm_i_edm_model.additional_properties = d
        return microsoft_o_data_edm_i_edm_model

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
