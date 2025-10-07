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
  from ..models.virinco_wats_web_dashboard_models_mes_tag import VirincoWATSWebDashboardModelsMesTag





T = TypeVar("T", bound="VirincoWATSWebDashboardControllersApiTagsChanges")



@_attrs_define
class VirincoWATSWebDashboardControllersApiTagsChanges:
    """ 
        Attributes:
            upsert_tags (Union[Unset, list['VirincoWATSWebDashboardModelsMesTag']]):
            delete_ids (Union[Unset, list[UUID]]):
     """

    upsert_tags: Union[Unset, list['VirincoWATSWebDashboardModelsMesTag']] = UNSET
    delete_ids: Union[Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_tag import VirincoWATSWebDashboardModelsMesTag
        upsert_tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.upsert_tags, Unset):
            upsert_tags = []
            for upsert_tags_item_data in self.upsert_tags:
                upsert_tags_item = upsert_tags_item_data.to_dict()
                upsert_tags.append(upsert_tags_item)



        delete_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.delete_ids, Unset):
            delete_ids = []
            for delete_ids_item_data in self.delete_ids:
                delete_ids_item = str(delete_ids_item_data)
                delete_ids.append(delete_ids_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if upsert_tags is not UNSET:
            field_dict["upsertTags"] = upsert_tags
        if delete_ids is not UNSET:
            field_dict["deleteIds"] = delete_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_tag import VirincoWATSWebDashboardModelsMesTag
        d = dict(src_dict)
        upsert_tags = []
        _upsert_tags = d.pop("upsertTags", UNSET)
        for upsert_tags_item_data in (_upsert_tags or []):
            upsert_tags_item = VirincoWATSWebDashboardModelsMesTag.from_dict(upsert_tags_item_data)



            upsert_tags.append(upsert_tags_item)


        delete_ids = []
        _delete_ids = d.pop("deleteIds", UNSET)
        for delete_ids_item_data in (_delete_ids or []):
            delete_ids_item = UUID(delete_ids_item_data)



            delete_ids.append(delete_ids_item)


        virinco_wats_web_dashboard_controllers_api_tags_changes = cls(
            upsert_tags=upsert_tags,
            delete_ids=delete_ids,
        )


        virinco_wats_web_dashboard_controllers_api_tags_changes.additional_properties = d
        return virinco_wats_web_dashboard_controllers_api_tags_changes

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
