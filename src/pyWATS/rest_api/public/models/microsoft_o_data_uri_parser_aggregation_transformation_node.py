from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.microsoft_o_data_uri_parser_aggregation_transformation_node_kind import MicrosoftODataUriParserAggregationTransformationNodeKind
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MicrosoftODataUriParserAggregationTransformationNode")



@_attrs_define
class MicrosoftODataUriParserAggregationTransformationNode:
    """ 
        Attributes:
            kind (Union[Unset, MicrosoftODataUriParserAggregationTransformationNodeKind]):
     """

    kind: Union[Unset, MicrosoftODataUriParserAggregationTransformationNodeKind] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind: Union[Unset, int] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if kind is not UNSET:
            field_dict["Kind"] = kind

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _kind = d.pop("Kind", UNSET)
        kind: Union[Unset, MicrosoftODataUriParserAggregationTransformationNodeKind]
        if isinstance(_kind,  Unset):
            kind = UNSET
        else:
            kind = MicrosoftODataUriParserAggregationTransformationNodeKind(_kind)




        microsoft_o_data_uri_parser_aggregation_transformation_node = cls(
            kind=kind,
        )


        microsoft_o_data_uri_parser_aggregation_transformation_node.additional_properties = d
        return microsoft_o_data_uri_parser_aggregation_transformation_node

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
