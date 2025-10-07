from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_status import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityStatus
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_relation import VirincoWATSWebDashboardModelsMesMITestSequenceRelation
  from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
  from ..models.virinco_wats_web_dashboard_models_mes_software_entity import VirincoWATSWebDashboardModelsMesSoftwareEntity
  from ..models.virinco_wats_web_dashboard_models_mes_conflicting_production_manager_relation import VirincoWATSWebDashboardModelsMesConflictingProductionManagerRelation
  from ..models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidation
  from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_relation import VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity:
    """ 
        Attributes:
            id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            parent_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            entity_type (Union[Unset, str]):
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            status (Union[Unset, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityStatus]):
            version (Union[Unset, int]):
            created (Union[Unset, datetime.datetime]):
            created_by (Union[Unset, str]):
            released (Union[Unset, datetime.datetime]):
            released_by (Union[Unset, str]):
            revoked (Union[Unset, datetime.datetime]):
            revoked_by (Union[Unset, str]):
            phases (Union[Unset, int]):
            instances_count (Union[Unset, int]):
            service_version (Union[Unset, int]):
            phases_string (Union[Unset, str]):
            process_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            repair_process_name (Union[Unset, str]):
            is_global (Union[Unset, bool]):
            add_child_units (Union[Unset, bool]):
            include_uur_misc_info_in_uut (Union[Unset, bool]):
            load_previous_misc_info (Union[Unset, bool]):
            on_fail_require_submit (Union[Unset, bool]):
            on_fail_require_repair (Union[Unset, int]):
            log_operator (Union[Unset, bool]):
            log_description (Union[Unset, bool]):
            create_unsubmitted_report_on_failed_step (Union[Unset, bool]):
            package_folder (Union[Unset, bool]):
            priority (Union[Unset, int]):
            modified_by (Union[Unset, str]):
            modified (Union[Unset, datetime.datetime]):
            relation_ids (Union[Unset, list[str]]):
            sites (Union[Unset, list[str]]):
            mi_relations (Union[Unset, list['VirincoWATSWebDashboardModelsMesMITestSequenceRelation']]):
            wf_relations (Union[Unset, list['VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation']]):
            conflicting_relations (Union[Unset,
                list['VirincoWATSWebDashboardModelsMesConflictingProductionManagerRelation']]):
            tags (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']]):
            deleted_tags (Union[Unset, list[str]]):
            software_entities (Union[Unset, list['VirincoWATSWebDashboardModelsMesSoftwareEntity']]):
            validation (Union[Unset, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidation]):
            mi_files (Union[Unset, list[str]]):
     """

    id: Union[Unset, UUID] = UNSET
    parent_id: Union[Unset, UUID] = UNSET
    entity_type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    status: Union[Unset, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityStatus] = UNSET
    version: Union[Unset, int] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    created_by: Union[Unset, str] = UNSET
    released: Union[Unset, datetime.datetime] = UNSET
    released_by: Union[Unset, str] = UNSET
    revoked: Union[Unset, datetime.datetime] = UNSET
    revoked_by: Union[Unset, str] = UNSET
    phases: Union[Unset, int] = UNSET
    instances_count: Union[Unset, int] = UNSET
    service_version: Union[Unset, int] = UNSET
    phases_string: Union[Unset, str] = UNSET
    process_id: Union[Unset, UUID] = UNSET
    repair_process_name: Union[Unset, str] = UNSET
    is_global: Union[Unset, bool] = UNSET
    add_child_units: Union[Unset, bool] = UNSET
    include_uur_misc_info_in_uut: Union[Unset, bool] = UNSET
    load_previous_misc_info: Union[Unset, bool] = UNSET
    on_fail_require_submit: Union[Unset, bool] = UNSET
    on_fail_require_repair: Union[Unset, int] = UNSET
    log_operator: Union[Unset, bool] = UNSET
    log_description: Union[Unset, bool] = UNSET
    create_unsubmitted_report_on_failed_step: Union[Unset, bool] = UNSET
    package_folder: Union[Unset, bool] = UNSET
    priority: Union[Unset, int] = UNSET
    modified_by: Union[Unset, str] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    relation_ids: Union[Unset, list[str]] = UNSET
    sites: Union[Unset, list[str]] = UNSET
    mi_relations: Union[Unset, list['VirincoWATSWebDashboardModelsMesMITestSequenceRelation']] = UNSET
    wf_relations: Union[Unset, list['VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation']] = UNSET
    conflicting_relations: Union[Unset, list['VirincoWATSWebDashboardModelsMesConflictingProductionManagerRelation']] = UNSET
    tags: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']] = UNSET
    deleted_tags: Union[Unset, list[str]] = UNSET
    software_entities: Union[Unset, list['VirincoWATSWebDashboardModelsMesSoftwareEntity']] = UNSET
    validation: Union[Unset, 'VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidation'] = UNSET
    mi_files: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_relation import VirincoWATSWebDashboardModelsMesMITestSequenceRelation
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_web_dashboard_models_mes_software_entity import VirincoWATSWebDashboardModelsMesSoftwareEntity
        from ..models.virinco_wats_web_dashboard_models_mes_conflicting_production_manager_relation import VirincoWATSWebDashboardModelsMesConflictingProductionManagerRelation
        from ..models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidation
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_relation import VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        parent_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_id, Unset):
            parent_id = str(self.parent_id)

        entity_type = self.entity_type

        name = self.name

        description = self.description

        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value


        version = self.version

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        created_by = self.created_by

        released: Union[Unset, str] = UNSET
        if not isinstance(self.released, Unset):
            released = self.released.isoformat()

        released_by = self.released_by

        revoked: Union[Unset, str] = UNSET
        if not isinstance(self.revoked, Unset):
            revoked = self.revoked.isoformat()

        revoked_by = self.revoked_by

        phases = self.phases

        instances_count = self.instances_count

        service_version = self.service_version

        phases_string = self.phases_string

        process_id: Union[Unset, str] = UNSET
        if not isinstance(self.process_id, Unset):
            process_id = str(self.process_id)

        repair_process_name = self.repair_process_name

        is_global = self.is_global

        add_child_units = self.add_child_units

        include_uur_misc_info_in_uut = self.include_uur_misc_info_in_uut

        load_previous_misc_info = self.load_previous_misc_info

        on_fail_require_submit = self.on_fail_require_submit

        on_fail_require_repair = self.on_fail_require_repair

        log_operator = self.log_operator

        log_description = self.log_description

        create_unsubmitted_report_on_failed_step = self.create_unsubmitted_report_on_failed_step

        package_folder = self.package_folder

        priority = self.priority

        modified_by = self.modified_by

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        relation_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.relation_ids, Unset):
            relation_ids = self.relation_ids



        sites: Union[Unset, list[str]] = UNSET
        if not isinstance(self.sites, Unset):
            sites = self.sites



        mi_relations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.mi_relations, Unset):
            mi_relations = []
            for mi_relations_item_data in self.mi_relations:
                mi_relations_item = mi_relations_item_data.to_dict()
                mi_relations.append(mi_relations_item)



        wf_relations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.wf_relations, Unset):
            wf_relations = []
            for wf_relations_item_data in self.wf_relations:
                wf_relations_item = wf_relations_item_data.to_dict()
                wf_relations.append(wf_relations_item)



        conflicting_relations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.conflicting_relations, Unset):
            conflicting_relations = []
            for conflicting_relations_item_data in self.conflicting_relations:
                conflicting_relations_item = conflicting_relations_item_data.to_dict()
                conflicting_relations.append(conflicting_relations_item)



        tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)



        deleted_tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.deleted_tags, Unset):
            deleted_tags = self.deleted_tags



        software_entities: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.software_entities, Unset):
            software_entities = []
            for software_entities_item_data in self.software_entities:
                software_entities_item = software_entities_item_data.to_dict()
                software_entities.append(software_entities_item)



        validation: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.validation, Unset):
            validation = self.validation.to_dict()

        mi_files: Union[Unset, list[str]] = UNSET
        if not isinstance(self.mi_files, Unset):
            mi_files = self.mi_files




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
        if description is not UNSET:
            field_dict["description"] = description
        if status is not UNSET:
            field_dict["status"] = status
        if version is not UNSET:
            field_dict["version"] = version
        if created is not UNSET:
            field_dict["created"] = created
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if released is not UNSET:
            field_dict["released"] = released
        if released_by is not UNSET:
            field_dict["releasedBy"] = released_by
        if revoked is not UNSET:
            field_dict["revoked"] = revoked
        if revoked_by is not UNSET:
            field_dict["revokedBy"] = revoked_by
        if phases is not UNSET:
            field_dict["phases"] = phases
        if instances_count is not UNSET:
            field_dict["instancesCount"] = instances_count
        if service_version is not UNSET:
            field_dict["serviceVersion"] = service_version
        if phases_string is not UNSET:
            field_dict["phasesString"] = phases_string
        if process_id is not UNSET:
            field_dict["processId"] = process_id
        if repair_process_name is not UNSET:
            field_dict["repairProcessName"] = repair_process_name
        if is_global is not UNSET:
            field_dict["isGlobal"] = is_global
        if add_child_units is not UNSET:
            field_dict["addChildUnits"] = add_child_units
        if include_uur_misc_info_in_uut is not UNSET:
            field_dict["includeUURMiscInfoInUUT"] = include_uur_misc_info_in_uut
        if load_previous_misc_info is not UNSET:
            field_dict["loadPreviousMiscInfo"] = load_previous_misc_info
        if on_fail_require_submit is not UNSET:
            field_dict["onFailRequireSubmit"] = on_fail_require_submit
        if on_fail_require_repair is not UNSET:
            field_dict["onFailRequireRepair"] = on_fail_require_repair
        if log_operator is not UNSET:
            field_dict["logOperator"] = log_operator
        if log_description is not UNSET:
            field_dict["logDescription"] = log_description
        if create_unsubmitted_report_on_failed_step is not UNSET:
            field_dict["createUnsubmittedReportOnFailedStep"] = create_unsubmitted_report_on_failed_step
        if package_folder is not UNSET:
            field_dict["packageFolder"] = package_folder
        if priority is not UNSET:
            field_dict["priority"] = priority
        if modified_by is not UNSET:
            field_dict["modifiedBy"] = modified_by
        if modified is not UNSET:
            field_dict["modified"] = modified
        if relation_ids is not UNSET:
            field_dict["relationIds"] = relation_ids
        if sites is not UNSET:
            field_dict["sites"] = sites
        if mi_relations is not UNSET:
            field_dict["miRelations"] = mi_relations
        if wf_relations is not UNSET:
            field_dict["wfRelations"] = wf_relations
        if conflicting_relations is not UNSET:
            field_dict["conflictingRelations"] = conflicting_relations
        if tags is not UNSET:
            field_dict["tags"] = tags
        if deleted_tags is not UNSET:
            field_dict["deletedTags"] = deleted_tags
        if software_entities is not UNSET:
            field_dict["softwareEntities"] = software_entities
        if validation is not UNSET:
            field_dict["validation"] = validation
        if mi_files is not UNSET:
            field_dict["miFiles"] = mi_files

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_relation import VirincoWATSWebDashboardModelsMesMITestSequenceRelation
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_web_dashboard_models_mes_software_entity import VirincoWATSWebDashboardModelsMesSoftwareEntity
        from ..models.virinco_wats_web_dashboard_models_mes_conflicting_production_manager_relation import VirincoWATSWebDashboardModelsMesConflictingProductionManagerRelation
        from ..models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_validation import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidation
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_relation import VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation
        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        _parent_id = d.pop("parentId", UNSET)
        parent_id: Union[Unset, UUID]
        if isinstance(_parent_id,  Unset):
            parent_id = UNSET
        else:
            parent_id = UUID(_parent_id)




        entity_type = d.pop("entityType", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityStatus(_status)




        version = d.pop("version", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created,  Unset):
            created = UNSET
        else:
            created = isoparse(_created)




        created_by = d.pop("createdBy", UNSET)

        _released = d.pop("released", UNSET)
        released: Union[Unset, datetime.datetime]
        if isinstance(_released,  Unset):
            released = UNSET
        else:
            released = isoparse(_released)




        released_by = d.pop("releasedBy", UNSET)

        _revoked = d.pop("revoked", UNSET)
        revoked: Union[Unset, datetime.datetime]
        if isinstance(_revoked,  Unset):
            revoked = UNSET
        else:
            revoked = isoparse(_revoked)




        revoked_by = d.pop("revokedBy", UNSET)

        phases = d.pop("phases", UNSET)

        instances_count = d.pop("instancesCount", UNSET)

        service_version = d.pop("serviceVersion", UNSET)

        phases_string = d.pop("phasesString", UNSET)

        _process_id = d.pop("processId", UNSET)
        process_id: Union[Unset, UUID]
        if isinstance(_process_id,  Unset):
            process_id = UNSET
        else:
            process_id = UUID(_process_id)




        repair_process_name = d.pop("repairProcessName", UNSET)

        is_global = d.pop("isGlobal", UNSET)

        add_child_units = d.pop("addChildUnits", UNSET)

        include_uur_misc_info_in_uut = d.pop("includeUURMiscInfoInUUT", UNSET)

        load_previous_misc_info = d.pop("loadPreviousMiscInfo", UNSET)

        on_fail_require_submit = d.pop("onFailRequireSubmit", UNSET)

        on_fail_require_repair = d.pop("onFailRequireRepair", UNSET)

        log_operator = d.pop("logOperator", UNSET)

        log_description = d.pop("logDescription", UNSET)

        create_unsubmitted_report_on_failed_step = d.pop("createUnsubmittedReportOnFailedStep", UNSET)

        package_folder = d.pop("packageFolder", UNSET)

        priority = d.pop("priority", UNSET)

        modified_by = d.pop("modifiedBy", UNSET)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified,  Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)




        relation_ids = cast(list[str], d.pop("relationIds", UNSET))


        sites = cast(list[str], d.pop("sites", UNSET))


        mi_relations = []
        _mi_relations = d.pop("miRelations", UNSET)
        for mi_relations_item_data in (_mi_relations or []):
            mi_relations_item = VirincoWATSWebDashboardModelsMesMITestSequenceRelation.from_dict(mi_relations_item_data)



            mi_relations.append(mi_relations_item)


        wf_relations = []
        _wf_relations = d.pop("wfRelations", UNSET)
        for wf_relations_item_data in (_wf_relations or []):
            wf_relations_item = VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation.from_dict(wf_relations_item_data)



            wf_relations.append(wf_relations_item)


        conflicting_relations = []
        _conflicting_relations = d.pop("conflictingRelations", UNSET)
        for conflicting_relations_item_data in (_conflicting_relations or []):
            conflicting_relations_item = VirincoWATSWebDashboardModelsMesConflictingProductionManagerRelation.from_dict(conflicting_relations_item_data)



            conflicting_relations.append(conflicting_relations_item)


        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in (_tags or []):
            tags_item = VirincoWATSWebDashboardModelsMesProductSetting.from_dict(tags_item_data)



            tags.append(tags_item)


        deleted_tags = cast(list[str], d.pop("deletedTags", UNSET))


        software_entities = []
        _software_entities = d.pop("softwareEntities", UNSET)
        for software_entities_item_data in (_software_entities or []):
            software_entities_item = VirincoWATSWebDashboardModelsMesSoftwareEntity.from_dict(software_entities_item_data)



            software_entities.append(software_entities_item)


        _validation = d.pop("validation", UNSET)
        validation: Union[Unset, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidation]
        if isinstance(_validation,  Unset):
            validation = UNSET
        else:
            validation = VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityValidation.from_dict(_validation)




        mi_files = cast(list[str], d.pop("miFiles", UNSET))


        virinco_wats_web_dashboard_models_mes_production_production_manager_entity = cls(
            id=id,
            parent_id=parent_id,
            entity_type=entity_type,
            name=name,
            description=description,
            status=status,
            version=version,
            created=created,
            created_by=created_by,
            released=released,
            released_by=released_by,
            revoked=revoked,
            revoked_by=revoked_by,
            phases=phases,
            instances_count=instances_count,
            service_version=service_version,
            phases_string=phases_string,
            process_id=process_id,
            repair_process_name=repair_process_name,
            is_global=is_global,
            add_child_units=add_child_units,
            include_uur_misc_info_in_uut=include_uur_misc_info_in_uut,
            load_previous_misc_info=load_previous_misc_info,
            on_fail_require_submit=on_fail_require_submit,
            on_fail_require_repair=on_fail_require_repair,
            log_operator=log_operator,
            log_description=log_description,
            create_unsubmitted_report_on_failed_step=create_unsubmitted_report_on_failed_step,
            package_folder=package_folder,
            priority=priority,
            modified_by=modified_by,
            modified=modified,
            relation_ids=relation_ids,
            sites=sites,
            mi_relations=mi_relations,
            wf_relations=wf_relations,
            conflicting_relations=conflicting_relations,
            tags=tags,
            deleted_tags=deleted_tags,
            software_entities=software_entities,
            validation=validation,
            mi_files=mi_files,
        )


        virinco_wats_web_dashboard_models_mes_production_production_manager_entity.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_production_production_manager_entity

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
