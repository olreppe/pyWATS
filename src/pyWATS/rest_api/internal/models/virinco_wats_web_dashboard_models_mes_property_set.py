from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_property_export_sequence_file import VirincoWATSWebDashboardModelsMesPropertyExportSequenceFile
  from ..models.virinco_wats_web_dashboard_models_mes_property import VirincoWATSWebDashboardModelsMesProperty





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesPropertySet")



@_attrs_define
class VirincoWATSWebDashboardModelsMesPropertySet:
    """ 
        Attributes:
            is_part_number_validation_enabled (Union[Unset, bool]):
            parent (Union[Unset, VirincoWATSWebDashboardModelsMesPropertyExportSequenceFile]): Model which represents either
                a software file or folder.
            part_number (Union[Unset, str]):
            properties (Union[Unset, list['VirincoWATSWebDashboardModelsMesProperty']]):
     """

    is_part_number_validation_enabled: Union[Unset, bool] = UNSET
    parent: Union[Unset, 'VirincoWATSWebDashboardModelsMesPropertyExportSequenceFile'] = UNSET
    part_number: Union[Unset, str] = UNSET
    properties: Union[Unset, list['VirincoWATSWebDashboardModelsMesProperty']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_property_export_sequence_file import VirincoWATSWebDashboardModelsMesPropertyExportSequenceFile
        from ..models.virinco_wats_web_dashboard_models_mes_property import VirincoWATSWebDashboardModelsMesProperty
        is_part_number_validation_enabled = self.is_part_number_validation_enabled

        parent: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parent, Unset):
            parent = self.parent.to_dict()

        part_number = self.part_number

        properties: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = []
            for properties_item_data in self.properties:
                properties_item = properties_item_data.to_dict()
                properties.append(properties_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if is_part_number_validation_enabled is not UNSET:
            field_dict["isPartNumberValidationEnabled"] = is_part_number_validation_enabled
        if parent is not UNSET:
            field_dict["parent"] = parent
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_property_export_sequence_file import VirincoWATSWebDashboardModelsMesPropertyExportSequenceFile
        from ..models.virinco_wats_web_dashboard_models_mes_property import VirincoWATSWebDashboardModelsMesProperty
        d = dict(src_dict)
        is_part_number_validation_enabled = d.pop("isPartNumberValidationEnabled", UNSET)

        _parent = d.pop("parent", UNSET)
        parent: Union[Unset, VirincoWATSWebDashboardModelsMesPropertyExportSequenceFile]
        if isinstance(_parent,  Unset):
            parent = UNSET
        else:
            parent = VirincoWATSWebDashboardModelsMesPropertyExportSequenceFile.from_dict(_parent)




        part_number = d.pop("partNumber", UNSET)

        properties = []
        _properties = d.pop("properties", UNSET)
        for properties_item_data in (_properties or []):
            properties_item = VirincoWATSWebDashboardModelsMesProperty.from_dict(properties_item_data)



            properties.append(properties_item)


        virinco_wats_web_dashboard_models_mes_property_set = cls(
            is_part_number_validation_enabled=is_part_number_validation_enabled,
            parent=parent,
            part_number=part_number,
            properties=properties,
        )


        virinco_wats_web_dashboard_models_mes_property_set.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_property_set

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
