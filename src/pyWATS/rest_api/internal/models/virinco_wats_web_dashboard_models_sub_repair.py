from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsSubRepair")



@_attrs_define
class VirincoWATSWebDashboardModelsSubRepair:
    """ 
        Attributes:
            parent_uuid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            uuid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            process_code (Union[Unset, str]):
            sn (Union[Unset, str]):
            pn (Union[Unset, str]):
            rev (Union[Unset, str]):
            state (Union[Unset, int]):
     """

    parent_uuid: Union[Unset, UUID] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    process_code: Union[Unset, str] = UNSET
    sn: Union[Unset, str] = UNSET
    pn: Union[Unset, str] = UNSET
    rev: Union[Unset, str] = UNSET
    state: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        parent_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.parent_uuid, Unset):
            parent_uuid = str(self.parent_uuid)

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        process_code = self.process_code

        sn = self.sn

        pn = self.pn

        rev = self.rev

        state = self.state


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if parent_uuid is not UNSET:
            field_dict["ParentUUID"] = parent_uuid
        if uuid is not UNSET:
            field_dict["UUID"] = uuid
        if process_code is not UNSET:
            field_dict["ProcessCode"] = process_code
        if sn is not UNSET:
            field_dict["SN"] = sn
        if pn is not UNSET:
            field_dict["PN"] = pn
        if rev is not UNSET:
            field_dict["Rev"] = rev
        if state is not UNSET:
            field_dict["State"] = state

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _parent_uuid = d.pop("ParentUUID", UNSET)
        parent_uuid: Union[Unset, UUID]
        if isinstance(_parent_uuid,  Unset):
            parent_uuid = UNSET
        else:
            parent_uuid = UUID(_parent_uuid)




        _uuid = d.pop("UUID", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid,  Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)




        process_code = d.pop("ProcessCode", UNSET)

        sn = d.pop("SN", UNSET)

        pn = d.pop("PN", UNSET)

        rev = d.pop("Rev", UNSET)

        state = d.pop("State", UNSET)

        virinco_wats_web_dashboard_models_sub_repair = cls(
            parent_uuid=parent_uuid,
            uuid=uuid,
            process_code=process_code,
            sn=sn,
            pn=pn,
            rev=rev,
            state=state,
        )


        virinco_wats_web_dashboard_models_sub_repair.additional_properties = d
        return virinco_wats_web_dashboard_models_sub_repair

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
