from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_asp_net_o_data_query_top_query_option import MicrosoftAspNetODataQueryTopQueryOption
  from ..models.microsoft_asp_net_o_data_query_skip_token_query_option import MicrosoftAspNetODataQuerySkipTokenQueryOption
  from ..models.microsoft_asp_net_o_data_query_order_by_query_option import MicrosoftAspNetODataQueryOrderByQueryOption
  from ..models.microsoft_asp_net_o_data_query_o_data_query_options_if_match import MicrosoftAspNetODataQueryODataQueryOptionsIfMatch
  from ..models.microsoft_asp_net_o_data_query_o_data_query_options_if_none_match import MicrosoftAspNetODataQueryODataQueryOptionsIfNoneMatch
  from ..models.microsoft_asp_net_o_data_query_skip_query_option import MicrosoftAspNetODataQuerySkipQueryOption
  from ..models.microsoft_asp_net_o_data_query_select_expand_query_option import MicrosoftAspNetODataQuerySelectExpandQueryOption
  from ..models.microsoft_asp_net_o_data_query_filter_query_option import MicrosoftAspNetODataQueryFilterQueryOption
  from ..models.microsoft_asp_net_o_data_query_apply_query_option import MicrosoftAspNetODataQueryApplyQueryOption
  from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
  from ..models.microsoft_asp_net_o_data_query_count_query_option import MicrosoftAspNetODataQueryCountQueryOption
  from ..models.microsoft_asp_net_o_data_query_o_data_query_options_request import MicrosoftAspNetODataQueryODataQueryOptionsRequest
  from ..models.microsoft_asp_net_o_data_query_o_data_raw_query_options import MicrosoftAspNetODataQueryODataRawQueryOptions
  from ..models.microsoft_asp_net_o_data_query_validators_o_data_query_validator import MicrosoftAspNetODataQueryValidatorsODataQueryValidator





T = TypeVar("T", bound="MicrosoftAspNetODataQueryODataQueryOptions")



