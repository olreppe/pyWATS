from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesMITestSequenceProcessRelation")



@_attrs_define
class VirincoWATSWebDashboardModelsMesMITestSequenceProcessRelation:
    """ 
        Attributes:
            test_sequence_process_relation_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            test_sequence_relation_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            process_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
     """

    test_sequence_process_relation_id: Union[Unset, UUID] = UNSET
    test_sequence_relation_id: Union[Unset, UUID] = UNSET
    process_id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        test_sequence_process_relation_id: Union[Unset, str] = UNSET
        if not isinstance(self.test_sequence_process_relation_id, Unset):
            test_sequence_process_relation_id = str(self.test_sequence_process_relation_id)

        test_sequence_relation_id: Union[Unset, str] = UNSET
        if not isinstance(self.test_sequence_relation_id, Unset):
            test_sequence_relation_id = str(self.test_sequence_relation_id)

        process_id: Union[Unset, str] = UNSET
        if not isinstance(self.process_id, Unset):
            process_id = str(self.process_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if test_sequence_process_relation_id is not UNSET:
            field_dict["TestSequenceProcessRelationId"] = test_sequence_process_relation_id
        if test_sequence_relation_id is not UNSET:
            field_dict["TestSequenceRelationId"] = test_sequence_relation_id
        if process_id is not UNSET:
            field_dict["ProcessId"] = process_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _test_sequence_process_relation_id = d.pop("TestSequenceProcessRelationId", UNSET)
        test_sequence_process_relation_id: Union[Unset, UUID]
        if isinstance(_test_sequence_process_relation_id,  Unset):
            test_sequence_process_relation_id = UNSET
        else:
            test_sequence_process_relation_id = UUID(_test_sequence_process_relation_id)




        _test_sequence_relation_id = d.pop("TestSequenceRelationId", UNSET)
        test_sequence_relation_id: Union[Unset, UUID]
        if isinstance(_test_sequence_relation_id,  Unset):
            test_sequence_relation_id = UNSET
        else:
            test_sequence_relation_id = UUID(_test_sequence_relation_id)




        _process_id = d.pop("ProcessId", UNSET)
        process_id: Union[Unset, UUID]
        if isinstance(_process_id,  Unset):
            process_id = UNSET
        else:
            process_id = UUID(_process_id)




        virinco_wats_web_dashboard_models_mes_mi_test_sequence_process_relation = cls(
            test_sequence_process_relation_id=test_sequence_process_relation_id,
            test_sequence_relation_id=test_sequence_relation_id,
            process_id=process_id,
        )


        virinco_wats_web_dashboard_models_mes_mi_test_sequence_process_relation.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_mi_test_sequence_process_relation

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
