from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesUnitPhase")



@_attrs_define
class VirincoWATSWebDashboardModelsMesUnitPhase:
    """ 
        Attributes:
            unit_phase_id (Union[Unset, int]):
            code (Union[Unset, str]):
            name (Union[Unset, str]):
            description (Union[Unset, str]):
     """

    unit_phase_id: Union[Unset, int] = UNSET
    code: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        unit_phase_id = self.unit_phase_id

        code = self.code

        name = self.name

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if unit_phase_id is not UNSET:
            field_dict["UnitPhaseId"] = unit_phase_id
        if code is not UNSET:
            field_dict["Code"] = code
        if name is not UNSET:
            field_dict["Name"] = name
        if description is not UNSET:
            field_dict["Description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        unit_phase_id = d.pop("UnitPhaseId", UNSET)

        code = d.pop("Code", UNSET)

        name = d.pop("Name", UNSET)

        description = d.pop("Description", UNSET)

        virinco_wats_web_dashboard_models_mes_unit_phase = cls(
            unit_phase_id=unit_phase_id,
            code=code,
            name=name,
            description=description,
        )


        virinco_wats_web_dashboard_models_mes_unit_phase.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_unit_phase

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
