from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MicrosoftAspNetODataQueryODataRawQueryOptions")



@_attrs_define
class MicrosoftAspNetODataQueryODataRawQueryOptions:
    """ 
        Attributes:
            filter_ (Union[Unset, str]):
            apply (Union[Unset, str]):
            order_by (Union[Unset, str]):
            top (Union[Unset, str]):
            skip (Union[Unset, str]):
            select (Union[Unset, str]):
            expand (Union[Unset, str]):
            count (Union[Unset, str]):
            format_ (Union[Unset, str]):
            skip_token (Union[Unset, str]):
            delta_token (Union[Unset, str]):
     """

    filter_: Union[Unset, str] = UNSET
    apply: Union[Unset, str] = UNSET
    order_by: Union[Unset, str] = UNSET
    top: Union[Unset, str] = UNSET
    skip: Union[Unset, str] = UNSET
    select: Union[Unset, str] = UNSET
    expand: Union[Unset, str] = UNSET
    count: Union[Unset, str] = UNSET
    format_: Union[Unset, str] = UNSET
    skip_token: Union[Unset, str] = UNSET
    delta_token: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        filter_ = self.filter_

        apply = self.apply

        order_by = self.order_by

        top = self.top

        skip = self.skip

        select = self.select

        expand = self.expand

        count = self.count

        format_ = self.format_

        skip_token = self.skip_token

        delta_token = self.delta_token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if filter_ is not UNSET:
            field_dict["Filter"] = filter_
        if apply is not UNSET:
            field_dict["Apply"] = apply
        if order_by is not UNSET:
            field_dict["OrderBy"] = order_by
        if top is not UNSET:
            field_dict["Top"] = top
        if skip is not UNSET:
            field_dict["Skip"] = skip
        if select is not UNSET:
            field_dict["Select"] = select
        if expand is not UNSET:
            field_dict["Expand"] = expand
        if count is not UNSET:
            field_dict["Count"] = count
        if format_ is not UNSET:
            field_dict["Format"] = format_
        if skip_token is not UNSET:
            field_dict["SkipToken"] = skip_token
        if delta_token is not UNSET:
            field_dict["DeltaToken"] = delta_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filter_ = d.pop("Filter", UNSET)

        apply = d.pop("Apply", UNSET)

        order_by = d.pop("OrderBy", UNSET)

        top = d.pop("Top", UNSET)

        skip = d.pop("Skip", UNSET)

        select = d.pop("Select", UNSET)

        expand = d.pop("Expand", UNSET)

        count = d.pop("Count", UNSET)

        format_ = d.pop("Format", UNSET)

        skip_token = d.pop("SkipToken", UNSET)

        delta_token = d.pop("DeltaToken", UNSET)

        microsoft_asp_net_o_data_query_o_data_raw_query_options = cls(
            filter_=filter_,
            apply=apply,
            order_by=order_by,
            top=top,
            skip=skip,
            select=select,
            expand=expand,
            count=count,
            format_=format_,
            skip_token=skip_token,
            delta_token=delta_token,
        )


        microsoft_asp_net_o_data_query_o_data_raw_query_options.additional_properties = d
        return microsoft_asp_net_o_data_query_o_data_raw_query_options

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
