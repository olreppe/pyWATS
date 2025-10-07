from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsWebCameraConfiguration")



@_attrs_define
class VirincoWATSWebDashboardModelsWebCameraConfiguration:
    """ 
        Attributes:
            device (Union[Unset, str]):
            device_name (Union[Unset, str]):
            resolution (Union[Unset, int]):
            format_ (Union[Unset, int]):
            quality (Union[Unset, int]):
            high_quality (Union[Unset, bool]):
     """

    device: Union[Unset, str] = UNSET
    device_name: Union[Unset, str] = UNSET
    resolution: Union[Unset, int] = UNSET
    format_: Union[Unset, int] = UNSET
    quality: Union[Unset, int] = UNSET
    high_quality: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        device = self.device

        device_name = self.device_name

        resolution = self.resolution

        format_ = self.format_

        quality = self.quality

        high_quality = self.high_quality


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if device is not UNSET:
            field_dict["Device"] = device
        if device_name is not UNSET:
            field_dict["DeviceName"] = device_name
        if resolution is not UNSET:
            field_dict["Resolution"] = resolution
        if format_ is not UNSET:
            field_dict["Format"] = format_
        if quality is not UNSET:
            field_dict["Quality"] = quality
        if high_quality is not UNSET:
            field_dict["HighQuality"] = high_quality

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        device = d.pop("Device", UNSET)

        device_name = d.pop("DeviceName", UNSET)

        resolution = d.pop("Resolution", UNSET)

        format_ = d.pop("Format", UNSET)

        quality = d.pop("Quality", UNSET)

        high_quality = d.pop("HighQuality", UNSET)

        virinco_wats_web_dashboard_models_web_camera_configuration = cls(
            device=device,
            device_name=device_name,
            resolution=resolution,
            format_=format_,
            quality=quality,
            high_quality=high_quality,
        )


        virinco_wats_web_dashboard_models_web_camera_configuration.additional_properties = d
        return virinco_wats_web_dashboard_models_web_camera_configuration

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
