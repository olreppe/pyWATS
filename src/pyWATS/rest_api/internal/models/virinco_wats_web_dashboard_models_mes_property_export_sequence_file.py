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
  from ..models.virinco_wats_web_dashboard_models_mes_property_set import VirincoWATSWebDashboardModelsMesPropertySet
  from ..models.virinco_wats_web_dashboard_models_mes_software_entity import VirincoWATSWebDashboardModelsMesSoftwareEntity
  from ..models.virinco_wats_web_dashboard_models_mes_property_export_sequence_file_file import VirincoWATSWebDashboardModelsMesPropertyExportSequenceFileFile





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesPropertyExportSequenceFile")



@_attrs_define
class VirincoWATSWebDashboardModelsMesPropertyExportSequenceFile:
    """ Model which represents either a software file or folder.

        Attributes:
            part_number_validation_description (Union[Unset, str]):
            part_number_validation_regex (Union[Unset, str]):
            parent_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            package_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            software_entity (Union[Unset, VirincoWATSWebDashboardModelsMesSoftwareEntity]): Model which represents either a
                software file or folder.
            checksum (Union[Unset, str]):
            file_name (Union[Unset, str]):
            save_count (Union[Unset, int]):
            file_version (Union[Unset, str]):
            repository_version (Union[Unset, int]):
            file (Union[Unset, VirincoWATSWebDashboardModelsMesPropertyExportSequenceFileFile]):
            file_versions (Union[Unset, list['VirincoWATSWebDashboardModelsMesSoftwareEntity']]):
            typedef_version (Union[Unset, int]): Version of cluster typedefinition, used for unflattening from xml to
                typedefinition.
                Used to ensure backward compatibility when cluster typedefinition is expanded or changed in some way.
            sequence_filename (Union[Unset, str]): The name of the sequence file from where the properties where exported.
            sequence_version (Union[Unset, str]): The version of the sequence at the time of export.
            export_time_stamp (Union[Unset, datetime.datetime]): Date and time from when the export was performed.
            user_name (Union[Unset, str]): The name of the user logged on to Teststand when the export was done.
            comment (Union[Unset, str]): Any comments added to the export in the export tool.
            property_sets (Union[Unset, list['VirincoWATSWebDashboardModelsMesPropertySet']]):
     """

    part_number_validation_description: Union[Unset, str] = UNSET
    part_number_validation_regex: Union[Unset, str] = UNSET
    parent_id: Union[Unset, UUID] = UNSET
    package_id: Union[Unset, UUID] = UNSET
    software_entity: Union[Unset, 'VirincoWATSWebDashboardModelsMesSoftwareEntity'] = UNSET
    checksum: Union[Unset, str] = UNSET
    file_name: Union[Unset, str] = UNSET
    save_count: Union[Unset, int] = UNSET
    file_version: Union[Unset, str] = UNSET
    repository_version: Union[Unset, int] = UNSET
    file: Union[Unset, 'VirincoWATSWebDashboardModelsMesPropertyExportSequenceFileFile'] = UNSET
    file_versions: Union[Unset, list['VirincoWATSWebDashboardModelsMesSoftwareEntity']] = UNSET
    typedef_version: Union[Unset, int] = UNSET
    sequence_filename: Union[Unset, str] = UNSET
    sequence_version: Union[Unset, str] = UNSET
    export_time_stamp: Union[Unset, datetime.datetime] = UNSET
    user_name: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    property_sets: Union[Unset, list['VirincoWATSWebDashboardModelsMesPropertySet']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_property_set import VirincoWATSWebDashboardModelsMesPropertySet
        from ..models.virinco_wats_web_dashboard_models_mes_software_entity import VirincoWATSWebDashboardModelsMesSoftwareEntity
        from ..models.virinco_wats_web_dashboard_models_mes_property_export_sequence_file_file import VirincoWATSWebDashboardModelsMesPropertyExportSequenceFileFile
        part_number_validation_description = self.part_number_validation_description

        part_number_validation_regex = self.part_number_validation_regex

        parent_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_id, Unset):
            parent_id = str(self.parent_id)

        package_id: Union[Unset, str] = UNSET
        if not isinstance(self.package_id, Unset):
            package_id = str(self.package_id)

        software_entity: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.software_entity, Unset):
            software_entity = self.software_entity.to_dict()

        checksum = self.checksum

        file_name = self.file_name

        save_count = self.save_count

        file_version = self.file_version

        repository_version = self.repository_version

        file: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_dict()

        file_versions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.file_versions, Unset):
            file_versions = []
            for file_versions_item_data in self.file_versions:
                file_versions_item = file_versions_item_data.to_dict()
                file_versions.append(file_versions_item)



        typedef_version = self.typedef_version

        sequence_filename = self.sequence_filename

        sequence_version = self.sequence_version

        export_time_stamp: Union[Unset, str] = UNSET
        if not isinstance(self.export_time_stamp, Unset):
            export_time_stamp = self.export_time_stamp.isoformat()

        user_name = self.user_name

        comment = self.comment

        property_sets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.property_sets, Unset):
            property_sets = []
            for property_sets_item_data in self.property_sets:
                property_sets_item = property_sets_item_data.to_dict()
                property_sets.append(property_sets_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if part_number_validation_description is not UNSET:
            field_dict["partNumberValidationDescription"] = part_number_validation_description
        if part_number_validation_regex is not UNSET:
            field_dict["partNumberValidationRegex"] = part_number_validation_regex
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if package_id is not UNSET:
            field_dict["packageId"] = package_id
        if software_entity is not UNSET:
            field_dict["softwareEntity"] = software_entity
        if checksum is not UNSET:
            field_dict["checksum"] = checksum
        if file_name is not UNSET:
            field_dict["fileName"] = file_name
        if save_count is not UNSET:
            field_dict["saveCount"] = save_count
        if file_version is not UNSET:
            field_dict["fileVersion"] = file_version
        if repository_version is not UNSET:
            field_dict["repositoryVersion"] = repository_version
        if file is not UNSET:
            field_dict["file"] = file
        if file_versions is not UNSET:
            field_dict["fileVersions"] = file_versions
        if typedef_version is not UNSET:
            field_dict["typedefVersion"] = typedef_version
        if sequence_filename is not UNSET:
            field_dict["sequenceFilename"] = sequence_filename
        if sequence_version is not UNSET:
            field_dict["sequenceVersion"] = sequence_version
        if export_time_stamp is not UNSET:
            field_dict["exportTimeStamp"] = export_time_stamp
        if user_name is not UNSET:
            field_dict["userName"] = user_name
        if comment is not UNSET:
            field_dict["comment"] = comment
        if property_sets is not UNSET:
            field_dict["propertySets"] = property_sets

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_property_set import VirincoWATSWebDashboardModelsMesPropertySet
        from ..models.virinco_wats_web_dashboard_models_mes_software_entity import VirincoWATSWebDashboardModelsMesSoftwareEntity
        from ..models.virinco_wats_web_dashboard_models_mes_property_export_sequence_file_file import VirincoWATSWebDashboardModelsMesPropertyExportSequenceFileFile
        d = dict(src_dict)
        part_number_validation_description = d.pop("partNumberValidationDescription", UNSET)

        part_number_validation_regex = d.pop("partNumberValidationRegex", UNSET)

        _parent_id = d.pop("parentId", UNSET)
        parent_id: Union[Unset, UUID]
        if isinstance(_parent_id,  Unset):
            parent_id = UNSET
        else:
            parent_id = UUID(_parent_id)




        _package_id = d.pop("packageId", UNSET)
        package_id: Union[Unset, UUID]
        if isinstance(_package_id,  Unset):
            package_id = UNSET
        else:
            package_id = UUID(_package_id)




        _software_entity = d.pop("softwareEntity", UNSET)
        software_entity: Union[Unset, VirincoWATSWebDashboardModelsMesSoftwareEntity]
        if isinstance(_software_entity,  Unset):
            software_entity = UNSET
        else:
            software_entity = VirincoWATSWebDashboardModelsMesSoftwareEntity.from_dict(_software_entity)




        checksum = d.pop("checksum", UNSET)

        file_name = d.pop("fileName", UNSET)

        save_count = d.pop("saveCount", UNSET)

        file_version = d.pop("fileVersion", UNSET)

        repository_version = d.pop("repositoryVersion", UNSET)

        _file = d.pop("file", UNSET)
        file: Union[Unset, VirincoWATSWebDashboardModelsMesPropertyExportSequenceFileFile]
        if isinstance(_file,  Unset):
            file = UNSET
        else:
            file = VirincoWATSWebDashboardModelsMesPropertyExportSequenceFileFile.from_dict(_file)




        file_versions = []
        _file_versions = d.pop("fileVersions", UNSET)
        for file_versions_item_data in (_file_versions or []):
            file_versions_item = VirincoWATSWebDashboardModelsMesSoftwareEntity.from_dict(file_versions_item_data)



            file_versions.append(file_versions_item)


        typedef_version = d.pop("typedefVersion", UNSET)

        sequence_filename = d.pop("sequenceFilename", UNSET)

        sequence_version = d.pop("sequenceVersion", UNSET)

        _export_time_stamp = d.pop("exportTimeStamp", UNSET)
        export_time_stamp: Union[Unset, datetime.datetime]
        if isinstance(_export_time_stamp,  Unset):
            export_time_stamp = UNSET
        else:
            export_time_stamp = isoparse(_export_time_stamp)




        user_name = d.pop("userName", UNSET)

        comment = d.pop("comment", UNSET)

        property_sets = []
        _property_sets = d.pop("propertySets", UNSET)
        for property_sets_item_data in (_property_sets or []):
            property_sets_item = VirincoWATSWebDashboardModelsMesPropertySet.from_dict(property_sets_item_data)



            property_sets.append(property_sets_item)


        virinco_wats_web_dashboard_models_mes_property_export_sequence_file = cls(
            part_number_validation_description=part_number_validation_description,
            part_number_validation_regex=part_number_validation_regex,
            parent_id=parent_id,
            package_id=package_id,
            software_entity=software_entity,
            checksum=checksum,
            file_name=file_name,
            save_count=save_count,
            file_version=file_version,
            repository_version=repository_version,
            file=file,
            file_versions=file_versions,
            typedef_version=typedef_version,
            sequence_filename=sequence_filename,
            sequence_version=sequence_version,
            export_time_stamp=export_time_stamp,
            user_name=user_name,
            comment=comment,
            property_sets=property_sets,
        )


        virinco_wats_web_dashboard_models_mes_property_export_sequence_file.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_property_export_sequence_file

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
