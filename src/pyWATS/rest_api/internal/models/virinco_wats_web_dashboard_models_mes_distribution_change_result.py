from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesDistributionChangeResult")



@_attrs_define
class VirincoWATSWebDashboardModelsMesDistributionChangeResult:
    """ 
        Attributes:
            c (Union[Unset, str]):
            t (Union[Unset, str]):
            id (Union[Unset, str]):
            ts (Union[Unset, str]):
            r (Union[Unset, bool]):
            m (Union[Unset, str]):
     """

    c: Union[Unset, str] = UNSET
    t: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    ts: Union[Unset, str] = UNSET
    r: Union[Unset, bool] = UNSET
    m: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        c = self.c

        t = self.t

        id = self.id

        ts = self.ts

        r = self.r

        m = self.m


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if c is not UNSET:
            field_dict["c"] = c
        if t is not UNSET:
            field_dict["t"] = t
        if id is not UNSET:
            field_dict["id"] = id
        if ts is not UNSET:
            field_dict["ts"] = ts
        if r is not UNSET:
            field_dict["r"] = r
        if m is not UNSET:
            field_dict["m"] = m

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        c = d.pop("c", UNSET)

        t = d.pop("t", UNSET)

        id = d.pop("id", UNSET)

        ts = d.pop("ts", UNSET)

        r = d.pop("r", UNSET)

        m = d.pop("m", UNSET)

        virinco_wats_web_dashboard_models_mes_distribution_change_result = cls(
            c=c,
            t=t,
            id=id,
            ts=ts,
            r=r,
            m=m,
        )


        virinco_wats_web_dashboard_models_mes_distribution_change_result.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_distribution_change_result

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
