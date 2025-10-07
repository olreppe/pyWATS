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





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductPublicProductRevision")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductPublicProductRevision:
    """ 
        Attributes:
            product_revision_id (Union[Unset, UUID]): ID of this revision Example: 00000000-0000-0000-0000-000000000000.
            product_id (Union[Unset, UUID]): ID of the product this revision belongs to Example:
                00000000-0000-0000-0000-000000000000.
            revision (Union[Unset, str]): Revision name, for example revision number or revision version
            name (Union[Unset, str]): Human readable name of revision
            description (Union[Unset, str]): Revision description
            state (Union[Unset, int]): Revision state. Can be Active(1) or Inactive(0)
            xml_data (Union[Unset, str]): Xml document with root element Root, and sub-elements with user specified names
                and value attribute (key value pairs).
                For example:
                &lt;Root&gt;
                    &lt;Site Value="01" /&gt;
                    &lt;ChangedDate Value="2019-01-01 13:55:00"/&gt;
                &lt;/Root&gt;
                Root may also contain a WSBF (WATS Standard BOM Format) document
            part_number (Union[Unset, str]):
            tags (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']]): JSON formated xmlData
     """

    product_revision_id: Union[Unset, UUID] = UNSET
    product_id: Union[Unset, UUID] = UNSET
    revision: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    state: Union[Unset, int] = UNSET
    xml_data: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    tags: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        product_revision_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_revision_id, Unset):
            product_revision_id = str(self.product_revision_id)

        product_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_id, Unset):
            product_id = str(self.product_id)

        revision = self.revision

        name = self.name

        description = self.description

        state = self.state

        xml_data = self.xml_data

        part_number = self.part_number

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
        if product_revision_id is not UNSET:
            field_dict["productRevisionId"] = product_revision_id
        if product_id is not UNSET:
            field_dict["productId"] = product_id
        if revision is not UNSET:
            field_dict["revision"] = revision
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if state is not UNSET:
            field_dict["state"] = state
        if xml_data is not UNSET:
            field_dict["xmlData"] = xml_data
        if part_number is not UNSET:
            field_dict["PartNumber"] = part_number
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        d = dict(src_dict)
        _product_revision_id = d.pop("productRevisionId", UNSET)
        product_revision_id: Union[Unset, UUID]
        if isinstance(_product_revision_id,  Unset):
            product_revision_id = UNSET
        else:
            product_revision_id = UUID(_product_revision_id)




        _product_id = d.pop("productId", UNSET)
        product_id: Union[Unset, UUID]
        if isinstance(_product_id,  Unset):
            product_id = UNSET
        else:
            product_id = UUID(_product_id)




        revision = d.pop("revision", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        state = d.pop("state", UNSET)

        xml_data = d.pop("xmlData", UNSET)

        part_number = d.pop("PartNumber", UNSET)

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in (_tags or []):
            tags_item = VirincoWATSWebDashboardModelsMesProductSetting.from_dict(tags_item_data)



            tags.append(tags_item)


        virinco_wats_web_dashboard_models_mes_product_public_product_revision = cls(
            product_revision_id=product_revision_id,
            product_id=product_id,
            revision=revision,
            name=name,
            description=description,
            state=state,
            xml_data=xml_data,
            part_number=part_number,
            tags=tags,
        )


        virinco_wats_web_dashboard_models_mes_product_public_product_revision.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_product_public_product_revision

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
