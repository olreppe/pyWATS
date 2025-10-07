from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_asp_net_o_data_query_order_by_node import MicrosoftAspNetODataQueryOrderByNode
  from ..models.microsoft_asp_net_o_data_query_validators_order_by_query_validator import MicrosoftAspNetODataQueryValidatorsOrderByQueryValidator
  from ..models.microsoft_o_data_uri_parser_order_by_clause import MicrosoftODataUriParserOrderByClause
  from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext





T = TypeVar("T", bound="MicrosoftAspNetODataQueryOrderByQueryOption")



@_attrs_define
class MicrosoftAspNetODataQueryOrderByQueryOption:
    """ 
        Attributes:
            context (Union[Unset, MicrosoftAspNetODataODataQueryContext]):
            order_by_nodes (Union[Unset, list['MicrosoftAspNetODataQueryOrderByNode']]):
            raw_value (Union[Unset, str]):
            validator (Union[Unset, MicrosoftAspNetODataQueryValidatorsOrderByQueryValidator]):
            order_by_clause (Union[Unset, MicrosoftODataUriParserOrderByClause]):
     """

    context: Union[Unset, 'MicrosoftAspNetODataODataQueryContext'] = UNSET
    order_by_nodes: Union[Unset, list['MicrosoftAspNetODataQueryOrderByNode']] = UNSET
    raw_value: Union[Unset, str] = UNSET
    validator: Union[Unset, 'MicrosoftAspNetODataQueryValidatorsOrderByQueryValidator'] = UNSET
    order_by_clause: Union[Unset, 'MicrosoftODataUriParserOrderByClause'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_asp_net_o_data_query_order_by_node import MicrosoftAspNetODataQueryOrderByNode
        from ..models.microsoft_asp_net_o_data_query_validators_order_by_query_validator import MicrosoftAspNetODataQueryValidatorsOrderByQueryValidator
        from ..models.microsoft_o_data_uri_parser_order_by_clause import MicrosoftODataUriParserOrderByClause
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        context: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        order_by_nodes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.order_by_nodes, Unset):
            order_by_nodes = []
            for order_by_nodes_item_data in self.order_by_nodes:
                order_by_nodes_item = order_by_nodes_item_data.to_dict()
                order_by_nodes.append(order_by_nodes_item)



        raw_value = self.raw_value

        validator: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.validator, Unset):
            validator = self.validator.to_dict()

        order_by_clause: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.order_by_clause, Unset):
            order_by_clause = self.order_by_clause.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if context is not UNSET:
            field_dict["Context"] = context
        if order_by_nodes is not UNSET:
            field_dict["OrderByNodes"] = order_by_nodes
        if raw_value is not UNSET:
            field_dict["RawValue"] = raw_value
        if validator is not UNSET:
            field_dict["Validator"] = validator
        if order_by_clause is not UNSET:
            field_dict["OrderByClause"] = order_by_clause

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_asp_net_o_data_query_order_by_node import MicrosoftAspNetODataQueryOrderByNode
        from ..models.microsoft_asp_net_o_data_query_validators_order_by_query_validator import MicrosoftAspNetODataQueryValidatorsOrderByQueryValidator
        from ..models.microsoft_o_data_uri_parser_order_by_clause import MicrosoftODataUriParserOrderByClause
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        d = dict(src_dict)
        _context = d.pop("Context", UNSET)
        context: Union[Unset, MicrosoftAspNetODataODataQueryContext]
        if isinstance(_context,  Unset):
            context = UNSET
        else:
            context = MicrosoftAspNetODataODataQueryContext.from_dict(_context)




        order_by_nodes = []
        _order_by_nodes = d.pop("OrderByNodes", UNSET)
        for order_by_nodes_item_data in (_order_by_nodes or []):
            order_by_nodes_item = MicrosoftAspNetODataQueryOrderByNode.from_dict(order_by_nodes_item_data)



            order_by_nodes.append(order_by_nodes_item)


        raw_value = d.pop("RawValue", UNSET)

        _validator = d.pop("Validator", UNSET)
        validator: Union[Unset, MicrosoftAspNetODataQueryValidatorsOrderByQueryValidator]
        if isinstance(_validator,  Unset):
            validator = UNSET
        else:
            validator = MicrosoftAspNetODataQueryValidatorsOrderByQueryValidator.from_dict(_validator)




        _order_by_clause = d.pop("OrderByClause", UNSET)
        order_by_clause: Union[Unset, MicrosoftODataUriParserOrderByClause]
        if isinstance(_order_by_clause,  Unset):
            order_by_clause = UNSET
        else:
            order_by_clause = MicrosoftODataUriParserOrderByClause.from_dict(_order_by_clause)




        microsoft_asp_net_o_data_query_order_by_query_option = cls(
            context=context,
            order_by_nodes=order_by_nodes,
            raw_value=raw_value,
            validator=validator,
            order_by_clause=order_by_clause,
        )


        microsoft_asp_net_o_data_query_order_by_query_option.additional_properties = d
        return microsoft_asp_net_o_data_query_order_by_query_option

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
