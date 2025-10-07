from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSSchemasWSJFChartSeries")



@_attrs_define
class VirincoWATSSchemasWSJFChartSeries:
    """ 
        Attributes:
            data_type (Union[Unset, str]): Data type of series, valid values: XYG.
            name (Union[Unset, str]): Name of series.
            xdata (Union[Unset, str]): Semicolon separated string of X-coordinates.
            ydata (Union[Unset, str]): Semicolon separated string of Y-coordinates.
     """

    data_type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    xdata: Union[Unset, str] = UNSET
    ydata: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        data_type = self.data_type

        name = self.name

        xdata = self.xdata

        ydata = self.ydata


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if data_type is not UNSET:
            field_dict["dataType"] = data_type
        if name is not UNSET:
            field_dict["name"] = name
        if xdata is not UNSET:
            field_dict["xdata"] = xdata
        if ydata is not UNSET:
            field_dict["ydata"] = ydata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data_type = d.pop("dataType", UNSET)

        name = d.pop("name", UNSET)

        xdata = d.pop("xdata", UNSET)

        ydata = d.pop("ydata", UNSET)

        virinco_wats_schemas_wsjf_chart_series = cls(
            data_type=data_type,
            name=name,
            xdata=xdata,
            ydata=ydata,
        )


        virinco_wats_schemas_wsjf_chart_series.additional_properties = d
        return virinco_wats_schemas_wsjf_chart_series

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
