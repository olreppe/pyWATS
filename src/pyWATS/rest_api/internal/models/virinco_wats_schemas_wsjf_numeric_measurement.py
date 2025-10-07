from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSSchemasWSJFNumericMeasurement")



@_attrs_define
class VirincoWATSSchemasWSJFNumericMeasurement:
    """ 
        Attributes:
            comp_op (Union[Unset, str]): Comparison operator, valid values:
                LOG,EQ,NE,GT,GE,LT,LE,GTLT,GTLE,GELT,GELE,LTGT,LTGE,LEGT,LEGE
            name (Union[Unset, str]): Name of measurement (required if multiple measurements in same step).
            status (Union[Unset, str]): Status of measurement, valid values: P,F,S (Passed, Failed, Skipped).
            unit (Union[Unset, str]): Unit of measurement.
            value (Union[Unset, float]): Value measured.
            value_format (Union[Unset, str]): Numeric format of value.
            high_limit (Union[Unset, float]): High limit, used in dual comparisons.
            high_limit_format (Union[Unset, str]): Numeric format of high limit.
            low_limit (Union[Unset, float]): Low limit, used also as limit if not dual comparison.
            low_limit_format (Union[Unset, str]): Numeric format of low limit.
     """

    comp_op: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    value: Union[Unset, float] = UNSET
    value_format: Union[Unset, str] = UNSET
    high_limit: Union[Unset, float] = UNSET
    high_limit_format: Union[Unset, str] = UNSET
    low_limit: Union[Unset, float] = UNSET
    low_limit_format: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        comp_op = self.comp_op

        name = self.name

        status = self.status

        unit = self.unit

        value = self.value

        value_format = self.value_format

        high_limit = self.high_limit

        high_limit_format = self.high_limit_format

        low_limit = self.low_limit

        low_limit_format = self.low_limit_format


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if comp_op is not UNSET:
            field_dict["compOp"] = comp_op
        if name is not UNSET:
            field_dict["name"] = name
        if status is not UNSET:
            field_dict["status"] = status
        if unit is not UNSET:
            field_dict["unit"] = unit
        if value is not UNSET:
            field_dict["value"] = value
        if value_format is not UNSET:
            field_dict["valueFormat"] = value_format
        if high_limit is not UNSET:
            field_dict["highLimit"] = high_limit
        if high_limit_format is not UNSET:
            field_dict["highLimitFormat"] = high_limit_format
        if low_limit is not UNSET:
            field_dict["lowLimit"] = low_limit
        if low_limit_format is not UNSET:
            field_dict["lowLimitFormat"] = low_limit_format

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        comp_op = d.pop("compOp", UNSET)

        name = d.pop("name", UNSET)

        status = d.pop("status", UNSET)

        unit = d.pop("unit", UNSET)

        value = d.pop("value", UNSET)

        value_format = d.pop("valueFormat", UNSET)

        high_limit = d.pop("highLimit", UNSET)

        high_limit_format = d.pop("highLimitFormat", UNSET)

        low_limit = d.pop("lowLimit", UNSET)

        low_limit_format = d.pop("lowLimitFormat", UNSET)

        virinco_wats_schemas_wsjf_numeric_measurement = cls(
            comp_op=comp_op,
            name=name,
            status=status,
            unit=unit,
            value=value,
            value_format=value_format,
            high_limit=high_limit,
            high_limit_format=high_limit_format,
            low_limit=low_limit,
            low_limit_format=low_limit_format,
        )


        virinco_wats_schemas_wsjf_numeric_measurement.additional_properties = d
        return virinco_wats_schemas_wsjf_numeric_measurement

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
