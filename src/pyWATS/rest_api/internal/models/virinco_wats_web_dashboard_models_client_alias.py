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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsClientAlias")



@_attrs_define
class VirincoWATSWebDashboardModelsClientAlias:
    """ 
        Attributes:
            client_id (Union[Unset, int]):
            station_id (Union[Unset, int]):
            first_seen (Union[Unset, datetime.datetime]):
            name (Union[Unset, str]):
            location (Union[Unset, str]):
            purpose (Union[Unset, str]):
     """

    client_id: Union[Unset, int] = UNSET
    station_id: Union[Unset, int] = UNSET
    first_seen: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        station_id = self.station_id

        first_seen: Union[Unset, str] = UNSET
        if not isinstance(self.first_seen, Unset):
            first_seen = self.first_seen.isoformat()

        name = self.name

        location = self.location

        purpose = self.purpose


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if client_id is not UNSET:
            field_dict["clientId"] = client_id
        if station_id is not UNSET:
            field_dict["stationId"] = station_id
        if first_seen is not UNSET:
            field_dict["firstSeen"] = first_seen
        if name is not UNSET:
            field_dict["name"] = name
        if location is not UNSET:
            field_dict["location"] = location
        if purpose is not UNSET:
            field_dict["purpose"] = purpose

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_id = d.pop("clientId", UNSET)

        station_id = d.pop("stationId", UNSET)

        _first_seen = d.pop("firstSeen", UNSET)
        first_seen: Union[Unset, datetime.datetime]
        if isinstance(_first_seen,  Unset):
            first_seen = UNSET
        else:
            first_seen = isoparse(_first_seen)




        name = d.pop("name", UNSET)

        location = d.pop("location", UNSET)

        purpose = d.pop("purpose", UNSET)

        virinco_wats_web_dashboard_models_client_alias = cls(
            client_id=client_id,
            station_id=station_id,
            first_seen=first_seen,
            name=name,
            location=location,
            purpose=purpose,
        )


        virinco_wats_web_dashboard_models_client_alias.additional_properties = d
        return virinco_wats_web_dashboard_models_client_alias

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
