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
  from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_relation import VirincoWATSWebDashboardModelsMesMITestSequenceRelation
  from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_definition_xaml import VirincoWATSWebDashboardModelsMesMITestSequenceDefinitionXaml





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesMITestSequenceDefinition")



@_attrs_define
class VirincoWATSWebDashboardModelsMesMITestSequenceDefinition:
    """ 
        Attributes:
            test_sequence_definition_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            virtual_folder_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            version (Union[Unset, int]):
            description (Union[Unset, str]):
            created (Union[Unset, datetime.datetime]):
            created_by (Union[Unset, str]):
            created_by_site (Union[Unset, str]):
            released (Union[Unset, datetime.datetime]):
            released_by (Union[Unset, str]):
            modified (Union[Unset, datetime.datetime]):
            modified_by (Union[Unset, str]):
            revoked (Union[Unset, datetime.datetime]):
            revoked_by (Union[Unset, str]):
            status (Union[Unset, int]):
            is_global (Union[Unset, bool]):
            on_fail_goto_cleanup (Union[Unset, bool]):
            on_fail_require_submit (Union[Unset, bool]):
            on_fail_require_repair (Union[Unset, int]):
            log_operator (Union[Unset, bool]):
            log_description (Union[Unset, bool]):
            create_unsubmitted_report_on_failed_step (Union[Unset, bool]):
            repair_process_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            add_child_units (Union[Unset, bool]):
            include_uur_misc_info_in_uut (Union[Unset, bool]):
            load_previous_misc_info (Union[Unset, bool]):
            relations (Union[Unset, list['VirincoWATSWebDashboardModelsMesMITestSequenceRelation']]):
            instances_count (Union[Unset, int]):
            xaml (Union[Unset, VirincoWATSWebDashboardModelsMesMITestSequenceDefinitionXaml]):
     """

    test_sequence_definition_id: Union[Unset, UUID] = UNSET
    virtual_folder_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    version: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    created_by: Union[Unset, str] = UNSET
    created_by_site: Union[Unset, str] = UNSET
    released: Union[Unset, datetime.datetime] = UNSET
    released_by: Union[Unset, str] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    modified_by: Union[Unset, str] = UNSET
    revoked: Union[Unset, datetime.datetime] = UNSET
    revoked_by: Union[Unset, str] = UNSET
    status: Union[Unset, int] = UNSET
    is_global: Union[Unset, bool] = UNSET
    on_fail_goto_cleanup: Union[Unset, bool] = UNSET
    on_fail_require_submit: Union[Unset, bool] = UNSET
    on_fail_require_repair: Union[Unset, int] = UNSET
    log_operator: Union[Unset, bool] = UNSET
    log_description: Union[Unset, bool] = UNSET
    create_unsubmitted_report_on_failed_step: Union[Unset, bool] = UNSET
    repair_process_id: Union[Unset, UUID] = UNSET
    add_child_units: Union[Unset, bool] = UNSET
    include_uur_misc_info_in_uut: Union[Unset, bool] = UNSET
    load_previous_misc_info: Union[Unset, bool] = UNSET
    relations: Union[Unset, list['VirincoWATSWebDashboardModelsMesMITestSequenceRelation']] = UNSET
    instances_count: Union[Unset, int] = UNSET
    xaml: Union[Unset, 'VirincoWATSWebDashboardModelsMesMITestSequenceDefinitionXaml'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_relation import VirincoWATSWebDashboardModelsMesMITestSequenceRelation
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_definition_xaml import VirincoWATSWebDashboardModelsMesMITestSequenceDefinitionXaml
        test_sequence_definition_id: Union[Unset, str] = UNSET
        if not isinstance(self.test_sequence_definition_id, Unset):
            test_sequence_definition_id = str(self.test_sequence_definition_id)

        virtual_folder_id: Union[Unset, str] = UNSET
        if not isinstance(self.virtual_folder_id, Unset):
            virtual_folder_id = str(self.virtual_folder_id)

        name = self.name

        version = self.version

        description = self.description

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        created_by = self.created_by

        created_by_site = self.created_by_site

        released: Union[Unset, str] = UNSET
        if not isinstance(self.released, Unset):
            released = self.released.isoformat()

        released_by = self.released_by

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        modified_by = self.modified_by

        revoked: Union[Unset, str] = UNSET
        if not isinstance(self.revoked, Unset):
            revoked = self.revoked.isoformat()

        revoked_by = self.revoked_by

        status = self.status

        is_global = self.is_global

        on_fail_goto_cleanup = self.on_fail_goto_cleanup

        on_fail_require_submit = self.on_fail_require_submit

        on_fail_require_repair = self.on_fail_require_repair

        log_operator = self.log_operator

        log_description = self.log_description

        create_unsubmitted_report_on_failed_step = self.create_unsubmitted_report_on_failed_step

        repair_process_id: Union[Unset, str] = UNSET
        if not isinstance(self.repair_process_id, Unset):
            repair_process_id = str(self.repair_process_id)

        add_child_units = self.add_child_units

        include_uur_misc_info_in_uut = self.include_uur_misc_info_in_uut

        load_previous_misc_info = self.load_previous_misc_info

        relations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.relations, Unset):
            relations = []
            for relations_item_data in self.relations:
                relations_item = relations_item_data.to_dict()
                relations.append(relations_item)



        instances_count = self.instances_count

        xaml: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.xaml, Unset):
            xaml = self.xaml.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if test_sequence_definition_id is not UNSET:
            field_dict["TestSequenceDefinitionId"] = test_sequence_definition_id
        if virtual_folder_id is not UNSET:
            field_dict["VirtualFolderId"] = virtual_folder_id
        if name is not UNSET:
            field_dict["Name"] = name
        if version is not UNSET:
            field_dict["Version"] = version
        if description is not UNSET:
            field_dict["Description"] = description
        if created is not UNSET:
            field_dict["Created"] = created
        if created_by is not UNSET:
            field_dict["CreatedBy"] = created_by
        if created_by_site is not UNSET:
            field_dict["CreatedBySite"] = created_by_site
        if released is not UNSET:
            field_dict["Released"] = released
        if released_by is not UNSET:
            field_dict["ReleasedBy"] = released_by
        if modified is not UNSET:
            field_dict["Modified"] = modified
        if modified_by is not UNSET:
            field_dict["ModifiedBy"] = modified_by
        if revoked is not UNSET:
            field_dict["Revoked"] = revoked
        if revoked_by is not UNSET:
            field_dict["RevokedBy"] = revoked_by
        if status is not UNSET:
            field_dict["Status"] = status
        if is_global is not UNSET:
            field_dict["IsGlobal"] = is_global
        if on_fail_goto_cleanup is not UNSET:
            field_dict["OnFailGotoCleanup"] = on_fail_goto_cleanup
        if on_fail_require_submit is not UNSET:
            field_dict["OnFailRequireSubmit"] = on_fail_require_submit
        if on_fail_require_repair is not UNSET:
            field_dict["OnFailRequireRepair"] = on_fail_require_repair
        if log_operator is not UNSET:
            field_dict["LogOperator"] = log_operator
        if log_description is not UNSET:
            field_dict["LogDescription"] = log_description
        if create_unsubmitted_report_on_failed_step is not UNSET:
            field_dict["CreateUnsubmittedReportOnFailedStep"] = create_unsubmitted_report_on_failed_step
        if repair_process_id is not UNSET:
            field_dict["RepairProcessId"] = repair_process_id
        if add_child_units is not UNSET:
            field_dict["AddChildUnits"] = add_child_units
        if include_uur_misc_info_in_uut is not UNSET:
            field_dict["IncludeUURMiscInfoInUUT"] = include_uur_misc_info_in_uut
        if load_previous_misc_info is not UNSET:
            field_dict["LoadPreviousMiscInfo"] = load_previous_misc_info
        if relations is not UNSET:
            field_dict["Relations"] = relations
        if instances_count is not UNSET:
            field_dict["InstancesCount"] = instances_count
        if xaml is not UNSET:
            field_dict["XAML"] = xaml

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_relation import VirincoWATSWebDashboardModelsMesMITestSequenceRelation
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_definition_xaml import VirincoWATSWebDashboardModelsMesMITestSequenceDefinitionXaml
        d = dict(src_dict)
        _test_sequence_definition_id = d.pop("TestSequenceDefinitionId", UNSET)
        test_sequence_definition_id: Union[Unset, UUID]
        if isinstance(_test_sequence_definition_id,  Unset):
            test_sequence_definition_id = UNSET
        else:
            test_sequence_definition_id = UUID(_test_sequence_definition_id)




        _virtual_folder_id = d.pop("VirtualFolderId", UNSET)
        virtual_folder_id: Union[Unset, UUID]
        if isinstance(_virtual_folder_id,  Unset):
            virtual_folder_id = UNSET
        else:
            virtual_folder_id = UUID(_virtual_folder_id)




        name = d.pop("Name", UNSET)

        version = d.pop("Version", UNSET)

        description = d.pop("Description", UNSET)

        _created = d.pop("Created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created,  Unset):
            created = UNSET
        else:
            created = isoparse(_created)




        created_by = d.pop("CreatedBy", UNSET)

        created_by_site = d.pop("CreatedBySite", UNSET)

        _released = d.pop("Released", UNSET)
        released: Union[Unset, datetime.datetime]
        if isinstance(_released,  Unset):
            released = UNSET
        else:
            released = isoparse(_released)




        released_by = d.pop("ReleasedBy", UNSET)

        _modified = d.pop("Modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified,  Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)




        modified_by = d.pop("ModifiedBy", UNSET)

        _revoked = d.pop("Revoked", UNSET)
        revoked: Union[Unset, datetime.datetime]
        if isinstance(_revoked,  Unset):
            revoked = UNSET
        else:
            revoked = isoparse(_revoked)




        revoked_by = d.pop("RevokedBy", UNSET)

        status = d.pop("Status", UNSET)

        is_global = d.pop("IsGlobal", UNSET)

        on_fail_goto_cleanup = d.pop("OnFailGotoCleanup", UNSET)

        on_fail_require_submit = d.pop("OnFailRequireSubmit", UNSET)

        on_fail_require_repair = d.pop("OnFailRequireRepair", UNSET)

        log_operator = d.pop("LogOperator", UNSET)

        log_description = d.pop("LogDescription", UNSET)

        create_unsubmitted_report_on_failed_step = d.pop("CreateUnsubmittedReportOnFailedStep", UNSET)

        _repair_process_id = d.pop("RepairProcessId", UNSET)
        repair_process_id: Union[Unset, UUID]
        if isinstance(_repair_process_id,  Unset):
            repair_process_id = UNSET
        else:
            repair_process_id = UUID(_repair_process_id)




        add_child_units = d.pop("AddChildUnits", UNSET)

        include_uur_misc_info_in_uut = d.pop("IncludeUURMiscInfoInUUT", UNSET)

        load_previous_misc_info = d.pop("LoadPreviousMiscInfo", UNSET)

        relations = []
        _relations = d.pop("Relations", UNSET)
        for relations_item_data in (_relations or []):
            relations_item = VirincoWATSWebDashboardModelsMesMITestSequenceRelation.from_dict(relations_item_data)



            relations.append(relations_item)


        instances_count = d.pop("InstancesCount", UNSET)

        _xaml = d.pop("XAML", UNSET)
        xaml: Union[Unset, VirincoWATSWebDashboardModelsMesMITestSequenceDefinitionXaml]
        if isinstance(_xaml,  Unset):
            xaml = UNSET
        else:
            xaml = VirincoWATSWebDashboardModelsMesMITestSequenceDefinitionXaml.from_dict(_xaml)




        virinco_wats_web_dashboard_models_mes_mi_test_sequence_definition = cls(
            test_sequence_definition_id=test_sequence_definition_id,
            virtual_folder_id=virtual_folder_id,
            name=name,
            version=version,
            description=description,
            created=created,
            created_by=created_by,
            created_by_site=created_by_site,
            released=released,
            released_by=released_by,
            modified=modified,
            modified_by=modified_by,
            revoked=revoked,
            revoked_by=revoked_by,
            status=status,
            is_global=is_global,
            on_fail_goto_cleanup=on_fail_goto_cleanup,
            on_fail_require_submit=on_fail_require_submit,
            on_fail_require_repair=on_fail_require_repair,
            log_operator=log_operator,
            log_description=log_description,
            create_unsubmitted_report_on_failed_step=create_unsubmitted_report_on_failed_step,
            repair_process_id=repair_process_id,
            add_child_units=add_child_units,
            include_uur_misc_info_in_uut=include_uur_misc_info_in_uut,
            load_previous_misc_info=load_previous_misc_info,
            relations=relations,
            instances_count=instances_count,
            xaml=xaml,
        )


        virinco_wats_web_dashboard_models_mes_mi_test_sequence_definition.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_mi_test_sequence_definition

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
