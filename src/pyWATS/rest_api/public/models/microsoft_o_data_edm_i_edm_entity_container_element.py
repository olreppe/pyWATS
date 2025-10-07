from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.microsoft_o_data_edm_i_edm_entity_container_element_container_element_kind import MicrosoftODataEdmIEdmEntityContainerElementContainerElementKind
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_entity_container import MicrosoftODataEdmIEdmEntityContainer





T = TypeVar("T", bound="MicrosoftODataEdmIEdmEntityContainerElement")



@_attrs_define
class MicrosoftODataEdmIEdmEntityContainerElement:
    """ 
        Attributes:
            container_element_kind (Union[Unset, MicrosoftODataEdmIEdmEntityContainerElementContainerElementKind]):
            container (Union[Unset, MicrosoftODataEdmIEdmEntityContainer]):
            name (Union[Unset, str]):
     """

    container_element_kind: Union[Unset, MicrosoftODataEdmIEdmEntityContainerElementContainerElementKind] = UNSET
    container: Union[Unset, 'MicrosoftODataEdmIEdmEntityContainer'] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_entity_container import MicrosoftODataEdmIEdmEntityContainer
        container_element_kind: Union[Unset, int] = UNSET
        if not isinstance(self.container_element_kind, Unset):
            container_element_kind = self.container_element_kind.value


        container: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.container, Unset):
            container = self.container.to_dict()

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if container_element_kind is not UNSET:
            field_dict["ContainerElementKind"] = container_element_kind
        if container is not UNSET:
            field_dict["Container"] = container
        if name is not UNSET:
            field_dict["Name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_entity_container import MicrosoftODataEdmIEdmEntityContainer
        d = dict(src_dict)
        _container_element_kind = d.pop("ContainerElementKind", UNSET)
        container_element_kind: Union[Unset, MicrosoftODataEdmIEdmEntityContainerElementContainerElementKind]
        if isinstance(_container_element_kind,  Unset):
            container_element_kind = UNSET
        else:
            container_element_kind = MicrosoftODataEdmIEdmEntityContainerElementContainerElementKind(_container_element_kind)




        _container = d.pop("Container", UNSET)
        container: Union[Unset, MicrosoftODataEdmIEdmEntityContainer]
        if isinstance(_container,  Unset):
            container = UNSET
        else:
            container = MicrosoftODataEdmIEdmEntityContainer.from_dict(_container)




        name = d.pop("Name", UNSET)

        microsoft_o_data_edm_i_edm_entity_container_element = cls(
            container_element_kind=container_element_kind,
            container=container,
            name=name,
        )


        microsoft_o_data_edm_i_edm_entity_container_element.additional_properties = d
        return microsoft_o_data_edm_i_edm_entity_container_element

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
