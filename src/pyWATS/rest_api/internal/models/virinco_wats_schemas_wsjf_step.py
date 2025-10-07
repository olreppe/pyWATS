from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_schemas_wsjf_sequence_call import VirincoWATSSchemasWSJFSequenceCall
  from ..models.virinco_wats_schemas_wsjf_message_popup import VirincoWATSSchemasWSJFMessagePopup
  from ..models.virinco_wats_schemas_wsjf_string_measurement import VirincoWATSSchemasWSJFStringMeasurement
  from ..models.virinco_wats_schemas_wsjf_attachment import VirincoWATSSchemasWSJFAttachment
  from ..models.virinco_wats_schemas_wsjf_call_exe import VirincoWATSSchemasWSJFCallExe
  from ..models.virinco_wats_schemas_wsjf_additional_data import VirincoWATSSchemasWSJFAdditionalData
  from ..models.virinco_wats_schemas_wsjf_chart import VirincoWATSSchemasWSJFChart
  from ..models.virinco_wats_schemas_wsjf_loop_info import VirincoWATSSchemasWSJFLoopInfo
  from ..models.virinco_wats_schemas_wsjf_boolean_measurement import VirincoWATSSchemasWSJFBooleanMeasurement
  from ..models.virinco_wats_schemas_wsjf_numeric_measurement import VirincoWATSSchemasWSJFNumericMeasurement





T = TypeVar("T", bound="VirincoWATSSchemasWSJFStep")



