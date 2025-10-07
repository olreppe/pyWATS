from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MicrosoftAspNetODataQueryDefaultQuerySettings")



@_attrs_define
class MicrosoftAspNetODataQueryDefaultQuerySettings:
    """ 
        Attributes:
            enable_expand (Union[Unset, bool]):
            enable_select (Union[Unset, bool]):
            enable_count (Union[Unset, bool]):
            enable_order_by (Union[Unset, bool]):
            enable_filter (Union[Unset, bool]):
            max_top (Union[Unset, int]):
            enable_skip_token (Union[Unset, bool]):
     """

    enable_expand: Union[Unset, bool] = UNSET
    enable_select: Union[Unset, bool] = UNSET
    enable_count: Union[Unset, bool] = UNSET
    enable_order_by: Union[Unset, bool] = UNSET
    enable_filter: Union[Unset, bool] = UNSET
    max_top: Union[Unset, int] = UNSET
    enable_skip_token: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        enable_expand = self.enable_expand

        enable_select = self.enable_select

        enable_count = self.enable_count

        enable_order_by = self.enable_order_by

        enable_filter = self.enable_filter

        max_top = self.max_top

        enable_skip_token = self.enable_skip_token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if enable_expand is not UNSET:
            field_dict["EnableExpand"] = enable_expand
        if enable_select is not UNSET:
            field_dict["EnableSelect"] = enable_select
        if enable_count is not UNSET:
            field_dict["EnableCount"] = enable_count
        if enable_order_by is not UNSET:
            field_dict["EnableOrderBy"] = enable_order_by
        if enable_filter is not UNSET:
            field_dict["EnableFilter"] = enable_filter
        if max_top is not UNSET:
            field_dict["MaxTop"] = max_top
        if enable_skip_token is not UNSET:
            field_dict["EnableSkipToken"] = enable_skip_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enable_expand = d.pop("EnableExpand", UNSET)

        enable_select = d.pop("EnableSelect", UNSET)

        enable_count = d.pop("EnableCount", UNSET)

        enable_order_by = d.pop("EnableOrderBy", UNSET)

        enable_filter = d.pop("EnableFilter", UNSET)

        max_top = d.pop("MaxTop", UNSET)

        enable_skip_token = d.pop("EnableSkipToken", UNSET)

        microsoft_asp_net_o_data_query_default_query_settings = cls(
            enable_expand=enable_expand,
            enable_select=enable_select,
            enable_count=enable_count,
            enable_order_by=enable_order_by,
            enable_filter=enable_filter,
            max_top=max_top,
            enable_skip_token=enable_skip_token,
        )


        microsoft_asp_net_o_data_query_default_query_settings.additional_properties = d
        return microsoft_asp_net_o_data_query_default_query_settings

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
