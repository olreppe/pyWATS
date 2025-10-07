from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmOperator")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmOperator:
    """ 
        Attributes:
            id (Union[Unset, int]):
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            identifier (Union[Unset, str]):
            sort_order (Union[Unset, int]):
     """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    sort_order: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        identifier = self.identifier

        sort_order = self.sort_order


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if sort_order is not UNSET:
            field_dict["sortOrder"] = sort_order

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        identifier = d.pop("identifier", UNSET)

        sort_order = d.pop("sortOrder", UNSET)

        virinco_wats_web_dashboard_models_tdm_operator = cls(
            id=id,
            name=name,
            description=description,
            identifier=identifier,
            sort_order=sort_order,
        )


        virinco_wats_web_dashboard_models_tdm_operator.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_operator

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
