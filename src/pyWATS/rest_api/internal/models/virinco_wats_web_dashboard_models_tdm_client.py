from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_tdm_client_client_type import VirincoWATSWebDashboardModelsTdmClientClientType
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmClient")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmClient:
    """ 
        Attributes:
            Client_ID (Union[Unset, int]):
            ClientId (Union[Unset, int]):
            name (Union[Unset, str]):
            display_name (Union[Unset, str]):
            guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            reg_date (Union[Unset, datetime.datetime]):
            status (Union[Unset, int]):
            parent_id (Union[Unset, int]):
            client_group_id (Union[Unset, int]):
            misc_info (Union[Unset, str]):
            misc_info_updated (Union[Unset, datetime.datetime]):
            location (Union[Unset, str]):
            purpose (Union[Unset, str]):
            client_type (Union[Unset, VirincoWATSWebDashboardModelsTdmClientClientType]):
            utc_offset (Union[Unset, float]):
            description (Union[Unset, str]):
            last_ping (Union[Unset, datetime.datetime]):
            status_text (Union[Unset, str]):
            machine_account_id (Union[Unset, str]):
            site_code (Union[Unset, str]):
     """

    Client_ID: Union[Unset, int] = UNSET
    ClientId: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    guid: Union[Unset, UUID] = UNSET
    reg_date: Union[Unset, datetime.datetime] = UNSET
    status: Union[Unset, int] = UNSET
    parent_id: Union[Unset, int] = UNSET
    client_group_id: Union[Unset, int] = UNSET
    misc_info: Union[Unset, str] = UNSET
    misc_info_updated: Union[Unset, datetime.datetime] = UNSET
    location: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    client_type: Union[Unset, VirincoWATSWebDashboardModelsTdmClientClientType] = UNSET
    utc_offset: Union[Unset, float] = UNSET
    description: Union[Unset, str] = UNSET
    last_ping: Union[Unset, datetime.datetime] = UNSET
    status_text: Union[Unset, str] = UNSET
    machine_account_id: Union[Unset, str] = UNSET
    site_code: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        Client_ID = self.Client_ID

        ClientId = self.ClientId

        name = self.name

        display_name = self.display_name

        guid: Union[Unset, str] = UNSET
        if not isinstance(self.guid, Unset):
            guid = str(self.guid)

        reg_date: Union[Unset, str] = UNSET
        if not isinstance(self.reg_date, Unset):
            reg_date = self.reg_date.isoformat()

        status = self.status

        parent_id = self.parent_id

        client_group_id = self.client_group_id

        misc_info = self.misc_info

        misc_info_updated: Union[Unset, str] = UNSET
        if not isinstance(self.misc_info_updated, Unset):
            misc_info_updated = self.misc_info_updated.isoformat()

        location = self.location

        purpose = self.purpose

        client_type: Union[Unset, int] = UNSET
        if not isinstance(self.client_type, Unset):
            client_type = self.client_type.value


        utc_offset = self.utc_offset

        description = self.description

        last_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_ping, Unset):
            last_ping = self.last_ping.isoformat()

        status_text = self.status_text

        machine_account_id = self.machine_account_id

        site_code = self.site_code


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if Client_ID is not UNSET:
            field_dict["Client_ID"] = Client_ID
        if ClientId is not UNSET:
            field_dict["ClientId"] = ClientId
        if name is not UNSET:
            field_dict["Name"] = name
        if display_name is not UNSET:
            field_dict["DisplayName"] = display_name
        if guid is not UNSET:
            field_dict["GUID"] = guid
        if reg_date is not UNSET:
            field_dict["RegDate"] = reg_date
        if status is not UNSET:
            field_dict["Status"] = status
        if parent_id is not UNSET:
            field_dict["ParentId"] = parent_id
        if client_group_id is not UNSET:
            field_dict["ClientGroupId"] = client_group_id
        if misc_info is not UNSET:
            field_dict["MiscInfo"] = misc_info
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
        if last_ping is not UNSET:
            field_dict["LastPing"] = last_ping
        if status_text is not UNSET:
            field_dict["StatusText"] = status_text
        if machine_account_id is not UNSET:
            field_dict["MachineAccountId"] = machine_account_id
        if site_code is not UNSET:
            field_dict["SiteCode"] = site_code

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        Client_ID = d.pop("Client_ID", UNSET)

        ClientId = d.pop("ClientId", UNSET)

        name = d.pop("Name", UNSET)

        display_name = d.pop("DisplayName", UNSET)

        _guid = d.pop("GUID", UNSET)
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

        parent_id = d.pop("ParentId", UNSET)

        client_group_id = d.pop("ClientGroupId", UNSET)

        misc_info = d.pop("MiscInfo", UNSET)

        _misc_info_updated = d.pop("MiscInfoUpdated", UNSET)
        misc_info_updated: Union[Unset, datetime.datetime]
        if isinstance(_misc_info_updated,  Unset):
            misc_info_updated = UNSET
        else:
            misc_info_updated = isoparse(_misc_info_updated)




        location = d.pop("Location", UNSET)

        purpose = d.pop("Purpose", UNSET)

        _client_type = d.pop("ClientType", UNSET)
        client_type: Union[Unset, VirincoWATSWebDashboardModelsTdmClientClientType]
        if isinstance(_client_type,  Unset):
            client_type = UNSET
        else:
            client_type = VirincoWATSWebDashboardModelsTdmClientClientType(_client_type)




        utc_offset = d.pop("UTCOffset", UNSET)

        description = d.pop("Description", UNSET)

        _last_ping = d.pop("LastPing", UNSET)
        last_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_ping,  Unset):
            last_ping = UNSET
        else:
            last_ping = isoparse(_last_ping)




        status_text = d.pop("StatusText", UNSET)

        machine_account_id = d.pop("MachineAccountId", UNSET)

        site_code = d.pop("SiteCode", UNSET)

        virinco_wats_web_dashboard_models_tdm_client = cls(
            Client_ID=Client_ID,
            ClientId=ClientId,
            name=name,
            display_name=display_name,
            guid=guid,
            reg_date=reg_date,
            status=status,
            parent_id=parent_id,
            client_group_id=client_group_id,
            misc_info=misc_info,
            misc_info_updated=misc_info_updated,
            location=location,
            purpose=purpose,
            client_type=client_type,
            utc_offset=utc_offset,
            description=description,
            last_ping=last_ping,
            status_text=status_text,
            machine_account_id=machine_account_id,
            site_code=site_code,
        )


        virinco_wats_web_dashboard_models_tdm_client.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_client

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
