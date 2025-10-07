from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_asp_net_o_data_query_validators_select_expand_query_validator import MicrosoftAspNetODataQueryValidatorsSelectExpandQueryValidator
  from ..models.microsoft_o_data_uri_parser_select_expand_clause import MicrosoftODataUriParserSelectExpandClause
  from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext





T = TypeVar("T", bound="MicrosoftAspNetODataQuerySelectExpandQueryOption")



@_attrs_define
class MicrosoftAspNetODataQuerySelectExpandQueryOption:
    """ 
        Attributes:
            context (Union[Unset, MicrosoftAspNetODataODataQueryContext]):
            raw_select (Union[Unset, str]):
            raw_expand (Union[Unset, str]):
            validator (Union[Unset, MicrosoftAspNetODataQueryValidatorsSelectExpandQueryValidator]):
            select_expand_clause (Union[Unset, MicrosoftODataUriParserSelectExpandClause]):
            levels_max_literal_expansion_depth (Union[Unset, int]):
     """

    context: Union[Unset, 'MicrosoftAspNetODataODataQueryContext'] = UNSET
    raw_select: Union[Unset, str] = UNSET
    raw_expand: Union[Unset, str] = UNSET
    validator: Union[Unset, 'MicrosoftAspNetODataQueryValidatorsSelectExpandQueryValidator'] = UNSET
    select_expand_clause: Union[Unset, 'MicrosoftODataUriParserSelectExpandClause'] = UNSET
    levels_max_literal_expansion_depth: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_asp_net_o_data_query_validators_select_expand_query_validator import MicrosoftAspNetODataQueryValidatorsSelectExpandQueryValidator
        from ..models.microsoft_o_data_uri_parser_select_expand_clause import MicrosoftODataUriParserSelectExpandClause
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        context: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        raw_select = self.raw_select

        raw_expand = self.raw_expand

        validator: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.validator, Unset):
            validator = self.validator.to_dict()

        select_expand_clause: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.select_expand_clause, Unset):
            select_expand_clause = self.select_expand_clause.to_dict()

        levels_max_literal_expansion_depth = self.levels_max_literal_expansion_depth


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if context is not UNSET:
            field_dict["Context"] = context
        if raw_select is not UNSET:
            field_dict["RawSelect"] = raw_select
        if raw_expand is not UNSET:
            field_dict["RawExpand"] = raw_expand
        if validator is not UNSET:
            field_dict["Validator"] = validator
        if select_expand_clause is not UNSET:
            field_dict["SelectExpandClause"] = select_expand_clause
        if levels_max_literal_expansion_depth is not UNSET:
            field_dict["LevelsMaxLiteralExpansionDepth"] = levels_max_literal_expansion_depth

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_asp_net_o_data_query_validators_select_expand_query_validator import MicrosoftAspNetODataQueryValidatorsSelectExpandQueryValidator
        from ..models.microsoft_o_data_uri_parser_select_expand_clause import MicrosoftODataUriParserSelectExpandClause
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        d = dict(src_dict)
        _context = d.pop("Context", UNSET)
        context: Union[Unset, MicrosoftAspNetODataODataQueryContext]
        if isinstance(_context,  Unset):
            context = UNSET
        else:
            context = MicrosoftAspNetODataODataQueryContext.from_dict(_context)




        raw_select = d.pop("RawSelect", UNSET)

        raw_expand = d.pop("RawExpand", UNSET)

        _validator = d.pop("Validator", UNSET)
        validator: Union[Unset, MicrosoftAspNetODataQueryValidatorsSelectExpandQueryValidator]
        if isinstance(_validator,  Unset):
            validator = UNSET
        else:
            validator = MicrosoftAspNetODataQueryValidatorsSelectExpandQueryValidator.from_dict(_validator)




        _select_expand_clause = d.pop("SelectExpandClause", UNSET)
        select_expand_clause: Union[Unset, MicrosoftODataUriParserSelectExpandClause]
        if isinstance(_select_expand_clause,  Unset):
            select_expand_clause = UNSET
        else:
            select_expand_clause = MicrosoftODataUriParserSelectExpandClause.from_dict(_select_expand_clause)




        levels_max_literal_expansion_depth = d.pop("LevelsMaxLiteralExpansionDepth", UNSET)

        microsoft_asp_net_o_data_query_select_expand_query_option = cls(
            context=context,
            raw_select=raw_select,
            raw_expand=raw_expand,
            validator=validator,
            select_expand_clause=select_expand_clause,
            levels_max_literal_expansion_depth=levels_max_literal_expansion_depth,
        )


        microsoft_asp_net_o_data_query_select_expand_query_option.additional_properties = d
        return microsoft_asp_net_o_data_query_select_expand_query_option

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
