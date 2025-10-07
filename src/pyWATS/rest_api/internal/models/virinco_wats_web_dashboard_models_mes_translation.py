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
  from ..models.virinco_wats_web_dashboard_models_mes_culture import VirincoWATSWebDashboardModelsMesCulture





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesTranslation")



@_attrs_define
class VirincoWATSWebDashboardModelsMesTranslation:
    """ 
        Attributes:
            translation_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            message_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            culture_id (Union[Unset, int]):
            translation_text (Union[Unset, str]):
            created (Union[Unset, datetime.datetime]):
            request_date (Union[Unset, datetime.datetime]):
            request_count (Union[Unset, int]):
            culture (Union[Unset, VirincoWATSWebDashboardModelsMesCulture]):
     """

    translation_id: Union[Unset, UUID] = UNSET
    message_id: Union[Unset, UUID] = UNSET
    culture_id: Union[Unset, int] = UNSET
    translation_text: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    request_date: Union[Unset, datetime.datetime] = UNSET
    request_count: Union[Unset, int] = UNSET
    culture: Union[Unset, 'VirincoWATSWebDashboardModelsMesCulture'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_culture import VirincoWATSWebDashboardModelsMesCulture
        translation_id: Union[Unset, str] = UNSET
        if not isinstance(self.translation_id, Unset):
            translation_id = str(self.translation_id)

        message_id: Union[Unset, str] = UNSET
        if not isinstance(self.message_id, Unset):
            message_id = str(self.message_id)

        culture_id = self.culture_id

        translation_text = self.translation_text

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        request_date: Union[Unset, str] = UNSET
        if not isinstance(self.request_date, Unset):
            request_date = self.request_date.isoformat()

        request_count = self.request_count

        culture: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.culture, Unset):
            culture = self.culture.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if translation_id is not UNSET:
            field_dict["translationId"] = translation_id
        if message_id is not UNSET:
            field_dict["messageId"] = message_id
        if culture_id is not UNSET:
            field_dict["cultureId"] = culture_id
        if translation_text is not UNSET:
            field_dict["translationText"] = translation_text
        if created is not UNSET:
            field_dict["created"] = created
        if request_date is not UNSET:
            field_dict["requestDate"] = request_date
        if request_count is not UNSET:
            field_dict["requestCount"] = request_count
        if culture is not UNSET:
            field_dict["culture"] = culture

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_culture import VirincoWATSWebDashboardModelsMesCulture
        d = dict(src_dict)
        _translation_id = d.pop("translationId", UNSET)
        translation_id: Union[Unset, UUID]
        if isinstance(_translation_id,  Unset):
            translation_id = UNSET
        else:
            translation_id = UUID(_translation_id)




        _message_id = d.pop("messageId", UNSET)
        message_id: Union[Unset, UUID]
        if isinstance(_message_id,  Unset):
            message_id = UNSET
        else:
            message_id = UUID(_message_id)




        culture_id = d.pop("cultureId", UNSET)

        translation_text = d.pop("translationText", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created,  Unset):
            created = UNSET
        else:
            created = isoparse(_created)




        _request_date = d.pop("requestDate", UNSET)
        request_date: Union[Unset, datetime.datetime]
        if isinstance(_request_date,  Unset):
            request_date = UNSET
        else:
            request_date = isoparse(_request_date)




        request_count = d.pop("requestCount", UNSET)

        _culture = d.pop("culture", UNSET)
        culture: Union[Unset, VirincoWATSWebDashboardModelsMesCulture]
        if isinstance(_culture,  Unset):
            culture = UNSET
        else:
            culture = VirincoWATSWebDashboardModelsMesCulture.from_dict(_culture)




        virinco_wats_web_dashboard_models_mes_translation = cls(
            translation_id=translation_id,
            message_id=message_id,
            culture_id=culture_id,
            translation_text=translation_text,
            created=created,
            request_date=request_date,
            request_count=request_count,
            culture=culture,
        )


        virinco_wats_web_dashboard_models_mes_translation.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_translation

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
