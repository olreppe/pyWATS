from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_workflow_client_workflow_activity import VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivity
  from ..models.virinco_wats_web_dashboard_models_mes_workflow_client_workflow_request_settings import VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettings





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowClientRequest")



@_attrs_define
class VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowClientRequest:
    """ 
        Attributes:
            serial_number (Union[Unset, str]):
            part_number (Union[Unset, str]):
            station_name (Union[Unset, str]):
            operator_name (Union[Unset, str]):
            activity (Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivity]):
            settings (Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettings]):
     """

    serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    station_name: Union[Unset, str] = UNSET
    operator_name: Union[Unset, str] = UNSET
    activity: Union[Unset, 'VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivity'] = UNSET
    settings: Union[Unset, 'VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettings'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_client_workflow_activity import VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivity
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_client_workflow_request_settings import VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettings
        serial_number = self.serial_number

        part_number = self.part_number

        station_name = self.station_name

        operator_name = self.operator_name

        activity: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.activity, Unset):
            activity = self.activity.to_dict()

        settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if station_name is not UNSET:
            field_dict["stationName"] = station_name
        if operator_name is not UNSET:
            field_dict["operatorName"] = operator_name
        if activity is not UNSET:
            field_dict["activity"] = activity
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_client_workflow_activity import VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivity
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_client_workflow_request_settings import VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettings
        d = dict(src_dict)
        serial_number = d.pop("serialNumber", UNSET)

        part_number = d.pop("partNumber", UNSET)

        station_name = d.pop("stationName", UNSET)

        operator_name = d.pop("operatorName", UNSET)

        _activity = d.pop("activity", UNSET)
        activity: Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivity]
        if isinstance(_activity,  Unset):
            activity = UNSET
        else:
            activity = VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowActivity.from_dict(_activity)




        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettings]
        if isinstance(_settings,  Unset):
            settings = UNSET
        else:
            settings = VirincoWATSWebDashboardModelsMesWorkflowClientWorkflowRequestSettings.from_dict(_settings)




        virinco_wats_web_dashboard_models_mes_workflow_client_workflow_client_request = cls(
            serial_number=serial_number,
            part_number=part_number,
            station_name=station_name,
            operator_name=operator_name,
            activity=activity,
            settings=settings,
        )


        virinco_wats_web_dashboard_models_mes_workflow_client_workflow_client_request.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_workflow_client_workflow_client_request

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
