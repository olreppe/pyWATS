from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter
  from ..models.virinco_wats_web_dashboard_models_tdm_kpi_target_request import VirincoWATSWebDashboardModelsTdmKpiTargetRequest





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmKpiTargetRequestBody")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmKpiTargetRequestBody:
    """ 
        Attributes:
            wats_filter (Union[Unset, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter]): Wats filter exposed in
                rest API
            kpi_target_requests (Union[Unset, list['VirincoWATSWebDashboardModelsTdmKpiTargetRequest']]):
     """

    wats_filter: Union[Unset, 'VirincoWATSWebDashboardControllersApiAppPublicWatsFilter'] = UNSET
    kpi_target_requests: Union[Unset, list['VirincoWATSWebDashboardModelsTdmKpiTargetRequest']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter
        from ..models.virinco_wats_web_dashboard_models_tdm_kpi_target_request import VirincoWATSWebDashboardModelsTdmKpiTargetRequest
        wats_filter: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.wats_filter, Unset):
            wats_filter = self.wats_filter.to_dict()

        kpi_target_requests: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.kpi_target_requests, Unset):
            kpi_target_requests = []
            for kpi_target_requests_item_data in self.kpi_target_requests:
                kpi_target_requests_item = kpi_target_requests_item_data.to_dict()
                kpi_target_requests.append(kpi_target_requests_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if wats_filter is not UNSET:
            field_dict["watsFilter"] = wats_filter
        if kpi_target_requests is not UNSET:
            field_dict["kpiTargetRequests"] = kpi_target_requests

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter
        from ..models.virinco_wats_web_dashboard_models_tdm_kpi_target_request import VirincoWATSWebDashboardModelsTdmKpiTargetRequest
        d = dict(src_dict)
        _wats_filter = d.pop("watsFilter", UNSET)
        wats_filter: Union[Unset, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter]
        if isinstance(_wats_filter,  Unset):
            wats_filter = UNSET
        else:
            wats_filter = VirincoWATSWebDashboardControllersApiAppPublicWatsFilter.from_dict(_wats_filter)




        kpi_target_requests = []
        _kpi_target_requests = d.pop("kpiTargetRequests", UNSET)
        for kpi_target_requests_item_data in (_kpi_target_requests or []):
            kpi_target_requests_item = VirincoWATSWebDashboardModelsTdmKpiTargetRequest.from_dict(kpi_target_requests_item_data)



            kpi_target_requests.append(kpi_target_requests_item)


        virinco_wats_web_dashboard_models_tdm_kpi_target_request_body = cls(
            wats_filter=wats_filter,
            kpi_target_requests=kpi_target_requests,
        )


        virinco_wats_web_dashboard_models_tdm_kpi_target_request_body.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_kpi_target_request_body

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
