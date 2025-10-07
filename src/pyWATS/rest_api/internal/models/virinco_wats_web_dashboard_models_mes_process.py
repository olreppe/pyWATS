from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProcess")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProcess:
    """ 
        Attributes:
            code (Union[Unset, int]):
            process_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            process_index (Union[Unset, int]):
            state (Union[Unset, int]):
            properties (Union[Unset, str]):
            is_test_operation (Union[Unset, bool]):
            is_wip_operation (Union[Unset, bool]):
            is_repair_operation (Union[Unset, bool]):
     """

    code: Union[Unset, int] = UNSET
    process_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    process_index: Union[Unset, int] = UNSET
    state: Union[Unset, int] = UNSET
    properties: Union[Unset, str] = UNSET
    is_test_operation: Union[Unset, bool] = UNSET
    is_wip_operation: Union[Unset, bool] = UNSET
    is_repair_operation: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        code = self.code

        process_id: Union[Unset, str] = UNSET
        if not isinstance(self.process_id, Unset):
            process_id = str(self.process_id)

        name = self.name

        description = self.description

        process_index = self.process_index

        state = self.state

        properties = self.properties

        is_test_operation = self.is_test_operation

        is_wip_operation = self.is_wip_operation

        is_repair_operation = self.is_repair_operation


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if code is not UNSET:
            field_dict["Code"] = code
        if process_id is not UNSET:
            field_dict["ProcessID"] = process_id
        if name is not UNSET:
            field_dict["Name"] = name
        if description is not UNSET:
            field_dict["Description"] = description
        if process_index is not UNSET:
            field_dict["ProcessIndex"] = process_index
        if state is not UNSET:
            field_dict["State"] = state
        if properties is not UNSET:
            field_dict["Properties"] = properties
        if is_test_operation is not UNSET:
            field_dict["IsTestOperation"] = is_test_operation
        if is_wip_operation is not UNSET:
            field_dict["IsWIPOperation"] = is_wip_operation
        if is_repair_operation is not UNSET:
            field_dict["IsRepairOperation"] = is_repair_operation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("Code", UNSET)

        _process_id = d.pop("ProcessID", UNSET)
        process_id: Union[Unset, UUID]
        if isinstance(_process_id,  Unset):
            process_id = UNSET
        else:
            process_id = UUID(_process_id)




        name = d.pop("Name", UNSET)

        description = d.pop("Description", UNSET)

        process_index = d.pop("ProcessIndex", UNSET)

        state = d.pop("State", UNSET)

        properties = d.pop("Properties", UNSET)

        is_test_operation = d.pop("IsTestOperation", UNSET)

        is_wip_operation = d.pop("IsWIPOperation", UNSET)

        is_repair_operation = d.pop("IsRepairOperation", UNSET)

        virinco_wats_web_dashboard_models_mes_process = cls(
            code=code,
            process_id=process_id,
            name=name,
            description=description,
            process_index=process_index,
            state=state,
            properties=properties,
            is_test_operation=is_test_operation,
            is_wip_operation=is_wip_operation,
            is_repair_operation=is_repair_operation,
        )


        virinco_wats_web_dashboard_models_mes_process.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_process

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
