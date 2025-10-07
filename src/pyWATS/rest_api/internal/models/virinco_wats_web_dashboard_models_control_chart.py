from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsControlChart")



@_attrs_define
class VirincoWATSWebDashboardModelsControlChart:
    """ 
        Attributes:
            i (Union[Unset, int]):
            v (Union[Unset, float]):
            ucl (Union[Unset, float]):
            lcl (Union[Unset, float]):
            ucl2 (Union[Unset, float]):
            lcl2 (Union[Unset, float]):
            ucl3 (Union[Unset, float]):
            lcl3 (Union[Unset, float]):
            ucl4 (Union[Unset, float]):
            lcl4 (Union[Unset, float]):
            cl (Union[Unset, float]):
            uc (Union[Unset, float]):
            lc (Union[Unset, float]):
            label (Union[Unset, str]):
     """

    i: Union[Unset, int] = UNSET
    v: Union[Unset, float] = UNSET
    ucl: Union[Unset, float] = UNSET
    lcl: Union[Unset, float] = UNSET
    ucl2: Union[Unset, float] = UNSET
    lcl2: Union[Unset, float] = UNSET
    ucl3: Union[Unset, float] = UNSET
    lcl3: Union[Unset, float] = UNSET
    ucl4: Union[Unset, float] = UNSET
    lcl4: Union[Unset, float] = UNSET
    cl: Union[Unset, float] = UNSET
    uc: Union[Unset, float] = UNSET
    lc: Union[Unset, float] = UNSET
    label: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        i = self.i

        v = self.v

        ucl = self.ucl

        lcl = self.lcl

        ucl2 = self.ucl2

        lcl2 = self.lcl2

        ucl3 = self.ucl3

        lcl3 = self.lcl3

        ucl4 = self.ucl4

        lcl4 = self.lcl4

        cl = self.cl

        uc = self.uc

        lc = self.lc

        label = self.label


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if i is not UNSET:
            field_dict["i"] = i
        if v is not UNSET:
            field_dict["v"] = v
        if ucl is not UNSET:
            field_dict["ucl"] = ucl
        if lcl is not UNSET:
            field_dict["lcl"] = lcl
        if ucl2 is not UNSET:
            field_dict["ucl2"] = ucl2
        if lcl2 is not UNSET:
            field_dict["lcl2"] = lcl2
        if ucl3 is not UNSET:
            field_dict["ucl3"] = ucl3
        if lcl3 is not UNSET:
            field_dict["lcl3"] = lcl3
        if ucl4 is not UNSET:
            field_dict["ucl4"] = ucl4
        if lcl4 is not UNSET:
            field_dict["lcl4"] = lcl4
        if cl is not UNSET:
            field_dict["cl"] = cl
        if uc is not UNSET:
            field_dict["uc"] = uc
        if lc is not UNSET:
            field_dict["lc"] = lc
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        i = d.pop("i", UNSET)

        v = d.pop("v", UNSET)

        ucl = d.pop("ucl", UNSET)

        lcl = d.pop("lcl", UNSET)

        ucl2 = d.pop("ucl2", UNSET)

        lcl2 = d.pop("lcl2", UNSET)

        ucl3 = d.pop("ucl3", UNSET)

        lcl3 = d.pop("lcl3", UNSET)

        ucl4 = d.pop("ucl4", UNSET)

        lcl4 = d.pop("lcl4", UNSET)

        cl = d.pop("cl", UNSET)

        uc = d.pop("uc", UNSET)

        lc = d.pop("lc", UNSET)

        label = d.pop("label", UNSET)

        virinco_wats_web_dashboard_models_control_chart = cls(
            i=i,
            v=v,
            ucl=ucl,
            lcl=lcl,
            ucl2=ucl2,
            lcl2=lcl2,
            ucl3=ucl3,
            lcl3=lcl3,
            ucl4=ucl4,
            lcl4=lcl4,
            cl=cl,
            uc=uc,
            lc=lc,
            label=label,
        )


        virinco_wats_web_dashboard_models_control_chart.additional_properties = d
        return virinco_wats_web_dashboard_models_control_chart

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
