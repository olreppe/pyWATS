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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsApiUtilitiesPingResult")



@_attrs_define
class VirincoWATSWebDashboardModelsApiUtilitiesPingResult:
    """ 
        Attributes:
            server_name (Union[Unset, str]):
            server_time (Union[Unset, datetime.datetime]):
     """

    server_name: Union[Unset, str] = UNSET
    server_time: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        server_name = self.server_name

        server_time: Union[Unset, str] = UNSET
        if not isinstance(self.server_time, Unset):
            server_time = self.server_time.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if server_name is not UNSET:
            field_dict["ServerName"] = server_name
        if server_time is not UNSET:
            field_dict["ServerTime"] = server_time

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        server_name = d.pop("ServerName", UNSET)

        _server_time = d.pop("ServerTime", UNSET)
        server_time: Union[Unset, datetime.datetime]
        if isinstance(_server_time,  Unset):
            server_time = UNSET
        else:
            server_time = isoparse(_server_time)




        virinco_wats_web_dashboard_models_api_utilities_ping_result = cls(
            server_name=server_name,
            server_time=server_time,
        )


        virinco_wats_web_dashboard_models_api_utilities_ping_result.additional_properties = d
        return virinco_wats_web_dashboard_models_api_utilities_ping_result

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
