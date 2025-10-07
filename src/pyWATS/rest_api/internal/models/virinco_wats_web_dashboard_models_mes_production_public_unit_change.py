from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductionPublicUnitChange")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductionPublicUnitChange:
    """ 
        Attributes:
            id (Union[Unset, int]):
            unit_serial_number (Union[Unset, str]):
            new_parent_serial_number (Union[Unset, str]):
            new_part_number (Union[Unset, str]):
            new_revision (Union[Unset, str]):
            new_unit_phase_id (Union[Unset, int]):
     """

    id: Union[Unset, int] = UNSET
    unit_serial_number: Union[Unset, str] = UNSET
    new_parent_serial_number: Union[Unset, str] = UNSET
    new_part_number: Union[Unset, str] = UNSET
    new_revision: Union[Unset, str] = UNSET
    new_unit_phase_id: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        unit_serial_number = self.unit_serial_number

        new_parent_serial_number = self.new_parent_serial_number

        new_part_number = self.new_part_number

        new_revision = self.new_revision

        new_unit_phase_id = self.new_unit_phase_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if unit_serial_number is not UNSET:
            field_dict["unitSerialNumber"] = unit_serial_number
        if new_parent_serial_number is not UNSET:
            field_dict["newParentSerialNumber"] = new_parent_serial_number
        if new_part_number is not UNSET:
            field_dict["newPartNumber"] = new_part_number
        if new_revision is not UNSET:
            field_dict["newRevision"] = new_revision
        if new_unit_phase_id is not UNSET:
            field_dict["newUnitPhaseId"] = new_unit_phase_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        unit_serial_number = d.pop("unitSerialNumber", UNSET)

        new_parent_serial_number = d.pop("newParentSerialNumber", UNSET)

        new_part_number = d.pop("newPartNumber", UNSET)

        new_revision = d.pop("newRevision", UNSET)

        new_unit_phase_id = d.pop("newUnitPhaseId", UNSET)

        virinco_wats_web_dashboard_models_mes_production_public_unit_change = cls(
            id=id,
            unit_serial_number=unit_serial_number,
            new_parent_serial_number=new_parent_serial_number,
            new_part_number=new_part_number,
            new_revision=new_revision,
            new_unit_phase_id=new_unit_phase_id,
        )


        virinco_wats_web_dashboard_models_mes_production_public_unit_change.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_production_public_unit_change

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
