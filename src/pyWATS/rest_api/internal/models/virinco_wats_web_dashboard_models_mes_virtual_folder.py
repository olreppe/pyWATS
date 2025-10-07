from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_definition import VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition
  from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_definition import VirincoWATSWebDashboardModelsMesMITestSequenceDefinition
  from ..models.virinco_wats_web_dashboard_models_mes_software_package import VirincoWATSWebDashboardModelsMesSoftwarePackage





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesVirtualFolder")



@_attrs_define
class VirincoWATSWebDashboardModelsMesVirtualFolder:
    """ 
        Attributes:
            id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            parent_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            type_ (Union[Unset, int]):
            image_url (Union[Unset, str]):
            virtual_folders (Union[Unset, list['VirincoWATSWebDashboardModelsMesVirtualFolder']]):
            packages (Union[Unset, list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]):
            children (Union[Unset, list['VirincoWATSWebDashboardModelsMesVirtualFolder']]):
            workflow_definition (Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition]):
            test_sequence_definition (Union[Unset, VirincoWATSWebDashboardModelsMesMITestSequenceDefinition]):
     """

    id: Union[Unset, UUID] = UNSET
    parent_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    type_: Union[Unset, int] = UNSET
    image_url: Union[Unset, str] = UNSET
    virtual_folders: Union[Unset, list['VirincoWATSWebDashboardModelsMesVirtualFolder']] = UNSET
    packages: Union[Unset, list['VirincoWATSWebDashboardModelsMesSoftwarePackage']] = UNSET
    children: Union[Unset, list['VirincoWATSWebDashboardModelsMesVirtualFolder']] = UNSET
    workflow_definition: Union[Unset, 'VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition'] = UNSET
    test_sequence_definition: Union[Unset, 'VirincoWATSWebDashboardModelsMesMITestSequenceDefinition'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_definition import VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_definition import VirincoWATSWebDashboardModelsMesMITestSequenceDefinition
        from ..models.virinco_wats_web_dashboard_models_mes_software_package import VirincoWATSWebDashboardModelsMesSoftwarePackage
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        parent_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_id, Unset):
            parent_id = str(self.parent_id)

        name = self.name

        description = self.description

        type_ = self.type_

        image_url = self.image_url

        virtual_folders: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.virtual_folders, Unset):
            virtual_folders = []
            for virtual_folders_item_data in self.virtual_folders:
                virtual_folders_item = virtual_folders_item_data.to_dict()
                virtual_folders.append(virtual_folders_item)



        packages: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.packages, Unset):
            packages = []
            for packages_item_data in self.packages:
                packages_item = packages_item_data.to_dict()
                packages.append(packages_item)



        children: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()
                children.append(children_item)



        workflow_definition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.workflow_definition, Unset):
            workflow_definition = self.workflow_definition.to_dict()

        test_sequence_definition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.test_sequence_definition, Unset):
            test_sequence_definition = self.test_sequence_definition.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if virtual_folders is not UNSET:
            field_dict["virtualFolders"] = virtual_folders
        if packages is not UNSET:
            field_dict["Packages"] = packages
        if children is not UNSET:
            field_dict["Children"] = children
        if workflow_definition is not UNSET:
            field_dict["WorkflowDefinition"] = workflow_definition
        if test_sequence_definition is not UNSET:
            field_dict["TestSequenceDefinition"] = test_sequence_definition

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_workflow_workflow_definition import VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition
        from ..models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_definition import VirincoWATSWebDashboardModelsMesMITestSequenceDefinition
        from ..models.virinco_wats_web_dashboard_models_mes_software_package import VirincoWATSWebDashboardModelsMesSoftwarePackage
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




        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        type_ = d.pop("type", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        virtual_folders = []
        _virtual_folders = d.pop("virtualFolders", UNSET)
        for virtual_folders_item_data in (_virtual_folders or []):
            virtual_folders_item = VirincoWATSWebDashboardModelsMesVirtualFolder.from_dict(virtual_folders_item_data)



            virtual_folders.append(virtual_folders_item)


        packages = []
        _packages = d.pop("Packages", UNSET)
        for packages_item_data in (_packages or []):
            packages_item = VirincoWATSWebDashboardModelsMesSoftwarePackage.from_dict(packages_item_data)



            packages.append(packages_item)


        children = []
        _children = d.pop("Children", UNSET)
        for children_item_data in (_children or []):
            children_item = VirincoWATSWebDashboardModelsMesVirtualFolder.from_dict(children_item_data)



            children.append(children_item)


        _workflow_definition = d.pop("WorkflowDefinition", UNSET)
        workflow_definition: Union[Unset, VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition]
        if isinstance(_workflow_definition,  Unset):
            workflow_definition = UNSET
        else:
            workflow_definition = VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition.from_dict(_workflow_definition)




        _test_sequence_definition = d.pop("TestSequenceDefinition", UNSET)
        test_sequence_definition: Union[Unset, VirincoWATSWebDashboardModelsMesMITestSequenceDefinition]
        if isinstance(_test_sequence_definition,  Unset):
            test_sequence_definition = UNSET
        else:
            test_sequence_definition = VirincoWATSWebDashboardModelsMesMITestSequenceDefinition.from_dict(_test_sequence_definition)




        virinco_wats_web_dashboard_models_mes_virtual_folder = cls(
            id=id,
            parent_id=parent_id,
            name=name,
            description=description,
            type_=type_,
            image_url=image_url,
            virtual_folders=virtual_folders,
            packages=packages,
            children=children,
            workflow_definition=workflow_definition,
            test_sequence_definition=test_sequence_definition,
        )


        virinco_wats_web_dashboard_models_mes_virtual_folder.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_virtual_folder

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
