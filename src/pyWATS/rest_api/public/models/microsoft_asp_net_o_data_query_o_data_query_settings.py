from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.microsoft_asp_net_o_data_query_o_data_query_settings_handle_null_propagation import MicrosoftAspNetODataQueryODataQuerySettingsHandleNullPropagation
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MicrosoftAspNetODataQueryODataQuerySettings")



@_attrs_define
class MicrosoftAspNetODataQueryODataQuerySettings:
    """ 
        Attributes:
            ensure_stable_ordering (Union[Unset, bool]):
            handle_null_propagation (Union[Unset, MicrosoftAspNetODataQueryODataQuerySettingsHandleNullPropagation]):
            enable_constant_parameterization (Union[Unset, bool]):
            enable_correlated_subquery_buffering (Union[Unset, bool]):
            page_size (Union[Unset, int]):
            handle_reference_navigation_property_expand_filter (Union[Unset, bool]):
     """

    ensure_stable_ordering: Union[Unset, bool] = UNSET
    handle_null_propagation: Union[Unset, MicrosoftAspNetODataQueryODataQuerySettingsHandleNullPropagation] = UNSET
    enable_constant_parameterization: Union[Unset, bool] = UNSET
    enable_correlated_subquery_buffering: Union[Unset, bool] = UNSET
    page_size: Union[Unset, int] = UNSET
    handle_reference_navigation_property_expand_filter: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        ensure_stable_ordering = self.ensure_stable_ordering

        handle_null_propagation: Union[Unset, int] = UNSET
        if not isinstance(self.handle_null_propagation, Unset):
            handle_null_propagation = self.handle_null_propagation.value


        enable_constant_parameterization = self.enable_constant_parameterization

        enable_correlated_subquery_buffering = self.enable_correlated_subquery_buffering

        page_size = self.page_size

        handle_reference_navigation_property_expand_filter = self.handle_reference_navigation_property_expand_filter


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if ensure_stable_ordering is not UNSET:
            field_dict["EnsureStableOrdering"] = ensure_stable_ordering
        if handle_null_propagation is not UNSET:
            field_dict["HandleNullPropagation"] = handle_null_propagation
        if enable_constant_parameterization is not UNSET:
            field_dict["EnableConstantParameterization"] = enable_constant_parameterization
        if enable_correlated_subquery_buffering is not UNSET:
            field_dict["EnableCorrelatedSubqueryBuffering"] = enable_correlated_subquery_buffering
        if page_size is not UNSET:
            field_dict["PageSize"] = page_size
        if handle_reference_navigation_property_expand_filter is not UNSET:
            field_dict["HandleReferenceNavigationPropertyExpandFilter"] = handle_reference_navigation_property_expand_filter

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ensure_stable_ordering = d.pop("EnsureStableOrdering", UNSET)

        _handle_null_propagation = d.pop("HandleNullPropagation", UNSET)
        handle_null_propagation: Union[Unset, MicrosoftAspNetODataQueryODataQuerySettingsHandleNullPropagation]
        if isinstance(_handle_null_propagation,  Unset):
            handle_null_propagation = UNSET
        else:
            handle_null_propagation = MicrosoftAspNetODataQueryODataQuerySettingsHandleNullPropagation(_handle_null_propagation)




        enable_constant_parameterization = d.pop("EnableConstantParameterization", UNSET)

        enable_correlated_subquery_buffering = d.pop("EnableCorrelatedSubqueryBuffering", UNSET)

        page_size = d.pop("PageSize", UNSET)

        handle_reference_navigation_property_expand_filter = d.pop("HandleReferenceNavigationPropertyExpandFilter", UNSET)

        microsoft_asp_net_o_data_query_o_data_query_settings = cls(
            ensure_stable_ordering=ensure_stable_ordering,
            handle_null_propagation=handle_null_propagation,
            enable_constant_parameterization=enable_constant_parameterization,
            enable_correlated_subquery_buffering=enable_correlated_subquery_buffering,
            page_size=page_size,
            handle_reference_navigation_property_expand_filter=handle_reference_navigation_property_expand_filter,
        )


        microsoft_asp_net_o_data_query_o_data_query_settings.additional_properties = d
        return microsoft_asp_net_o_data_query_o_data_query_settings

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
