from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_tag_type import VirincoWATSWebDashboardModelsMesTagType
from ..models.virinco_wats_web_dashboard_models_mes_tag_value_config import VirincoWATSWebDashboardModelsMesTagValueConfig
from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesTag")



@_attrs_define
class VirincoWATSWebDashboardModelsMesTag:
    """ 
        Attributes:
            tag_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            type_ (Union[Unset, VirincoWATSWebDashboardModelsMesTagType]):
            defined_values (Union[Unset, str]): Semicolon separated list of user defined values for this tag
            value_config (Union[Unset, VirincoWATSWebDashboardModelsMesTagValueConfig]): Option describing how
                {Virinco.WATS.Web.Dashboard.Models.Mes.Tag.DefinedValues} must be handled.
     """

    tag_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    type_: Union[Unset, VirincoWATSWebDashboardModelsMesTagType] = UNSET
    defined_values: Union[Unset, str] = UNSET
    value_config: Union[Unset, VirincoWATSWebDashboardModelsMesTagValueConfig] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        tag_id: Union[Unset, str] = UNSET
        if not isinstance(self.tag_id, Unset):
            tag_id = str(self.tag_id)

        name = self.name

        description = self.description

        type_: Union[Unset, int] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        defined_values = self.defined_values

        value_config: Union[Unset, int] = UNSET
        if not isinstance(self.value_config, Unset):
            value_config = self.value_config.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if tag_id is not UNSET:
            field_dict["TagId"] = tag_id
        if name is not UNSET:
            field_dict["Name"] = name
        if description is not UNSET:
            field_dict["Description"] = description
        if type_ is not UNSET:
            field_dict["Type"] = type_
        if defined_values is not UNSET:
            field_dict["definedValues"] = defined_values
        if value_config is not UNSET:
            field_dict["valueConfig"] = value_config

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _tag_id = d.pop("TagId", UNSET)
        tag_id: Union[Unset, UUID]
        if isinstance(_tag_id,  Unset):
            tag_id = UNSET
        else:
            tag_id = UUID(_tag_id)




        name = d.pop("Name", UNSET)

        description = d.pop("Description", UNSET)

        _type_ = d.pop("Type", UNSET)
        type_: Union[Unset, VirincoWATSWebDashboardModelsMesTagType]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = VirincoWATSWebDashboardModelsMesTagType(_type_)




        defined_values = d.pop("definedValues", UNSET)

        _value_config = d.pop("valueConfig", UNSET)
        value_config: Union[Unset, VirincoWATSWebDashboardModelsMesTagValueConfig]
        if isinstance(_value_config,  Unset):
            value_config = UNSET
        else:
            value_config = VirincoWATSWebDashboardModelsMesTagValueConfig(_value_config)




        virinco_wats_web_dashboard_models_mes_tag = cls(
            tag_id=tag_id,
            name=name,
            description=description,
            type_=type_,
            defined_values=defined_values,
            value_config=value_config,
        )


        virinco_wats_web_dashboard_models_mes_tag.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_tag

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
