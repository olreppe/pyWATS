from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction:
    """ 
        Attributes:
            id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            entity_type (Union[Unset, str]):
     """

    id: Union[Unset, UUID] = UNSET
    entity_type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        entity_type = self.entity_type


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if entity_type is not UNSET:
            field_dict["entityType"] = entity_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        entity_type = d.pop("entityType", UNSET)

        virinco_wats_web_dashboard_models_mes_production_production_manager_entity_modification_instruction = cls(
            id=id,
            entity_type=entity_type,
        )


        virinco_wats_web_dashboard_models_mes_production_production_manager_entity_modification_instruction.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_production_production_manager_entity_modification_instruction

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
