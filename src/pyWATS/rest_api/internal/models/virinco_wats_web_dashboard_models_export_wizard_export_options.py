from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_export_wizard_export_options_certificate_details_item import VirincoWATSWebDashboardModelsExportWizardExportOptionsCertificateDetailsItem
from ..models.virinco_wats_web_dashboard_models_export_wizard_export_options_export_data_source import VirincoWATSWebDashboardModelsExportWizardExportOptionsExportDataSource
from ..models.virinco_wats_web_dashboard_models_export_wizard_export_options_export_format import VirincoWATSWebDashboardModelsExportWizardExportOptionsExportFormat
from ..models.virinco_wats_web_dashboard_models_export_wizard_export_options_export_type import VirincoWATSWebDashboardModelsExportWizardExportOptionsExportType
from ..models.virinco_wats_web_dashboard_models_export_wizard_export_options_failure_details_item import VirincoWATSWebDashboardModelsExportWizardExportOptionsFailureDetailsItem
from ..models.virinco_wats_web_dashboard_models_export_wizard_export_options_header_details_item import VirincoWATSWebDashboardModelsExportWizardExportOptionsHeaderDetailsItem
from ..models.virinco_wats_web_dashboard_models_export_wizard_export_options_numeric_format import VirincoWATSWebDashboardModelsExportWizardExportOptionsNumericFormat
from ..models.virinco_wats_web_dashboard_models_export_wizard_export_options_step_details_item import VirincoWATSWebDashboardModelsExportWizardExportOptionsStepDetailsItem
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsExportWizardExportOptions")



