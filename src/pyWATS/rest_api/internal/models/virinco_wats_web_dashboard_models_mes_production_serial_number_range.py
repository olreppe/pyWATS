from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_production_serial_number_range_identifier import VirincoWATSWebDashboardModelsMesProductionSerialNumberRangeIdentifier
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductionSerialNumberRange")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductionSerialNumberRange:
    """ 
        Attributes:
            type_ (Union[Unset, str]):
            identifier (Union[Unset, VirincoWATSWebDashboardModelsMesProductionSerialNumberRangeIdentifier]):
            identifier_name (Union[Unset, str]):
            start_address (Union[Unset, str]):
            end_address (Union[Unset, str]):
            total (Union[Unset, int]):
            free (Union[Unset, int]):
            taken (Union[Unset, int]):
            reserved (Union[Unset, int]):
     """

    type_: Union[Unset, str] = UNSET
    identifier: Union[Unset, VirincoWATSWebDashboardModelsMesProductionSerialNumberRangeIdentifier] = UNSET
    identifier_name: Union[Unset, str] = UNSET
    start_address: Union[Unset, str] = UNSET
    end_address: Union[Unset, str] = UNSET
    total: Union[Unset, int] = UNSET
    free: Union[Unset, int] = UNSET
    taken: Union[Unset, int] = UNSET
    reserved: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        identifier: Union[Unset, int] = UNSET
        if not isinstance(self.identifier, Unset):
            identifier = self.identifier.value


        identifier_name = self.identifier_name

        start_address = self.start_address

        end_address = self.end_address

        total = self.total

        free = self.free

        taken = self.taken

        reserved = self.reserved


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["type"] = type_
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if identifier_name is not UNSET:
            field_dict["identifierName"] = identifier_name
        if start_address is not UNSET:
            field_dict["startAddress"] = start_address
        if end_address is not UNSET:
            field_dict["endAddress"] = end_address
        if total is not UNSET:
            field_dict["total"] = total
        if free is not UNSET:
            field_dict["free"] = free
        if taken is not UNSET:
            field_dict["taken"] = taken
        if reserved is not UNSET:
            field_dict["reserved"] = reserved

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        _identifier = d.pop("identifier", UNSET)
        identifier: Union[Unset, VirincoWATSWebDashboardModelsMesProductionSerialNumberRangeIdentifier]
        if isinstance(_identifier,  Unset):
            identifier = UNSET
        else:
            identifier = VirincoWATSWebDashboardModelsMesProductionSerialNumberRangeIdentifier(_identifier)




        identifier_name = d.pop("identifierName", UNSET)

        start_address = d.pop("startAddress", UNSET)

        end_address = d.pop("endAddress", UNSET)

        total = d.pop("total", UNSET)

        free = d.pop("free", UNSET)

        taken = d.pop("taken", UNSET)

        reserved = d.pop("reserved", UNSET)

        virinco_wats_web_dashboard_models_mes_production_serial_number_range = cls(
            type_=type_,
            identifier=identifier,
            identifier_name=identifier_name,
            start_address=start_address,
            end_address=end_address,
            total=total,
            free=free,
            taken=taken,
            reserved=reserved,
        )


        virinco_wats_web_dashboard_models_mes_production_serial_number_range.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_production_serial_number_range

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
