from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_asset_o_data_asset_state import VirincoWATSWebDashboardModelsMesAssetODataAssetState
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesAssetODataAsset")



@_attrs_define
class VirincoWATSWebDashboardModelsMesAssetODataAsset:
    """ 
        Attributes:
            asset_id (Union[Unset, str]):
            parent_asset_id (Union[Unset, str]):
            asset_name (Union[Unset, str]):
            serial_number (Union[Unset, str]):
            parent_serial_number (Union[Unset, str]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            type_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            state (Union[Unset, VirincoWATSWebDashboardModelsMesAssetODataAssetState]):
            description (Union[Unset, str]):
            location (Union[Unset, str]):
            first_seen_date (Union[Unset, datetime.datetime]):
            last_seen_date (Union[Unset, datetime.datetime]):
            last_maintenance_date (Union[Unset, datetime.datetime]):
            next_maintenance_date (Union[Unset, datetime.datetime]):
            last_calibration_date (Union[Unset, datetime.datetime]):
            next_calibration_date (Union[Unset, datetime.datetime]):
            total_count (Union[Unset, int]):
            running_count (Union[Unset, int]):
            xml_data (Union[Unset, str]): Use an XPath to filter by tags. Only supports the 'eq' operator. Returns as an XML
                string.
     """

    asset_id: Union[Unset, str] = UNSET
    parent_asset_id: Union[Unset, str] = UNSET
    asset_name: Union[Unset, str] = UNSET
    serial_number: Union[Unset, str] = UNSET
    parent_serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    type_id: Union[Unset, UUID] = UNSET
    state: Union[Unset, VirincoWATSWebDashboardModelsMesAssetODataAssetState] = UNSET
    description: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    first_seen_date: Union[Unset, datetime.datetime] = UNSET
    last_seen_date: Union[Unset, datetime.datetime] = UNSET
    last_maintenance_date: Union[Unset, datetime.datetime] = UNSET
    next_maintenance_date: Union[Unset, datetime.datetime] = UNSET
    last_calibration_date: Union[Unset, datetime.datetime] = UNSET
    next_calibration_date: Union[Unset, datetime.datetime] = UNSET
    total_count: Union[Unset, int] = UNSET
    running_count: Union[Unset, int] = UNSET
    xml_data: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        asset_id = self.asset_id

        parent_asset_id = self.parent_asset_id

        asset_name = self.asset_name

        serial_number = self.serial_number

        parent_serial_number = self.parent_serial_number

        part_number = self.part_number

        revision = self.revision

        type_id: Union[Unset, str] = UNSET
        if not isinstance(self.type_id, Unset):
            type_id = str(self.type_id)

        state: Union[Unset, int] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value


        description = self.description

        location = self.location

        first_seen_date: Union[Unset, str] = UNSET
        if not isinstance(self.first_seen_date, Unset):
            first_seen_date = self.first_seen_date.isoformat()

        last_seen_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_seen_date, Unset):
            last_seen_date = self.last_seen_date.isoformat()

        last_maintenance_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_maintenance_date, Unset):
            last_maintenance_date = self.last_maintenance_date.isoformat()

        next_maintenance_date: Union[Unset, str] = UNSET
        if not isinstance(self.next_maintenance_date, Unset):
            next_maintenance_date = self.next_maintenance_date.isoformat()

        last_calibration_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_calibration_date, Unset):
            last_calibration_date = self.last_calibration_date.isoformat()

        next_calibration_date: Union[Unset, str] = UNSET
        if not isinstance(self.next_calibration_date, Unset):
            next_calibration_date = self.next_calibration_date.isoformat()

        total_count = self.total_count

        running_count = self.running_count

        xml_data = self.xml_data


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if asset_id is not UNSET:
            field_dict["assetId"] = asset_id
        if parent_asset_id is not UNSET:
            field_dict["parentAssetId"] = parent_asset_id
        if asset_name is not UNSET:
            field_dict["assetName"] = asset_name
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if parent_serial_number is not UNSET:
            field_dict["parentSerialNumber"] = parent_serial_number
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if type_id is not UNSET:
            field_dict["typeId"] = type_id
        if state is not UNSET:
            field_dict["state"] = state
        if description is not UNSET:
            field_dict["description"] = description
        if location is not UNSET:
            field_dict["location"] = location
        if first_seen_date is not UNSET:
            field_dict["firstSeenDate"] = first_seen_date
        if last_seen_date is not UNSET:
            field_dict["lastSeenDate"] = last_seen_date
        if last_maintenance_date is not UNSET:
            field_dict["lastMaintenanceDate"] = last_maintenance_date
        if next_maintenance_date is not UNSET:
            field_dict["nextMaintenanceDate"] = next_maintenance_date
        if last_calibration_date is not UNSET:
            field_dict["lastCalibrationDate"] = last_calibration_date
        if next_calibration_date is not UNSET:
            field_dict["nextCalibrationDate"] = next_calibration_date
        if total_count is not UNSET:
            field_dict["totalCount"] = total_count
        if running_count is not UNSET:
            field_dict["runningCount"] = running_count
        if xml_data is not UNSET:
            field_dict["xmlData"] = xml_data

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        asset_id = d.pop("assetId", UNSET)

        parent_asset_id = d.pop("parentAssetId", UNSET)

        asset_name = d.pop("assetName", UNSET)

        serial_number = d.pop("serialNumber", UNSET)

        parent_serial_number = d.pop("parentSerialNumber", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        _type_id = d.pop("typeId", UNSET)
        type_id: Union[Unset, UUID]
        if isinstance(_type_id,  Unset):
            type_id = UNSET
        else:
            type_id = UUID(_type_id)




        _state = d.pop("state", UNSET)
        state: Union[Unset, VirincoWATSWebDashboardModelsMesAssetODataAssetState]
        if isinstance(_state,  Unset):
            state = UNSET
        else:
            state = VirincoWATSWebDashboardModelsMesAssetODataAssetState(_state)




        description = d.pop("description", UNSET)

        location = d.pop("location", UNSET)

        _first_seen_date = d.pop("firstSeenDate", UNSET)
        first_seen_date: Union[Unset, datetime.datetime]
        if isinstance(_first_seen_date,  Unset):
            first_seen_date = UNSET
        else:
            first_seen_date = isoparse(_first_seen_date)




        _last_seen_date = d.pop("lastSeenDate", UNSET)
        last_seen_date: Union[Unset, datetime.datetime]
        if isinstance(_last_seen_date,  Unset):
            last_seen_date = UNSET
        else:
            last_seen_date = isoparse(_last_seen_date)




        _last_maintenance_date = d.pop("lastMaintenanceDate", UNSET)
        last_maintenance_date: Union[Unset, datetime.datetime]
        if isinstance(_last_maintenance_date,  Unset):
            last_maintenance_date = UNSET
        else:
            last_maintenance_date = isoparse(_last_maintenance_date)




        _next_maintenance_date = d.pop("nextMaintenanceDate", UNSET)
        next_maintenance_date: Union[Unset, datetime.datetime]
        if isinstance(_next_maintenance_date,  Unset):
            next_maintenance_date = UNSET
        else:
            next_maintenance_date = isoparse(_next_maintenance_date)




        _last_calibration_date = d.pop("lastCalibrationDate", UNSET)
        last_calibration_date: Union[Unset, datetime.datetime]
        if isinstance(_last_calibration_date,  Unset):
            last_calibration_date = UNSET
        else:
            last_calibration_date = isoparse(_last_calibration_date)




        _next_calibration_date = d.pop("nextCalibrationDate", UNSET)
        next_calibration_date: Union[Unset, datetime.datetime]
        if isinstance(_next_calibration_date,  Unset):
            next_calibration_date = UNSET
        else:
            next_calibration_date = isoparse(_next_calibration_date)




        total_count = d.pop("totalCount", UNSET)

        running_count = d.pop("runningCount", UNSET)

        xml_data = d.pop("xmlData", UNSET)

        virinco_wats_web_dashboard_models_mes_asset_o_data_asset = cls(
            asset_id=asset_id,
            parent_asset_id=parent_asset_id,
            asset_name=asset_name,
            serial_number=serial_number,
            parent_serial_number=parent_serial_number,
            part_number=part_number,
            revision=revision,
            type_id=type_id,
            state=state,
            description=description,
            location=location,
            first_seen_date=first_seen_date,
            last_seen_date=last_seen_date,
            last_maintenance_date=last_maintenance_date,
            next_maintenance_date=next_maintenance_date,
            last_calibration_date=last_calibration_date,
            next_calibration_date=next_calibration_date,
            total_count=total_count,
            running_count=running_count,
            xml_data=xml_data,
        )


        virinco_wats_web_dashboard_models_mes_asset_o_data_asset.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_asset_o_data_asset

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
