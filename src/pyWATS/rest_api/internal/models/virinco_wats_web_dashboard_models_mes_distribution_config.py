from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_distribution_config_site_config import VirincoWATSWebDashboardModelsMesDistributionConfigSiteConfig





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesDistributionConfig")



@_attrs_define
class VirincoWATSWebDashboardModelsMesDistributionConfig:
    """ 
        Attributes:
            server_name (Union[Unset, str]): This servers name. Use null to not set server name.
            site_code (Union[Unset, str]): This servers site code. Use null to not register a site code.
            is_local_server (Union[Unset, bool]): Disables write permission to the entities that are syncable.

                If true, {Virinco.WATS.Web.Dashboard.Models.Mes.DistributionConfig.Sites} must only one site, and this server's
                clientgroup will be child of that site.
            is_conflict_winner (Union[Unset, bool]): Decides whether local changes are overwritten or kept.
                For two way sync (unit sync) required on both servers. Use null to not set/change the setting.
            sites (Union[Unset, list['VirincoWATSWebDashboardModelsMesDistributionConfigSiteConfig']]): Sites to sync to.
                Use null or emtpy list to not create any sites.

                Note: If this server is part of two way sync (unit sync), both servers must have sync enabled to the other
                server. Sync enabled value is not synced by site sync.
            initialize_sync (Union[Unset, bool]): If true, log changes for everything that currently exists to all sites
                that are enabled.
            is_culture_enabled (Union[Unset, bool]): Whether or not changes to Cultures will be logged for sync.
                Use null to not set/change the setting.
            is_message_enabled (Union[Unset, bool]): Whether or not changes to Messages will be logged for sync.
                Use null to not set/change the setting.
            is_process_enabled (Union[Unset, bool]): Whether or not changes to Processes will be logged for sync.
                Use null to not set/change the setting.
            is_product_category_enabled (Union[Unset, bool]): Whether or not changes to ProductCategories will be logged for
                sync.
                Use null to not set/change the setting.
            is_product_enabled (Union[Unset, bool]): Whether or not changes to Products will be logged for sync.
                Use null to not set/change the setting.
            is_product_groups_enabled (Union[Unset, bool]): Whether or not changes to product groups (ProductSelections)
                will be logged for sync.
                Use null to not set/change the setting.
            is_production_batch_enabled (Union[Unset, bool]): Whether or not changes to ProductionBatches will be logged for
                sync.
                Use null to not set/change the setting.
            is_product_revision_enabled (Union[Unset, bool]): Whether or not changes to ProductRevisions will be logged for
                sync.
                Use null to not set/change the setting.
            is_product_revision_relation_enabled (Union[Unset, bool]): Whether or not changes to ProductRevisionRelations
                will be logged for sync.
                Use null to not set/change the setting.
            is_site_enabled (Union[Unset, bool]): Whether or not changes to Sites will be logged for sync.
                Use null to not set/change the setting.
            is_software_package_enabled (Union[Unset, bool]): Whether or not changes to SoftwarePackages will be logged for
                sync.
                Use null to not set/change the setting.
            is_tag_enabled (Union[Unset, bool]): Whether or not changes to Tags will be logged for sync.
                Use null to not set/change the setting.
            is_test_sequence_enabled (Union[Unset, bool]): Whether or not changes to TestSequences will be logged for sync.
                Use null to not set/change the setting.
            is_translation_enabled (Union[Unset, bool]): Whether or not changes to Translations will be logged for sync.
                Use null to not set/change the setting.
            is_unit_enabled (Union[Unset, bool]): Whether or not changes to Units will be logged for sync.
                Use null to not set/change the setting.
            is_virtual_folder_enabled (Union[Unset, bool]): Whether or not changes to VirtualFolder will be logged for sync.
                Use null to not set/change the setting.
            is_workflow_enabled (Union[Unset, bool]): Whether or not changes to Workflow will be logged for sync.
                Use null to not set/change the setting.
     """

    server_name: Union[Unset, str] = UNSET
    site_code: Union[Unset, str] = UNSET
    is_local_server: Union[Unset, bool] = UNSET
    is_conflict_winner: Union[Unset, bool] = UNSET
    sites: Union[Unset, list['VirincoWATSWebDashboardModelsMesDistributionConfigSiteConfig']] = UNSET
    initialize_sync: Union[Unset, bool] = UNSET
    is_culture_enabled: Union[Unset, bool] = UNSET
    is_message_enabled: Union[Unset, bool] = UNSET
    is_process_enabled: Union[Unset, bool] = UNSET
    is_product_category_enabled: Union[Unset, bool] = UNSET
    is_product_enabled: Union[Unset, bool] = UNSET
    is_product_groups_enabled: Union[Unset, bool] = UNSET
    is_production_batch_enabled: Union[Unset, bool] = UNSET
    is_product_revision_enabled: Union[Unset, bool] = UNSET
    is_product_revision_relation_enabled: Union[Unset, bool] = UNSET
    is_site_enabled: Union[Unset, bool] = UNSET
    is_software_package_enabled: Union[Unset, bool] = UNSET
    is_tag_enabled: Union[Unset, bool] = UNSET
    is_test_sequence_enabled: Union[Unset, bool] = UNSET
    is_translation_enabled: Union[Unset, bool] = UNSET
    is_unit_enabled: Union[Unset, bool] = UNSET
    is_virtual_folder_enabled: Union[Unset, bool] = UNSET
    is_workflow_enabled: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_distribution_config_site_config import VirincoWATSWebDashboardModelsMesDistributionConfigSiteConfig
        server_name = self.server_name

        site_code = self.site_code

        is_local_server = self.is_local_server

        is_conflict_winner = self.is_conflict_winner

        sites: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sites, Unset):
            sites = []
            for sites_item_data in self.sites:
                sites_item = sites_item_data.to_dict()
                sites.append(sites_item)



        initialize_sync = self.initialize_sync

        is_culture_enabled = self.is_culture_enabled

        is_message_enabled = self.is_message_enabled

        is_process_enabled = self.is_process_enabled

        is_product_category_enabled = self.is_product_category_enabled

        is_product_enabled = self.is_product_enabled

        is_product_groups_enabled = self.is_product_groups_enabled

        is_production_batch_enabled = self.is_production_batch_enabled

        is_product_revision_enabled = self.is_product_revision_enabled

        is_product_revision_relation_enabled = self.is_product_revision_relation_enabled

        is_site_enabled = self.is_site_enabled

        is_software_package_enabled = self.is_software_package_enabled

        is_tag_enabled = self.is_tag_enabled

        is_test_sequence_enabled = self.is_test_sequence_enabled

        is_translation_enabled = self.is_translation_enabled

        is_unit_enabled = self.is_unit_enabled

        is_virtual_folder_enabled = self.is_virtual_folder_enabled

        is_workflow_enabled = self.is_workflow_enabled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if server_name is not UNSET:
            field_dict["ServerName"] = server_name
        if site_code is not UNSET:
            field_dict["SiteCode"] = site_code
        if is_local_server is not UNSET:
            field_dict["IsLocalServer"] = is_local_server
        if is_conflict_winner is not UNSET:
            field_dict["IsConflictWinner"] = is_conflict_winner
        if sites is not UNSET:
            field_dict["Sites"] = sites
        if initialize_sync is not UNSET:
            field_dict["InitializeSync"] = initialize_sync
        if is_culture_enabled is not UNSET:
            field_dict["IsCultureEnabled"] = is_culture_enabled
        if is_message_enabled is not UNSET:
            field_dict["IsMessageEnabled"] = is_message_enabled
        if is_process_enabled is not UNSET:
            field_dict["IsProcessEnabled"] = is_process_enabled
        if is_product_category_enabled is not UNSET:
            field_dict["IsProductCategoryEnabled"] = is_product_category_enabled
        if is_product_enabled is not UNSET:
            field_dict["IsProductEnabled"] = is_product_enabled
        if is_product_groups_enabled is not UNSET:
            field_dict["IsProductGroupsEnabled"] = is_product_groups_enabled
        if is_production_batch_enabled is not UNSET:
            field_dict["IsProductionBatchEnabled"] = is_production_batch_enabled
        if is_product_revision_enabled is not UNSET:
            field_dict["IsProductRevisionEnabled"] = is_product_revision_enabled
        if is_product_revision_relation_enabled is not UNSET:
            field_dict["IsProductRevisionRelationEnabled"] = is_product_revision_relation_enabled
        if is_site_enabled is not UNSET:
            field_dict["IsSiteEnabled"] = is_site_enabled
        if is_software_package_enabled is not UNSET:
            field_dict["IsSoftwarePackageEnabled"] = is_software_package_enabled
        if is_tag_enabled is not UNSET:
            field_dict["IsTagEnabled"] = is_tag_enabled
        if is_test_sequence_enabled is not UNSET:
            field_dict["IsTestSequenceEnabled"] = is_test_sequence_enabled
        if is_translation_enabled is not UNSET:
            field_dict["IsTranslationEnabled"] = is_translation_enabled
        if is_unit_enabled is not UNSET:
            field_dict["IsUnitEnabled"] = is_unit_enabled
        if is_virtual_folder_enabled is not UNSET:
            field_dict["IsVirtualFolderEnabled"] = is_virtual_folder_enabled
        if is_workflow_enabled is not UNSET:
            field_dict["IsWorkflowEnabled"] = is_workflow_enabled

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_distribution_config_site_config import VirincoWATSWebDashboardModelsMesDistributionConfigSiteConfig
        d = dict(src_dict)
        server_name = d.pop("ServerName", UNSET)

        site_code = d.pop("SiteCode", UNSET)

        is_local_server = d.pop("IsLocalServer", UNSET)

        is_conflict_winner = d.pop("IsConflictWinner", UNSET)

        sites = []
        _sites = d.pop("Sites", UNSET)
        for sites_item_data in (_sites or []):
            sites_item = VirincoWATSWebDashboardModelsMesDistributionConfigSiteConfig.from_dict(sites_item_data)



            sites.append(sites_item)


        initialize_sync = d.pop("InitializeSync", UNSET)

        is_culture_enabled = d.pop("IsCultureEnabled", UNSET)

        is_message_enabled = d.pop("IsMessageEnabled", UNSET)

        is_process_enabled = d.pop("IsProcessEnabled", UNSET)

        is_product_category_enabled = d.pop("IsProductCategoryEnabled", UNSET)

        is_product_enabled = d.pop("IsProductEnabled", UNSET)

        is_product_groups_enabled = d.pop("IsProductGroupsEnabled", UNSET)

        is_production_batch_enabled = d.pop("IsProductionBatchEnabled", UNSET)

        is_product_revision_enabled = d.pop("IsProductRevisionEnabled", UNSET)

        is_product_revision_relation_enabled = d.pop("IsProductRevisionRelationEnabled", UNSET)

        is_site_enabled = d.pop("IsSiteEnabled", UNSET)

        is_software_package_enabled = d.pop("IsSoftwarePackageEnabled", UNSET)

        is_tag_enabled = d.pop("IsTagEnabled", UNSET)

        is_test_sequence_enabled = d.pop("IsTestSequenceEnabled", UNSET)

        is_translation_enabled = d.pop("IsTranslationEnabled", UNSET)

        is_unit_enabled = d.pop("IsUnitEnabled", UNSET)

        is_virtual_folder_enabled = d.pop("IsVirtualFolderEnabled", UNSET)

        is_workflow_enabled = d.pop("IsWorkflowEnabled", UNSET)

        virinco_wats_web_dashboard_models_mes_distribution_config = cls(
            server_name=server_name,
            site_code=site_code,
            is_local_server=is_local_server,
            is_conflict_winner=is_conflict_winner,
            sites=sites,
            initialize_sync=initialize_sync,
            is_culture_enabled=is_culture_enabled,
            is_message_enabled=is_message_enabled,
            is_process_enabled=is_process_enabled,
            is_product_category_enabled=is_product_category_enabled,
            is_product_enabled=is_product_enabled,
            is_product_groups_enabled=is_product_groups_enabled,
            is_production_batch_enabled=is_production_batch_enabled,
            is_product_revision_enabled=is_product_revision_enabled,
            is_product_revision_relation_enabled=is_product_revision_relation_enabled,
            is_site_enabled=is_site_enabled,
            is_software_package_enabled=is_software_package_enabled,
            is_tag_enabled=is_tag_enabled,
            is_test_sequence_enabled=is_test_sequence_enabled,
            is_translation_enabled=is_translation_enabled,
            is_unit_enabled=is_unit_enabled,
            is_virtual_folder_enabled=is_virtual_folder_enabled,
            is_workflow_enabled=is_workflow_enabled,
        )


        virinco_wats_web_dashboard_models_mes_distribution_config.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_distribution_config

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
