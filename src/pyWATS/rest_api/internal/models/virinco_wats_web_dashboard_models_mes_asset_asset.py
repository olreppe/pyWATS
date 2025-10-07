from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_state import VirincoWATSWebDashboardModelsMesAssetAssetState
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_type import VirincoWATSWebDashboardModelsMesAssetAssetType
  from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
  from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_log import VirincoWATSWebDashboardModelsMesAssetAssetLog





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesAssetAsset")



@_attrs_define
class VirincoWATSWebDashboardModelsMesAssetAsset:
    """ External Asset Model (Public REST API)

        Attributes:
            serial_number (str):
            type_id (UUID):  Example: 00000000-0000-0000-0000-000000000000.
            asset_id (Union[Unset, str]):
            parent_asset_id (Union[Unset, str]):
            parent_serial_number (Union[Unset, str]):
            asset_name (Union[Unset, str]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            client_id (Union[Unset, int]):
            state (Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetState]):
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
            tags (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']]):
            asset_children (Union[Unset, list['VirincoWATSWebDashboardModelsMesAssetAsset']]):
            asset_type (Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetType]):
            asset_log (Union[Unset, list['VirincoWATSWebDashboardModelsMesAssetAssetLog']]):
     """

    serial_number: str
    type_id: UUID
    asset_id: Union[Unset, str] = UNSET
    parent_asset_id: Union[Unset, str] = UNSET
    parent_serial_number: Union[Unset, str] = UNSET
    asset_name: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    client_id: Union[Unset, int] = UNSET
    state: Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetState] = UNSET
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
    tags: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']] = UNSET
    asset_children: Union[Unset, list['VirincoWATSWebDashboardModelsMesAssetAsset']] = UNSET
    asset_type: Union[Unset, 'VirincoWATSWebDashboardModelsMesAssetAssetType'] = UNSET
    asset_log: Union[Unset, list['VirincoWATSWebDashboardModelsMesAssetAssetLog']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_type import VirincoWATSWebDashboardModelsMesAssetAssetType
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_log import VirincoWATSWebDashboardModelsMesAssetAssetLog
        serial_number = self.serial_number

        type_id = str(self.type_id)

        asset_id = self.asset_id

        parent_asset_id = self.parent_asset_id

        parent_serial_number = self.parent_serial_number

        asset_name = self.asset_name

        part_number = self.part_number

        revision = self.revision

        client_id = self.client_id

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

        tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)



        asset_children: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.asset_children, Unset):
            asset_children = []
            for asset_children_item_data in self.asset_children:
                asset_children_item = asset_children_item_data.to_dict()
                asset_children.append(asset_children_item)



        asset_type: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.asset_type, Unset):
            asset_type = self.asset_type.to_dict()

        asset_log: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.asset_log, Unset):
            asset_log = []
            for asset_log_item_data in self.asset_log:
                asset_log_item = asset_log_item_data.to_dict()
                asset_log.append(asset_log_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "serialNumber": serial_number,
            "typeId": type_id,
        })
        if asset_id is not UNSET:
            field_dict["assetId"] = asset_id
        if parent_asset_id is not UNSET:
            field_dict["parentAssetId"] = parent_asset_id
        if parent_serial_number is not UNSET:
            field_dict["parentSerialNumber"] = parent_serial_number
        if asset_name is not UNSET:
            field_dict["assetName"] = asset_name
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if client_id is not UNSET:
            field_dict["ClientId"] = client_id
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
        if tags is not UNSET:
            field_dict["tags"] = tags
        if asset_children is not UNSET:
            field_dict["assetChildren"] = asset_children
        if asset_type is not UNSET:
            field_dict["assetType"] = asset_type
        if asset_log is not UNSET:
            field_dict["assetLog"] = asset_log

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_type import VirincoWATSWebDashboardModelsMesAssetAssetType
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_log import VirincoWATSWebDashboardModelsMesAssetAssetLog
        d = dict(src_dict)
        serial_number = d.pop("serialNumber")

        type_id = UUID(d.pop("typeId"))




        asset_id = d.pop("assetId", UNSET)

        parent_asset_id = d.pop("parentAssetId", UNSET)

        parent_serial_number = d.pop("parentSerialNumber", UNSET)

        asset_name = d.pop("assetName", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        client_id = d.pop("ClientId", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetState]
        if isinstance(_state,  Unset):
            state = UNSET
        else:
            state = VirincoWATSWebDashboardModelsMesAssetAssetState(_state)




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

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in (_tags or []):
            tags_item = VirincoWATSWebDashboardModelsMesProductSetting.from_dict(tags_item_data)



            tags.append(tags_item)


        asset_children = []
        _asset_children = d.pop("assetChildren", UNSET)
        for asset_children_item_data in (_asset_children or []):
            asset_children_item = VirincoWATSWebDashboardModelsMesAssetAsset.from_dict(asset_children_item_data)



            asset_children.append(asset_children_item)


        _asset_type = d.pop("assetType", UNSET)
        asset_type: Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetType]
        if isinstance(_asset_type,  Unset):
            asset_type = UNSET
        else:
            asset_type = VirincoWATSWebDashboardModelsMesAssetAssetType.from_dict(_asset_type)




        asset_log = []
        _asset_log = d.pop("assetLog", UNSET)
        for asset_log_item_data in (_asset_log or []):
            asset_log_item = VirincoWATSWebDashboardModelsMesAssetAssetLog.from_dict(asset_log_item_data)



            asset_log.append(asset_log_item)


        virinco_wats_web_dashboard_models_mes_asset_asset = cls(
            serial_number=serial_number,
            type_id=type_id,
            asset_id=asset_id,
            parent_asset_id=parent_asset_id,
            parent_serial_number=parent_serial_number,
            asset_name=asset_name,
            part_number=part_number,
            revision=revision,
            client_id=client_id,
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
            tags=tags,
            asset_children=asset_children,
            asset_type=asset_type,
            asset_log=asset_log,
        )


        virinco_wats_web_dashboard_models_mes_asset_asset.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_asset_asset

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
