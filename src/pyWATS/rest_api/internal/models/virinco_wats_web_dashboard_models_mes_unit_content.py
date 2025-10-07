from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_production_unit import VirincoWATSWebDashboardModelsMesProductionUnit





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesUnitContent")



@_attrs_define
class VirincoWATSWebDashboardModelsMesUnitContent:
    """ 
        Attributes:
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            product_name (Union[Unset, str]):
            revision_name (Union[Unset, str]):
            revision_mask (Union[Unset, str]):
            is_bom_loaded (Union[Unset, bool]):
            level (Union[Unset, int]):
            item_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            parent_item_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            children (Union[Unset, list['VirincoWATSWebDashboardModelsMesUnitContent']]):
            units (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductionUnit']]):
     """

    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    product_name: Union[Unset, str] = UNSET
    revision_name: Union[Unset, str] = UNSET
    revision_mask: Union[Unset, str] = UNSET
    is_bom_loaded: Union[Unset, bool] = UNSET
    level: Union[Unset, int] = UNSET
    item_id: Union[Unset, UUID] = UNSET
    parent_item_id: Union[Unset, UUID] = UNSET
    children: Union[Unset, list['VirincoWATSWebDashboardModelsMesUnitContent']] = UNSET
    units: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductionUnit']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_production_unit import VirincoWATSWebDashboardModelsMesProductionUnit
        part_number = self.part_number

        revision = self.revision

        product_name = self.product_name

        revision_name = self.revision_name

        revision_mask = self.revision_mask

        is_bom_loaded = self.is_bom_loaded

        level = self.level

        item_id: Union[Unset, str] = UNSET
        if not isinstance(self.item_id, Unset):
            item_id = str(self.item_id)

        parent_item_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_item_id, Unset):
            parent_item_id = str(self.parent_item_id)

        children: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()
                children.append(children_item)



        units: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.units, Unset):
            units = []
            for units_item_data in self.units:
                units_item = units_item_data.to_dict()
                units.append(units_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if part_number is not UNSET:
            field_dict["PartNumber"] = part_number
        if revision is not UNSET:
            field_dict["Revision"] = revision
        if product_name is not UNSET:
            field_dict["ProductName"] = product_name
        if revision_name is not UNSET:
            field_dict["RevisionName"] = revision_name
        if revision_mask is not UNSET:
            field_dict["RevisionMask"] = revision_mask
        if is_bom_loaded is not UNSET:
            field_dict["IsBOMLoaded"] = is_bom_loaded
        if level is not UNSET:
            field_dict["Level"] = level
        if item_id is not UNSET:
            field_dict["ItemId"] = item_id
        if parent_item_id is not UNSET:
            field_dict["ParentItemId"] = parent_item_id
        if children is not UNSET:
            field_dict["Children"] = children
        if units is not UNSET:
            field_dict["Units"] = units

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_production_unit import VirincoWATSWebDashboardModelsMesProductionUnit
        d = dict(src_dict)
        part_number = d.pop("PartNumber", UNSET)

        revision = d.pop("Revision", UNSET)

        product_name = d.pop("ProductName", UNSET)

        revision_name = d.pop("RevisionName", UNSET)

        revision_mask = d.pop("RevisionMask", UNSET)

        is_bom_loaded = d.pop("IsBOMLoaded", UNSET)

        level = d.pop("Level", UNSET)

        _item_id = d.pop("ItemId", UNSET)
        item_id: Union[Unset, UUID]
        if isinstance(_item_id,  Unset):
            item_id = UNSET
        else:
            item_id = UUID(_item_id)




        _parent_item_id = d.pop("ParentItemId", UNSET)
        parent_item_id: Union[Unset, UUID]
        if isinstance(_parent_item_id,  Unset):
            parent_item_id = UNSET
        else:
            parent_item_id = UUID(_parent_item_id)




        children = []
        _children = d.pop("Children", UNSET)
        for children_item_data in (_children or []):
            children_item = VirincoWATSWebDashboardModelsMesUnitContent.from_dict(children_item_data)



            children.append(children_item)


        units = []
        _units = d.pop("Units", UNSET)
        for units_item_data in (_units or []):
            units_item = VirincoWATSWebDashboardModelsMesProductionUnit.from_dict(units_item_data)



            units.append(units_item)


        virinco_wats_web_dashboard_models_mes_unit_content = cls(
            part_number=part_number,
            revision=revision,
            product_name=product_name,
            revision_name=revision_name,
            revision_mask=revision_mask,
            is_bom_loaded=is_bom_loaded,
            level=level,
            item_id=item_id,
            parent_item_id=parent_item_id,
            children=children,
            units=units,
        )


        virinco_wats_web_dashboard_models_mes_unit_content.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_unit_content

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
