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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesAssetAssetFile")



@_attrs_define
class VirincoWATSWebDashboardModelsMesAssetAssetFile:
    """ 
        Attributes:
            file_name (Union[Unset, str]):
            file_size (Union[Unset, int]):
            uploaded_utc (Union[Unset, datetime.datetime]):
            uploaded_by (Union[Unset, str]):
     """

    file_name: Union[Unset, str] = UNSET
    file_size: Union[Unset, int] = UNSET
    uploaded_utc: Union[Unset, datetime.datetime] = UNSET
    uploaded_by: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_name = self.file_name

        file_size = self.file_size

        uploaded_utc: Union[Unset, str] = UNSET
        if not isinstance(self.uploaded_utc, Unset):
            uploaded_utc = self.uploaded_utc.isoformat()

        uploaded_by = self.uploaded_by


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if file_name is not UNSET:
            field_dict["fileName"] = file_name
        if file_size is not UNSET:
            field_dict["fileSize"] = file_size
        if uploaded_utc is not UNSET:
            field_dict["uploadedUtc"] = uploaded_utc
        if uploaded_by is not UNSET:
            field_dict["uploadedBy"] = uploaded_by

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_name = d.pop("fileName", UNSET)

        file_size = d.pop("fileSize", UNSET)

        _uploaded_utc = d.pop("uploadedUtc", UNSET)
        uploaded_utc: Union[Unset, datetime.datetime]
        if isinstance(_uploaded_utc,  Unset):
            uploaded_utc = UNSET
        else:
            uploaded_utc = isoparse(_uploaded_utc)




        uploaded_by = d.pop("uploadedBy", UNSET)

        virinco_wats_web_dashboard_models_mes_asset_asset_file = cls(
            file_name=file_name,
            file_size=file_size,
            uploaded_utc=uploaded_utc,
            uploaded_by=uploaded_by,
        )


        virinco_wats_web_dashboard_models_mes_asset_asset_file.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_asset_asset_file

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
