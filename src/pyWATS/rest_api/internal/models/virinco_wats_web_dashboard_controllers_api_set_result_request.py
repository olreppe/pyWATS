from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardControllersApiSetResultRequest")



@_attrs_define
class VirincoWATSWebDashboardControllersApiSetResultRequest:
    """ 
        Attributes:
            rulename (Union[Unset, str]):
            uuid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            result (Union[Unset, int]):
            message (Union[Unset, str]):
     """

    rulename: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    result: Union[Unset, int] = UNSET
    message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        rulename = self.rulename

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        result = self.result

        message = self.message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if rulename is not UNSET:
            field_dict["rulename"] = rulename
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if result is not UNSET:
            field_dict["result"] = result
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rulename = d.pop("rulename", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid,  Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)




        result = d.pop("result", UNSET)

        message = d.pop("message", UNSET)

        virinco_wats_web_dashboard_controllers_api_set_result_request = cls(
            rulename=rulename,
            uuid=uuid,
            result=result,
            message=message,
        )


        virinco_wats_web_dashboard_controllers_api_set_result_request.additional_properties = d
        return virinco_wats_web_dashboard_controllers_api_set_result_request

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
