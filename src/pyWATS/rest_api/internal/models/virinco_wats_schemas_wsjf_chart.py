from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_schemas_wsjf_chart_series import VirincoWATSSchemasWSJFChartSeries





T = TypeVar("T", bound="VirincoWATSSchemasWSJFChart")



@_attrs_define
class VirincoWATSSchemasWSJFChart:
    """ 
        Attributes:
            chart_type (Union[Unset, str]): Type of chart, valid values:
            label (Union[Unset, str]): Chart label.
            x_label (Union[Unset, str]): X-axis label.
            x_unit (Union[Unset, str]): X-axis unit.
            y_label (Union[Unset, str]): Y-axis label.
            y_unit (Union[Unset, str]): Y-axis unit.
            series (Union[Unset, list['VirincoWATSSchemasWSJFChartSeries']]): List of chart series.
     """

    chart_type: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    x_label: Union[Unset, str] = UNSET
    x_unit: Union[Unset, str] = UNSET
    y_label: Union[Unset, str] = UNSET
    y_unit: Union[Unset, str] = UNSET
    series: Union[Unset, list['VirincoWATSSchemasWSJFChartSeries']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_schemas_wsjf_chart_series import VirincoWATSSchemasWSJFChartSeries
        chart_type = self.chart_type

        label = self.label

        x_label = self.x_label

        x_unit = self.x_unit

        y_label = self.y_label

        y_unit = self.y_unit

        series: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.series, Unset):
            series = []
            for series_item_data in self.series:
                series_item = series_item_data.to_dict()
                series.append(series_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if chart_type is not UNSET:
            field_dict["chartType"] = chart_type
        if label is not UNSET:
            field_dict["label"] = label
        if x_label is not UNSET:
            field_dict["xLabel"] = x_label
        if x_unit is not UNSET:
            field_dict["xUnit"] = x_unit
        if y_label is not UNSET:
            field_dict["yLabel"] = y_label
        if y_unit is not UNSET:
            field_dict["yUnit"] = y_unit
        if series is not UNSET:
            field_dict["series"] = series

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_schemas_wsjf_chart_series import VirincoWATSSchemasWSJFChartSeries
        d = dict(src_dict)
        chart_type = d.pop("chartType", UNSET)

        label = d.pop("label", UNSET)

        x_label = d.pop("xLabel", UNSET)

        x_unit = d.pop("xUnit", UNSET)

        y_label = d.pop("yLabel", UNSET)

        y_unit = d.pop("yUnit", UNSET)

        series = []
        _series = d.pop("series", UNSET)
        for series_item_data in (_series or []):
            series_item = VirincoWATSSchemasWSJFChartSeries.from_dict(series_item_data)



            series.append(series_item)


        virinco_wats_schemas_wsjf_chart = cls(
            chart_type=chart_type,
            label=label,
            x_label=x_label,
            x_unit=x_unit,
            y_label=y_label,
            y_unit=y_unit,
            series=series,
        )


        virinco_wats_schemas_wsjf_chart.additional_properties = d
        return virinco_wats_schemas_wsjf_chart

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
