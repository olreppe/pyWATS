from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardControllersApiTransferResultRequest")



@_attrs_define
class VirincoWATSWebDashboardControllersApiTransferResultRequest:
    """ 
        Attributes:
            uuid (Union[Unset, UUID]): Report UUID Example: 00000000-0000-0000-0000-000000000000.
            st (Union[Unset, str]): Transfer-state

                Acknowledged transfer-states:
                 P Pending		Not started (or reset) - default value (old value: 0)
                 R Reserved		Reserved by package (old value: 1)
                 T Transferring	Transfer in progress - dequeued for transfer, (old value: 2)
                 S Stopped		Transfer cancelled - dequeued during TA Stop, (old value: 6)
                 F Failed		Transfer failed - set by SetTransferResult (old value: 7)
                 C Completed    Transfer completed - is never set in tx.pending. Will cause pending record to move into
                tx.processed (old value: 16 or 24)
            msg (Union[Unset, str]): Transfer result or error message
     """

    uuid: Union[Unset, UUID] = UNSET
    st: Union[Unset, str] = UNSET
    msg: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        st = self.st

        msg = self.msg


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if st is not UNSET:
            field_dict["st"] = st
        if msg is not UNSET:
            field_dict["msg"] = msg

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




        st = d.pop("st", UNSET)

        msg = d.pop("msg", UNSET)

        virinco_wats_web_dashboard_controllers_api_transfer_result_request = cls(
            uuid=uuid,
            st=st,
            msg=msg,
        )


        virinco_wats_web_dashboard_controllers_api_transfer_result_request.additional_properties = d
        return virinco_wats_web_dashboard_controllers_api_transfer_result_request

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
