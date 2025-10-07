from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSSchemasWSJFMessagePopup")



@_attrs_define
class VirincoWATSSchemasWSJFMessagePopup:
    """ 
        Attributes:
            response (Union[Unset, str]): Response from popup.
            button (Union[Unset, int]): Index of button on popup pressed.
            button_format (Union[Unset, str]): Numeric format of button.
     """

    response: Union[Unset, str] = UNSET
    button: Union[Unset, int] = UNSET
    button_format: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        response = self.response

        button = self.button

        button_format = self.button_format


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if response is not UNSET:
            field_dict["response"] = response
        if button is not UNSET:
            field_dict["button"] = button
        if button_format is not UNSET:
            field_dict["buttonFormat"] = button_format

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        response = d.pop("response", UNSET)

        button = d.pop("button", UNSET)

        button_format = d.pop("buttonFormat", UNSET)

        virinco_wats_schemas_wsjf_message_popup = cls(
            response=response,
            button=button,
            button_format=button_format,
        )


        virinco_wats_schemas_wsjf_message_popup.additional_properties = d
        return virinco_wats_schemas_wsjf_message_popup

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
