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
  from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
  from ..models.virinco_wats_web_dashboard_models_mes_product_product_category import VirincoWATSWebDashboardModelsMesProductProductCategory
  from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision import VirincoWATSWebDashboardModelsMesProductProductRevision





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductProduct")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductProduct:
    """ 
        Attributes:
            product_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            non_serial (Union[Unset, bool]):
            part_number (Union[Unset, str]):
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            state (Union[Unset, int]):
            product_category_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            product_revisions (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductProductRevision']]):
            product_category (Union[Unset, VirincoWATSWebDashboardModelsMesProductProductCategory]):
            settings (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']]):
            category (Union[Unset, str]):
     """

    product_id: Union[Unset, UUID] = UNSET
    non_serial: Union[Unset, bool] = UNSET
    part_number: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    state: Union[Unset, int] = UNSET
    product_category_id: Union[Unset, UUID] = UNSET
    product_revisions: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductProductRevision']] = UNSET
    product_category: Union[Unset, 'VirincoWATSWebDashboardModelsMesProductProductCategory'] = UNSET
    settings: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']] = UNSET
    category: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_web_dashboard_models_mes_product_product_category import VirincoWATSWebDashboardModelsMesProductProductCategory
        from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision import VirincoWATSWebDashboardModelsMesProductProductRevision
        product_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_id, Unset):
            product_id = str(self.product_id)

        non_serial = self.non_serial

        part_number = self.part_number

        name = self.name

        description = self.description

        state = self.state

        product_category_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_category_id, Unset):
            product_category_id = str(self.product_category_id)

        product_revisions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.product_revisions, Unset):
            product_revisions = []
            for product_revisions_item_data in self.product_revisions:
                product_revisions_item = product_revisions_item_data.to_dict()
                product_revisions.append(product_revisions_item)



        product_category: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.product_category, Unset):
            product_category = self.product_category.to_dict()

        settings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = []
            for settings_item_data in self.settings:
                settings_item = settings_item_data.to_dict()
                settings.append(settings_item)



        category = self.category


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if product_id is not UNSET:
            field_dict["ProductId"] = product_id
        if non_serial is not UNSET:
            field_dict["NonSerial"] = non_serial
        if part_number is not UNSET:
            field_dict["PartNumber"] = part_number
        if name is not UNSET:
            field_dict["Name"] = name
        if description is not UNSET:
            field_dict["Description"] = description
        if state is not UNSET:
            field_dict["State"] = state
        if product_category_id is not UNSET:
            field_dict["ProductCategoryId"] = product_category_id
        if product_revisions is not UNSET:
            field_dict["ProductRevisions"] = product_revisions
        if product_category is not UNSET:
            field_dict["ProductCategory"] = product_category
        if settings is not UNSET:
            field_dict["Settings"] = settings
        if category is not UNSET:
            field_dict["Category"] = category

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_web_dashboard_models_mes_product_product_category import VirincoWATSWebDashboardModelsMesProductProductCategory
        from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision import VirincoWATSWebDashboardModelsMesProductProductRevision
        d = dict(src_dict)
        _product_id = d.pop("ProductId", UNSET)
        product_id: Union[Unset, UUID]
        if isinstance(_product_id,  Unset):
            product_id = UNSET
        else:
            product_id = UUID(_product_id)




        non_serial = d.pop("NonSerial", UNSET)

        part_number = d.pop("PartNumber", UNSET)

        name = d.pop("Name", UNSET)

        description = d.pop("Description", UNSET)

        state = d.pop("State", UNSET)

        _product_category_id = d.pop("ProductCategoryId", UNSET)
        product_category_id: Union[Unset, UUID]
        if isinstance(_product_category_id,  Unset):
            product_category_id = UNSET
        else:
            product_category_id = UUID(_product_category_id)




        product_revisions = []
        _product_revisions = d.pop("ProductRevisions", UNSET)
        for product_revisions_item_data in (_product_revisions or []):
            product_revisions_item = VirincoWATSWebDashboardModelsMesProductProductRevision.from_dict(product_revisions_item_data)



            product_revisions.append(product_revisions_item)


        _product_category = d.pop("ProductCategory", UNSET)
        product_category: Union[Unset, VirincoWATSWebDashboardModelsMesProductProductCategory]
        if isinstance(_product_category,  Unset):
            product_category = UNSET
        else:
            product_category = VirincoWATSWebDashboardModelsMesProductProductCategory.from_dict(_product_category)




        settings = []
        _settings = d.pop("Settings", UNSET)
        for settings_item_data in (_settings or []):
            settings_item = VirincoWATSWebDashboardModelsMesProductSetting.from_dict(settings_item_data)



            settings.append(settings_item)


        category = d.pop("Category", UNSET)

        virinco_wats_web_dashboard_models_mes_product_product = cls(
            product_id=product_id,
            non_serial=non_serial,
            part_number=part_number,
            name=name,
            description=description,
            state=state,
            product_category_id=product_category_id,
            product_revisions=product_revisions,
            product_category=product_category,
            settings=settings,
            category=category,
        )


        virinco_wats_web_dashboard_models_mes_product_product.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_product_product

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
