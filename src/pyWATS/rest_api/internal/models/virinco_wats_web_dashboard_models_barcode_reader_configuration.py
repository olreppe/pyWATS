from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsBarcodeReaderConfiguration")



@_attrs_define
class VirincoWATSWebDashboardModelsBarcodeReaderConfiguration:
    """ 
        Attributes:
            type_ (Union[Unset, int]):
            prefixes (Union[Unset, list[str]]):
            suffixes (Union[Unset, list[str]]):
     """

    type_: Union[Unset, int] = UNSET
    prefixes: Union[Unset, list[str]] = UNSET
    suffixes: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        prefixes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.prefixes, Unset):
            prefixes = self.prefixes



        suffixes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.suffixes, Unset):
            suffixes = self.suffixes




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["Type"] = type_
        if prefixes is not UNSET:
            field_dict["Prefixes"] = prefixes
        if suffixes is not UNSET:
            field_dict["Suffixes"] = suffixes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("Type", UNSET)

        prefixes = cast(list[str], d.pop("Prefixes", UNSET))


        suffixes = cast(list[str], d.pop("Suffixes", UNSET))


        virinco_wats_web_dashboard_models_barcode_reader_configuration = cls(
            type_=type_,
            prefixes=prefixes,
            suffixes=suffixes,
        )


        virinco_wats_web_dashboard_models_barcode_reader_configuration.additional_properties = d
        return virinco_wats_web_dashboard_models_barcode_reader_configuration

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
