from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_web_models_root_cause_attachment import VirincoWATSWebModelsRootCauseAttachment





T = TypeVar("T", bound="VirincoWATSWebModelsRootCauseUpdate")



@_attrs_define
class VirincoWATSWebModelsRootCauseUpdate:
    """ 
        Attributes:
            update_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            update_utc (Union[Unset, datetime.datetime]):
            update_user (Union[Unset, str]):
            content (Union[Unset, str]):
            update_type (Union[Unset, int]): 0 = Ticket content (text)
                1 = Progress changed
                2 = Ticket properties (assignee, status, etc.)
                3 = Notification info (reminder/mail)
            attachments (Union[Unset, list['VirincoWATSWebModelsRootCauseAttachment']]):
     """

    update_id: Union[Unset, UUID] = UNSET
    update_utc: Union[Unset, datetime.datetime] = UNSET
    update_user: Union[Unset, str] = UNSET
    content: Union[Unset, str] = UNSET
    update_type: Union[Unset, int] = UNSET
    attachments: Union[Unset, list['VirincoWATSWebModelsRootCauseAttachment']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_models_root_cause_attachment import VirincoWATSWebModelsRootCauseAttachment
        update_id: Union[Unset, str] = UNSET
        if not isinstance(self.update_id, Unset):
            update_id = str(self.update_id)

        update_utc: Union[Unset, str] = UNSET
        if not isinstance(self.update_utc, Unset):
            update_utc = self.update_utc.isoformat()

        update_user = self.update_user

        content = self.content

        update_type = self.update_type

        attachments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = []
            for attachments_item_data in self.attachments:
                attachments_item = attachments_item_data.to_dict()
                attachments.append(attachments_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if update_id is not UNSET:
            field_dict["updateId"] = update_id
        if update_utc is not UNSET:
            field_dict["updateUtc"] = update_utc
        if update_user is not UNSET:
            field_dict["updateUser"] = update_user
        if content is not UNSET:
            field_dict["content"] = content
        if update_type is not UNSET:
            field_dict["updateType"] = update_type
        if attachments is not UNSET:
            field_dict["attachments"] = attachments

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_models_root_cause_attachment import VirincoWATSWebModelsRootCauseAttachment
        d = dict(src_dict)
        _update_id = d.pop("updateId", UNSET)
        update_id: Union[Unset, UUID]
        if isinstance(_update_id,  Unset):
            update_id = UNSET
        else:
            update_id = UUID(_update_id)




        _update_utc = d.pop("updateUtc", UNSET)
        update_utc: Union[Unset, datetime.datetime]
        if isinstance(_update_utc,  Unset):
            update_utc = UNSET
        else:
            update_utc = isoparse(_update_utc)




        update_user = d.pop("updateUser", UNSET)

        content = d.pop("content", UNSET)

        update_type = d.pop("updateType", UNSET)

        attachments = []
        _attachments = d.pop("attachments", UNSET)
        for attachments_item_data in (_attachments or []):
            attachments_item = VirincoWATSWebModelsRootCauseAttachment.from_dict(attachments_item_data)



            attachments.append(attachments_item)


        virinco_wats_web_models_root_cause_update = cls(
            update_id=update_id,
            update_utc=update_utc,
            update_user=update_user,
            content=content,
            update_type=update_type,
            attachments=attachments,
        )


        virinco_wats_web_models_root_cause_update.additional_properties = d
        return virinco_wats_web_models_root_cause_update

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
