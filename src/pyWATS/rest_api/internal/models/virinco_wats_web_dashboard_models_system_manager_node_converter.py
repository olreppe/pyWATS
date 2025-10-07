from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.system_collections_generic_key_value_pair_system_string_system_string import SystemCollectionsGenericKeyValuePairSystemStringSystemString





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsSystemManagerNodeConverter")



@_attrs_define
class VirincoWATSWebDashboardModelsSystemManagerNodeConverter:
    """ 
        Attributes:
            name (Union[Unset, str]):
            state (Union[Unset, str]):
            version (Union[Unset, str]):
            total (Union[Unset, str]):
            error (Union[Unset, str]):
            assembly (Union[Unset, str]):
            class_ (Union[Unset, str]):
            filter_ (Union[Unset, str]):
            post_process_action (Union[Unset, str]):
            input_path (Union[Unset, str]):
            parameters (Union[Unset, list['SystemCollectionsGenericKeyValuePairSystemStringSystemString']]):
     """

    name: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    total: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    assembly: Union[Unset, str] = UNSET
    class_: Union[Unset, str] = UNSET
    filter_: Union[Unset, str] = UNSET
    post_process_action: Union[Unset, str] = UNSET
    input_path: Union[Unset, str] = UNSET
    parameters: Union[Unset, list['SystemCollectionsGenericKeyValuePairSystemStringSystemString']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.system_collections_generic_key_value_pair_system_string_system_string import SystemCollectionsGenericKeyValuePairSystemStringSystemString
        name = self.name

        state = self.state

        version = self.version

        total = self.total

        error = self.error

        assembly = self.assembly

        class_ = self.class_

        filter_ = self.filter_

        post_process_action = self.post_process_action

        input_path = self.input_path

        parameters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = []
            for parameters_item_data in self.parameters:
                parameters_item = parameters_item_data.to_dict()
                parameters.append(parameters_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if state is not UNSET:
            field_dict["state"] = state
        if version is not UNSET:
            field_dict["version"] = version
        if total is not UNSET:
            field_dict["total"] = total
        if error is not UNSET:
            field_dict["error"] = error
        if assembly is not UNSET:
            field_dict["assembly"] = assembly
        if class_ is not UNSET:
            field_dict["class"] = class_
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if post_process_action is not UNSET:
            field_dict["postProcessAction"] = post_process_action
        if input_path is not UNSET:
            field_dict["inputPath"] = input_path
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.system_collections_generic_key_value_pair_system_string_system_string import SystemCollectionsGenericKeyValuePairSystemStringSystemString
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        state = d.pop("state", UNSET)

        version = d.pop("version", UNSET)

        total = d.pop("total", UNSET)

        error = d.pop("error", UNSET)

        assembly = d.pop("assembly", UNSET)

        class_ = d.pop("class", UNSET)

        filter_ = d.pop("filter", UNSET)

        post_process_action = d.pop("postProcessAction", UNSET)

        input_path = d.pop("inputPath", UNSET)

        parameters = []
        _parameters = d.pop("parameters", UNSET)
        for parameters_item_data in (_parameters or []):
            parameters_item = SystemCollectionsGenericKeyValuePairSystemStringSystemString.from_dict(parameters_item_data)



            parameters.append(parameters_item)


        virinco_wats_web_dashboard_models_system_manager_node_converter = cls(
            name=name,
            state=state,
            version=version,
            total=total,
            error=error,
            assembly=assembly,
            class_=class_,
            filter_=filter_,
            post_process_action=post_process_action,
            input_path=input_path,
            parameters=parameters,
        )


        virinco_wats_web_dashboard_models_system_manager_node_converter.additional_properties = d
        return virinco_wats_web_dashboard_models_system_manager_node_converter

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
