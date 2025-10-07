from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_uri_parser_aggregation_transformation_node import MicrosoftODataUriParserAggregationTransformationNode





T = TypeVar("T", bound="MicrosoftODataUriParserAggregationApplyClause")



@_attrs_define
class MicrosoftODataUriParserAggregationApplyClause:
    """ 
        Attributes:
            transformations (Union[Unset, list['MicrosoftODataUriParserAggregationTransformationNode']]):
     """

    transformations: Union[Unset, list['MicrosoftODataUriParserAggregationTransformationNode']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_uri_parser_aggregation_transformation_node import MicrosoftODataUriParserAggregationTransformationNode
        transformations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.transformations, Unset):
            transformations = []
            for transformations_item_data in self.transformations:
                transformations_item = transformations_item_data.to_dict()
                transformations.append(transformations_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if transformations is not UNSET:
            field_dict["Transformations"] = transformations

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_uri_parser_aggregation_transformation_node import MicrosoftODataUriParserAggregationTransformationNode
        d = dict(src_dict)
        transformations = []
        _transformations = d.pop("Transformations", UNSET)
        for transformations_item_data in (_transformations or []):
            transformations_item = MicrosoftODataUriParserAggregationTransformationNode.from_dict(transformations_item_data)



            transformations.append(transformations_item)


        microsoft_o_data_uri_parser_aggregation_apply_clause = cls(
            transformations=transformations,
        )


        microsoft_o_data_uri_parser_aggregation_apply_clause.additional_properties = d
        return microsoft_o_data_uri_parser_aggregation_apply_clause

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
