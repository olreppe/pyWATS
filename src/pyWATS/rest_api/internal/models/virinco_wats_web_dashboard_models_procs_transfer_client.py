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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsProcsTransferClient")



@_attrs_define
class VirincoWATSWebDashboardModelsProcsTransferClient:
    """ 
        Attributes:
            client_id (Union[Unset, int]):
            name (Union[Unset, str]):
            guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            reg_date (Union[Unset, datetime.datetime]):
            status (Union[Unset, int]):
            site_code (Union[Unset, str]):
            misc_info_updated (Union[Unset, datetime.datetime]):
            location (Union[Unset, str]):
            purpose (Union[Unset, str]):
            client_type (Union[Unset, int]):
            utc_offset (Union[Unset, float]):
            description (Union[Unset, str]):
            status_text (Union[Unset, str]):
            machine_account_id (Union[Unset, str]):
            legacy_member_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            misc_info (Union[Unset, str]):
            ext_info (Union[Unset, str]):
            last_ping (Union[Unset, datetime.datetime]):
            parent_name (Union[Unset, str]):
            group_name (Union[Unset, str]):
     """

    client_id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    guid: Union[Unset, UUID] = UNSET
    reg_date: Union[Unset, datetime.datetime] = UNSET
    status: Union[Unset, int] = UNSET
    site_code: Union[Unset, str] = UNSET
    misc_info_updated: Union[Unset, datetime.datetime] = UNSET
    location: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    client_type: Union[Unset, int] = UNSET
    utc_offset: Union[Unset, float] = UNSET
    description: Union[Unset, str] = UNSET
    status_text: Union[Unset, str] = UNSET
    machine_account_id: Union[Unset, str] = UNSET
    legacy_member_id: Union[Unset, UUID] = UNSET
    misc_info: Union[Unset, str] = UNSET
    ext_info: Union[Unset, str] = UNSET
    last_ping: Union[Unset, datetime.datetime] = UNSET
    parent_name: Union[Unset, str] = UNSET
    group_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        name = self.name

        guid: Union[Unset, str] = UNSET
        if not isinstance(self.guid, Unset):
            guid = str(self.guid)

        reg_date: Union[Unset, str] = UNSET
        if not isinstance(self.reg_date, Unset):
            reg_date = self.reg_date.isoformat()

        status = self.status

        site_code = self.site_code

        misc_info_updated: Union[Unset, str] = UNSET
        if not isinstance(self.misc_info_updated, Unset):
            misc_info_updated = self.misc_info_updated.isoformat()

        location = self.location

        purpose = self.purpose

        client_type = self.client_type

        utc_offset = self.utc_offset

        description = self.description

        status_text = self.status_text

        machine_account_id = self.machine_account_id

        legacy_member_id: Union[Unset, str] = UNSET
        if not isinstance(self.legacy_member_id, Unset):
            legacy_member_id = str(self.legacy_member_id)

        misc_info = self.misc_info

        ext_info = self.ext_info

        last_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_ping, Unset):
            last_ping = self.last_ping.isoformat()

        parent_name = self.parent_name

        group_name = self.group_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if client_id is not UNSET:
            field_dict["ClientId"] = client_id
        if name is not UNSET:
            field_dict["Name"] = name
        if guid is not UNSET:
            field_dict["Guid"] = guid
        if reg_date is not UNSET:
            field_dict["RegDate"] = reg_date
        if status is not UNSET:
            field_dict["Status"] = status
        if site_code is not UNSET:
            field_dict["SiteCode"] = site_code
        if misc_info_updated is not UNSET:
            field_dict["MiscInfoUpdated"] = misc_info_updated
        if location is not UNSET:
            field_dict["Location"] = location
        if purpose is not UNSET:
            field_dict["Purpose"] = purpose
        if client_type is not UNSET:
            field_dict["ClientType"] = client_type
        if utc_offset is not UNSET:
            field_dict["UTCOffset"] = utc_offset
        if description is not UNSET:
            field_dict["Description"] = description
        if status_text is not UNSET:
            field_dict["StatusText"] = status_text
        if machine_account_id is not UNSET:
            field_dict["MachineAccountId"] = machine_account_id
        if legacy_member_id is not UNSET:
            field_dict["LegacyMemberId"] = legacy_member_id
        if misc_info is not UNSET:
            field_dict["MiscInfo"] = misc_info
        if ext_info is not UNSET:
            field_dict["ExtInfo"] = ext_info
        if last_ping is not UNSET:
            field_dict["LastPing"] = last_ping
        if parent_name is not UNSET:
            field_dict["ParentName"] = parent_name
        if group_name is not UNSET:
            field_dict["GroupName"] = group_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_id = d.pop("ClientId", UNSET)

        name = d.pop("Name", UNSET)

        _guid = d.pop("Guid", UNSET)
        guid: Union[Unset, UUID]
        if isinstance(_guid,  Unset):
            guid = UNSET
        else:
            guid = UUID(_guid)




        _reg_date = d.pop("RegDate", UNSET)
        reg_date: Union[Unset, datetime.datetime]
        if isinstance(_reg_date,  Unset):
            reg_date = UNSET
        else:
            reg_date = isoparse(_reg_date)




        status = d.pop("Status", UNSET)

        site_code = d.pop("SiteCode", UNSET)

        _misc_info_updated = d.pop("MiscInfoUpdated", UNSET)
        misc_info_updated: Union[Unset, datetime.datetime]
        if isinstance(_misc_info_updated,  Unset):
            misc_info_updated = UNSET
        else:
            misc_info_updated = isoparse(_misc_info_updated)




        location = d.pop("Location", UNSET)

        purpose = d.pop("Purpose", UNSET)

        client_type = d.pop("ClientType", UNSET)

        utc_offset = d.pop("UTCOffset", UNSET)

        description = d.pop("Description", UNSET)

        status_text = d.pop("StatusText", UNSET)

        machine_account_id = d.pop("MachineAccountId", UNSET)

        _legacy_member_id = d.pop("LegacyMemberId", UNSET)
        legacy_member_id: Union[Unset, UUID]
        if isinstance(_legacy_member_id,  Unset):
            legacy_member_id = UNSET
        else:
            legacy_member_id = UUID(_legacy_member_id)




        misc_info = d.pop("MiscInfo", UNSET)

        ext_info = d.pop("ExtInfo", UNSET)

        _last_ping = d.pop("LastPing", UNSET)
        last_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_ping,  Unset):
            last_ping = UNSET
        else:
            last_ping = isoparse(_last_ping)




        parent_name = d.pop("ParentName", UNSET)

        group_name = d.pop("GroupName", UNSET)

        virinco_wats_web_dashboard_models_procs_transfer_client = cls(
            client_id=client_id,
            name=name,
            guid=guid,
            reg_date=reg_date,
            status=status,
            site_code=site_code,
            misc_info_updated=misc_info_updated,
            location=location,
            purpose=purpose,
            client_type=client_type,
            utc_offset=utc_offset,
            description=description,
            status_text=status_text,
            machine_account_id=machine_account_id,
            legacy_member_id=legacy_member_id,
            misc_info=misc_info,
            ext_info=ext_info,
            last_ping=last_ping,
            parent_name=parent_name,
            group_name=group_name,
        )


        virinco_wats_web_dashboard_models_procs_transfer_client.additional_properties = d
        return virinco_wats_web_dashboard_models_procs_transfer_client

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
