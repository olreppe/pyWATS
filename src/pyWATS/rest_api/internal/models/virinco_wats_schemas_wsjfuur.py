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






T = TypeVar("T", bound="VirincoWATSSchemasWSJFUUR")



@_attrs_define
class VirincoWATSSchemasWSJFUUR:
    """ 
        Attributes:
            comment (Union[Unset, str]): Comment of the report.
            user (Union[Unset, str]): Name of repair operator.
            process_code (Union[Unset, int]): Referenced UUT process code.
            process_code_format (Union[Unset, str]): Numeric format of UUT process code.
            process_name (Union[Unset, str]): Referenced UUT process code.
            ref_uut (Union[Unset, UUID]): Referenced UUT id. Example: 00000000-0000-0000-0000-000000000000.
            confirm_date (Union[Unset, datetime.datetime]): Confirm date/time of repair.
            finalize_date (Union[Unset, datetime.datetime]): Finalize date/time of repair.
            exec_time (Union[Unset, float]): Execution time of repair.
            parent (Union[Unset, UUID]): Id of parent repair report. If set, this report will be considered a sub-repair
                report. Example: 00000000-0000-0000-0000-000000000000.
            children (Union[Unset, list[UUID]]): Ids of sub repair reports.
     """

    comment: Union[Unset, str] = UNSET
    user: Union[Unset, str] = UNSET
    process_code: Union[Unset, int] = UNSET
    process_code_format: Union[Unset, str] = UNSET
    process_name: Union[Unset, str] = UNSET
    ref_uut: Union[Unset, UUID] = UNSET
    confirm_date: Union[Unset, datetime.datetime] = UNSET
    finalize_date: Union[Unset, datetime.datetime] = UNSET
    exec_time: Union[Unset, float] = UNSET
    parent: Union[Unset, UUID] = UNSET
    children: Union[Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        comment = self.comment

        user = self.user

        process_code = self.process_code

        process_code_format = self.process_code_format

        process_name = self.process_name

        ref_uut: Union[Unset, str] = UNSET
        if not isinstance(self.ref_uut, Unset):
            ref_uut = str(self.ref_uut)

        confirm_date: Union[Unset, str] = UNSET
        if not isinstance(self.confirm_date, Unset):
            confirm_date = self.confirm_date.isoformat()

        finalize_date: Union[Unset, str] = UNSET
        if not isinstance(self.finalize_date, Unset):
            finalize_date = self.finalize_date.isoformat()

        exec_time = self.exec_time

        parent: Union[Unset, str] = UNSET
        if not isinstance(self.parent, Unset):
            parent = str(self.parent)

        children: Union[Unset, list[str]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = str(children_item_data)
                children.append(children_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if comment is not UNSET:
            field_dict["comment"] = comment
        if user is not UNSET:
            field_dict["user"] = user
        if process_code is not UNSET:
            field_dict["processCode"] = process_code
        if process_code_format is not UNSET:
            field_dict["processCodeFormat"] = process_code_format
        if process_name is not UNSET:
            field_dict["processName"] = process_name
        if ref_uut is not UNSET:
            field_dict["refUUT"] = ref_uut
        if confirm_date is not UNSET:
            field_dict["confirmDate"] = confirm_date
        if finalize_date is not UNSET:
            field_dict["finalizeDate"] = finalize_date
        if exec_time is not UNSET:
            field_dict["execTime"] = exec_time
        if parent is not UNSET:
            field_dict["parent"] = parent
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        comment = d.pop("comment", UNSET)

        user = d.pop("user", UNSET)

        process_code = d.pop("processCode", UNSET)

        process_code_format = d.pop("processCodeFormat", UNSET)

        process_name = d.pop("processName", UNSET)

        _ref_uut = d.pop("refUUT", UNSET)
        ref_uut: Union[Unset, UUID]
        if isinstance(_ref_uut,  Unset):
            ref_uut = UNSET
        else:
            ref_uut = UUID(_ref_uut)




        _confirm_date = d.pop("confirmDate", UNSET)
        confirm_date: Union[Unset, datetime.datetime]
        if isinstance(_confirm_date,  Unset):
            confirm_date = UNSET
        else:
            confirm_date = isoparse(_confirm_date)




        _finalize_date = d.pop("finalizeDate", UNSET)
        finalize_date: Union[Unset, datetime.datetime]
        if isinstance(_finalize_date,  Unset):
            finalize_date = UNSET
        else:
            finalize_date = isoparse(_finalize_date)




        exec_time = d.pop("execTime", UNSET)

        _parent = d.pop("parent", UNSET)
        parent: Union[Unset, UUID]
        if isinstance(_parent,  Unset):
            parent = UNSET
        else:
            parent = UUID(_parent)




        children = []
        _children = d.pop("children", UNSET)
        for children_item_data in (_children or []):
            children_item = UUID(children_item_data)



            children.append(children_item)


        virinco_wats_schemas_wsjfuur = cls(
            comment=comment,
            user=user,
            process_code=process_code,
            process_code_format=process_code_format,
            process_name=process_name,
            ref_uut=ref_uut,
            confirm_date=confirm_date,
            finalize_date=finalize_date,
            exec_time=exec_time,
            parent=parent,
            children=children,
        )


        virinco_wats_schemas_wsjfuur.additional_properties = d
        return virinco_wats_schemas_wsjfuur

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
