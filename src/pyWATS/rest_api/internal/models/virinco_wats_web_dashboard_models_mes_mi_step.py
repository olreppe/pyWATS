from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_mi_step_add_attachments import VirincoWATSWebDashboardModelsMesMIStepAddAttachments
from ..models.virinco_wats_web_dashboard_models_mes_mi_step_result import VirincoWATSWebDashboardModelsMesMIStepResult
from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesMIStep")



@_attrs_define
class VirincoWATSWebDashboardModelsMesMIStep:
    """ 
        Attributes:
            definition_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            id (Union[Unset, int]):
            parent_id (Union[Unset, int]):
            name (Union[Unset, str]):
            type_ (Union[Unset, str]):
            desc (Union[Unset, str]):
            result (Union[Unset, VirincoWATSWebDashboardModelsMesMIStepResult]):
            operator (Union[Unset, str]):
            url (Union[Unset, str]):
            exec_time (Union[Unset, float]):
            pass_all_affected (Union[Unset, bool]):
            allow_skip (Union[Unset, bool]):
            comment (Union[Unset, str]):
            add_attachments (Union[Unset, VirincoWATSWebDashboardModelsMesMIStepAddAttachments]):
     """

    definition_id: Union[Unset, UUID] = UNSET
    id: Union[Unset, int] = UNSET
    parent_id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    desc: Union[Unset, str] = UNSET
    result: Union[Unset, VirincoWATSWebDashboardModelsMesMIStepResult] = UNSET
    operator: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    exec_time: Union[Unset, float] = UNSET
    pass_all_affected: Union[Unset, bool] = UNSET
    allow_skip: Union[Unset, bool] = UNSET
    comment: Union[Unset, str] = UNSET
    add_attachments: Union[Unset, VirincoWATSWebDashboardModelsMesMIStepAddAttachments] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        definition_id: Union[Unset, str] = UNSET
        if not isinstance(self.definition_id, Unset):
            definition_id = str(self.definition_id)

        id = self.id

        parent_id = self.parent_id

        name = self.name

        type_ = self.type_

        desc = self.desc

        result: Union[Unset, int] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.value


        operator = self.operator

        url = self.url

        exec_time = self.exec_time

        pass_all_affected = self.pass_all_affected

        allow_skip = self.allow_skip

        comment = self.comment

        add_attachments: Union[Unset, int] = UNSET
        if not isinstance(self.add_attachments, Unset):
            add_attachments = self.add_attachments.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if definition_id is not UNSET:
            field_dict["definitionId"] = definition_id
        if id is not UNSET:
            field_dict["id"] = id
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if desc is not UNSET:
            field_dict["desc"] = desc
        if result is not UNSET:
            field_dict["result"] = result
        if operator is not UNSET:
            field_dict["operator"] = operator
        if url is not UNSET:
            field_dict["url"] = url
        if exec_time is not UNSET:
            field_dict["execTime"] = exec_time
        if pass_all_affected is not UNSET:
            field_dict["passAllAffected"] = pass_all_affected
        if allow_skip is not UNSET:
            field_dict["allowSkip"] = allow_skip
        if comment is not UNSET:
            field_dict["comment"] = comment
        if add_attachments is not UNSET:
            field_dict["addAttachments"] = add_attachments

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _definition_id = d.pop("definitionId", UNSET)
        definition_id: Union[Unset, UUID]
        if isinstance(_definition_id,  Unset):
            definition_id = UNSET
        else:
            definition_id = UUID(_definition_id)




        id = d.pop("id", UNSET)

        parent_id = d.pop("parentId", UNSET)

        name = d.pop("name", UNSET)

        type_ = d.pop("type", UNSET)

        desc = d.pop("desc", UNSET)

        _result = d.pop("result", UNSET)
        result: Union[Unset, VirincoWATSWebDashboardModelsMesMIStepResult]
        if isinstance(_result,  Unset):
            result = UNSET
        else:
            result = VirincoWATSWebDashboardModelsMesMIStepResult(_result)




        operator = d.pop("operator", UNSET)

        url = d.pop("url", UNSET)

        exec_time = d.pop("execTime", UNSET)

        pass_all_affected = d.pop("passAllAffected", UNSET)

        allow_skip = d.pop("allowSkip", UNSET)

        comment = d.pop("comment", UNSET)

        _add_attachments = d.pop("addAttachments", UNSET)
        add_attachments: Union[Unset, VirincoWATSWebDashboardModelsMesMIStepAddAttachments]
        if isinstance(_add_attachments,  Unset):
            add_attachments = UNSET
        else:
            add_attachments = VirincoWATSWebDashboardModelsMesMIStepAddAttachments(_add_attachments)




        virinco_wats_web_dashboard_models_mes_mi_step = cls(
            definition_id=definition_id,
            id=id,
            parent_id=parent_id,
            name=name,
            type_=type_,
            desc=desc,
            result=result,
            operator=operator,
            url=url,
            exec_time=exec_time,
            pass_all_affected=pass_all_affected,
            allow_skip=allow_skip,
            comment=comment,
            add_attachments=add_attachments,
        )


        virinco_wats_web_dashboard_models_mes_mi_step.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_mi_step

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
