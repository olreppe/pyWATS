from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_controllers_api_dashboard_controller_widget_add_data_data import VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataData
  from ..models.virinco_wats_web_dashboard_controllers_api_dashboard_controller_widget_add_data_filter import VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataFilter





T = TypeVar("T", bound="VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData")



@_attrs_define
class VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData:
    """ 
        Attributes:
            filter_ (Union[Unset, VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataFilter]):
            data (Union[Unset, VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataData]):
     """

    filter_: Union[Unset, 'VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataFilter'] = UNSET
    data: Union[Unset, 'VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataData'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_controllers_api_dashboard_controller_widget_add_data_data import VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataData
        from ..models.virinco_wats_web_dashboard_controllers_api_dashboard_controller_widget_add_data_filter import VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataFilter
        filter_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_controllers_api_dashboard_controller_widget_add_data_data import VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataData
        from ..models.virinco_wats_web_dashboard_controllers_api_dashboard_controller_widget_add_data_filter import VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataFilter
        d = dict(src_dict)
        _filter_ = d.pop("filter", UNSET)
        filter_: Union[Unset, VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataFilter]
        if isinstance(_filter_,  Unset):
            filter_ = UNSET
        else:
            filter_ = VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataFilter.from_dict(_filter_)




        _data = d.pop("data", UNSET)
        data: Union[Unset, VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataData]
        if isinstance(_data,  Unset):
            data = UNSET
        else:
            data = VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddDataData.from_dict(_data)




        virinco_wats_web_dashboard_controllers_api_dashboard_controller_widget_add_data = cls(
            filter_=filter_,
            data=data,
        )


        virinco_wats_web_dashboard_controllers_api_dashboard_controller_widget_add_data.additional_properties = d
        return virinco_wats_web_dashboard_controllers_api_dashboard_controller_widget_add_data

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
