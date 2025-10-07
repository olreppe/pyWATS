from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsSnHistoryUnit")



@_attrs_define
class VirincoWATSWebDashboardModelsSnHistoryUnit:
    """ 
        Attributes:
            uuid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            serial_number (Union[Unset, str]):
            part_number (Union[Unset, str]):
            product_name (Union[Unset, str]):
            entity (Union[Unset, str]):
            process (Union[Unset, str]):
            phase (Union[Unset, str]):
            parent_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            unit_first_seen_utc (Union[Unset, datetime.datetime]):
            unit_first_seen_local (Union[Unset, datetime.datetime]):
            uut_count (Union[Unset, int]):
            uur_count (Union[Unset, int]):
     """

    uuid: Union[Unset, UUID] = UNSET
    serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    product_name: Union[Unset, str] = UNSET
    entity: Union[Unset, str] = UNSET
    process: Union[Unset, str] = UNSET
    phase: Union[Unset, str] = UNSET
    parent_id: Union[Unset, UUID] = UNSET
    unit_first_seen_utc: Union[Unset, datetime.datetime] = UNSET
    unit_first_seen_local: Union[Unset, datetime.datetime] = UNSET
    uut_count: Union[Unset, int] = UNSET
    uur_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        serial_number = self.serial_number

        part_number = self.part_number

        product_name = self.product_name

        entity = self.entity

        process = self.process

        phase = self.phase

        parent_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_id, Unset):
            parent_id = str(self.parent_id)

        unit_first_seen_utc: Union[Unset, str] = UNSET
        if not isinstance(self.unit_first_seen_utc, Unset):
            unit_first_seen_utc = self.unit_first_seen_utc.isoformat()

        unit_first_seen_local: Union[Unset, str] = UNSET
        if not isinstance(self.unit_first_seen_local, Unset):
            unit_first_seen_local = self.unit_first_seen_local.isoformat()

        uut_count = self.uut_count

        uur_count = self.uur_count


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if product_name is not UNSET:
            field_dict["productName"] = product_name
        if entity is not UNSET:
            field_dict["entity"] = entity
        if process is not UNSET:
            field_dict["process"] = process
        if phase is not UNSET:
            field_dict["phase"] = phase
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if unit_first_seen_utc is not UNSET:
            field_dict["unitFirstSeenUtc"] = unit_first_seen_utc
        if unit_first_seen_local is not UNSET:
            field_dict["unitFirstSeenLocal"] = unit_first_seen_local
        if uut_count is not UNSET:
            field_dict["uutCount"] = uut_count
        if uur_count is not UNSET:
            field_dict["uurCount"] = uur_count

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid,  Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)




        serial_number = d.pop("serialNumber", UNSET)

        part_number = d.pop("partNumber", UNSET)

        product_name = d.pop("productName", UNSET)

        entity = d.pop("entity", UNSET)

        process = d.pop("process", UNSET)

        phase = d.pop("phase", UNSET)

        _parent_id = d.pop("parentId", UNSET)
        parent_id: Union[Unset, UUID]
        if isinstance(_parent_id,  Unset):
            parent_id = UNSET
        else:
            parent_id = UUID(_parent_id)




        _unit_first_seen_utc = d.pop("unitFirstSeenUtc", UNSET)
        unit_first_seen_utc: Union[Unset, datetime.datetime]
        if isinstance(_unit_first_seen_utc,  Unset):
            unit_first_seen_utc = UNSET
        else:
            unit_first_seen_utc = isoparse(_unit_first_seen_utc)




        _unit_first_seen_local = d.pop("unitFirstSeenLocal", UNSET)
        unit_first_seen_local: Union[Unset, datetime.datetime]
        if isinstance(_unit_first_seen_local,  Unset):
            unit_first_seen_local = UNSET
        else:
            unit_first_seen_local = isoparse(_unit_first_seen_local)




        uut_count = d.pop("uutCount", UNSET)

        uur_count = d.pop("uurCount", UNSET)

        virinco_wats_web_dashboard_models_sn_history_unit = cls(
            uuid=uuid,
            serial_number=serial_number,
            part_number=part_number,
            product_name=product_name,
            entity=entity,
            process=process,
            phase=phase,
            parent_id=parent_id,
            unit_first_seen_utc=unit_first_seen_utc,
            unit_first_seen_local=unit_first_seen_local,
            uut_count=uut_count,
            uur_count=uur_count,
        )


        virinco_wats_web_dashboard_models_sn_history_unit.additional_properties = d
        return virinco_wats_web_dashboard_models_sn_history_unit

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
