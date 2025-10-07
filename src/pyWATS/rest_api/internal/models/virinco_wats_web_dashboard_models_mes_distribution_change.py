from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesDistributionChange")



@_attrs_define
class VirincoWATSWebDashboardModelsMesDistributionChange:
    """ 
        Attributes:
            site_code (Union[Unset, str]):
            entity (Union[Unset, str]):
            entity_id (Union[Unset, str]):
            column_id (Union[Unset, int]):
            action (Union[Unset, str]):
            created (Union[Unset, datetime.datetime]):
            updated (Union[Unset, datetime.datetime]):
            tstamp (Union[Unset, str]):
     """

    site_code: Union[Unset, str] = UNSET
    entity: Union[Unset, str] = UNSET
    entity_id: Union[Unset, str] = UNSET
    column_id: Union[Unset, int] = UNSET
    action: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    tstamp: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        site_code = self.site_code

        entity = self.entity

        entity_id = self.entity_id

        column_id = self.column_id

        action = self.action

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        tstamp = self.tstamp


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if site_code is not UNSET:
            field_dict["SiteCode"] = site_code
        if entity is not UNSET:
            field_dict["Entity"] = entity
        if entity_id is not UNSET:
            field_dict["EntityId"] = entity_id
        if column_id is not UNSET:
            field_dict["ColumnId"] = column_id
        if action is not UNSET:
            field_dict["Action"] = action
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated
        if tstamp is not UNSET:
            field_dict["tstamp"] = tstamp

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        site_code = d.pop("SiteCode", UNSET)

        entity = d.pop("Entity", UNSET)

        entity_id = d.pop("EntityId", UNSET)

        column_id = d.pop("ColumnId", UNSET)

        action = d.pop("Action", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created,  Unset):
            created = UNSET
        else:
            created = isoparse(_created)




        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated,  Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)




        tstamp = d.pop("tstamp", UNSET)

        virinco_wats_web_dashboard_models_mes_distribution_change = cls(
            site_code=site_code,
            entity=entity,
            entity_id=entity_id,
            column_id=column_id,
            action=action,
            created=created,
            updated=updated,
            tstamp=tstamp,
        )


        virinco_wats_web_dashboard_models_mes_distribution_change.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_distribution_change

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
