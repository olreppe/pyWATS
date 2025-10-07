from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_interface_models_failcode import VirincoWATSInterfaceModelsFailcode
  from ..models.virinco_wats_interface_models_misc_info import VirincoWATSInterfaceModelsMiscInfo





T = TypeVar("T", bound="VirincoWATSInterfaceModelsRepairType")



@_attrs_define
class VirincoWATSInterfaceModelsRepairType:
    """ 
        Attributes:
            description (Union[Unset, str]):
            uut_required (Union[Unset, int]):
            comp_ref_mask (Union[Unset, str]):
            comp_ref_mask_description (Union[Unset, str]):
            bom_constraint (Union[Unset, str]):
            bom_required (Union[Unset, int]):
            vendor_required (Union[Unset, int]):
            categories (Union[Unset, list['VirincoWATSInterfaceModelsFailcode']]):
            misc_infos (Union[Unset, list['VirincoWATSInterfaceModelsMiscInfo']]):
     """

    description: Union[Unset, str] = UNSET
    uut_required: Union[Unset, int] = UNSET
    comp_ref_mask: Union[Unset, str] = UNSET
    comp_ref_mask_description: Union[Unset, str] = UNSET
    bom_constraint: Union[Unset, str] = UNSET
    bom_required: Union[Unset, int] = UNSET
    vendor_required: Union[Unset, int] = UNSET
    categories: Union[Unset, list['VirincoWATSInterfaceModelsFailcode']] = UNSET
    misc_infos: Union[Unset, list['VirincoWATSInterfaceModelsMiscInfo']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_interface_models_failcode import VirincoWATSInterfaceModelsFailcode
        from ..models.virinco_wats_interface_models_misc_info import VirincoWATSInterfaceModelsMiscInfo
        description = self.description

        uut_required = self.uut_required

        comp_ref_mask = self.comp_ref_mask

        comp_ref_mask_description = self.comp_ref_mask_description

        bom_constraint = self.bom_constraint

        bom_required = self.bom_required

        vendor_required = self.vendor_required

        categories: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)



        misc_infos: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.misc_infos, Unset):
            misc_infos = []
            for misc_infos_item_data in self.misc_infos:
                misc_infos_item = misc_infos_item_data.to_dict()
                misc_infos.append(misc_infos_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if description is not UNSET:
            field_dict["Description"] = description
        if uut_required is not UNSET:
            field_dict["UUTRequired"] = uut_required
        if comp_ref_mask is not UNSET:
            field_dict["CompRefMask"] = comp_ref_mask
        if comp_ref_mask_description is not UNSET:
            field_dict["CompRefMaskDescription"] = comp_ref_mask_description
        if bom_constraint is not UNSET:
            field_dict["BomConstraint"] = bom_constraint
        if bom_required is not UNSET:
            field_dict["BOMRequired"] = bom_required
        if vendor_required is not UNSET:
            field_dict["VendorRequired"] = vendor_required
        if categories is not UNSET:
            field_dict["Categories"] = categories
        if misc_infos is not UNSET:
            field_dict["MiscInfos"] = misc_infos

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_interface_models_failcode import VirincoWATSInterfaceModelsFailcode
        from ..models.virinco_wats_interface_models_misc_info import VirincoWATSInterfaceModelsMiscInfo
        d = dict(src_dict)
        description = d.pop("Description", UNSET)

        uut_required = d.pop("UUTRequired", UNSET)

        comp_ref_mask = d.pop("CompRefMask", UNSET)

        comp_ref_mask_description = d.pop("CompRefMaskDescription", UNSET)

        bom_constraint = d.pop("BomConstraint", UNSET)

        bom_required = d.pop("BOMRequired", UNSET)

        vendor_required = d.pop("VendorRequired", UNSET)

        categories = []
        _categories = d.pop("Categories", UNSET)
        for categories_item_data in (_categories or []):
            categories_item = VirincoWATSInterfaceModelsFailcode.from_dict(categories_item_data)



            categories.append(categories_item)


        misc_infos = []
        _misc_infos = d.pop("MiscInfos", UNSET)
        for misc_infos_item_data in (_misc_infos or []):
            misc_infos_item = VirincoWATSInterfaceModelsMiscInfo.from_dict(misc_infos_item_data)



            misc_infos.append(misc_infos_item)


        virinco_wats_interface_models_repair_type = cls(
            description=description,
            uut_required=uut_required,
            comp_ref_mask=comp_ref_mask,
            comp_ref_mask_description=comp_ref_mask_description,
            bom_constraint=bom_constraint,
            bom_required=bom_required,
            vendor_required=vendor_required,
            categories=categories,
            misc_infos=misc_infos,
        )


        virinco_wats_interface_models_repair_type.additional_properties = d
        return virinco_wats_interface_models_repair_type

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