@_attrs_define
class MicrosoftAspNetODataQueryODataQueryOptions:
    """ 
        Attributes:
            request (Union[Unset, MicrosoftAspNetODataQueryODataQueryOptionsRequest]):
            context (Union[Unset, MicrosoftAspNetODataODataQueryContext]):
            raw_values (Union[Unset, MicrosoftAspNetODataQueryODataRawQueryOptions]):
            select_expand (Union[Unset, MicrosoftAspNetODataQuerySelectExpandQueryOption]):
            apply (Union[Unset, MicrosoftAspNetODataQueryApplyQueryOption]):
            filter_ (Union[Unset, MicrosoftAspNetODataQueryFilterQueryOption]):
            order_by (Union[Unset, MicrosoftAspNetODataQueryOrderByQueryOption]):
            skip (Union[Unset, MicrosoftAspNetODataQuerySkipQueryOption]):
            skip_token (Union[Unset, MicrosoftAspNetODataQuerySkipTokenQueryOption]):
            top (Union[Unset, MicrosoftAspNetODataQueryTopQueryOption]):
            count (Union[Unset, MicrosoftAspNetODataQueryCountQueryOption]):
            validator (Union[Unset, MicrosoftAspNetODataQueryValidatorsODataQueryValidator]):
            if_match (Union[Unset, MicrosoftAspNetODataQueryODataQueryOptionsIfMatch]):
            if_none_match (Union[Unset, MicrosoftAspNetODataQueryODataQueryOptionsIfNoneMatch]):
     """

    request: Union[Unset, 'MicrosoftAspNetODataQueryODataQueryOptionsRequest'] = UNSET
    context: Union[Unset, 'MicrosoftAspNetODataODataQueryContext'] = UNSET
    raw_values: Union[Unset, 'MicrosoftAspNetODataQueryODataRawQueryOptions'] = UNSET
    select_expand: Union[Unset, 'MicrosoftAspNetODataQuerySelectExpandQueryOption'] = UNSET
    apply: Union[Unset, 'MicrosoftAspNetODataQueryApplyQueryOption'] = UNSET
    filter_: Union[Unset, 'MicrosoftAspNetODataQueryFilterQueryOption'] = UNSET
    order_by: Union[Unset, 'MicrosoftAspNetODataQueryOrderByQueryOption'] = UNSET
    skip: Union[Unset, 'MicrosoftAspNetODataQuerySkipQueryOption'] = UNSET
    skip_token: Union[Unset, 'MicrosoftAspNetODataQuerySkipTokenQueryOption'] = UNSET
    top: Union[Unset, 'MicrosoftAspNetODataQueryTopQueryOption'] = UNSET
    count: Union[Unset, 'MicrosoftAspNetODataQueryCountQueryOption'] = UNSET
    validator: Union[Unset, 'MicrosoftAspNetODataQueryValidatorsODataQueryValidator'] = UNSET
    if_match: Union[Unset, 'MicrosoftAspNetODataQueryODataQueryOptionsIfMatch'] = UNSET
    if_none_match: Union[Unset, 'MicrosoftAspNetODataQueryODataQueryOptionsIfNoneMatch'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_asp_net_o_data_query_top_query_option import MicrosoftAspNetODataQueryTopQueryOption
        from ..models.microsoft_asp_net_o_data_query_skip_token_query_option import MicrosoftAspNetODataQuerySkipTokenQueryOption
        from ..models.microsoft_asp_net_o_data_query_order_by_query_option import MicrosoftAspNetODataQueryOrderByQueryOption
        from ..models.microsoft_asp_net_o_data_query_o_data_query_options_if_match import MicrosoftAspNetODataQueryODataQueryOptionsIfMatch
        from ..models.microsoft_asp_net_o_data_query_o_data_query_options_if_none_match import MicrosoftAspNetODataQueryODataQueryOptionsIfNoneMatch
        from ..models.microsoft_asp_net_o_data_query_skip_query_option import MicrosoftAspNetODataQuerySkipQueryOption
        from ..models.microsoft_asp_net_o_data_query_select_expand_query_option import MicrosoftAspNetODataQuerySelectExpandQueryOption
        from ..models.microsoft_asp_net_o_data_query_filter_query_option import MicrosoftAspNetODataQueryFilterQueryOption
        from ..models.microsoft_asp_net_o_data_query_apply_query_option import MicrosoftAspNetODataQueryApplyQueryOption
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        from ..models.microsoft_asp_net_o_data_query_count_query_option import MicrosoftAspNetODataQueryCountQueryOption
        from ..models.microsoft_asp_net_o_data_query_o_data_query_options_request import MicrosoftAspNetODataQueryODataQueryOptionsRequest
        from ..models.microsoft_asp_net_o_data_query_o_data_raw_query_options import MicrosoftAspNetODataQueryODataRawQueryOptions
        from ..models.microsoft_asp_net_o_data_query_validators_o_data_query_validator import MicrosoftAspNetODataQueryValidatorsODataQueryValidator
        request: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.request, Unset):
            request = self.request.to_dict()

        context: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        raw_values: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.raw_values, Unset):
            raw_values = self.raw_values.to_dict()

        select_expand: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.select_expand, Unset):
            select_expand = self.select_expand.to_dict()

        apply: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.apply, Unset):
            apply = self.apply.to_dict()

        filter_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        order_by: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.order_by, Unset):
            order_by = self.order_by.to_dict()

        skip: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.skip, Unset):
            skip = self.skip.to_dict()

        skip_token: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.skip_token, Unset):
            skip_token = self.skip_token.to_dict()

        top: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.top, Unset):
            top = self.top.to_dict()

        count: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.count, Unset):
            count = self.count.to_dict()

        validator: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.validator, Unset):
            validator = self.validator.to_dict()

        if_match: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.if_match, Unset):
            if_match = self.if_match.to_dict()

        if_none_match: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.if_none_match, Unset):
            if_none_match = self.if_none_match.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if request is not UNSET:
            field_dict["Request"] = request
        if context is not UNSET:
            field_dict["Context"] = context
        if raw_values is not UNSET:
            field_dict["RawValues"] = raw_values
        if select_expand is not UNSET:
            field_dict["SelectExpand"] = select_expand
        if apply is not UNSET:
            field_dict["Apply"] = apply
        if filter_ is not UNSET:
            field_dict["Filter"] = filter_
        if order_by is not UNSET:
            field_dict["OrderBy"] = order_by
        if skip is not UNSET:
            field_dict["Skip"] = skip
        if skip_token is not UNSET:
            field_dict["SkipToken"] = skip_token
        if top is not UNSET:
            field_dict["Top"] = top
        if count is not UNSET:
            field_dict["Count"] = count
        if validator is not UNSET:
            field_dict["Validator"] = validator
        if if_match is not UNSET:
            field_dict["IfMatch"] = if_match
        if if_none_match is not UNSET:
            field_dict["IfNoneMatch"] = if_none_match

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_asp_net_o_data_query_top_query_option import MicrosoftAspNetODataQueryTopQueryOption
        from ..models.microsoft_asp_net_o_data_query_skip_token_query_option import MicrosoftAspNetODataQuerySkipTokenQueryOption
        from ..models.microsoft_asp_net_o_data_query_order_by_query_option import MicrosoftAspNetODataQueryOrderByQueryOption
        from ..models.microsoft_asp_net_o_data_query_o_data_query_options_if_match import MicrosoftAspNetODataQueryODataQueryOptionsIfMatch
        from ..models.microsoft_asp_net_o_data_query_o_data_query_options_if_none_match import MicrosoftAspNetODataQueryODataQueryOptionsIfNoneMatch
        from ..models.microsoft_asp_net_o_data_query_skip_query_option import MicrosoftAspNetODataQuerySkipQueryOption
        from ..models.microsoft_asp_net_o_data_query_select_expand_query_option import MicrosoftAspNetODataQuerySelectExpandQueryOption
        from ..models.microsoft_asp_net_o_data_query_filter_query_option import MicrosoftAspNetODataQueryFilterQueryOption
        from ..models.microsoft_asp_net_o_data_query_apply_query_option import MicrosoftAspNetODataQueryApplyQueryOption
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        from ..models.microsoft_asp_net_o_data_query_count_query_option import MicrosoftAspNetODataQueryCountQueryOption
        from ..models.microsoft_asp_net_o_data_query_o_data_query_options_request import MicrosoftAspNetODataQueryODataQueryOptionsRequest
        from ..models.microsoft_asp_net_o_data_query_o_data_raw_query_options import MicrosoftAspNetODataQueryODataRawQueryOptions
        from ..models.microsoft_asp_net_o_data_query_validators_o_data_query_validator import MicrosoftAspNetODataQueryValidatorsODataQueryValidator
        d = dict(src_dict)
        _request = d.pop("Request", UNSET)
        request: Union[Unset, MicrosoftAspNetODataQueryODataQueryOptionsRequest]
        if isinstance(_request,  Unset):
            request = UNSET
        else:
            request = MicrosoftAspNetODataQueryODataQueryOptionsRequest.from_dict(_request)




        _context = d.pop("Context", UNSET)
        context: Union[Unset, MicrosoftAspNetODataODataQueryContext]
        if isinstance(_context,  Unset):
            context = UNSET
        else:
            context = MicrosoftAspNetODataODataQueryContext.from_dict(_context)




        _raw_values = d.pop("RawValues", UNSET)
        raw_values: Union[Unset, MicrosoftAspNetODataQueryODataRawQueryOptions]
        if isinstance(_raw_values,  Unset):
            raw_values = UNSET
        else:
            raw_values = MicrosoftAspNetODataQueryODataRawQueryOptions.from_dict(_raw_values)




        _select_expand = d.pop("SelectExpand", UNSET)
        select_expand: Union[Unset, MicrosoftAspNetODataQuerySelectExpandQueryOption]
        if isinstance(_select_expand,  Unset):
            select_expand = UNSET
        else:
            select_expand = MicrosoftAspNetODataQuerySelectExpandQueryOption.from_dict(_select_expand)




        _apply = d.pop("Apply", UNSET)
        apply: Union[Unset, MicrosoftAspNetODataQueryApplyQueryOption]
        if isinstance(_apply,  Unset):
            apply = UNSET
        else:
            apply = MicrosoftAspNetODataQueryApplyQueryOption.from_dict(_apply)




        _filter_ = d.pop("Filter", UNSET)
        filter_: Union[Unset, MicrosoftAspNetODataQueryFilterQueryOption]
        if isinstance(_filter_,  Unset):
            filter_ = UNSET
        else:
            filter_ = MicrosoftAspNetODataQueryFilterQueryOption.from_dict(_filter_)




        _order_by = d.pop("OrderBy", UNSET)
        order_by: Union[Unset, MicrosoftAspNetODataQueryOrderByQueryOption]
        if isinstance(_order_by,  Unset):
            order_by = UNSET
        else:
            order_by = MicrosoftAspNetODataQueryOrderByQueryOption.from_dict(_order_by)




        _skip = d.pop("Skip", UNSET)
        skip: Union[Unset, MicrosoftAspNetODataQuerySkipQueryOption]
        if isinstance(_skip,  Unset):
            skip = UNSET
        else:
            skip = MicrosoftAspNetODataQuerySkipQueryOption.from_dict(_skip)




        _skip_token = d.pop("SkipToken", UNSET)
        skip_token: Union[Unset, MicrosoftAspNetODataQuerySkipTokenQueryOption]
        if isinstance(_skip_token,  Unset):
            skip_token = UNSET
        else:
            skip_token = MicrosoftAspNetODataQuerySkipTokenQueryOption.from_dict(_skip_token)




        _top = d.pop("Top", UNSET)
        top: Union[Unset, MicrosoftAspNetODataQueryTopQueryOption]
        if isinstance(_top,  Unset):
            top = UNSET
        else:
            top = MicrosoftAspNetODataQueryTopQueryOption.from_dict(_top)




        _count = d.pop("Count", UNSET)
        count: Union[Unset, MicrosoftAspNetODataQueryCountQueryOption]
        if isinstance(_count,  Unset):
            count = UNSET
        else:
            count = MicrosoftAspNetODataQueryCountQueryOption.from_dict(_count)




        _validator = d.pop("Validator", UNSET)
        validator: Union[Unset, MicrosoftAspNetODataQueryValidatorsODataQueryValidator]
        if isinstance(_validator,  Unset):
            validator = UNSET
        else:
            validator = MicrosoftAspNetODataQueryValidatorsODataQueryValidator.from_dict(_validator)




        _if_match = d.pop("IfMatch", UNSET)
        if_match: Union[Unset, MicrosoftAspNetODataQueryODataQueryOptionsIfMatch]
        if isinstance(_if_match,  Unset):
            if_match = UNSET
        else:
            if_match = MicrosoftAspNetODataQueryODataQueryOptionsIfMatch.from_dict(_if_match)




        _if_none_match = d.pop("IfNoneMatch", UNSET)
        if_none_match: Union[Unset, MicrosoftAspNetODataQueryODataQueryOptionsIfNoneMatch]
        if isinstance(_if_none_match,  Unset):
            if_none_match = UNSET
        else:
            if_none_match = MicrosoftAspNetODataQueryODataQueryOptionsIfNoneMatch.from_dict(_if_none_match)




        microsoft_asp_net_o_data_query_o_data_query_options = cls(
            request=request,
            context=context,
            raw_values=raw_values,
            select_expand=select_expand,
            apply=apply,
            filter_=filter_,
            order_by=order_by,
            skip=skip,
            skip_token=skip_token,
            top=top,
            count=count,
            validator=validator,
            if_match=if_match,
            if_none_match=if_none_match,
        )


        microsoft_asp_net_o_data_query_o_data_query_options.additional_properties = d
        return microsoft_asp_net_o_data_query_o_data_query_options

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
