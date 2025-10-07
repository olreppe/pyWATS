from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsChartDataPoint")



@_attrs_define
class VirincoWATSWebDashboardModelsChartDataPoint:
    """ 
        Attributes:
            x (Union[Unset, float]):
            y (Union[Unset, float]):
            guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            step_order_number (Union[Unset, int]):
     """

    x: Union[Unset, float] = UNSET
    y: Union[Unset, float] = UNSET
    guid: Union[Unset, UUID] = UNSET
    step_order_number: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        x = self.x

        y = self.y

        guid: Union[Unset, str] = UNSET
        if not isinstance(self.guid, Unset):
            guid = str(self.guid)

        step_order_number = self.step_order_number


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if x is not UNSET:
            field_dict["x"] = x
        if y is not UNSET:
            field_dict["y"] = y
        if guid is not UNSET:
            field_dict["guid"] = guid
        if step_order_number is not UNSET:
            field_dict["stepOrderNumber"] = step_order_number

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        x = d.pop("x", UNSET)

        y = d.pop("y", UNSET)

        _guid = d.pop("guid", UNSET)
        guid: Union[Unset, UUID]
        if isinstance(_guid,  Unset):
            guid = UNSET
        else:
            guid = UUID(_guid)




        step_order_number = d.pop("stepOrderNumber", UNSET)

        virinco_wats_web_dashboard_models_chart_data_point = cls(
            x=x,
            y=y,
            guid=guid,
            step_order_number=step_order_number,
        )


        virinco_wats_web_dashboard_models_chart_data_point.additional_properties = d
        return virinco_wats_web_dashboard_models_chart_data_point

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
