from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_asp_net_o_data_query_validators_filter_query_validator import MicrosoftAspNetODataQueryValidatorsFilterQueryValidator
  from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
  from ..models.microsoft_o_data_uri_parser_filter_clause import MicrosoftODataUriParserFilterClause





T = TypeVar("T", bound="MicrosoftAspNetODataQueryFilterQueryOption")



@_attrs_define
class MicrosoftAspNetODataQueryFilterQueryOption:
    """ 
        Attributes:
            context (Union[Unset, MicrosoftAspNetODataODataQueryContext]):
            validator (Union[Unset, MicrosoftAspNetODataQueryValidatorsFilterQueryValidator]):
            filter_clause (Union[Unset, MicrosoftODataUriParserFilterClause]):
            raw_value (Union[Unset, str]):
     """

    context: Union[Unset, 'MicrosoftAspNetODataODataQueryContext'] = UNSET
    validator: Union[Unset, 'MicrosoftAspNetODataQueryValidatorsFilterQueryValidator'] = UNSET
    filter_clause: Union[Unset, 'MicrosoftODataUriParserFilterClause'] = UNSET
    raw_value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_asp_net_o_data_query_validators_filter_query_validator import MicrosoftAspNetODataQueryValidatorsFilterQueryValidator
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        from ..models.microsoft_o_data_uri_parser_filter_clause import MicrosoftODataUriParserFilterClause
        context: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        validator: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.validator, Unset):
            validator = self.validator.to_dict()

        filter_clause: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_clause, Unset):
            filter_clause = self.filter_clause.to_dict()

        raw_value = self.raw_value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if context is not UNSET:
            field_dict["Context"] = context
        if validator is not UNSET:
            field_dict["Validator"] = validator
        if filter_clause is not UNSET:
            field_dict["FilterClause"] = filter_clause
        if raw_value is not UNSET:
            field_dict["RawValue"] = raw_value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_asp_net_o_data_query_validators_filter_query_validator import MicrosoftAspNetODataQueryValidatorsFilterQueryValidator
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        from ..models.microsoft_o_data_uri_parser_filter_clause import MicrosoftODataUriParserFilterClause
        d = dict(src_dict)
        _context = d.pop("Context", UNSET)
        context: Union[Unset, MicrosoftAspNetODataODataQueryContext]
        if isinstance(_context,  Unset):
            context = UNSET
        else:
            context = MicrosoftAspNetODataODataQueryContext.from_dict(_context)




        _validator = d.pop("Validator", UNSET)
        validator: Union[Unset, MicrosoftAspNetODataQueryValidatorsFilterQueryValidator]
        if isinstance(_validator,  Unset):
            validator = UNSET
        else:
            validator = MicrosoftAspNetODataQueryValidatorsFilterQueryValidator.from_dict(_validator)




        _filter_clause = d.pop("FilterClause", UNSET)
        filter_clause: Union[Unset, MicrosoftODataUriParserFilterClause]
        if isinstance(_filter_clause,  Unset):
            filter_clause = UNSET
        else:
            filter_clause = MicrosoftODataUriParserFilterClause.from_dict(_filter_clause)




        raw_value = d.pop("RawValue", UNSET)

        microsoft_asp_net_o_data_query_filter_query_option = cls(
            context=context,
            validator=validator,
            filter_clause=filter_clause,
            raw_value=raw_value,
        )


        microsoft_asp_net_o_data_query_filter_query_option.additional_properties = d
        return microsoft_asp_net_o_data_query_filter_query_option

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
