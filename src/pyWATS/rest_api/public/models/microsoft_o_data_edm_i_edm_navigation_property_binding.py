from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_navigation_source import MicrosoftODataEdmIEdmNavigationSource
  from ..models.microsoft_o_data_edm_i_edm_navigation_property import MicrosoftODataEdmIEdmNavigationProperty
  from ..models.microsoft_o_data_edm_i_edm_path_expression import MicrosoftODataEdmIEdmPathExpression





T = TypeVar("T", bound="MicrosoftODataEdmIEdmNavigationPropertyBinding")



@_attrs_define
class MicrosoftODataEdmIEdmNavigationPropertyBinding:
    """ 
        Attributes:
            navigation_property (Union[Unset, MicrosoftODataEdmIEdmNavigationProperty]):
            target (Union[Unset, MicrosoftODataEdmIEdmNavigationSource]):
            path (Union[Unset, MicrosoftODataEdmIEdmPathExpression]):
     """

    navigation_property: Union[Unset, 'MicrosoftODataEdmIEdmNavigationProperty'] = UNSET
    target: Union[Unset, 'MicrosoftODataEdmIEdmNavigationSource'] = UNSET
    path: Union[Unset, 'MicrosoftODataEdmIEdmPathExpression'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_navigation_source import MicrosoftODataEdmIEdmNavigationSource
        from ..models.microsoft_o_data_edm_i_edm_navigation_property import MicrosoftODataEdmIEdmNavigationProperty
        from ..models.microsoft_o_data_edm_i_edm_path_expression import MicrosoftODataEdmIEdmPathExpression
        navigation_property: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.navigation_property, Unset):
            navigation_property = self.navigation_property.to_dict()

        target: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.target, Unset):
            target = self.target.to_dict()

        path: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.path, Unset):
            path = self.path.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if navigation_property is not UNSET:
            field_dict["NavigationProperty"] = navigation_property
        if target is not UNSET:
            field_dict["Target"] = target
        if path is not UNSET:
            field_dict["Path"] = path

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_navigation_source import MicrosoftODataEdmIEdmNavigationSource
        from ..models.microsoft_o_data_edm_i_edm_navigation_property import MicrosoftODataEdmIEdmNavigationProperty
        from ..models.microsoft_o_data_edm_i_edm_path_expression import MicrosoftODataEdmIEdmPathExpression
        d = dict(src_dict)
        _navigation_property = d.pop("NavigationProperty", UNSET)
        navigation_property: Union[Unset, MicrosoftODataEdmIEdmNavigationProperty]
        if isinstance(_navigation_property,  Unset):
            navigation_property = UNSET
        else:
            navigation_property = MicrosoftODataEdmIEdmNavigationProperty.from_dict(_navigation_property)




        _target = d.pop("Target", UNSET)
        target: Union[Unset, MicrosoftODataEdmIEdmNavigationSource]
        if isinstance(_target,  Unset):
            target = UNSET
        else:
            target = MicrosoftODataEdmIEdmNavigationSource.from_dict(_target)




        _path = d.pop("Path", UNSET)
        path: Union[Unset, MicrosoftODataEdmIEdmPathExpression]
        if isinstance(_path,  Unset):
            path = UNSET
        else:
            path = MicrosoftODataEdmIEdmPathExpression.from_dict(_path)




        microsoft_o_data_edm_i_edm_navigation_property_binding = cls(
            navigation_property=navigation_property,
            target=target,
            path=path,
        )


        microsoft_o_data_edm_i_edm_navigation_property_binding.additional_properties = d
        return microsoft_o_data_edm_i_edm_navigation_property_binding

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
