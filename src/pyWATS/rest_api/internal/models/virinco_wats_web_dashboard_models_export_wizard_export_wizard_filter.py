from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_export_wizard_export_wizard_filter_step_grouping import VirincoWATSWebDashboardModelsExportWizardExportWizardFilterStepGrouping
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_export_wizard_export_options import VirincoWATSWebDashboardModelsExportWizardExportOptions
  from ..models.virinco_wats_web_dashboard_models_sequence_selection import VirincoWATSWebDashboardModelsSequenceSelection
  from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsExportWizardExportWizardFilter")



@_attrs_define
class VirincoWATSWebDashboardModelsExportWizardExportWizardFilter:
    """ 
        Attributes:
            wats_filter (Union[Unset, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter]): Wats filter exposed in
                rest API
            selection_filter (Union[Unset, list['VirincoWATSWebDashboardModelsSequenceSelection']]):
            step_grouping (Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportWizardFilterStepGrouping]):
            export_options (Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptions]):
            email (Union[Unset, str]):
     """

    wats_filter: Union[Unset, 'VirincoWATSWebDashboardControllersApiAppPublicWatsFilter'] = UNSET
    selection_filter: Union[Unset, list['VirincoWATSWebDashboardModelsSequenceSelection']] = UNSET
    step_grouping: Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportWizardFilterStepGrouping] = UNSET
    export_options: Union[Unset, 'VirincoWATSWebDashboardModelsExportWizardExportOptions'] = UNSET
    email: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_export_wizard_export_options import VirincoWATSWebDashboardModelsExportWizardExportOptions
        from ..models.virinco_wats_web_dashboard_models_sequence_selection import VirincoWATSWebDashboardModelsSequenceSelection
        from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter
        wats_filter: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.wats_filter, Unset):
            wats_filter = self.wats_filter.to_dict()

        selection_filter: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.selection_filter, Unset):
            selection_filter = []
            for selection_filter_item_data in self.selection_filter:
                selection_filter_item = selection_filter_item_data.to_dict()
                selection_filter.append(selection_filter_item)



        step_grouping: Union[Unset, int] = UNSET
        if not isinstance(self.step_grouping, Unset):
            step_grouping = self.step_grouping.value


        export_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.export_options, Unset):
            export_options = self.export_options.to_dict()

        email = self.email


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if wats_filter is not UNSET:
            field_dict["watsFilter"] = wats_filter
        if selection_filter is not UNSET:
            field_dict["selectionFilter"] = selection_filter
        if step_grouping is not UNSET:
            field_dict["stepGrouping"] = step_grouping
        if export_options is not UNSET:
            field_dict["exportOptions"] = export_options
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_export_wizard_export_options import VirincoWATSWebDashboardModelsExportWizardExportOptions
        from ..models.virinco_wats_web_dashboard_models_sequence_selection import VirincoWATSWebDashboardModelsSequenceSelection
        from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter
        d = dict(src_dict)
        _wats_filter = d.pop("watsFilter", UNSET)
        wats_filter: Union[Unset, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter]
        if isinstance(_wats_filter,  Unset):
            wats_filter = UNSET
        else:
            wats_filter = VirincoWATSWebDashboardControllersApiAppPublicWatsFilter.from_dict(_wats_filter)




        selection_filter = []
        _selection_filter = d.pop("selectionFilter", UNSET)
        for selection_filter_item_data in (_selection_filter or []):
            selection_filter_item = VirincoWATSWebDashboardModelsSequenceSelection.from_dict(selection_filter_item_data)



            selection_filter.append(selection_filter_item)


        _step_grouping = d.pop("stepGrouping", UNSET)
        step_grouping: Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportWizardFilterStepGrouping]
        if isinstance(_step_grouping,  Unset):
            step_grouping = UNSET
        else:
            step_grouping = VirincoWATSWebDashboardModelsExportWizardExportWizardFilterStepGrouping(_step_grouping)




        _export_options = d.pop("exportOptions", UNSET)
        export_options: Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptions]
        if isinstance(_export_options,  Unset):
            export_options = UNSET
        else:
            export_options = VirincoWATSWebDashboardModelsExportWizardExportOptions.from_dict(_export_options)




        email = d.pop("email", UNSET)

        virinco_wats_web_dashboard_models_export_wizard_export_wizard_filter = cls(
            wats_filter=wats_filter,
            selection_filter=selection_filter,
            step_grouping=step_grouping,
            export_options=export_options,
            email=email,
        )


        virinco_wats_web_dashboard_models_export_wizard_export_wizard_filter.additional_properties = d
        return virinco_wats_web_dashboard_models_export_wizard_export_wizard_filter

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
