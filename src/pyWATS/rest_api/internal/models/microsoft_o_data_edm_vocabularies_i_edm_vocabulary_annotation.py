from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_expression import MicrosoftODataEdmIEdmExpression
  from ..models.microsoft_o_data_edm_vocabularies_i_edm_term import MicrosoftODataEdmVocabulariesIEdmTerm
  from ..models.microsoft_o_data_edm_vocabularies_i_edm_vocabulary_annotatable import MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotatable





T = TypeVar("T", bound="MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotation")



@_attrs_define
class MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotation:
    """ 
        Attributes:
            qualifier (Union[Unset, str]):
            term (Union[Unset, MicrosoftODataEdmVocabulariesIEdmTerm]):
            target (Union[Unset, MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotatable]):
            value (Union[Unset, MicrosoftODataEdmIEdmExpression]):
     """

    qualifier: Union[Unset, str] = UNSET
    term: Union[Unset, 'MicrosoftODataEdmVocabulariesIEdmTerm'] = UNSET
    target: Union[Unset, 'MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotatable'] = UNSET
    value: Union[Unset, 'MicrosoftODataEdmIEdmExpression'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_expression import MicrosoftODataEdmIEdmExpression
        from ..models.microsoft_o_data_edm_vocabularies_i_edm_term import MicrosoftODataEdmVocabulariesIEdmTerm
        from ..models.microsoft_o_data_edm_vocabularies_i_edm_vocabulary_annotatable import MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotatable
        qualifier = self.qualifier

        term: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.term, Unset):
            term = self.term.to_dict()

        target: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.target, Unset):
            target = self.target.to_dict()

        value: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if qualifier is not UNSET:
            field_dict["Qualifier"] = qualifier
        if term is not UNSET:
            field_dict["Term"] = term
        if target is not UNSET:
            field_dict["Target"] = target
        if value is not UNSET:
            field_dict["Value"] = value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_expression import MicrosoftODataEdmIEdmExpression
        from ..models.microsoft_o_data_edm_vocabularies_i_edm_term import MicrosoftODataEdmVocabulariesIEdmTerm
        from ..models.microsoft_o_data_edm_vocabularies_i_edm_vocabulary_annotatable import MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotatable
        d = dict(src_dict)
        qualifier = d.pop("Qualifier", UNSET)

        _term = d.pop("Term", UNSET)
        term: Union[Unset, MicrosoftODataEdmVocabulariesIEdmTerm]
        if isinstance(_term,  Unset):
            term = UNSET
        else:
            term = MicrosoftODataEdmVocabulariesIEdmTerm.from_dict(_term)




        _target = d.pop("Target", UNSET)
        target: Union[Unset, MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotatable]
        if isinstance(_target,  Unset):
            target = UNSET
        else:
            target = MicrosoftODataEdmVocabulariesIEdmVocabularyAnnotatable.from_dict(_target)




        _value = d.pop("Value", UNSET)
        value: Union[Unset, MicrosoftODataEdmIEdmExpression]
        if isinstance(_value,  Unset):
            value = UNSET
        else:
            value = MicrosoftODataEdmIEdmExpression.from_dict(_value)




        microsoft_o_data_edm_vocabularies_i_edm_vocabulary_annotation = cls(
            qualifier=qualifier,
            term=term,
            target=target,
            value=value,
        )


        microsoft_o_data_edm_vocabularies_i_edm_vocabulary_annotation.additional_properties = d
        return microsoft_o_data_edm_vocabularies_i_edm_vocabulary_annotation

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
