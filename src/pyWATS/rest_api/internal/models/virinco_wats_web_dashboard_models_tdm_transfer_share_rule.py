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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmTransferShareRule")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmTransferShareRule:
    """ 
        Attributes:
            id (Union[Unset, int]):
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            processed_last_24_hours (Union[Unset, int]):
            processed_this_year (Union[Unset, int]):
            processed_total (Union[Unset, int]):
            queued (Union[Unset, int]):
            errors (Union[Unset, int]):
            active (Union[Unset, bool]):
            status (Union[Unset, str]):
            url (Union[Unset, str]):
            token (Union[Unset, str]):
            filter_ (Union[Unset, str]):
            process_map (Union[Unset, str]):
            created_by (Union[Unset, str]):
            updated_utc (Union[Unset, datetime.datetime]):
            uut (Union[Unset, bool]):
            uur (Union[Unset, bool]):
     """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    processed_last_24_hours: Union[Unset, int] = UNSET
    processed_this_year: Union[Unset, int] = UNSET
    processed_total: Union[Unset, int] = UNSET
    queued: Union[Unset, int] = UNSET
    errors: Union[Unset, int] = UNSET
    active: Union[Unset, bool] = UNSET
    status: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    filter_: Union[Unset, str] = UNSET
    process_map: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_utc: Union[Unset, datetime.datetime] = UNSET
    uut: Union[Unset, bool] = UNSET
    uur: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        processed_last_24_hours = self.processed_last_24_hours

        processed_this_year = self.processed_this_year

        processed_total = self.processed_total

        queued = self.queued

        errors = self.errors

        active = self.active

        status = self.status

        url = self.url

        token = self.token

        filter_ = self.filter_

        process_map = self.process_map

        created_by = self.created_by

        updated_utc: Union[Unset, str] = UNSET
        if not isinstance(self.updated_utc, Unset):
            updated_utc = self.updated_utc.isoformat()

        uut = self.uut

        uur = self.uur


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if processed_last_24_hours is not UNSET:
            field_dict["processedLast24Hours"] = processed_last_24_hours
        if processed_this_year is not UNSET:
            field_dict["processedThisYear"] = processed_this_year
        if processed_total is not UNSET:
            field_dict["processedTotal"] = processed_total
        if queued is not UNSET:
            field_dict["queued"] = queued
        if errors is not UNSET:
            field_dict["errors"] = errors
        if active is not UNSET:
            field_dict["active"] = active
        if status is not UNSET:
            field_dict["status"] = status
        if url is not UNSET:
            field_dict["url"] = url
        if token is not UNSET:
            field_dict["token"] = token
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if process_map is not UNSET:
            field_dict["processMap"] = process_map
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if updated_utc is not UNSET:
            field_dict["updatedUtc"] = updated_utc
        if uut is not UNSET:
            field_dict["uut"] = uut
        if uur is not UNSET:
            field_dict["uur"] = uur

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        processed_last_24_hours = d.pop("processedLast24Hours", UNSET)

        processed_this_year = d.pop("processedThisYear", UNSET)

        processed_total = d.pop("processedTotal", UNSET)

        queued = d.pop("queued", UNSET)

        errors = d.pop("errors", UNSET)

        active = d.pop("active", UNSET)

        status = d.pop("status", UNSET)

        url = d.pop("url", UNSET)

        token = d.pop("token", UNSET)

        filter_ = d.pop("filter", UNSET)

        process_map = d.pop("processMap", UNSET)

        created_by = d.pop("createdBy", UNSET)

        _updated_utc = d.pop("updatedUtc", UNSET)
        updated_utc: Union[Unset, datetime.datetime]
        if isinstance(_updated_utc,  Unset):
            updated_utc = UNSET
        else:
            updated_utc = isoparse(_updated_utc)




        uut = d.pop("uut", UNSET)

        uur = d.pop("uur", UNSET)

        virinco_wats_web_dashboard_models_tdm_transfer_share_rule = cls(
            id=id,
            name=name,
            description=description,
            processed_last_24_hours=processed_last_24_hours,
            processed_this_year=processed_this_year,
            processed_total=processed_total,
            queued=queued,
            errors=errors,
            active=active,
            status=status,
            url=url,
            token=token,
            filter_=filter_,
            process_map=process_map,
            created_by=created_by,
            updated_utc=updated_utc,
            uut=uut,
            uur=uur,
        )


        virinco_wats_web_dashboard_models_tdm_transfer_share_rule.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_transfer_share_rule

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
