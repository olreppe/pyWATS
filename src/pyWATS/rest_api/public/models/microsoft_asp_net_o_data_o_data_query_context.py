from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.system_i_service_provider import SystemIServiceProvider
  from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
  from ..models.microsoft_o_data_edm_i_edm_navigation_source import MicrosoftODataEdmIEdmNavigationSource
  from ..models.microsoft_o_data_edm_i_edm_model import MicrosoftODataEdmIEdmModel
  from ..models.microsoft_asp_net_o_data_routing_o_data_path import MicrosoftAspNetODataRoutingODataPath
  from ..models.microsoft_asp_net_o_data_query_default_query_settings import MicrosoftAspNetODataQueryDefaultQuerySettings





T = TypeVar("T", bound="MicrosoftAspNetODataODataQueryContext")



@_attrs_define
class MicrosoftAspNetODataODataQueryContext:
    """ 
        Attributes:
            default_query_settings (Union[Unset, MicrosoftAspNetODataQueryDefaultQuerySettings]):
            model (Union[Unset, MicrosoftODataEdmIEdmModel]):
            element_type (Union[Unset, MicrosoftODataEdmIEdmType]):
            navigation_source (Union[Unset, MicrosoftODataEdmIEdmNavigationSource]):
            element_clr_type (Union[Unset, str]):
            path (Union[Unset, MicrosoftAspNetODataRoutingODataPath]):
            request_container (Union[Unset, SystemIServiceProvider]):
     """

    default_query_settings: Union[Unset, 'MicrosoftAspNetODataQueryDefaultQuerySettings'] = UNSET
    model: Union[Unset, 'MicrosoftODataEdmIEdmModel'] = UNSET
    element_type: Union[Unset, 'MicrosoftODataEdmIEdmType'] = UNSET
    navigation_source: Union[Unset, 'MicrosoftODataEdmIEdmNavigationSource'] = UNSET
    element_clr_type: Union[Unset, str] = UNSET
    path: Union[Unset, 'MicrosoftAspNetODataRoutingODataPath'] = UNSET
    request_container: Union[Unset, 'SystemIServiceProvider'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.system_i_service_provider import SystemIServiceProvider
        from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
        from ..models.microsoft_o_data_edm_i_edm_navigation_source import MicrosoftODataEdmIEdmNavigationSource
        from ..models.microsoft_o_data_edm_i_edm_model import MicrosoftODataEdmIEdmModel
        from ..models.microsoft_asp_net_o_data_routing_o_data_path import MicrosoftAspNetODataRoutingODataPath
        from ..models.microsoft_asp_net_o_data_query_default_query_settings import MicrosoftAspNetODataQueryDefaultQuerySettings
        default_query_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default_query_settings, Unset):
            default_query_settings = self.default_query_settings.to_dict()

        model: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.model, Unset):
            model = self.model.to_dict()

        element_type: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.element_type, Unset):
            element_type = self.element_type.to_dict()

        navigation_source: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.navigation_source, Unset):
            navigation_source = self.navigation_source.to_dict()

        element_clr_type = self.element_clr_type

        path: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.path, Unset):
            path = self.path.to_dict()

        request_container: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.request_container, Unset):
            request_container = self.request_container.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if default_query_settings is not UNSET:
            field_dict["DefaultQuerySettings"] = default_query_settings
        if model is not UNSET:
            field_dict["Model"] = model
        if element_type is not UNSET:
            field_dict["ElementType"] = element_type
        if navigation_source is not UNSET:
            field_dict["NavigationSource"] = navigation_source
        if element_clr_type is not UNSET:
            field_dict["ElementClrType"] = element_clr_type
        if path is not UNSET:
            field_dict["Path"] = path
        if request_container is not UNSET:
            field_dict["RequestContainer"] = request_container

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.system_i_service_provider import SystemIServiceProvider
        from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
        from ..models.microsoft_o_data_edm_i_edm_navigation_source import MicrosoftODataEdmIEdmNavigationSource
        from ..models.microsoft_o_data_edm_i_edm_model import MicrosoftODataEdmIEdmModel
        from ..models.microsoft_asp_net_o_data_routing_o_data_path import MicrosoftAspNetODataRoutingODataPath
        from ..models.microsoft_asp_net_o_data_query_default_query_settings import MicrosoftAspNetODataQueryDefaultQuerySettings
        d = dict(src_dict)
        _default_query_settings = d.pop("DefaultQuerySettings", UNSET)
        default_query_settings: Union[Unset, MicrosoftAspNetODataQueryDefaultQuerySettings]
        if isinstance(_default_query_settings,  Unset):
            default_query_settings = UNSET
        else:
            default_query_settings = MicrosoftAspNetODataQueryDefaultQuerySettings.from_dict(_default_query_settings)




        _model = d.pop("Model", UNSET)
        model: Union[Unset, MicrosoftODataEdmIEdmModel]
        if isinstance(_model,  Unset):
            model = UNSET
        else:
            model = MicrosoftODataEdmIEdmModel.from_dict(_model)




        _element_type = d.pop("ElementType", UNSET)
        element_type: Union[Unset, MicrosoftODataEdmIEdmType]
        if isinstance(_element_type,  Unset):
            element_type = UNSET
        else:
            element_type = MicrosoftODataEdmIEdmType.from_dict(_element_type)




        _navigation_source = d.pop("NavigationSource", UNSET)
        navigation_source: Union[Unset, MicrosoftODataEdmIEdmNavigationSource]
        if isinstance(_navigation_source,  Unset):
            navigation_source = UNSET
        else:
            navigation_source = MicrosoftODataEdmIEdmNavigationSource.from_dict(_navigation_source)




        element_clr_type = d.pop("ElementClrType", UNSET)

        _path = d.pop("Path", UNSET)
        path: Union[Unset, MicrosoftAspNetODataRoutingODataPath]
        if isinstance(_path,  Unset):
            path = UNSET
        else:
            path = MicrosoftAspNetODataRoutingODataPath.from_dict(_path)




        _request_container = d.pop("RequestContainer", UNSET)
        request_container: Union[Unset, SystemIServiceProvider]
        if isinstance(_request_container,  Unset):
            request_container = UNSET
        else:
            request_container = SystemIServiceProvider.from_dict(_request_container)




        microsoft_asp_net_o_data_o_data_query_context = cls(
            default_query_settings=default_query_settings,
            model=model,
            element_type=element_type,
            navigation_source=navigation_source,
            element_clr_type=element_clr_type,
            path=path,
            request_container=request_container,
        )


        microsoft_asp_net_o_data_o_data_query_context.additional_properties = d
        return microsoft_asp_net_o_data_o_data_query_context

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
