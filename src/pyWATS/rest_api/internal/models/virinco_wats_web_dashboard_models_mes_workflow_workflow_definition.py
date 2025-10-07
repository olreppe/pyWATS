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
  from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_relation import VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation
  from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_definition_xaml import VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinitionXaml





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition")



@_attrs_define
class VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition:
    """ 
        Attributes:
            phases_model (Union[Unset, list[int]]):
            workflow_definition_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            virtual_folder_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            version (Union[Unset, int]):
            description (Union[Unset, str]):
            created (Union[Unset, datetime.datetime]):
            created_by (Union[Unset, str]):
            modified (Union[Unset, datetime.datetime]):
            modified_by (Union[Unset, str]):
            released (Union[Unset, datetime.datetime]):
            released_by (Union[Unset, str]):
            revoked (Union[Unset, datetime.datetime]):
            revoked_by (Union[Unset, str]):
            phases (Union[Unset, int]):
            status (Union[Unset, int]):
            t_stamp (Union[Unset, str]):
            service_version (Union[Unset, int]):
            relations (Union[Unset, list['VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation']]):
            instances_count (Union[Unset, int]):
            xaml (Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinitionXaml]):
     """

    phases_model: Union[Unset, list[int]] = UNSET
    workflow_definition_id: Union[Unset, UUID] = UNSET
    virtual_folder_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    version: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    created_by: Union[Unset, str] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    modified_by: Union[Unset, str] = UNSET
    released: Union[Unset, datetime.datetime] = UNSET
    released_by: Union[Unset, str] = UNSET
    revoked: Union[Unset, datetime.datetime] = UNSET
    revoked_by: Union[Unset, str] = UNSET
    phases: Union[Unset, int] = UNSET
    status: Union[Unset, int] = UNSET
    t_stamp: Union[Unset, str] = UNSET
    service_version: Union[Unset, int] = UNSET
    relations: Union[Unset, list['VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation']] = UNSET
    instances_count: Union[Unset, int] = UNSET
    xaml: Union[Unset, 'VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinitionXaml'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_relation import VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_definition_xaml import VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinitionXaml
        phases_model: Union[Unset, list[int]] = UNSET
        if not isinstance(self.phases_model, Unset):
            phases_model = self.phases_model



        workflow_definition_id: Union[Unset, str] = UNSET
        if not isinstance(self.workflow_definition_id, Unset):
            workflow_definition_id = str(self.workflow_definition_id)

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

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        modified_by = self.modified_by

        released: Union[Unset, str] = UNSET
        if not isinstance(self.released, Unset):
            released = self.released.isoformat()

        released_by = self.released_by

        revoked: Union[Unset, str] = UNSET
        if not isinstance(self.revoked, Unset):
            revoked = self.revoked.isoformat()

        revoked_by = self.revoked_by

        phases = self.phases

        status = self.status

        t_stamp = self.t_stamp

        service_version = self.service_version

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
        if phases_model is not UNSET:
            field_dict["PhasesModel"] = phases_model
        if workflow_definition_id is not UNSET:
            field_dict["WorkflowDefinitionId"] = workflow_definition_id
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
        if modified is not UNSET:
            field_dict["Modified"] = modified
        if modified_by is not UNSET:
            field_dict["ModifiedBy"] = modified_by
        if released is not UNSET:
            field_dict["Released"] = released
        if released_by is not UNSET:
            field_dict["ReleasedBy"] = released_by
        if revoked is not UNSET:
            field_dict["Revoked"] = revoked
        if revoked_by is not UNSET:
            field_dict["RevokedBy"] = revoked_by
        if phases is not UNSET:
            field_dict["Phases"] = phases
        if status is not UNSET:
            field_dict["Status"] = status
        if t_stamp is not UNSET:
            field_dict["TStamp"] = t_stamp
        if service_version is not UNSET:
            field_dict["ServiceVersion"] = service_version
        if relations is not UNSET:
            field_dict["Relations"] = relations
        if instances_count is not UNSET:
            field_dict["InstancesCount"] = instances_count
        if xaml is not UNSET:
            field_dict["XAML"] = xaml

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_relation import VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_definition_xaml import VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinitionXaml
        d = dict(src_dict)
        phases_model = cast(list[int], d.pop("PhasesModel", UNSET))


        _workflow_definition_id = d.pop("WorkflowDefinitionId", UNSET)
        workflow_definition_id: Union[Unset, UUID]
        if isinstance(_workflow_definition_id,  Unset):
            workflow_definition_id = UNSET
        else:
            workflow_definition_id = UUID(_workflow_definition_id)




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

        _modified = d.pop("Modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified,  Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)




        modified_by = d.pop("ModifiedBy", UNSET)

        _released = d.pop("Released", UNSET)
        released: Union[Unset, datetime.datetime]
        if isinstance(_released,  Unset):
            released = UNSET
        else:
            released = isoparse(_released)




        released_by = d.pop("ReleasedBy", UNSET)

        _revoked = d.pop("Revoked", UNSET)
        revoked: Union[Unset, datetime.datetime]
        if isinstance(_revoked,  Unset):
            revoked = UNSET
        else:
            revoked = isoparse(_revoked)




        revoked_by = d.pop("RevokedBy", UNSET)

        phases = d.pop("Phases", UNSET)

        status = d.pop("Status", UNSET)

        t_stamp = d.pop("TStamp", UNSET)

        service_version = d.pop("ServiceVersion", UNSET)

        relations = []
        _relations = d.pop("Relations", UNSET)
        for relations_item_data in (_relations or []):
            relations_item = VirincoWATSWebDashboardModelsMesWorkflowWorkflowRelation.from_dict(relations_item_data)



            relations.append(relations_item)


        instances_count = d.pop("InstancesCount", UNSET)

        _xaml = d.pop("XAML", UNSET)
        xaml: Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinitionXaml]
        if isinstance(_xaml,  Unset):
            xaml = UNSET
        else:
            xaml = VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinitionXaml.from_dict(_xaml)




        virinco_wats_web_dashboard_models_mes_workflow_workflow_definition = cls(
            phases_model=phases_model,
            workflow_definition_id=workflow_definition_id,
            virtual_folder_id=virtual_folder_id,
            name=name,
            version=version,
            description=description,
            created=created,
            created_by=created_by,
            modified=modified,
            modified_by=modified_by,
            released=released,
            released_by=released_by,
            revoked=revoked,
            revoked_by=revoked_by,
            phases=phases,
            status=status,
            t_stamp=t_stamp,
            service_version=service_version,
            relations=relations,
            instances_count=instances_count,
            xaml=xaml,
        )


        virinco_wats_web_dashboard_models_mes_workflow_workflow_definition.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_workflow_workflow_definition

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
