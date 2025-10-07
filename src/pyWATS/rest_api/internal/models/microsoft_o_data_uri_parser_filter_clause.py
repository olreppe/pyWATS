from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference
  from ..models.microsoft_o_data_uri_parser_range_variable import MicrosoftODataUriParserRangeVariable
  from ..models.microsoft_o_data_uri_parser_single_value_node import MicrosoftODataUriParserSingleValueNode





T = TypeVar("T", bound="MicrosoftODataUriParserFilterClause")



@_attrs_define
class MicrosoftODataUriParserFilterClause:
    """ 
        Attributes:
            expression (Union[Unset, MicrosoftODataUriParserSingleValueNode]):
            range_variable (Union[Unset, MicrosoftODataUriParserRangeVariable]):
            item_type (Union[Unset, MicrosoftODataEdmIEdmTypeReference]):
     """

    expression: Union[Unset, 'MicrosoftODataUriParserSingleValueNode'] = UNSET
    range_variable: Union[Unset, 'MicrosoftODataUriParserRangeVariable'] = UNSET
    item_type: Union[Unset, 'MicrosoftODataEdmIEdmTypeReference'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference
        from ..models.microsoft_o_data_uri_parser_range_variable import MicrosoftODataUriParserRangeVariable
        from ..models.microsoft_o_data_uri_parser_single_value_node import MicrosoftODataUriParserSingleValueNode
        expression: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.expression, Unset):
            expression = self.expression.to_dict()

        range_variable: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.range_variable, Unset):
            range_variable = self.range_variable.to_dict()

        item_type: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.item_type, Unset):
            item_type = self.item_type.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if expression is not UNSET:
            field_dict["Expression"] = expression
        if range_variable is not UNSET:
            field_dict["RangeVariable"] = range_variable
        if item_type is not UNSET:
            field_dict["ItemType"] = item_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference
        from ..models.microsoft_o_data_uri_parser_range_variable import MicrosoftODataUriParserRangeVariable
        from ..models.microsoft_o_data_uri_parser_single_value_node import MicrosoftODataUriParserSingleValueNode
        d = dict(src_dict)
        _expression = d.pop("Expression", UNSET)
        expression: Union[Unset, MicrosoftODataUriParserSingleValueNode]
        if isinstance(_expression,  Unset):
            expression = UNSET
        else:
            expression = MicrosoftODataUriParserSingleValueNode.from_dict(_expression)




        _range_variable = d.pop("RangeVariable", UNSET)
        range_variable: Union[Unset, MicrosoftODataUriParserRangeVariable]
        if isinstance(_range_variable,  Unset):
            range_variable = UNSET
        else:
            range_variable = MicrosoftODataUriParserRangeVariable.from_dict(_range_variable)




        _item_type = d.pop("ItemType", UNSET)
        item_type: Union[Unset, MicrosoftODataEdmIEdmTypeReference]
        if isinstance(_item_type,  Unset):
            item_type = UNSET
        else:
            item_type = MicrosoftODataEdmIEdmTypeReference.from_dict(_item_type)




        microsoft_o_data_uri_parser_filter_clause = cls(
            expression=expression,
            range_variable=range_variable,
            item_type=item_type,
        )


        microsoft_o_data_uri_parser_filter_clause.additional_properties = d
        return microsoft_o_data_uri_parser_filter_clause

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
