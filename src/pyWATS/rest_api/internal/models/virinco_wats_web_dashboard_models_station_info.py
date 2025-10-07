from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_configuration import VirincoWATSWebDashboardModelsMesConfiguration
  from ..models.virinco_wats_web_dashboard_models_station_configuration import VirincoWATSWebDashboardModelsStationConfiguration





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsStationInfo")



@_attrs_define
class VirincoWATSWebDashboardModelsStationInfo:
    """ 
        Attributes:
            name (Union[Unset, str]):
            location (Union[Unset, str]):
            purpose (Union[Unset, str]):
            processes (Union[Unset, list[str]]):
            mes (Union[Unset, VirincoWATSWebDashboardModelsMesConfiguration]):
            station (Union[Unset, VirincoWATSWebDashboardModelsStationConfiguration]):
     """

    name: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    processes: Union[Unset, list[str]] = UNSET
    mes: Union[Unset, 'VirincoWATSWebDashboardModelsMesConfiguration'] = UNSET
    station: Union[Unset, 'VirincoWATSWebDashboardModelsStationConfiguration'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_configuration import VirincoWATSWebDashboardModelsMesConfiguration
        from ..models.virinco_wats_web_dashboard_models_station_configuration import VirincoWATSWebDashboardModelsStationConfiguration
        name = self.name

        location = self.location

        purpose = self.purpose

        processes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.processes, Unset):
            processes = self.processes



        mes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.mes, Unset):
            mes = self.mes.to_dict()

        station: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.station, Unset):
            station = self.station.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["Name"] = name
        if location is not UNSET:
            field_dict["Location"] = location
        if purpose is not UNSET:
            field_dict["Purpose"] = purpose
        if processes is not UNSET:
            field_dict["Processes"] = processes
        if mes is not UNSET:
            field_dict["MES"] = mes
        if station is not UNSET:
            field_dict["Station"] = station

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_configuration import VirincoWATSWebDashboardModelsMesConfiguration
        from ..models.virinco_wats_web_dashboard_models_station_configuration import VirincoWATSWebDashboardModelsStationConfiguration
        d = dict(src_dict)
        name = d.pop("Name", UNSET)

        location = d.pop("Location", UNSET)

        purpose = d.pop("Purpose", UNSET)

        processes = cast(list[str], d.pop("Processes", UNSET))


        _mes = d.pop("MES", UNSET)
        mes: Union[Unset, VirincoWATSWebDashboardModelsMesConfiguration]
        if isinstance(_mes,  Unset):
            mes = UNSET
        else:
            mes = VirincoWATSWebDashboardModelsMesConfiguration.from_dict(_mes)




        _station = d.pop("Station", UNSET)
        station: Union[Unset, VirincoWATSWebDashboardModelsStationConfiguration]
        if isinstance(_station,  Unset):
            station = UNSET
        else:
            station = VirincoWATSWebDashboardModelsStationConfiguration.from_dict(_station)




        virinco_wats_web_dashboard_models_station_info = cls(
            name=name,
            location=location,
            purpose=purpose,
            processes=processes,
            mes=mes,
            station=station,
        )


        virinco_wats_web_dashboard_models_station_info.additional_properties = d
        return virinco_wats_web_dashboard_models_station_info

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
