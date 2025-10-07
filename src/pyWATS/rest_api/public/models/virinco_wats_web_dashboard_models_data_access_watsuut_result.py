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

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_data_access_watsuut_misc import VirincoWATSWebDashboardModelsDataAccessWATSUUTMisc





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsDataAccessWATSUUTResult")



@_attrs_define
class VirincoWATSWebDashboardModelsDataAccessWATSUUTResult:
    """ 
        Attributes:
            misc_data (Union[Unset, list['VirincoWATSWebDashboardModelsDataAccessWATSUUTMisc']]):
            serial_number (Union[Unset, str]):
            part_number (Union[Unset, str]):
            start (Union[Unset, datetime.datetime]):
            result (Union[Unset, str]):
            uuid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            process_code (Union[Unset, int]):
            process_name (Union[Unset, str]):
     """

    misc_data: Union[Unset, list['VirincoWATSWebDashboardModelsDataAccessWATSUUTMisc']] = UNSET
    serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    start: Union[Unset, datetime.datetime] = UNSET
    result: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    process_code: Union[Unset, int] = UNSET
    process_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_data_access_watsuut_misc import VirincoWATSWebDashboardModelsDataAccessWATSUUTMisc
        misc_data: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.misc_data, Unset):
            misc_data = []
            for misc_data_item_data in self.misc_data:
                misc_data_item = misc_data_item_data.to_dict()
                misc_data.append(misc_data_item)



        serial_number = self.serial_number

        part_number = self.part_number

        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        result = self.result

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        process_code = self.process_code

        process_name = self.process_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if misc_data is not UNSET:
            field_dict["miscData"] = misc_data
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if start is not UNSET:
            field_dict["start"] = start
        if result is not UNSET:
            field_dict["result"] = result
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if process_code is not UNSET:
            field_dict["processCode"] = process_code
        if process_name is not UNSET:
            field_dict["processName"] = process_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_data_access_watsuut_misc import VirincoWATSWebDashboardModelsDataAccessWATSUUTMisc
        d = dict(src_dict)
        misc_data = []
        _misc_data = d.pop("miscData", UNSET)
        for misc_data_item_data in (_misc_data or []):
            misc_data_item = VirincoWATSWebDashboardModelsDataAccessWATSUUTMisc.from_dict(misc_data_item_data)



            misc_data.append(misc_data_item)


        serial_number = d.pop("serialNumber", UNSET)

        part_number = d.pop("partNumber", UNSET)

        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.datetime]
        if isinstance(_start,  Unset):
            start = UNSET
        else:
            start = isoparse(_start)




        result = d.pop("result", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid,  Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)




        process_code = d.pop("processCode", UNSET)

        process_name = d.pop("processName", UNSET)

        virinco_wats_web_dashboard_models_data_access_watsuut_result = cls(
            misc_data=misc_data,
            serial_number=serial_number,
            part_number=part_number,
            start=start,
            result=result,
            uuid=uuid,
            process_code=process_code,
            process_name=process_name,
        )


        virinco_wats_web_dashboard_models_data_access_watsuut_result.additional_properties = d
        return virinco_wats_web_dashboard_models_data_access_watsuut_result

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
