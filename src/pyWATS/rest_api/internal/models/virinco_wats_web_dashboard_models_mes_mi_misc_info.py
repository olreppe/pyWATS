from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_mi_misc_info_type import VirincoWATSWebDashboardModelsMesMIMiscInfoType
from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesMIMiscInfo")



@_attrs_define
class VirincoWATSWebDashboardModelsMesMIMiscInfo:
    """ 
        Attributes:
            guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            regex (Union[Unset, str]):
            value (Union[Unset, str]):
            is_valid (Union[Unset, bool]):
            type_ (Union[Unset, VirincoWATSWebDashboardModelsMesMIMiscInfoType]):
     """

    guid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    regex: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    is_valid: Union[Unset, bool] = UNSET
    type_: Union[Unset, VirincoWATSWebDashboardModelsMesMIMiscInfoType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        guid: Union[Unset, str] = UNSET
        if not isinstance(self.guid, Unset):
            guid = str(self.guid)

        name = self.name

        regex = self.regex

        value = self.value

        is_valid = self.is_valid

        type_: Union[Unset, int] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if guid is not UNSET:
            field_dict["guid"] = guid
        if name is not UNSET:
            field_dict["name"] = name
        if regex is not UNSET:
            field_dict["regex"] = regex
        if value is not UNSET:
            field_dict["value"] = value
        if is_valid is not UNSET:
            field_dict["isValid"] = is_valid
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _guid = d.pop("guid", UNSET)
        guid: Union[Unset, UUID]
        if isinstance(_guid,  Unset):
            guid = UNSET
        else:
            guid = UUID(_guid)




        name = d.pop("name", UNSET)

        regex = d.pop("regex", UNSET)

        value = d.pop("value", UNSET)

        is_valid = d.pop("isValid", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, VirincoWATSWebDashboardModelsMesMIMiscInfoType]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = VirincoWATSWebDashboardModelsMesMIMiscInfoType(_type_)




        virinco_wats_web_dashboard_models_mes_mi_misc_info = cls(
            guid=guid,
            name=name,
            regex=regex,
            value=value,
            is_valid=is_valid,
            type_=type_,
        )


        virinco_wats_web_dashboard_models_mes_mi_misc_info.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_mi_misc_info

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
