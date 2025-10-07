from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation_entry_level import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryLevel
from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation_entry_key_values import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryKeyValues





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntry")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntry:
    """ 
        Attributes:
            level (Union[Unset, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryLevel]):
            description (Union[Unset, str]):
            id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            key_values (Union[Unset,
                VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryKeyValues]):
     """

    level: Union[Unset, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryLevel] = UNSET
    description: Union[Unset, str] = UNSET
    id: Union[Unset, UUID] = UNSET
    key_values: Union[Unset, 'VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryKeyValues'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation_entry_key_values import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryKeyValues
        level: Union[Unset, int] = UNSET
        if not isinstance(self.level, Unset):
            level = self.level.value


        description = self.description

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        key_values: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.key_values, Unset):
            key_values = self.key_values.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if level is not UNSET:
            field_dict["level"] = level
        if description is not UNSET:
            field_dict["description"] = description
        if id is not UNSET:
            field_dict["id"] = id
        if key_values is not UNSET:
            field_dict["keyValues"] = key_values

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation_entry_key_values import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryKeyValues
        d = dict(src_dict)
        _level = d.pop("level", UNSET)
        level: Union[Unset, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryLevel]
        if isinstance(_level,  Unset):
            level = UNSET
        else:
            level = VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryLevel(_level)




        description = d.pop("description", UNSET)

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        _key_values = d.pop("keyValues", UNSET)
        key_values: Union[Unset, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryKeyValues]
        if isinstance(_key_values,  Unset):
            key_values = UNSET
        else:
            key_values = VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntryKeyValues.from_dict(_key_values)




        virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation_entry = cls(
            level=level,
            description=description,
            id=id,
            key_values=key_values,
        )


        virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation_entry.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation_entry

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
