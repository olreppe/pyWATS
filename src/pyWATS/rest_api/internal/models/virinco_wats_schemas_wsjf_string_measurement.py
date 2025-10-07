from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSSchemasWSJFStringMeasurement")



@_attrs_define
class VirincoWATSSchemasWSJFStringMeasurement:
    """ 
        Attributes:
            comp_op (Union[Unset, str]): Comparison operator, valid values: LOG,EQ,NE,IGNORECAS,CASESENIT
            name (Union[Unset, str]): Name of measurement (required if multiple measurements in same step).
            status (Union[Unset, str]): Status of measurement, valid values: P,F,S (Passed, Failed, Skipped).
            value (Union[Unset, str]): Measured value.
            limit (Union[Unset, str]): String to compare against.
     """

    comp_op: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    limit: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        comp_op = self.comp_op

        name = self.name

        status = self.status

        value = self.value

        limit = self.limit


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
        if value is not UNSET:
            field_dict["value"] = value
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        comp_op = d.pop("compOp", UNSET)

        name = d.pop("name", UNSET)

        status = d.pop("status", UNSET)

        value = d.pop("value", UNSET)

        limit = d.pop("limit", UNSET)

        virinco_wats_schemas_wsjf_string_measurement = cls(
            comp_op=comp_op,
            name=name,
            status=status,
            value=value,
            limit=limit,
        )


        virinco_wats_schemas_wsjf_string_measurement.additional_properties = d
        return virinco_wats_schemas_wsjf_string_measurement

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