@_attrs_define
class VirincoWATSSchemasWSJFStep:
    """ 
        Attributes:
            id (Union[Unset, int]): StepID = "step order number". Runtime index of step. Also used as unique step identifier
                within a report.
            group (Union[Unset, str]): Step group, valid values: S,M,C (Setup, Main, Cleanup).
            step_type (Union[Unset, str]): Step type, textual description of step.
            interactive_exe_num (Union[Unset, int]): Interactive exe number of step.
            interactive_exe_num_format (Union[Unset, str]): Numeric format of interactive exe number.
            loop (Union[Unset, VirincoWATSSchemasWSJFLoopInfo]):
            name (Union[Unset, str]): Step name.
            start (Union[Unset, datetime.datetime]): Start date/time of step (with utc offset).
            status (Union[Unset, str]): Step status, valid values: P,F,D,S,E,T,U (Passed, Failed, Done, Skipped, Error,
                Terminated, Unknown).
            error_code (Union[Unset, int]): Step error code.
            error_code_format (Union[Unset, str]): Numeric format of error code.
            error_message (Union[Unset, str]): Step error message.
            ts_guid (Union[Unset, str]):
            tot_time (Union[Unset, float]): Total time of step.
            tot_time_format (Union[Unset, str]): Numeric format of total time.
            caused_seq_failure (Union[Unset, bool]): Did the step cause the sequence to fail?
            caused_uut_failure (Union[Unset, bool]): Did the step cause the UUT to fail?
            report_text (Union[Unset, str]): Step comment.
            steps (Union[Unset, list['VirincoWATSSchemasWSJFStep']]): List of sub steps.
            numeric_meas (Union[Unset, list['VirincoWATSSchemasWSJFNumericMeasurement']]): List of numeric limit
                measurements.
            string_meas (Union[Unset, list['VirincoWATSSchemasWSJFStringMeasurement']]): List of string value measurements.
            boolean_meas (Union[Unset, list['VirincoWATSSchemasWSJFBooleanMeasurement']]): List of pass/fail measurements.
            additional_results (Union[Unset, list['VirincoWATSSchemasWSJFAdditionalData']]): List of additional results
                (free xml).
            seq_call (Union[Unset, VirincoWATSSchemasWSJFSequenceCall]):
            call_exe (Union[Unset, VirincoWATSSchemasWSJFCallExe]):
            message_popup (Union[Unset, VirincoWATSSchemasWSJFMessagePopup]):
            chart (Union[Unset, VirincoWATSSchemasWSJFChart]):
            attachment (Union[Unset, VirincoWATSSchemasWSJFAttachment]):
     """

    id: Union[Unset, int] = UNSET
    group: Union[Unset, str] = UNSET
    step_type: Union[Unset, str] = UNSET
    interactive_exe_num: Union[Unset, int] = UNSET
    interactive_exe_num_format: Union[Unset, str] = UNSET
    loop: Union[Unset, 'VirincoWATSSchemasWSJFLoopInfo'] = UNSET
    name: Union[Unset, str] = UNSET
    start: Union[Unset, datetime.datetime] = UNSET
    status: Union[Unset, str] = UNSET
    error_code: Union[Unset, int] = UNSET
    error_code_format: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    ts_guid: Union[Unset, str] = UNSET
    tot_time: Union[Unset, float] = UNSET
    tot_time_format: Union[Unset, str] = UNSET
    caused_seq_failure: Union[Unset, bool] = UNSET
    caused_uut_failure: Union[Unset, bool] = UNSET
    report_text: Union[Unset, str] = UNSET
    steps: Union[Unset, list['VirincoWATSSchemasWSJFStep']] = UNSET
    numeric_meas: Union[Unset, list['VirincoWATSSchemasWSJFNumericMeasurement']] = UNSET
    string_meas: Union[Unset, list['VirincoWATSSchemasWSJFStringMeasurement']] = UNSET
    boolean_meas: Union[Unset, list['VirincoWATSSchemasWSJFBooleanMeasurement']] = UNSET
    additional_results: Union[Unset, list['VirincoWATSSchemasWSJFAdditionalData']] = UNSET
    seq_call: Union[Unset, 'VirincoWATSSchemasWSJFSequenceCall'] = UNSET
    call_exe: Union[Unset, 'VirincoWATSSchemasWSJFCallExe'] = UNSET
    message_popup: Union[Unset, 'VirincoWATSSchemasWSJFMessagePopup'] = UNSET
    chart: Union[Unset, 'VirincoWATSSchemasWSJFChart'] = UNSET
    attachment: Union[Unset, 'VirincoWATSSchemasWSJFAttachment'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_schemas_wsjf_sequence_call import VirincoWATSSchemasWSJFSequenceCall
        from ..models.virinco_wats_schemas_wsjf_message_popup import VirincoWATSSchemasWSJFMessagePopup
        from ..models.virinco_wats_schemas_wsjf_string_measurement import VirincoWATSSchemasWSJFStringMeasurement
        from ..models.virinco_wats_schemas_wsjf_attachment import VirincoWATSSchemasWSJFAttachment
        from ..models.virinco_wats_schemas_wsjf_call_exe import VirincoWATSSchemasWSJFCallExe
        from ..models.virinco_wats_schemas_wsjf_additional_data import VirincoWATSSchemasWSJFAdditionalData
        from ..models.virinco_wats_schemas_wsjf_chart import VirincoWATSSchemasWSJFChart
        from ..models.virinco_wats_schemas_wsjf_loop_info import VirincoWATSSchemasWSJFLoopInfo
        from ..models.virinco_wats_schemas_wsjf_boolean_measurement import VirincoWATSSchemasWSJFBooleanMeasurement
        from ..models.virinco_wats_schemas_wsjf_numeric_measurement import VirincoWATSSchemasWSJFNumericMeasurement
        id = self.id

        group = self.group

        step_type = self.step_type

        interactive_exe_num = self.interactive_exe_num

        interactive_exe_num_format = self.interactive_exe_num_format

        loop: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.loop, Unset):
            loop = self.loop.to_dict()

        name = self.name

        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        status = self.status

        error_code = self.error_code

        error_code_format = self.error_code_format

        error_message = self.error_message

        ts_guid = self.ts_guid

        tot_time = self.tot_time

        tot_time_format = self.tot_time_format

        caused_seq_failure = self.caused_seq_failure

        caused_uut_failure = self.caused_uut_failure

        report_text = self.report_text

        steps: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.steps, Unset):
            steps = []
            for steps_item_data in self.steps:
                steps_item = steps_item_data.to_dict()
                steps.append(steps_item)



        numeric_meas: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.numeric_meas, Unset):
            numeric_meas = []
            for numeric_meas_item_data in self.numeric_meas:
                numeric_meas_item = numeric_meas_item_data.to_dict()
                numeric_meas.append(numeric_meas_item)



        string_meas: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.string_meas, Unset):
            string_meas = []
            for string_meas_item_data in self.string_meas:
                string_meas_item = string_meas_item_data.to_dict()
                string_meas.append(string_meas_item)



        boolean_meas: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.boolean_meas, Unset):
            boolean_meas = []
            for boolean_meas_item_data in self.boolean_meas:
                boolean_meas_item = boolean_meas_item_data.to_dict()
                boolean_meas.append(boolean_meas_item)



        additional_results: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.additional_results, Unset):
            additional_results = []
            for additional_results_item_data in self.additional_results:
                additional_results_item = additional_results_item_data.to_dict()
                additional_results.append(additional_results_item)



        seq_call: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.seq_call, Unset):
            seq_call = self.seq_call.to_dict()

        call_exe: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.call_exe, Unset):
            call_exe = self.call_exe.to_dict()

        message_popup: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.message_popup, Unset):
            message_popup = self.message_popup.to_dict()

        chart: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.chart, Unset):
            chart = self.chart.to_dict()

        attachment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attachment, Unset):
            attachment = self.attachment.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if group is not UNSET:
            field_dict["group"] = group
        if step_type is not UNSET:
            field_dict["stepType"] = step_type
        if interactive_exe_num is not UNSET:
            field_dict["interactiveExeNum"] = interactive_exe_num
        if interactive_exe_num_format is not UNSET:
            field_dict["interactiveExeNumFormat"] = interactive_exe_num_format
        if loop is not UNSET:
            field_dict["loop"] = loop
        if name is not UNSET:
            field_dict["name"] = name
        if start is not UNSET:
            field_dict["start"] = start
        if status is not UNSET:
            field_dict["status"] = status
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if error_code_format is not UNSET:
            field_dict["errorCodeFormat"] = error_code_format
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if ts_guid is not UNSET:
            field_dict["tsGuid"] = ts_guid
        if tot_time is not UNSET:
            field_dict["totTime"] = tot_time
        if tot_time_format is not UNSET:
            field_dict["totTimeFormat"] = tot_time_format
        if caused_seq_failure is not UNSET:
            field_dict["causedSeqFailure"] = caused_seq_failure
        if caused_uut_failure is not UNSET:
            field_dict["causedUUTFailure"] = caused_uut_failure
        if report_text is not UNSET:
            field_dict["reportText"] = report_text
        if steps is not UNSET:
            field_dict["steps"] = steps
        if numeric_meas is not UNSET:
            field_dict["numericMeas"] = numeric_meas
        if string_meas is not UNSET:
            field_dict["stringMeas"] = string_meas
        if boolean_meas is not UNSET:
            field_dict["booleanMeas"] = boolean_meas
        if additional_results is not UNSET:
            field_dict["additionalResults"] = additional_results
        if seq_call is not UNSET:
            field_dict["seqCall"] = seq_call
        if call_exe is not UNSET:
            field_dict["callExe"] = call_exe
        if message_popup is not UNSET:
            field_dict["messagePopup"] = message_popup
        if chart is not UNSET:
            field_dict["chart"] = chart
        if attachment is not UNSET:
            field_dict["attachment"] = attachment

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_schemas_wsjf_sequence_call import VirincoWATSSchemasWSJFSequenceCall
        from ..models.virinco_wats_schemas_wsjf_message_popup import VirincoWATSSchemasWSJFMessagePopup
        from ..models.virinco_wats_schemas_wsjf_string_measurement import VirincoWATSSchemasWSJFStringMeasurement
        from ..models.virinco_wats_schemas_wsjf_attachment import VirincoWATSSchemasWSJFAttachment
        from ..models.virinco_wats_schemas_wsjf_call_exe import VirincoWATSSchemasWSJFCallExe
        from ..models.virinco_wats_schemas_wsjf_additional_data import VirincoWATSSchemasWSJFAdditionalData
        from ..models.virinco_wats_schemas_wsjf_chart import VirincoWATSSchemasWSJFChart
        from ..models.virinco_wats_schemas_wsjf_loop_info import VirincoWATSSchemasWSJFLoopInfo
        from ..models.virinco_wats_schemas_wsjf_boolean_measurement import VirincoWATSSchemasWSJFBooleanMeasurement
        from ..models.virinco_wats_schemas_wsjf_numeric_measurement import VirincoWATSSchemasWSJFNumericMeasurement
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        group = d.pop("group", UNSET)

        step_type = d.pop("stepType", UNSET)

        interactive_exe_num = d.pop("interactiveExeNum", UNSET)

        interactive_exe_num_format = d.pop("interactiveExeNumFormat", UNSET)

        _loop = d.pop("loop", UNSET)
        loop: Union[Unset, VirincoWATSSchemasWSJFLoopInfo]
        if isinstance(_loop,  Unset):
            loop = UNSET
        else:
            loop = VirincoWATSSchemasWSJFLoopInfo.from_dict(_loop)




        name = d.pop("name", UNSET)

        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.datetime]
        if isinstance(_start,  Unset):
            start = UNSET
        else:
            start = isoparse(_start)




        status = d.pop("status", UNSET)

        error_code = d.pop("errorCode", UNSET)

        error_code_format = d.pop("errorCodeFormat", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        ts_guid = d.pop("tsGuid", UNSET)

        tot_time = d.pop("totTime", UNSET)

        tot_time_format = d.pop("totTimeFormat", UNSET)

        caused_seq_failure = d.pop("causedSeqFailure", UNSET)

        caused_uut_failure = d.pop("causedUUTFailure", UNSET)

        report_text = d.pop("reportText", UNSET)

        steps = []
        _steps = d.pop("steps", UNSET)
        for steps_item_data in (_steps or []):
            steps_item = VirincoWATSSchemasWSJFStep.from_dict(steps_item_data)



            steps.append(steps_item)


        numeric_meas = []
        _numeric_meas = d.pop("numericMeas", UNSET)
        for numeric_meas_item_data in (_numeric_meas or []):
            numeric_meas_item = VirincoWATSSchemasWSJFNumericMeasurement.from_dict(numeric_meas_item_data)



            numeric_meas.append(numeric_meas_item)


        string_meas = []
        _string_meas = d.pop("stringMeas", UNSET)
        for string_meas_item_data in (_string_meas or []):
            string_meas_item = VirincoWATSSchemasWSJFStringMeasurement.from_dict(string_meas_item_data)



            string_meas.append(string_meas_item)


        boolean_meas = []
        _boolean_meas = d.pop("booleanMeas", UNSET)
        for boolean_meas_item_data in (_boolean_meas or []):
            boolean_meas_item = VirincoWATSSchemasWSJFBooleanMeasurement.from_dict(boolean_meas_item_data)



            boolean_meas.append(boolean_meas_item)


        additional_results = []
        _additional_results = d.pop("additionalResults", UNSET)
        for additional_results_item_data in (_additional_results or []):
            additional_results_item = VirincoWATSSchemasWSJFAdditionalData.from_dict(additional_results_item_data)



            additional_results.append(additional_results_item)


        _seq_call = d.pop("seqCall", UNSET)
        seq_call: Union[Unset, VirincoWATSSchemasWSJFSequenceCall]
        if isinstance(_seq_call,  Unset):
            seq_call = UNSET
        else:
            seq_call = VirincoWATSSchemasWSJFSequenceCall.from_dict(_seq_call)




        _call_exe = d.pop("callExe", UNSET)
        call_exe: Union[Unset, VirincoWATSSchemasWSJFCallExe]
        if isinstance(_call_exe,  Unset):
            call_exe = UNSET
        else:
            call_exe = VirincoWATSSchemasWSJFCallExe.from_dict(_call_exe)




        _message_popup = d.pop("messagePopup", UNSET)
        message_popup: Union[Unset, VirincoWATSSchemasWSJFMessagePopup]
        if isinstance(_message_popup,  Unset):
            message_popup = UNSET
        else:
            message_popup = VirincoWATSSchemasWSJFMessagePopup.from_dict(_message_popup)




        _chart = d.pop("chart", UNSET)
        chart: Union[Unset, VirincoWATSSchemasWSJFChart]
        if isinstance(_chart,  Unset):
            chart = UNSET
        else:
            chart = VirincoWATSSchemasWSJFChart.from_dict(_chart)




        _attachment = d.pop("attachment", UNSET)
        attachment: Union[Unset, VirincoWATSSchemasWSJFAttachment]
        if isinstance(_attachment,  Unset):
            attachment = UNSET
        else:
            attachment = VirincoWATSSchemasWSJFAttachment.from_dict(_attachment)




        virinco_wats_schemas_wsjf_step = cls(
            id=id,
            group=group,
            step_type=step_type,
            interactive_exe_num=interactive_exe_num,
            interactive_exe_num_format=interactive_exe_num_format,
            loop=loop,
            name=name,
            start=start,
            status=status,
            error_code=error_code,
            error_code_format=error_code_format,
            error_message=error_message,
            ts_guid=ts_guid,
            tot_time=tot_time,
            tot_time_format=tot_time_format,
            caused_seq_failure=caused_seq_failure,
            caused_uut_failure=caused_uut_failure,
            report_text=report_text,
            steps=steps,
            numeric_meas=numeric_meas,
            string_meas=string_meas,
            boolean_meas=boolean_meas,
            additional_results=additional_results,
            seq_call=seq_call,
            call_exe=call_exe,
            message_popup=message_popup,
            chart=chart,
            attachment=attachment,
        )


        virinco_wats_schemas_wsjf_step.additional_properties = d
        return virinco_wats_schemas_wsjf_step

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
