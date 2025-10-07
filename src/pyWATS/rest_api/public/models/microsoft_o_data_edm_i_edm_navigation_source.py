from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
  from ..models.microsoft_o_data_edm_i_edm_navigation_property_binding import MicrosoftODataEdmIEdmNavigationPropertyBinding
  from ..models.microsoft_o_data_edm_i_edm_path_expression import MicrosoftODataEdmIEdmPathExpression





T = TypeVar("T", bound="MicrosoftODataEdmIEdmNavigationSource")



@_attrs_define
class MicrosoftODataEdmIEdmNavigationSource:
    """ 
        Attributes:
            navigation_property_bindings (Union[Unset, list['MicrosoftODataEdmIEdmNavigationPropertyBinding']]):
            path (Union[Unset, MicrosoftODataEdmIEdmPathExpression]):
            type_ (Union[Unset, MicrosoftODataEdmIEdmType]):
            name (Union[Unset, str]):
     """

    navigation_property_bindings: Union[Unset, list['MicrosoftODataEdmIEdmNavigationPropertyBinding']] = UNSET
    path: Union[Unset, 'MicrosoftODataEdmIEdmPathExpression'] = UNSET
    type_: Union[Unset, 'MicrosoftODataEdmIEdmType'] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
        from ..models.microsoft_o_data_edm_i_edm_navigation_property_binding import MicrosoftODataEdmIEdmNavigationPropertyBinding
        from ..models.microsoft_o_data_edm_i_edm_path_expression import MicrosoftODataEdmIEdmPathExpression
        navigation_property_bindings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.navigation_property_bindings, Unset):
            navigation_property_bindings = []
            for navigation_property_bindings_item_data in self.navigation_property_bindings:
                navigation_property_bindings_item = navigation_property_bindings_item_data.to_dict()
                navigation_property_bindings.append(navigation_property_bindings_item)



        path: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.path, Unset):
            path = self.path.to_dict()

        type_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.to_dict()

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if navigation_property_bindings is not UNSET:
            field_dict["NavigationPropertyBindings"] = navigation_property_bindings
        if path is not UNSET:
            field_dict["Path"] = path
        if type_ is not UNSET:
            field_dict["Type"] = type_
        if name is not UNSET:
            field_dict["Name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
        from ..models.microsoft_o_data_edm_i_edm_navigation_property_binding import MicrosoftODataEdmIEdmNavigationPropertyBinding
        from ..models.microsoft_o_data_edm_i_edm_path_expression import MicrosoftODataEdmIEdmPathExpression
        d = dict(src_dict)
        navigation_property_bindings = []
        _navigation_property_bindings = d.pop("NavigationPropertyBindings", UNSET)
        for navigation_property_bindings_item_data in (_navigation_property_bindings or []):
            navigation_property_bindings_item = MicrosoftODataEdmIEdmNavigationPropertyBinding.from_dict(navigation_property_bindings_item_data)



            navigation_property_bindings.append(navigation_property_bindings_item)


        _path = d.pop("Path", UNSET)
        path: Union[Unset, MicrosoftODataEdmIEdmPathExpression]
        if isinstance(_path,  Unset):
            path = UNSET
        else:
            path = MicrosoftODataEdmIEdmPathExpression.from_dict(_path)




        _type_ = d.pop("Type", UNSET)
        type_: Union[Unset, MicrosoftODataEdmIEdmType]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = MicrosoftODataEdmIEdmType.from_dict(_type_)




        name = d.pop("Name", UNSET)

        microsoft_o_data_edm_i_edm_navigation_source = cls(
            navigation_property_bindings=navigation_property_bindings,
            path=path,
            type_=type_,
            name=name,
        )


        microsoft_o_data_edm_i_edm_navigation_source.additional_properties = d
        return microsoft_o_data_edm_i_edm_navigation_source

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
