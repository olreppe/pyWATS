from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.workflow_user_input_json_body_additional_property import WorkflowUserInputJsonBodyAdditionalProperty





T = TypeVar("T", bound="WorkflowUserInputJsonBody")



@_attrs_define
class WorkflowUserInputJsonBody:
    """ 
     """

    additional_properties: dict[str, 'WorkflowUserInputJsonBodyAdditionalProperty'] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.workflow_user_input_json_body_additional_property import WorkflowUserInputJsonBodyAdditionalProperty
        
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()


        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workflow_user_input_json_body_additional_property import WorkflowUserInputJsonBodyAdditionalProperty
        d = dict(src_dict)
        workflow_user_input_json_body = cls(
        )


        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = WorkflowUserInputJsonBodyAdditionalProperty.from_dict(prop_dict)



            additional_properties[prop_name] = additional_property

        workflow_user_input_json_body.additional_properties = additional_properties
        return workflow_user_input_json_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> 'WorkflowUserInputJsonBodyAdditionalProperty':
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: 'WorkflowUserInputJsonBodyAdditionalProperty') -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
