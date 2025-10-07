from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_controllers_api_alvea_controller_alvea_request_parameters import VirincoWATSWebDashboardControllersApiAlveaControllerAlveaRequestParameters
  from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter





T = TypeVar("T", bound="VirincoWATSWebDashboardControllersApiAlveaControllerAlveaRequest")



@_attrs_define
class VirincoWATSWebDashboardControllersApiAlveaControllerAlveaRequest:
    """ 
        Attributes:
            filter_ (Union[Unset, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter]): Wats filter exposed in rest
                API
            parameters (Union[Unset, VirincoWATSWebDashboardControllersApiAlveaControllerAlveaRequestParameters]):
     """

    filter_: Union[Unset, 'VirincoWATSWebDashboardControllersApiAppPublicWatsFilter'] = UNSET
    parameters: Union[Unset, 'VirincoWATSWebDashboardControllersApiAlveaControllerAlveaRequestParameters'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_controllers_api_alvea_controller_alvea_request_parameters import VirincoWATSWebDashboardControllersApiAlveaControllerAlveaRequestParameters
        from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter
        filter_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        parameters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_controllers_api_alvea_controller_alvea_request_parameters import VirincoWATSWebDashboardControllersApiAlveaControllerAlveaRequestParameters
        from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter
        d = dict(src_dict)
        _filter_ = d.pop("filter", UNSET)
        filter_: Union[Unset, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter]
        if isinstance(_filter_,  Unset):
            filter_ = UNSET
        else:
            filter_ = VirincoWATSWebDashboardControllersApiAppPublicWatsFilter.from_dict(_filter_)




        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, VirincoWATSWebDashboardControllersApiAlveaControllerAlveaRequestParameters]
        if isinstance(_parameters,  Unset):
            parameters = UNSET
        else:
            parameters = VirincoWATSWebDashboardControllersApiAlveaControllerAlveaRequestParameters.from_dict(_parameters)




        virinco_wats_web_dashboard_controllers_api_alvea_controller_alvea_request = cls(
            filter_=filter_,
            parameters=parameters,
        )


        virinco_wats_web_dashboard_controllers_api_alvea_controller_alvea_request.additional_properties = d
        return virinco_wats_web_dashboard_controllers_api_alvea_controller_alvea_request

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
