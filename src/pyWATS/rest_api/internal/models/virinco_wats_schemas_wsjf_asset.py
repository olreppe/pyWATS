from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSSchemasWSJFAsset")



@_attrs_define
class VirincoWATSSchemasWSJFAsset:
    """ 
        Attributes:
            asset_sn (Union[Unset, str]): Serial number of the asset.
            usage_count (Union[Unset, int]): How much the asset was used.
            usage_count_format (Union[Unset, str]): Number format of usageCount.
     """

    asset_sn: Union[Unset, str] = UNSET
    usage_count: Union[Unset, int] = UNSET
    usage_count_format: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        asset_sn = self.asset_sn

        usage_count = self.usage_count

        usage_count_format = self.usage_count_format


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if asset_sn is not UNSET:
            field_dict["assetSN"] = asset_sn
        if usage_count is not UNSET:
            field_dict["usageCount"] = usage_count
        if usage_count_format is not UNSET:
            field_dict["usageCountFormat"] = usage_count_format

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        asset_sn = d.pop("assetSN", UNSET)

        usage_count = d.pop("usageCount", UNSET)

        usage_count_format = d.pop("usageCountFormat", UNSET)

        virinco_wats_schemas_wsjf_asset = cls(
            asset_sn=asset_sn,
            usage_count=usage_count,
            usage_count_format=usage_count_format,
        )


        virinco_wats_schemas_wsjf_asset.additional_properties = d
        return virinco_wats_schemas_wsjf_asset

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
