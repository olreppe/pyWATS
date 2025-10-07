from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesMITestSequenceSiteRelation")



@_attrs_define
class VirincoWATSWebDashboardModelsMesMITestSequenceSiteRelation:
    """ 
        Attributes:
            test_sequence_site_relation_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            site_code (Union[Unset, str]):
            test_sequence_relation_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
     """

    test_sequence_site_relation_id: Union[Unset, UUID] = UNSET
    site_code: Union[Unset, str] = UNSET
    test_sequence_relation_id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        test_sequence_site_relation_id: Union[Unset, str] = UNSET
        if not isinstance(self.test_sequence_site_relation_id, Unset):
            test_sequence_site_relation_id = str(self.test_sequence_site_relation_id)

        site_code = self.site_code

        test_sequence_relation_id: Union[Unset, str] = UNSET
        if not isinstance(self.test_sequence_relation_id, Unset):
            test_sequence_relation_id = str(self.test_sequence_relation_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if test_sequence_site_relation_id is not UNSET:
            field_dict["TestSequenceSiteRelationId"] = test_sequence_site_relation_id
        if site_code is not UNSET:
            field_dict["SiteCode"] = site_code
        if test_sequence_relation_id is not UNSET:
            field_dict["TestSequenceRelationId"] = test_sequence_relation_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _test_sequence_site_relation_id = d.pop("TestSequenceSiteRelationId", UNSET)
        test_sequence_site_relation_id: Union[Unset, UUID]
        if isinstance(_test_sequence_site_relation_id,  Unset):
            test_sequence_site_relation_id = UNSET
        else:
            test_sequence_site_relation_id = UUID(_test_sequence_site_relation_id)




        site_code = d.pop("SiteCode", UNSET)

        _test_sequence_relation_id = d.pop("TestSequenceRelationId", UNSET)
        test_sequence_relation_id: Union[Unset, UUID]
        if isinstance(_test_sequence_relation_id,  Unset):
            test_sequence_relation_id = UNSET
        else:
            test_sequence_relation_id = UUID(_test_sequence_relation_id)




        virinco_wats_web_dashboard_models_mes_mi_test_sequence_site_relation = cls(
            test_sequence_site_relation_id=test_sequence_site_relation_id,
            site_code=site_code,
            test_sequence_relation_id=test_sequence_relation_id,
        )


        virinco_wats_web_dashboard_models_mes_mi_test_sequence_site_relation.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_mi_test_sequence_site_relation

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
