from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.microsoft_o_data_edm_i_edm_expression_expression_kind import MicrosoftODataEdmIEdmExpressionExpressionKind
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MicrosoftODataEdmIEdmExpression")



@_attrs_define
class MicrosoftODataEdmIEdmExpression:
    """ 
        Attributes:
            expression_kind (Union[Unset, MicrosoftODataEdmIEdmExpressionExpressionKind]):
     """

    expression_kind: Union[Unset, MicrosoftODataEdmIEdmExpressionExpressionKind] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        expression_kind: Union[Unset, int] = UNSET
        if not isinstance(self.expression_kind, Unset):
            expression_kind = self.expression_kind.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if expression_kind is not UNSET:
            field_dict["ExpressionKind"] = expression_kind

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _expression_kind = d.pop("ExpressionKind", UNSET)
        expression_kind: Union[Unset, MicrosoftODataEdmIEdmExpressionExpressionKind]
        if isinstance(_expression_kind,  Unset):
            expression_kind = UNSET
        else:
            expression_kind = MicrosoftODataEdmIEdmExpressionExpressionKind(_expression_kind)




        microsoft_o_data_edm_i_edm_expression = cls(
            expression_kind=expression_kind,
        )


        microsoft_o_data_edm_i_edm_expression.additional_properties = d
        return microsoft_o_data_edm_i_edm_expression

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
