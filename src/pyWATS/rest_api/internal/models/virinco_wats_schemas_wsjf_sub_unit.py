from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_schemas_wsjf_failure import VirincoWATSSchemasWSJFFailure





T = TypeVar("T", bound="VirincoWATSSchemasWSJFSubUnit")



@_attrs_define
class VirincoWATSSchemasWSJFSubUnit:
    """ 
        Attributes:
            part_type (Union[Unset, str]): Type of unit.
            pn (Union[Unset, str]): Unit part number.
            rev (Union[Unset, str]): Unit revision number.
            sn (Union[Unset, str]): Unit serial number.
            idx (Union[Unset, int]): Unit index (only used in repair).
            parent_idx (Union[Unset, int]): Index of parent unit (only used in repair).
            position (Union[Unset, int]): Position of unit.
            replaced_idx (Union[Unset, int]): Index of unit this unit was replaced by (only valid for repair).
            failures (Union[Unset, list['VirincoWATSSchemasWSJFFailure']]): Failures in this unit.
     """

    part_type: Union[Unset, str] = UNSET
    pn: Union[Unset, str] = UNSET
    rev: Union[Unset, str] = UNSET
    sn: Union[Unset, str] = UNSET
    idx: Union[Unset, int] = UNSET
    parent_idx: Union[Unset, int] = UNSET
    position: Union[Unset, int] = UNSET
    replaced_idx: Union[Unset, int] = UNSET
    failures: Union[Unset, list['VirincoWATSSchemasWSJFFailure']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_schemas_wsjf_failure import VirincoWATSSchemasWSJFFailure
        part_type = self.part_type

        pn = self.pn

        rev = self.rev

        sn = self.sn

        idx = self.idx

        parent_idx = self.parent_idx

        position = self.position

        replaced_idx = self.replaced_idx

        failures: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.failures, Unset):
            failures = []
            for failures_item_data in self.failures:
                failures_item = failures_item_data.to_dict()
                failures.append(failures_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if part_type is not UNSET:
            field_dict["partType"] = part_type
        if pn is not UNSET:
            field_dict["pn"] = pn
        if rev is not UNSET:
            field_dict["rev"] = rev
        if sn is not UNSET:
            field_dict["sn"] = sn
        if idx is not UNSET:
            field_dict["idx"] = idx
        if parent_idx is not UNSET:
            field_dict["parentIdx"] = parent_idx
        if position is not UNSET:
            field_dict["position"] = position
        if replaced_idx is not UNSET:
            field_dict["replacedIdx"] = replaced_idx
        if failures is not UNSET:
            field_dict["failures"] = failures

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_schemas_wsjf_failure import VirincoWATSSchemasWSJFFailure
        d = dict(src_dict)
        part_type = d.pop("partType", UNSET)

        pn = d.pop("pn", UNSET)

        rev = d.pop("rev", UNSET)

        sn = d.pop("sn", UNSET)

        idx = d.pop("idx", UNSET)

        parent_idx = d.pop("parentIdx", UNSET)

        position = d.pop("position", UNSET)

        replaced_idx = d.pop("replacedIdx", UNSET)

        failures = []
        _failures = d.pop("failures", UNSET)
        for failures_item_data in (_failures or []):
            failures_item = VirincoWATSSchemasWSJFFailure.from_dict(failures_item_data)



            failures.append(failures_item)


        virinco_wats_schemas_wsjf_sub_unit = cls(
            part_type=part_type,
            pn=pn,
            rev=rev,
            sn=sn,
            idx=idx,
            parent_idx=parent_idx,
            position=position,
            replaced_idx=replaced_idx,
            failures=failures,
        )


        virinco_wats_schemas_wsjf_sub_unit.additional_properties = d
        return virinco_wats_schemas_wsjf_sub_unit

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
