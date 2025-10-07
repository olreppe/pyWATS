from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_manager_entity_state import VirincoWATSWebDashboardModelsMesAssetAssetManagerEntityState
from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_manager_entity_status import VirincoWATSWebDashboardModelsMesAssetAssetManagerEntityStatus
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_file import VirincoWATSWebDashboardModelsMesAssetAssetFile





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity")



@_attrs_define
class VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity:
    """ 
        Attributes:
            id (Union[Unset, str]):
            parent_id (Union[Unset, str]):
            entity_type (Union[Unset, str]):
            name (Union[Unset, str]):
            location (Union[Unset, str]):
            serial_number (Union[Unset, str]):
            description (Union[Unset, str]):
            type_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            state (Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetManagerEntityState]):
            status (Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetManagerEntityStatus]):
            first_seen_date (Union[Unset, datetime.datetime]):
            last_seen_date (Union[Unset, datetime.datetime]):
            running_count (Union[Unset, int]):
            total_count (Union[Unset, int]):
            last_calibration_date (Union[Unset, datetime.datetime]):
            last_maintenance_date (Union[Unset, datetime.datetime]):
            next_calibration_date (Union[Unset, datetime.datetime]):
            next_maintenance_date (Union[Unset, datetime.datetime]):
            client_id (Union[Unset, int]):
            image_id (Union[Unset, str]):
            files (Union[Unset, list['VirincoWATSWebDashboardModelsMesAssetAssetFile']]):
     """

    id: Union[Unset, str] = UNSET
    parent_id: Union[Unset, str] = UNSET
    entity_type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    serial_number: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    type_id: Union[Unset, UUID] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    state: Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetManagerEntityState] = UNSET
    status: Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetManagerEntityStatus] = UNSET
    first_seen_date: Union[Unset, datetime.datetime] = UNSET
    last_seen_date: Union[Unset, datetime.datetime] = UNSET
    running_count: Union[Unset, int] = UNSET
    total_count: Union[Unset, int] = UNSET
    last_calibration_date: Union[Unset, datetime.datetime] = UNSET
    last_maintenance_date: Union[Unset, datetime.datetime] = UNSET
    next_calibration_date: Union[Unset, datetime.datetime] = UNSET
    next_maintenance_date: Union[Unset, datetime.datetime] = UNSET
    client_id: Union[Unset, int] = UNSET
    image_id: Union[Unset, str] = UNSET
    files: Union[Unset, list['VirincoWATSWebDashboardModelsMesAssetAssetFile']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_file import VirincoWATSWebDashboardModelsMesAssetAssetFile
        id = self.id

        parent_id = self.parent_id

        entity_type = self.entity_type

        name = self.name

        location = self.location

        serial_number = self.serial_number

        description = self.description

        type_id: Union[Unset, str] = UNSET
        if not isinstance(self.type_id, Unset):
            type_id = str(self.type_id)

        part_number = self.part_number

        revision = self.revision

        state: Union[Unset, int] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value


        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value


        first_seen_date: Union[Unset, str] = UNSET
        if not isinstance(self.first_seen_date, Unset):
            first_seen_date = self.first_seen_date.isoformat()

        last_seen_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_seen_date, Unset):
            last_seen_date = self.last_seen_date.isoformat()

        running_count = self.running_count

        total_count = self.total_count

        last_calibration_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_calibration_date, Unset):
            last_calibration_date = self.last_calibration_date.isoformat()

        last_maintenance_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_maintenance_date, Unset):
            last_maintenance_date = self.last_maintenance_date.isoformat()

        next_calibration_date: Union[Unset, str] = UNSET
        if not isinstance(self.next_calibration_date, Unset):
            next_calibration_date = self.next_calibration_date.isoformat()

        next_maintenance_date: Union[Unset, str] = UNSET
        if not isinstance(self.next_maintenance_date, Unset):
            next_maintenance_date = self.next_maintenance_date.isoformat()

        client_id = self.client_id

        image_id = self.image_id

        files: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if entity_type is not UNSET:
            field_dict["entityType"] = entity_type
        if name is not UNSET:
            field_dict["name"] = name
        if location is not UNSET:
            field_dict["location"] = location
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if description is not UNSET:
            field_dict["description"] = description
        if type_id is not UNSET:
            field_dict["typeId"] = type_id
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if state is not UNSET:
            field_dict["state"] = state
        if status is not UNSET:
            field_dict["status"] = status
        if first_seen_date is not UNSET:
            field_dict["firstSeenDate"] = first_seen_date
        if last_seen_date is not UNSET:
            field_dict["lastSeenDate"] = last_seen_date
        if running_count is not UNSET:
            field_dict["runningCount"] = running_count
        if total_count is not UNSET:
            field_dict["totalCount"] = total_count
        if last_calibration_date is not UNSET:
            field_dict["lastCalibrationDate"] = last_calibration_date
        if last_maintenance_date is not UNSET:
            field_dict["lastMaintenanceDate"] = last_maintenance_date
        if next_calibration_date is not UNSET:
            field_dict["nextCalibrationDate"] = next_calibration_date
        if next_maintenance_date is not UNSET:
            field_dict["nextMaintenanceDate"] = next_maintenance_date
        if client_id is not UNSET:
            field_dict["clientId"] = client_id
        if image_id is not UNSET:
            field_dict["imageId"] = image_id
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_file import VirincoWATSWebDashboardModelsMesAssetAssetFile
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        parent_id = d.pop("parentId", UNSET)

        entity_type = d.pop("entityType", UNSET)

        name = d.pop("name", UNSET)

        location = d.pop("location", UNSET)

        serial_number = d.pop("serialNumber", UNSET)

        description = d.pop("description", UNSET)

        _type_id = d.pop("typeId", UNSET)
        type_id: Union[Unset, UUID]
        if isinstance(_type_id,  Unset):
            type_id = UNSET
        else:
            type_id = UUID(_type_id)




        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetManagerEntityState]
        if isinstance(_state,  Unset):
            state = UNSET
        else:
            state = VirincoWATSWebDashboardModelsMesAssetAssetManagerEntityState(_state)




        _status = d.pop("status", UNSET)
        status: Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetManagerEntityStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = VirincoWATSWebDashboardModelsMesAssetAssetManagerEntityStatus(_status)




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




        running_count = d.pop("runningCount", UNSET)

        total_count = d.pop("totalCount", UNSET)

        _last_calibration_date = d.pop("lastCalibrationDate", UNSET)
        last_calibration_date: Union[Unset, datetime.datetime]
        if isinstance(_last_calibration_date,  Unset):
            last_calibration_date = UNSET
        else:
            last_calibration_date = isoparse(_last_calibration_date)




        _last_maintenance_date = d.pop("lastMaintenanceDate", UNSET)
        last_maintenance_date: Union[Unset, datetime.datetime]
        if isinstance(_last_maintenance_date,  Unset):
            last_maintenance_date = UNSET
        else:
            last_maintenance_date = isoparse(_last_maintenance_date)




        _next_calibration_date = d.pop("nextCalibrationDate", UNSET)
        next_calibration_date: Union[Unset, datetime.datetime]
        if isinstance(_next_calibration_date,  Unset):
            next_calibration_date = UNSET
        else:
            next_calibration_date = isoparse(_next_calibration_date)




        _next_maintenance_date = d.pop("nextMaintenanceDate", UNSET)
        next_maintenance_date: Union[Unset, datetime.datetime]
        if isinstance(_next_maintenance_date,  Unset):
            next_maintenance_date = UNSET
        else:
            next_maintenance_date = isoparse(_next_maintenance_date)




        client_id = d.pop("clientId", UNSET)

        image_id = d.pop("imageId", UNSET)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in (_files or []):
            files_item = VirincoWATSWebDashboardModelsMesAssetAssetFile.from_dict(files_item_data)



            files.append(files_item)


        virinco_wats_web_dashboard_models_mes_asset_asset_manager_entity = cls(
            id=id,
            parent_id=parent_id,
            entity_type=entity_type,
            name=name,
            location=location,
            serial_number=serial_number,
            description=description,
            type_id=type_id,
            part_number=part_number,
            revision=revision,
            state=state,
            status=status,
            first_seen_date=first_seen_date,
            last_seen_date=last_seen_date,
            running_count=running_count,
            total_count=total_count,
            last_calibration_date=last_calibration_date,
            last_maintenance_date=last_maintenance_date,
            next_calibration_date=next_calibration_date,
            next_maintenance_date=next_maintenance_date,
            client_id=client_id,
            image_id=image_id,
            files=files,
        )


        virinco_wats_web_dashboard_models_mes_asset_asset_manager_entity.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_asset_asset_manager_entity

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