@_attrs_define
class VirincoWATSWebDashboardModelsExportWizardExportOptions:
    """ 
        Attributes:
            export_type (Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsExportType]):
            export_data_source (Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsExportDataSource]):
            export_format (Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsExportFormat]):
            header_details (Union[Unset, list[VirincoWATSWebDashboardModelsExportWizardExportOptionsHeaderDetailsItem]]):
            step_details (Union[Unset, list[VirincoWATSWebDashboardModelsExportWizardExportOptionsStepDetailsItem]]):
            failure_details (Union[Unset, list[VirincoWATSWebDashboardModelsExportWizardExportOptionsFailureDetailsItem]]):
            certificate_details (Union[Unset,
                list[VirincoWATSWebDashboardModelsExportWizardExportOptionsCertificateDetailsItem]]):
            body_footer (Union[Unset, str]):
            document_footer (Union[Unset, str]):
            numeric_format (Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsNumericFormat]):
            selected_steps (Union[Unset, list[list[int]]]):
            selected_step_paths (Union[Unset, list[str]]):
     """

    export_type: Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsExportType] = UNSET
    export_data_source: Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsExportDataSource] = UNSET
    export_format: Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsExportFormat] = UNSET
    header_details: Union[Unset, list[VirincoWATSWebDashboardModelsExportWizardExportOptionsHeaderDetailsItem]] = UNSET
    step_details: Union[Unset, list[VirincoWATSWebDashboardModelsExportWizardExportOptionsStepDetailsItem]] = UNSET
    failure_details: Union[Unset, list[VirincoWATSWebDashboardModelsExportWizardExportOptionsFailureDetailsItem]] = UNSET
    certificate_details: Union[Unset, list[VirincoWATSWebDashboardModelsExportWizardExportOptionsCertificateDetailsItem]] = UNSET
    body_footer: Union[Unset, str] = UNSET
    document_footer: Union[Unset, str] = UNSET
    numeric_format: Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsNumericFormat] = UNSET
    selected_steps: Union[Unset, list[list[int]]] = UNSET
    selected_step_paths: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        export_type: Union[Unset, int] = UNSET
        if not isinstance(self.export_type, Unset):
            export_type = self.export_type.value


        export_data_source: Union[Unset, int] = UNSET
        if not isinstance(self.export_data_source, Unset):
            export_data_source = self.export_data_source.value


        export_format: Union[Unset, int] = UNSET
        if not isinstance(self.export_format, Unset):
            export_format = self.export_format.value


        header_details: Union[Unset, list[int]] = UNSET
        if not isinstance(self.header_details, Unset):
            header_details = []
            for header_details_item_data in self.header_details:
                header_details_item = header_details_item_data.value
                header_details.append(header_details_item)



        step_details: Union[Unset, list[int]] = UNSET
        if not isinstance(self.step_details, Unset):
            step_details = []
            for step_details_item_data in self.step_details:
                step_details_item = step_details_item_data.value
                step_details.append(step_details_item)



        failure_details: Union[Unset, list[int]] = UNSET
        if not isinstance(self.failure_details, Unset):
            failure_details = []
            for failure_details_item_data in self.failure_details:
                failure_details_item = failure_details_item_data.value
                failure_details.append(failure_details_item)



        certificate_details: Union[Unset, list[int]] = UNSET
        if not isinstance(self.certificate_details, Unset):
            certificate_details = []
            for certificate_details_item_data in self.certificate_details:
                certificate_details_item = certificate_details_item_data.value
                certificate_details.append(certificate_details_item)



        body_footer = self.body_footer

        document_footer = self.document_footer

        numeric_format: Union[Unset, int] = UNSET
        if not isinstance(self.numeric_format, Unset):
            numeric_format = self.numeric_format.value


        selected_steps: Union[Unset, list[list[int]]] = UNSET
        if not isinstance(self.selected_steps, Unset):
            selected_steps = []
            for selected_steps_item_data in self.selected_steps:
                selected_steps_item = selected_steps_item_data


                selected_steps.append(selected_steps_item)



        selected_step_paths: Union[Unset, list[str]] = UNSET
        if not isinstance(self.selected_step_paths, Unset):
            selected_step_paths = self.selected_step_paths




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if export_type is not UNSET:
            field_dict["exportType"] = export_type
        if export_data_source is not UNSET:
            field_dict["exportDataSource"] = export_data_source
        if export_format is not UNSET:
            field_dict["exportFormat"] = export_format
        if header_details is not UNSET:
            field_dict["headerDetails"] = header_details
        if step_details is not UNSET:
            field_dict["stepDetails"] = step_details
        if failure_details is not UNSET:
            field_dict["failureDetails"] = failure_details
        if certificate_details is not UNSET:
            field_dict["certificateDetails"] = certificate_details
        if body_footer is not UNSET:
            field_dict["bodyFooter"] = body_footer
        if document_footer is not UNSET:
            field_dict["documentFooter"] = document_footer
        if numeric_format is not UNSET:
            field_dict["numericFormat"] = numeric_format
        if selected_steps is not UNSET:
            field_dict["selectedSteps"] = selected_steps
        if selected_step_paths is not UNSET:
            field_dict["selectedStepPaths"] = selected_step_paths

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _export_type = d.pop("exportType", UNSET)
        export_type: Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsExportType]
        if isinstance(_export_type,  Unset):
            export_type = UNSET
        else:
            export_type = VirincoWATSWebDashboardModelsExportWizardExportOptionsExportType(_export_type)




        _export_data_source = d.pop("exportDataSource", UNSET)
        export_data_source: Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsExportDataSource]
        if isinstance(_export_data_source,  Unset):
            export_data_source = UNSET
        else:
            export_data_source = VirincoWATSWebDashboardModelsExportWizardExportOptionsExportDataSource(_export_data_source)




        _export_format = d.pop("exportFormat", UNSET)
        export_format: Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsExportFormat]
        if isinstance(_export_format,  Unset):
            export_format = UNSET
        else:
            export_format = VirincoWATSWebDashboardModelsExportWizardExportOptionsExportFormat(_export_format)




        header_details = []
        _header_details = d.pop("headerDetails", UNSET)
        for header_details_item_data in (_header_details or []):
            header_details_item = VirincoWATSWebDashboardModelsExportWizardExportOptionsHeaderDetailsItem(header_details_item_data)



            header_details.append(header_details_item)


        step_details = []
        _step_details = d.pop("stepDetails", UNSET)
        for step_details_item_data in (_step_details or []):
            step_details_item = VirincoWATSWebDashboardModelsExportWizardExportOptionsStepDetailsItem(step_details_item_data)



            step_details.append(step_details_item)


        failure_details = []
        _failure_details = d.pop("failureDetails", UNSET)
        for failure_details_item_data in (_failure_details or []):
            failure_details_item = VirincoWATSWebDashboardModelsExportWizardExportOptionsFailureDetailsItem(failure_details_item_data)



            failure_details.append(failure_details_item)


        certificate_details = []
        _certificate_details = d.pop("certificateDetails", UNSET)
        for certificate_details_item_data in (_certificate_details or []):
            certificate_details_item = VirincoWATSWebDashboardModelsExportWizardExportOptionsCertificateDetailsItem(certificate_details_item_data)



            certificate_details.append(certificate_details_item)


        body_footer = d.pop("bodyFooter", UNSET)

        document_footer = d.pop("documentFooter", UNSET)

        _numeric_format = d.pop("numericFormat", UNSET)
        numeric_format: Union[Unset, VirincoWATSWebDashboardModelsExportWizardExportOptionsNumericFormat]
        if isinstance(_numeric_format,  Unset):
            numeric_format = UNSET
        else:
            numeric_format = VirincoWATSWebDashboardModelsExportWizardExportOptionsNumericFormat(_numeric_format)




        selected_steps = []
        _selected_steps = d.pop("selectedSteps", UNSET)
        for selected_steps_item_data in (_selected_steps or []):
            selected_steps_item = cast(list[int], selected_steps_item_data)

            selected_steps.append(selected_steps_item)


        selected_step_paths = cast(list[str], d.pop("selectedStepPaths", UNSET))


        virinco_wats_web_dashboard_models_export_wizard_export_options = cls(
            export_type=export_type,
            export_data_source=export_data_source,
            export_format=export_format,
            header_details=header_details,
            step_details=step_details,
            failure_details=failure_details,
            certificate_details=certificate_details,
            body_footer=body_footer,
            document_footer=document_footer,
            numeric_format=numeric_format,
            selected_steps=selected_steps,
            selected_step_paths=selected_step_paths,
        )


        virinco_wats_web_dashboard_models_export_wizard_export_options.additional_properties = d
        return virinco_wats_web_dashboard_models_export_wizard_export_options

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
