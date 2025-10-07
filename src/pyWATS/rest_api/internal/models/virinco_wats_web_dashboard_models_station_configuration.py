from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_station_configuration_page import VirincoWATSWebDashboardModelsStationConfigurationPage
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_web_camera_configuration import VirincoWATSWebDashboardModelsWebCameraConfiguration
  from ..models.virinco_wats_web_dashboard_models_barcode_reader_configuration import VirincoWATSWebDashboardModelsBarcodeReaderConfiguration





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsStationConfiguration")



@_attrs_define
class VirincoWATSWebDashboardModelsStationConfiguration:
    """ 
        Attributes:
            culture (Union[Unset, str]):
            page (Union[Unset, VirincoWATSWebDashboardModelsStationConfigurationPage]):
            sound (Union[Unset, bool]):
            web_camera (Union[Unset, VirincoWATSWebDashboardModelsWebCameraConfiguration]):
            barcode_reader (Union[Unset, VirincoWATSWebDashboardModelsBarcodeReaderConfiguration]):
     """

    culture: Union[Unset, str] = UNSET
    page: Union[Unset, VirincoWATSWebDashboardModelsStationConfigurationPage] = UNSET
    sound: Union[Unset, bool] = UNSET
    web_camera: Union[Unset, 'VirincoWATSWebDashboardModelsWebCameraConfiguration'] = UNSET
    barcode_reader: Union[Unset, 'VirincoWATSWebDashboardModelsBarcodeReaderConfiguration'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_web_camera_configuration import VirincoWATSWebDashboardModelsWebCameraConfiguration
        from ..models.virinco_wats_web_dashboard_models_barcode_reader_configuration import VirincoWATSWebDashboardModelsBarcodeReaderConfiguration
        culture = self.culture

        page: Union[Unset, int] = UNSET
        if not isinstance(self.page, Unset):
            page = self.page.value


        sound = self.sound

        web_camera: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.web_camera, Unset):
            web_camera = self.web_camera.to_dict()

        barcode_reader: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.barcode_reader, Unset):
            barcode_reader = self.barcode_reader.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if culture is not UNSET:
            field_dict["Culture"] = culture
        if page is not UNSET:
            field_dict["Page"] = page
        if sound is not UNSET:
            field_dict["Sound"] = sound
        if web_camera is not UNSET:
            field_dict["WebCamera"] = web_camera
        if barcode_reader is not UNSET:
            field_dict["BarcodeReader"] = barcode_reader

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_web_camera_configuration import VirincoWATSWebDashboardModelsWebCameraConfiguration
        from ..models.virinco_wats_web_dashboard_models_barcode_reader_configuration import VirincoWATSWebDashboardModelsBarcodeReaderConfiguration
        d = dict(src_dict)
        culture = d.pop("Culture", UNSET)

        _page = d.pop("Page", UNSET)
        page: Union[Unset, VirincoWATSWebDashboardModelsStationConfigurationPage]
        if isinstance(_page,  Unset):
            page = UNSET
        else:
            page = VirincoWATSWebDashboardModelsStationConfigurationPage(_page)




        sound = d.pop("Sound", UNSET)

        _web_camera = d.pop("WebCamera", UNSET)
        web_camera: Union[Unset, VirincoWATSWebDashboardModelsWebCameraConfiguration]
        if isinstance(_web_camera,  Unset):
            web_camera = UNSET
        else:
            web_camera = VirincoWATSWebDashboardModelsWebCameraConfiguration.from_dict(_web_camera)




        _barcode_reader = d.pop("BarcodeReader", UNSET)
        barcode_reader: Union[Unset, VirincoWATSWebDashboardModelsBarcodeReaderConfiguration]
        if isinstance(_barcode_reader,  Unset):
            barcode_reader = UNSET
        else:
            barcode_reader = VirincoWATSWebDashboardModelsBarcodeReaderConfiguration.from_dict(_barcode_reader)




        virinco_wats_web_dashboard_models_station_configuration = cls(
            culture=culture,
            page=page,
            sound=sound,
            web_camera=web_camera,
            barcode_reader=barcode_reader,
        )


        virinco_wats_web_dashboard_models_station_configuration.additional_properties = d
        return virinco_wats_web_dashboard_models_station_configuration

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
