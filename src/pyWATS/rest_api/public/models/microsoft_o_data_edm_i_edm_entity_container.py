from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.microsoft_o_data_edm_i_edm_entity_container_schema_element_kind import MicrosoftODataEdmIEdmEntityContainerSchemaElementKind
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_entity_container_element import MicrosoftODataEdmIEdmEntityContainerElement





T = TypeVar("T", bound="MicrosoftODataEdmIEdmEntityContainer")



@_attrs_define
class MicrosoftODataEdmIEdmEntityContainer:
    """ 
        Attributes:
            elements (Union[Unset, list['MicrosoftODataEdmIEdmEntityContainerElement']]):
            schema_element_kind (Union[Unset, MicrosoftODataEdmIEdmEntityContainerSchemaElementKind]):
            namespace (Union[Unset, str]):
            name (Union[Unset, str]):
     """

    elements: Union[Unset, list['MicrosoftODataEdmIEdmEntityContainerElement']] = UNSET
    schema_element_kind: Union[Unset, MicrosoftODataEdmIEdmEntityContainerSchemaElementKind] = UNSET
    namespace: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_entity_container_element import MicrosoftODataEdmIEdmEntityContainerElement
        elements: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.elements, Unset):
            elements = []
            for elements_item_data in self.elements:
                elements_item = elements_item_data.to_dict()
                elements.append(elements_item)



        schema_element_kind: Union[Unset, int] = UNSET
        if not isinstance(self.schema_element_kind, Unset):
            schema_element_kind = self.schema_element_kind.value


        namespace = self.namespace

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if elements is not UNSET:
            field_dict["Elements"] = elements
        if schema_element_kind is not UNSET:
            field_dict["SchemaElementKind"] = schema_element_kind
        if namespace is not UNSET:
            field_dict["Namespace"] = namespace
        if name is not UNSET:
            field_dict["Name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_entity_container_element import MicrosoftODataEdmIEdmEntityContainerElement
        d = dict(src_dict)
        elements = []
        _elements = d.pop("Elements", UNSET)
        for elements_item_data in (_elements or []):
            elements_item = MicrosoftODataEdmIEdmEntityContainerElement.from_dict(elements_item_data)



            elements.append(elements_item)


        _schema_element_kind = d.pop("SchemaElementKind", UNSET)
        schema_element_kind: Union[Unset, MicrosoftODataEdmIEdmEntityContainerSchemaElementKind]
        if isinstance(_schema_element_kind,  Unset):
            schema_element_kind = UNSET
        else:
            schema_element_kind = MicrosoftODataEdmIEdmEntityContainerSchemaElementKind(_schema_element_kind)




        namespace = d.pop("Namespace", UNSET)

        name = d.pop("Name", UNSET)

        microsoft_o_data_edm_i_edm_entity_container = cls(
            elements=elements,
            schema_element_kind=schema_element_kind,
            namespace=namespace,
            name=name,
        )


        microsoft_o_data_edm_i_edm_entity_container.additional_properties = d
        return microsoft_o_data_edm_i_edm_entity_container

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
