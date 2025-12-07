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
  from ..models.virinco_wats_web_dashboard_models_mes_product_public_product_revision import VirincoWATSWebDashboardModelsMesProductPublicProductRevision
  from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductPublicProduct")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductPublicProduct:
    """ 
        Attributes:
            product_id (Union[Unset, UUID]): Product ID Example: 00000000-0000-0000-0000-000000000000.
            non_serial (Union[Unset, bool]): Flag indicating if the product can have units.
            part_number (Union[Unset, str]): Part number
            name (Union[Unset, str]): Product name/Part name
            description (Union[Unset, str]): Description
            state (Union[Unset, int]): State. Can be Active (1) or Inactive(0)
            xml_data (Union[Unset, str]): Xml document with root element Root, and sub-elements with user specified names
                and value attribute (key value pairs).
                For example:
                &lt;Root&gt;
                    &lt;Site Value="01" /&gt;
                    &lt;ChangedDate Value="2019-01-01 13:55:00"/&gt;
                &lt;/Root&gt;
                Root may also contain a WSBF (WATS Standard BOM Format) document
            product_category_id (Union[Unset, UUID]): ID of category this product belongs to Example:
                00000000-0000-0000-0000-000000000000.
            product_category_name (Union[Unset, str]):
            revisions (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductPublicProductRevision']]): List of
                revisions of this product
            tags (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']]): JSON formated xmlData
     """

    product_id: Union[Unset, UUID] = UNSET
    non_serial: Union[Unset, bool] = UNSET
    part_number: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    state: Union[Unset, int] = UNSET
    xml_data: Union[Unset, str] = UNSET
    product_category_id: Union[Unset, UUID] = UNSET
    product_category_name: Union[Unset, str] = UNSET
    revisions: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductPublicProductRevision']] = UNSET
    tags: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_product_public_product_revision import VirincoWATSWebDashboardModelsMesProductPublicProductRevision
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        product_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_id, Unset):
            product_id = str(self.product_id)

        non_serial = self.non_serial

        part_number = self.part_number

        name = self.name

        description = self.description

        state = self.state

        xml_data = self.xml_data

        product_category_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_category_id, Unset):
            product_category_id = str(self.product_category_id)

        product_category_name = self.product_category_name

        revisions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.revisions, Unset):
            revisions = []
            for revisions_item_data in self.revisions:
                revisions_item = revisions_item_data.to_dict()
                revisions.append(revisions_item)



        tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if product_id is not UNSET:
            field_dict["productId"] = product_id
        if non_serial is not UNSET:
            field_dict["nonSerial"] = non_serial
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if state is not UNSET:
            field_dict["state"] = state
        if xml_data is not UNSET:
            field_dict["xmlData"] = xml_data
        if product_category_id is not UNSET:
            field_dict["productCategoryId"] = product_category_id
        if product_category_name is not UNSET:
            field_dict["productCategoryName"] = product_category_name
        if revisions is not UNSET:
            field_dict["revisions"] = revisions
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_product_public_product_revision import VirincoWATSWebDashboardModelsMesProductPublicProductRevision
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        d = dict(src_dict)
        _product_id = d.pop("productId", UNSET)
        product_id: Union[Unset, UUID]
        if isinstance(_product_id, Unset) or _product_id is None or _product_id == "":
            product_id = UNSET
        else:
            product_id = UUID(_product_id)




        non_serial = d.pop("nonSerial", UNSET)

        part_number = d.pop("partNumber", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        state = d.pop("state", UNSET)

        xml_data = d.pop("xmlData", UNSET)

        _product_category_id = d.pop("productCategoryId", UNSET)
        product_category_id: Union[Unset, UUID]
        if isinstance(_product_category_id, Unset) or _product_category_id is None or _product_category_id == "":
            product_category_id = UNSET
        else:
            product_category_id = UUID(_product_category_id)




        product_category_name = d.pop("productCategoryName", UNSET)

        revisions = []
        _revisions = d.pop("revisions", UNSET)
        for revisions_item_data in (_revisions or []):
            revisions_item = VirincoWATSWebDashboardModelsMesProductPublicProductRevision.from_dict(revisions_item_data)



            revisions.append(revisions_item)


        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in (_tags or []):
            tags_item = VirincoWATSWebDashboardModelsMesProductSetting.from_dict(tags_item_data)



            tags.append(tags_item)


        virinco_wats_web_dashboard_models_mes_product_public_product = cls(
            product_id=product_id,
            non_serial=non_serial,
            part_number=part_number,
            name=name,
            description=description,
            state=state,
            xml_data=xml_data,
            product_category_id=product_category_id,
            product_category_name=product_category_name,
            revisions=revisions,
            tags=tags,
        )


        virinco_wats_web_dashboard_models_mes_product_public_product.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_product_public_product

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
