from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
  from ..models.microsoft_o_data_uri_parser_aggregation_apply_clause import MicrosoftODataUriParserAggregationApplyClause





T = TypeVar("T", bound="MicrosoftAspNetODataQueryApplyQueryOption")



@_attrs_define
class MicrosoftAspNetODataQueryApplyQueryOption:
    """ 
        Attributes:
            context (Union[Unset, MicrosoftAspNetODataODataQueryContext]):
            result_clr_type (Union[Unset, str]):
            apply_clause (Union[Unset, MicrosoftODataUriParserAggregationApplyClause]):
            raw_value (Union[Unset, str]):
     """

    context: Union[Unset, 'MicrosoftAspNetODataODataQueryContext'] = UNSET
    result_clr_type: Union[Unset, str] = UNSET
    apply_clause: Union[Unset, 'MicrosoftODataUriParserAggregationApplyClause'] = UNSET
    raw_value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        from ..models.microsoft_o_data_uri_parser_aggregation_apply_clause import MicrosoftODataUriParserAggregationApplyClause
        context: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        result_clr_type = self.result_clr_type

        apply_clause: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.apply_clause, Unset):
            apply_clause = self.apply_clause.to_dict()

        raw_value = self.raw_value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if context is not UNSET:
            field_dict["Context"] = context
        if result_clr_type is not UNSET:
            field_dict["ResultClrType"] = result_clr_type
        if apply_clause is not UNSET:
            field_dict["ApplyClause"] = apply_clause
        if raw_value is not UNSET:
            field_dict["RawValue"] = raw_value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        from ..models.microsoft_o_data_uri_parser_aggregation_apply_clause import MicrosoftODataUriParserAggregationApplyClause
        d = dict(src_dict)
        _context = d.pop("Context", UNSET)
        context: Union[Unset, MicrosoftAspNetODataODataQueryContext]
        if isinstance(_context,  Unset):
            context = UNSET
        else:
            context = MicrosoftAspNetODataODataQueryContext.from_dict(_context)




        result_clr_type = d.pop("ResultClrType", UNSET)

        _apply_clause = d.pop("ApplyClause", UNSET)
        apply_clause: Union[Unset, MicrosoftODataUriParserAggregationApplyClause]
        if isinstance(_apply_clause,  Unset):
            apply_clause = UNSET
        else:
            apply_clause = MicrosoftODataUriParserAggregationApplyClause.from_dict(_apply_clause)




        raw_value = d.pop("RawValue", UNSET)

        microsoft_asp_net_o_data_query_apply_query_option = cls(
            context=context,
            result_clr_type=result_clr_type,
            apply_clause=apply_clause,
            raw_value=raw_value,
        )


        microsoft_asp_net_o_data_query_apply_query_option.additional_properties = d
        return microsoft_asp_net_o_data_query_apply_query_option

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
