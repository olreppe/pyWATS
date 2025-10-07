from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmProductSelectionsUsage")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmProductSelectionsUsage:
    """ 
        Attributes:
            used_in_test_sequence_relations (Union[Unset, list[int]]):
            used_in_workflow_relations (Union[Unset, list[int]]):
            used_in_user_restrictions (Union[Unset, list[int]]):
     """

    used_in_test_sequence_relations: Union[Unset, list[int]] = UNSET
    used_in_workflow_relations: Union[Unset, list[int]] = UNSET
    used_in_user_restrictions: Union[Unset, list[int]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        used_in_test_sequence_relations: Union[Unset, list[int]] = UNSET
        if not isinstance(self.used_in_test_sequence_relations, Unset):
            used_in_test_sequence_relations = self.used_in_test_sequence_relations



        used_in_workflow_relations: Union[Unset, list[int]] = UNSET
        if not isinstance(self.used_in_workflow_relations, Unset):
            used_in_workflow_relations = self.used_in_workflow_relations



        used_in_user_restrictions: Union[Unset, list[int]] = UNSET
        if not isinstance(self.used_in_user_restrictions, Unset):
            used_in_user_restrictions = self.used_in_user_restrictions




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if used_in_test_sequence_relations is not UNSET:
            field_dict["UsedInTestSequenceRelations"] = used_in_test_sequence_relations
        if used_in_workflow_relations is not UNSET:
            field_dict["UsedInWorkflowRelations"] = used_in_workflow_relations
        if used_in_user_restrictions is not UNSET:
            field_dict["UsedInUserRestrictions"] = used_in_user_restrictions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        used_in_test_sequence_relations = cast(list[int], d.pop("UsedInTestSequenceRelations", UNSET))


        used_in_workflow_relations = cast(list[int], d.pop("UsedInWorkflowRelations", UNSET))


        used_in_user_restrictions = cast(list[int], d.pop("UsedInUserRestrictions", UNSET))


        virinco_wats_web_dashboard_models_tdm_product_selections_usage = cls(
            used_in_test_sequence_relations=used_in_test_sequence_relations,
            used_in_workflow_relations=used_in_workflow_relations,
            used_in_user_restrictions=used_in_user_restrictions,
        )


        virinco_wats_web_dashboard_models_tdm_product_selections_usage.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_product_selections_usage

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
