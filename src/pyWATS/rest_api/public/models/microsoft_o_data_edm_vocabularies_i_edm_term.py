from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.microsoft_o_data_edm_vocabularies_i_edm_term_schema_element_kind import MicrosoftODataEdmVocabulariesIEdmTermSchemaElementKind
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference





T = TypeVar("T", bound="MicrosoftODataEdmVocabulariesIEdmTerm")



@_attrs_define
class MicrosoftODataEdmVocabulariesIEdmTerm:
    """ 
        Attributes:
            type_ (Union[Unset, MicrosoftODataEdmIEdmTypeReference]):
            applies_to (Union[Unset, str]):
            default_value (Union[Unset, str]):
            schema_element_kind (Union[Unset, MicrosoftODataEdmVocabulariesIEdmTermSchemaElementKind]):
            namespace (Union[Unset, str]):
            name (Union[Unset, str]):
     """

    type_: Union[Unset, 'MicrosoftODataEdmIEdmTypeReference'] = UNSET
    applies_to: Union[Unset, str] = UNSET
    default_value: Union[Unset, str] = UNSET
    schema_element_kind: Union[Unset, MicrosoftODataEdmVocabulariesIEdmTermSchemaElementKind] = UNSET
    namespace: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference
        type_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.to_dict()

        applies_to = self.applies_to

        default_value = self.default_value

        schema_element_kind: Union[Unset, int] = UNSET
        if not isinstance(self.schema_element_kind, Unset):
            schema_element_kind = self.schema_element_kind.value


        namespace = self.namespace

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["Type"] = type_
        if applies_to is not UNSET:
            field_dict["AppliesTo"] = applies_to
        if default_value is not UNSET:
            field_dict["DefaultValue"] = default_value
        if schema_element_kind is not UNSET:
            field_dict["SchemaElementKind"] = schema_element_kind
        if namespace is not UNSET:
            field_dict["Namespace"] = namespace
        if name is not UNSET:
            field_dict["Name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference
        d = dict(src_dict)
        _type_ = d.pop("Type", UNSET)
        type_: Union[Unset, MicrosoftODataEdmIEdmTypeReference]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = MicrosoftODataEdmIEdmTypeReference.from_dict(_type_)




        applies_to = d.pop("AppliesTo", UNSET)

        default_value = d.pop("DefaultValue", UNSET)

        _schema_element_kind = d.pop("SchemaElementKind", UNSET)
        schema_element_kind: Union[Unset, MicrosoftODataEdmVocabulariesIEdmTermSchemaElementKind]
        if isinstance(_schema_element_kind,  Unset):
            schema_element_kind = UNSET
        else:
            schema_element_kind = MicrosoftODataEdmVocabulariesIEdmTermSchemaElementKind(_schema_element_kind)




        namespace = d.pop("Namespace", UNSET)

        name = d.pop("Name", UNSET)

        microsoft_o_data_edm_vocabularies_i_edm_term = cls(
            type_=type_,
            applies_to=applies_to,
            default_value=default_value,
            schema_element_kind=schema_element_kind,
            namespace=namespace,
            name=name,
        )


        microsoft_o_data_edm_vocabularies_i_edm_term.additional_properties = d
        return microsoft_o_data_edm_vocabularies_i_edm_term

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
