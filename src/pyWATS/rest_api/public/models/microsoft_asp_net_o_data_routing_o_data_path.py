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
  from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
  from ..models.microsoft_o_data_uri_parser_o_data_path_segment import MicrosoftODataUriParserODataPathSegment





T = TypeVar("T", bound="MicrosoftAspNetODataRoutingODataPath")



@_attrs_define
class MicrosoftAspNetODataRoutingODataPath:
    """ 
        Attributes:
            edm_type (Union[Unset, MicrosoftODataEdmIEdmType]):
            navigation_source (Union[Unset, MicrosoftODataEdmIEdmNavigationSource]):
            segments (Union[Unset, list['MicrosoftODataUriParserODataPathSegment']]):
            path_template (Union[Unset, str]):
            path (Union[Unset, list['MicrosoftODataUriParserODataPathSegment']]):
     """

    edm_type: Union[Unset, 'MicrosoftODataEdmIEdmType'] = UNSET
    navigation_source: Union[Unset, 'MicrosoftODataEdmIEdmNavigationSource'] = UNSET
    segments: Union[Unset, list['MicrosoftODataUriParserODataPathSegment']] = UNSET
    path_template: Union[Unset, str] = UNSET
    path: Union[Unset, list['MicrosoftODataUriParserODataPathSegment']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_navigation_source import MicrosoftODataEdmIEdmNavigationSource
        from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
        from ..models.microsoft_o_data_uri_parser_o_data_path_segment import MicrosoftODataUriParserODataPathSegment
        edm_type: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.edm_type, Unset):
            edm_type = self.edm_type.to_dict()

        navigation_source: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.navigation_source, Unset):
            navigation_source = self.navigation_source.to_dict()

        segments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.segments, Unset):
            segments = []
            for segments_item_data in self.segments:
                segments_item = segments_item_data.to_dict()
                segments.append(segments_item)



        path_template = self.path_template

        path: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.path, Unset):
            path = []
            for path_item_data in self.path:
                path_item = path_item_data.to_dict()
                path.append(path_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if edm_type is not UNSET:
            field_dict["EdmType"] = edm_type
        if navigation_source is not UNSET:
            field_dict["NavigationSource"] = navigation_source
        if segments is not UNSET:
            field_dict["Segments"] = segments
        if path_template is not UNSET:
            field_dict["PathTemplate"] = path_template
        if path is not UNSET:
            field_dict["Path"] = path

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_navigation_source import MicrosoftODataEdmIEdmNavigationSource
        from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
        from ..models.microsoft_o_data_uri_parser_o_data_path_segment import MicrosoftODataUriParserODataPathSegment
        d = dict(src_dict)
        _edm_type = d.pop("EdmType", UNSET)
        edm_type: Union[Unset, MicrosoftODataEdmIEdmType]
        if isinstance(_edm_type,  Unset):
            edm_type = UNSET
        else:
            edm_type = MicrosoftODataEdmIEdmType.from_dict(_edm_type)




        _navigation_source = d.pop("NavigationSource", UNSET)
        navigation_source: Union[Unset, MicrosoftODataEdmIEdmNavigationSource]
        if isinstance(_navigation_source,  Unset):
            navigation_source = UNSET
        else:
            navigation_source = MicrosoftODataEdmIEdmNavigationSource.from_dict(_navigation_source)




        segments = []
        _segments = d.pop("Segments", UNSET)
        for segments_item_data in (_segments or []):
            segments_item = MicrosoftODataUriParserODataPathSegment.from_dict(segments_item_data)



            segments.append(segments_item)


        path_template = d.pop("PathTemplate", UNSET)

        path = []
        _path = d.pop("Path", UNSET)
        for path_item_data in (_path or []):
            path_item = MicrosoftODataUriParserODataPathSegment.from_dict(path_item_data)



            path.append(path_item)


        microsoft_asp_net_o_data_routing_o_data_path = cls(
            edm_type=edm_type,
            navigation_source=navigation_source,
            segments=segments,
            path_template=path_template,
            path=path,
        )


        microsoft_asp_net_o_data_routing_o_data_path.additional_properties = d
        return microsoft_asp_net_o_data_routing_o_data_path

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
