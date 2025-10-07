from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesKeyValue")



@_attrs_define
class VirincoWATSWebDashboardModelsMesKeyValue:
    """ 
        Attributes:
            key (Union[Unset, str]):
            value (Union[Unset, str]):
            xml (Union[Unset, str]):
     """

    key: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    xml: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        key = self.key

        value = self.value

        xml = self.xml


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value
        if xml is not UNSET:
            field_dict["xml"] = xml

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key", UNSET)

        value = d.pop("value", UNSET)

        xml = d.pop("xml", UNSET)

        virinco_wats_web_dashboard_models_mes_key_value = cls(
            key=key,
            value=value,
            xml=xml,
        )


        virinco_wats_web_dashboard_models_mes_key_value.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_key_value

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
