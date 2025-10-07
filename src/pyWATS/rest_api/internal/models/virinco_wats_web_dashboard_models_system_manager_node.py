from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_system_manager_node_status import VirincoWATSWebDashboardModelsSystemManagerNodeStatus
from ..models.virinco_wats_web_dashboard_models_system_manager_node_type_enum import VirincoWATSWebDashboardModelsSystemManagerNodeTypeEnum
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_system_manager_node_package_info import VirincoWATSWebDashboardModelsSystemManagerNodePackageInfo
  from ..models.virinco_wats_web_dashboard_models_system_manager_node_converter import VirincoWATSWebDashboardModelsSystemManagerNodeConverter
  from ..models.virinco_wats_web_dashboard_models_system_manager_node_disk import VirincoWATSWebDashboardModelsSystemManagerNodeDisk
  from ..models.virinco_wats_web_dashboard_models_system_manager_node_product import VirincoWATSWebDashboardModelsSystemManagerNodeProduct





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsSystemManagerNode")



@_attrs_define
class VirincoWATSWebDashboardModelsSystemManagerNode:
    """ 
        Attributes:
            id (Union[Unset, int]):
            parent_id (Union[Unset, int]): If type == level =&gt; ClientGroup.ParentId
                If type == client =&gt; Client.ClientGroupId
            is_self (Union[Unset, bool]):
            client_group_id (Union[Unset, int]):
            client_id (Union[Unset, int]):
            name (Union[Unset, str]):
            display_name (Union[Unset, str]):
            site_code (Union[Unset, str]):
            reg_date_utc (Union[Unset, datetime.datetime]):
            misc_info_updated_utc (Union[Unset, datetime.datetime]):
            location (Union[Unset, str]):
            purpose (Union[Unset, str]):
            type_enum (Union[Unset, VirincoWATSWebDashboardModelsSystemManagerNodeTypeEnum]):
            type_ (Union[Unset, str]):
            accepted_version (Union[Unset, str]):
            utc_offset (Union[Unset, float]):
            description (Union[Unset, str]):
            last_ping_utc (Union[Unset, datetime.datetime]):
            machine_account_id (Union[Unset, str]):
            recent_report_count (Union[Unset, int]):
            last_report_utc (Union[Unset, datetime.datetime]):
            pending_count (Union[Unset, int]):
            gps (Union[Unset, str]):
            status (Union[Unset, VirincoWATSWebDashboardModelsSystemManagerNodeStatus]):
            inactive_since_utc (Union[Unset, datetime.datetime]):
            status_string (Union[Unset, str]): return status string, Offline,Pending, Inactive or Online
            image_name (Union[Unset, str]):
            license_company (Union[Unset, str]):
            license_name (Union[Unset, str]):
            license_number (Union[Unset, str]):
            version (Union[Unset, str]):
            os_version (Union[Unset, str]):
            clr_version (Union[Unset, str]):
            db_engine (Union[Unset, str]):
            country_code (Union[Unset, str]):
            os_architecture (Union[Unset, str]):
            os_language (Union[Unset, str]):
            domain (Union[Unset, str]):
            total_physical_memory (Union[Unset, str]):
            computer_model (Union[Unset, str]):
            manufacturer (Union[Unset, str]):
            free_space (Union[Unset, int]):
            disks (Union[Unset, list['VirincoWATSWebDashboardModelsSystemManagerNodeDisk']]):
            converters (Union[Unset, list['VirincoWATSWebDashboardModelsSystemManagerNodeConverter']]):
            deployments (Union[Unset, list['VirincoWATSWebDashboardModelsSystemManagerNodeProduct']]):
            software_packages (Union[Unset, list['VirincoWATSWebDashboardModelsSystemManagerNodePackageInfo']]):
            update_status (Union[Unset, str]):
     """

    id: Union[Unset, int] = UNSET
    parent_id: Union[Unset, int] = UNSET
    is_self: Union[Unset, bool] = UNSET
    client_group_id: Union[Unset, int] = UNSET
    client_id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    site_code: Union[Unset, str] = UNSET
    reg_date_utc: Union[Unset, datetime.datetime] = UNSET
    misc_info_updated_utc: Union[Unset, datetime.datetime] = UNSET
    location: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    type_enum: Union[Unset, VirincoWATSWebDashboardModelsSystemManagerNodeTypeEnum] = UNSET
    type_: Union[Unset, str] = UNSET
    accepted_version: Union[Unset, str] = UNSET
    utc_offset: Union[Unset, float] = UNSET
    description: Union[Unset, str] = UNSET
    last_ping_utc: Union[Unset, datetime.datetime] = UNSET
    machine_account_id: Union[Unset, str] = UNSET
    recent_report_count: Union[Unset, int] = UNSET
    last_report_utc: Union[Unset, datetime.datetime] = UNSET
    pending_count: Union[Unset, int] = UNSET
    gps: Union[Unset, str] = UNSET
    status: Union[Unset, VirincoWATSWebDashboardModelsSystemManagerNodeStatus] = UNSET
    inactive_since_utc: Union[Unset, datetime.datetime] = UNSET
    status_string: Union[Unset, str] = UNSET
    image_name: Union[Unset, str] = UNSET
    license_company: Union[Unset, str] = UNSET
    license_name: Union[Unset, str] = UNSET
    license_number: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    os_version: Union[Unset, str] = UNSET
    clr_version: Union[Unset, str] = UNSET
    db_engine: Union[Unset, str] = UNSET
    country_code: Union[Unset, str] = UNSET
    os_architecture: Union[Unset, str] = UNSET
    os_language: Union[Unset, str] = UNSET
    domain: Union[Unset, str] = UNSET
    total_physical_memory: Union[Unset, str] = UNSET
    computer_model: Union[Unset, str] = UNSET
    manufacturer: Union[Unset, str] = UNSET
    free_space: Union[Unset, int] = UNSET
    disks: Union[Unset, list['VirincoWATSWebDashboardModelsSystemManagerNodeDisk']] = UNSET
    converters: Union[Unset, list['VirincoWATSWebDashboardModelsSystemManagerNodeConverter']] = UNSET
    deployments: Union[Unset, list['VirincoWATSWebDashboardModelsSystemManagerNodeProduct']] = UNSET
    software_packages: Union[Unset, list['VirincoWATSWebDashboardModelsSystemManagerNodePackageInfo']] = UNSET
    update_status: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_system_manager_node_package_info import VirincoWATSWebDashboardModelsSystemManagerNodePackageInfo
        from ..models.virinco_wats_web_dashboard_models_system_manager_node_converter import VirincoWATSWebDashboardModelsSystemManagerNodeConverter
        from ..models.virinco_wats_web_dashboard_models_system_manager_node_disk import VirincoWATSWebDashboardModelsSystemManagerNodeDisk
        from ..models.virinco_wats_web_dashboard_models_system_manager_node_product import VirincoWATSWebDashboardModelsSystemManagerNodeProduct
        id = self.id

        parent_id = self.parent_id

        is_self = self.is_self

        client_group_id = self.client_group_id

        client_id = self.client_id

        name = self.name

        display_name = self.display_name

        site_code = self.site_code

        reg_date_utc: Union[Unset, str] = UNSET
        if not isinstance(self.reg_date_utc, Unset):
            reg_date_utc = self.reg_date_utc.isoformat()

        misc_info_updated_utc: Union[Unset, str] = UNSET
        if not isinstance(self.misc_info_updated_utc, Unset):
            misc_info_updated_utc = self.misc_info_updated_utc.isoformat()

        location = self.location

        purpose = self.purpose

        type_enum: Union[Unset, int] = UNSET
        if not isinstance(self.type_enum, Unset):
            type_enum = self.type_enum.value


        type_ = self.type_

        accepted_version = self.accepted_version

        utc_offset = self.utc_offset

        description = self.description

        last_ping_utc: Union[Unset, str] = UNSET
        if not isinstance(self.last_ping_utc, Unset):
            last_ping_utc = self.last_ping_utc.isoformat()

        machine_account_id = self.machine_account_id

        recent_report_count = self.recent_report_count

        last_report_utc: Union[Unset, str] = UNSET
        if not isinstance(self.last_report_utc, Unset):
            last_report_utc = self.last_report_utc.isoformat()

        pending_count = self.pending_count

        gps = self.gps

        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value


        inactive_since_utc: Union[Unset, str] = UNSET
        if not isinstance(self.inactive_since_utc, Unset):
            inactive_since_utc = self.inactive_since_utc.isoformat()

        status_string = self.status_string

        image_name = self.image_name

        license_company = self.license_company

        license_name = self.license_name

        license_number = self.license_number

        version = self.version

        os_version = self.os_version

        clr_version = self.clr_version

        db_engine = self.db_engine

        country_code = self.country_code

        os_architecture = self.os_architecture

        os_language = self.os_language

        domain = self.domain

        total_physical_memory = self.total_physical_memory

        computer_model = self.computer_model

        manufacturer = self.manufacturer

        free_space = self.free_space

        disks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.disks, Unset):
            disks = []
            for disks_item_data in self.disks:
                disks_item = disks_item_data.to_dict()
                disks.append(disks_item)



        converters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.converters, Unset):
            converters = []
            for converters_item_data in self.converters:
                converters_item = converters_item_data.to_dict()
                converters.append(converters_item)



        deployments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.deployments, Unset):
            deployments = []
            for deployments_item_data in self.deployments:
                deployments_item = deployments_item_data.to_dict()
                deployments.append(deployments_item)



        software_packages: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.software_packages, Unset):
            software_packages = []
            for software_packages_item_data in self.software_packages:
                software_packages_item = software_packages_item_data.to_dict()
                software_packages.append(software_packages_item)



        update_status = self.update_status


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if is_self is not UNSET:
            field_dict["isSelf"] = is_self
        if client_group_id is not UNSET:
            field_dict["clientGroupId"] = client_group_id
        if client_id is not UNSET:
            field_dict["clientId"] = client_id
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if site_code is not UNSET:
            field_dict["siteCode"] = site_code
        if reg_date_utc is not UNSET:
            field_dict["regDateUtc"] = reg_date_utc
        if misc_info_updated_utc is not UNSET:
            field_dict["miscInfoUpdatedUtc"] = misc_info_updated_utc
        if location is not UNSET:
            field_dict["location"] = location
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if type_enum is not UNSET:
            field_dict["typeEnum"] = type_enum
        if type_ is not UNSET:
            field_dict["type"] = type_
        if accepted_version is not UNSET:
            field_dict["acceptedVersion"] = accepted_version
        if utc_offset is not UNSET:
            field_dict["utcOffset"] = utc_offset
        if description is not UNSET:
            field_dict["description"] = description
        if last_ping_utc is not UNSET:
            field_dict["lastPingUtc"] = last_ping_utc
        if machine_account_id is not UNSET:
            field_dict["machineAccountId"] = machine_account_id
        if recent_report_count is not UNSET:
            field_dict["recentReportCount"] = recent_report_count
        if last_report_utc is not UNSET:
            field_dict["lastReportUtc"] = last_report_utc
        if pending_count is not UNSET:
            field_dict["pendingCount"] = pending_count
        if gps is not UNSET:
            field_dict["gps"] = gps
        if status is not UNSET:
            field_dict["status"] = status
        if inactive_since_utc is not UNSET:
            field_dict["inactiveSinceUtc"] = inactive_since_utc
        if status_string is not UNSET:
            field_dict["statusString"] = status_string
        if image_name is not UNSET:
            field_dict["imageName"] = image_name
        if license_company is not UNSET:
            field_dict["licenseCompany"] = license_company
        if license_name is not UNSET:
            field_dict["licenseName"] = license_name
        if license_number is not UNSET:
            field_dict["licenseNumber"] = license_number
        if version is not UNSET:
            field_dict["version"] = version
        if os_version is not UNSET:
            field_dict["osVersion"] = os_version
        if clr_version is not UNSET:
            field_dict["clrVersion"] = clr_version
        if db_engine is not UNSET:
            field_dict["dbEngine"] = db_engine
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if os_architecture is not UNSET:
            field_dict["osArchitecture"] = os_architecture
        if os_language is not UNSET:
            field_dict["osLanguage"] = os_language
        if domain is not UNSET:
            field_dict["domain"] = domain
        if total_physical_memory is not UNSET:
            field_dict["totalPhysicalMemory"] = total_physical_memory
        if computer_model is not UNSET:
            field_dict["computerModel"] = computer_model
        if manufacturer is not UNSET:
            field_dict["manufacturer"] = manufacturer
        if free_space is not UNSET:
            field_dict["freeSpace"] = free_space
        if disks is not UNSET:
            field_dict["disks"] = disks
        if converters is not UNSET:
            field_dict["converters"] = converters
        if deployments is not UNSET:
            field_dict["deployments"] = deployments
        if software_packages is not UNSET:
            field_dict["softwarePackages"] = software_packages
        if update_status is not UNSET:
            field_dict["updateStatus"] = update_status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_system_manager_node_package_info import VirincoWATSWebDashboardModelsSystemManagerNodePackageInfo
        from ..models.virinco_wats_web_dashboard_models_system_manager_node_converter import VirincoWATSWebDashboardModelsSystemManagerNodeConverter
        from ..models.virinco_wats_web_dashboard_models_system_manager_node_disk import VirincoWATSWebDashboardModelsSystemManagerNodeDisk
        from ..models.virinco_wats_web_dashboard_models_system_manager_node_product import VirincoWATSWebDashboardModelsSystemManagerNodeProduct
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        parent_id = d.pop("parentId", UNSET)

        is_self = d.pop("isSelf", UNSET)

        client_group_id = d.pop("clientGroupId", UNSET)

        client_id = d.pop("clientId", UNSET)

        name = d.pop("name", UNSET)

        display_name = d.pop("displayName", UNSET)

        site_code = d.pop("siteCode", UNSET)

        _reg_date_utc = d.pop("regDateUtc", UNSET)
        reg_date_utc: Union[Unset, datetime.datetime]
        if isinstance(_reg_date_utc,  Unset):
            reg_date_utc = UNSET
        else:
            reg_date_utc = isoparse(_reg_date_utc)




        _misc_info_updated_utc = d.pop("miscInfoUpdatedUtc", UNSET)
        misc_info_updated_utc: Union[Unset, datetime.datetime]
        if isinstance(_misc_info_updated_utc,  Unset):
            misc_info_updated_utc = UNSET
        else:
            misc_info_updated_utc = isoparse(_misc_info_updated_utc)




        location = d.pop("location", UNSET)

        purpose = d.pop("purpose", UNSET)

        _type_enum = d.pop("typeEnum", UNSET)
        type_enum: Union[Unset, VirincoWATSWebDashboardModelsSystemManagerNodeTypeEnum]
        if isinstance(_type_enum,  Unset):
            type_enum = UNSET
        else:
            type_enum = VirincoWATSWebDashboardModelsSystemManagerNodeTypeEnum(_type_enum)




        type_ = d.pop("type", UNSET)

        accepted_version = d.pop("acceptedVersion", UNSET)

        utc_offset = d.pop("utcOffset", UNSET)

        description = d.pop("description", UNSET)

        _last_ping_utc = d.pop("lastPingUtc", UNSET)
        last_ping_utc: Union[Unset, datetime.datetime]
        if isinstance(_last_ping_utc,  Unset):
            last_ping_utc = UNSET
        else:
            last_ping_utc = isoparse(_last_ping_utc)




        machine_account_id = d.pop("machineAccountId", UNSET)

        recent_report_count = d.pop("recentReportCount", UNSET)

        _last_report_utc = d.pop("lastReportUtc", UNSET)
        last_report_utc: Union[Unset, datetime.datetime]
        if isinstance(_last_report_utc,  Unset):
            last_report_utc = UNSET
        else:
            last_report_utc = isoparse(_last_report_utc)




        pending_count = d.pop("pendingCount", UNSET)

        gps = d.pop("gps", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, VirincoWATSWebDashboardModelsSystemManagerNodeStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = VirincoWATSWebDashboardModelsSystemManagerNodeStatus(_status)




        _inactive_since_utc = d.pop("inactiveSinceUtc", UNSET)
        inactive_since_utc: Union[Unset, datetime.datetime]
        if isinstance(_inactive_since_utc,  Unset):
            inactive_since_utc = UNSET
        else:
            inactive_since_utc = isoparse(_inactive_since_utc)




        status_string = d.pop("statusString", UNSET)

        image_name = d.pop("imageName", UNSET)

        license_company = d.pop("licenseCompany", UNSET)

        license_name = d.pop("licenseName", UNSET)

        license_number = d.pop("licenseNumber", UNSET)

        version = d.pop("version", UNSET)

        os_version = d.pop("osVersion", UNSET)

        clr_version = d.pop("clrVersion", UNSET)

        db_engine = d.pop("dbEngine", UNSET)

        country_code = d.pop("countryCode", UNSET)

        os_architecture = d.pop("osArchitecture", UNSET)

        os_language = d.pop("osLanguage", UNSET)

        domain = d.pop("domain", UNSET)

        total_physical_memory = d.pop("totalPhysicalMemory", UNSET)

        computer_model = d.pop("computerModel", UNSET)

        manufacturer = d.pop("manufacturer", UNSET)

        free_space = d.pop("freeSpace", UNSET)

        disks = []
        _disks = d.pop("disks", UNSET)
        for disks_item_data in (_disks or []):
            disks_item = VirincoWATSWebDashboardModelsSystemManagerNodeDisk.from_dict(disks_item_data)



            disks.append(disks_item)


        converters = []
        _converters = d.pop("converters", UNSET)
        for converters_item_data in (_converters or []):
            converters_item = VirincoWATSWebDashboardModelsSystemManagerNodeConverter.from_dict(converters_item_data)



            converters.append(converters_item)


        deployments = []
        _deployments = d.pop("deployments", UNSET)
        for deployments_item_data in (_deployments or []):
            deployments_item = VirincoWATSWebDashboardModelsSystemManagerNodeProduct.from_dict(deployments_item_data)



            deployments.append(deployments_item)


        software_packages = []
        _software_packages = d.pop("softwarePackages", UNSET)
        for software_packages_item_data in (_software_packages or []):
            software_packages_item = VirincoWATSWebDashboardModelsSystemManagerNodePackageInfo.from_dict(software_packages_item_data)



            software_packages.append(software_packages_item)


        update_status = d.pop("updateStatus", UNSET)

        virinco_wats_web_dashboard_models_system_manager_node = cls(
            id=id,
            parent_id=parent_id,
            is_self=is_self,
            client_group_id=client_group_id,
            client_id=client_id,
            name=name,
            display_name=display_name,
            site_code=site_code,
            reg_date_utc=reg_date_utc,
            misc_info_updated_utc=misc_info_updated_utc,
            location=location,
            purpose=purpose,
            type_enum=type_enum,
            type_=type_,
            accepted_version=accepted_version,
            utc_offset=utc_offset,
            description=description,
            last_ping_utc=last_ping_utc,
            machine_account_id=machine_account_id,
            recent_report_count=recent_report_count,
            last_report_utc=last_report_utc,
            pending_count=pending_count,
            gps=gps,
            status=status,
            inactive_since_utc=inactive_since_utc,
            status_string=status_string,
            image_name=image_name,
            license_company=license_company,
            license_name=license_name,
            license_number=license_number,
            version=version,
            os_version=os_version,
            clr_version=clr_version,
            db_engine=db_engine,
            country_code=country_code,
            os_architecture=os_architecture,
            os_language=os_language,
            domain=domain,
            total_physical_memory=total_physical_memory,
            computer_model=computer_model,
            manufacturer=manufacturer,
            free_space=free_space,
            disks=disks,
            converters=converters,
            deployments=deployments,
            software_packages=software_packages,
            update_status=update_status,
        )


        virinco_wats_web_dashboard_models_system_manager_node.additional_properties = d
        return virinco_wats_web_dashboard_models_system_manager_node

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
