from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsUnitFlowUnitFlowUnit")



@_attrs_define
class VirincoWATSWebDashboardModelsUnitFlowUnitFlowUnit:
    """ 
        Attributes:
            source (Union[Unset, int]):
            target (Union[Unset, int]):
            unit_id (Union[Unset, int]):
            is_old (Union[Unset, bool]):
            is_last (Union[Unset, bool]):
            is_last_passed (Union[Unset, bool]):
            has_passed (Union[Unset, bool]):
            has_failed (Union[Unset, bool]):
            has_retest (Union[Unset, bool]):
            orders (Union[Unset, list[int]]):
            result_histories (Union[Unset, list[str]]):
     """

    source: Union[Unset, int] = UNSET
    target: Union[Unset, int] = UNSET
    unit_id: Union[Unset, int] = UNSET
    is_old: Union[Unset, bool] = UNSET
    is_last: Union[Unset, bool] = UNSET
    is_last_passed: Union[Unset, bool] = UNSET
    has_passed: Union[Unset, bool] = UNSET
    has_failed: Union[Unset, bool] = UNSET
    has_retest: Union[Unset, bool] = UNSET
    orders: Union[Unset, list[int]] = UNSET
    result_histories: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        source = self.source

        target = self.target

        unit_id = self.unit_id

        is_old = self.is_old

        is_last = self.is_last

        is_last_passed = self.is_last_passed

        has_passed = self.has_passed

        has_failed = self.has_failed

        has_retest = self.has_retest

        orders: Union[Unset, list[int]] = UNSET
        if not isinstance(self.orders, Unset):
            orders = self.orders



        result_histories: Union[Unset, list[str]] = UNSET
        if not isinstance(self.result_histories, Unset):
            result_histories = self.result_histories




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if source is not UNSET:
            field_dict["source"] = source
        if target is not UNSET:
            field_dict["target"] = target
        if unit_id is not UNSET:
            field_dict["unitId"] = unit_id
        if is_old is not UNSET:
            field_dict["isOld"] = is_old
        if is_last is not UNSET:
            field_dict["isLast"] = is_last
        if is_last_passed is not UNSET:
            field_dict["isLastPassed"] = is_last_passed
        if has_passed is not UNSET:
            field_dict["hasPassed"] = has_passed
        if has_failed is not UNSET:
            field_dict["hasFailed"] = has_failed
        if has_retest is not UNSET:
            field_dict["hasRetest"] = has_retest
        if orders is not UNSET:
            field_dict["orders"] = orders
        if result_histories is not UNSET:
            field_dict["resultHistories"] = result_histories

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = d.pop("source", UNSET)

        target = d.pop("target", UNSET)

        unit_id = d.pop("unitId", UNSET)

        is_old = d.pop("isOld", UNSET)

        is_last = d.pop("isLast", UNSET)

        is_last_passed = d.pop("isLastPassed", UNSET)

        has_passed = d.pop("hasPassed", UNSET)

        has_failed = d.pop("hasFailed", UNSET)

        has_retest = d.pop("hasRetest", UNSET)

        orders = cast(list[int], d.pop("orders", UNSET))


        result_histories = cast(list[str], d.pop("resultHistories", UNSET))


        virinco_wats_web_dashboard_models_unit_flow_unit_flow_unit = cls(
            source=source,
            target=target,
            unit_id=unit_id,
            is_old=is_old,
            is_last=is_last,
            is_last_passed=is_last_passed,
            has_passed=has_passed,
            has_failed=has_failed,
            has_retest=has_retest,
            orders=orders,
            result_histories=result_histories,
        )


        virinco_wats_web_dashboard_models_unit_flow_unit_flow_unit.additional_properties = d
        return virinco_wats_web_dashboard_models_unit_flow_unit_flow_unit

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
