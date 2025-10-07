from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebModelsRootCauseAttachment")



@_attrs_define
class VirincoWATSWebModelsRootCauseAttachment:
    """ 
        Attributes:
            attachment_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            filename (Union[Unset, str]):
     """

    attachment_id: Union[Unset, UUID] = UNSET
    filename: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        attachment_id: Union[Unset, str] = UNSET
        if not isinstance(self.attachment_id, Unset):
            attachment_id = str(self.attachment_id)

        filename = self.filename


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if attachment_id is not UNSET:
            field_dict["attachmentId"] = attachment_id
        if filename is not UNSET:
            field_dict["filename"] = filename

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _attachment_id = d.pop("attachmentId", UNSET)
        attachment_id: Union[Unset, UUID]
        if isinstance(_attachment_id,  Unset):
            attachment_id = UNSET
        else:
            attachment_id = UUID(_attachment_id)




        filename = d.pop("filename", UNSET)

        virinco_wats_web_models_root_cause_attachment = cls(
            attachment_id=attachment_id,
            filename=filename,
        )


        virinco_wats_web_models_root_cause_attachment.additional_properties = d
        return virinco_wats_web_models_root_cause_attachment

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
