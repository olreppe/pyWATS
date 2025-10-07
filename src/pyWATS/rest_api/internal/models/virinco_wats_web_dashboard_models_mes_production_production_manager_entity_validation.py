from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation_entry import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntry





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidation")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidation:
    """ 
        Attributes:
            description (Union[Unset, str]):
            entries (Union[Unset,
                list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntry']]):
     """

    description: Union[Unset, str] = UNSET
    entries: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntry']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation_entry import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntry
        description = self.description

        entries: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.entries, Unset):
            entries = []
            for entries_item_data in self.entries:
                entries_item = entries_item_data.to_dict()
                entries.append(entries_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if description is not UNSET:
            field_dict["description"] = description
        if entries is not UNSET:
            field_dict["entries"] = entries

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation_entry import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntry
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        entries = []
        _entries = d.pop("entries", UNSET)
        for entries_item_data in (_entries or []):
            entries_item = VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidationEntry.from_dict(entries_item_data)



            entries.append(entries_item)


        virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation = cls(
            description=description,
            entries=entries,
        )


        virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation

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
