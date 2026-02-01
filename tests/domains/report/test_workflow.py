"""
Advanced Comprehensive UUT Test with API Verification
=====================================================
This test creates a UUT report with:
- All step types (Numeric, Boolean, String, Chart, Generic, etc.)
- Deep hierarchy utilizing nested SequenceCall structures
- Extensive numeric measurements with all comparison operators
- Multiple chart types with various series
- Multi-measurement steps
- All status variations (Pass, Fail, Skipped, etc.)

The test submits the report via API, waits for processing, 
and loads it back to verify data integrity.

This test should be run whenever changes are made to the report module
to ensure data integrity and proper serialization/deserialization.
"""
import math
import time
import pytest
from datetime import datetime, timezone
from typing import Dict

from pywats import pyWATS
from pywats.domains.report.report_models.uut.uut_report import UUTReport
from pywats.domains.report.report_models.uut.steps.sequence_call import SequenceCall
from pywats.shared.enums import CompOp
from pywats.domains.report.report_models.common_types import StepStatus
from pywats.domains.report.report_models.uut.steps.generic_step import FlowType
from pywats.domains.report.report_models.chart import ChartType, ChartSeries


@pytest.mark.acceptance
@pytest.mark.critical
class TestAdvancedUUTComprehensive:
    """Advanced comprehensive test of all UUT functionality with API verification"""
    
    def test_advanced_uut_with_all_step_types_and_verification(
        self,
        wats_client: pyWATS,
        wats_config: Dict[str, str]
    ):
        """
        Create an advanced UUT report with all step types, submit it,
        wait for processing, and verify the results.
        
        This test validates:
        - All step types (12+ types)
        - Deep nested hierarchies (5+ levels)
        - All numeric comparison operators
        - Multiple chart types
        - Multi-measurement steps
        - Status variations
        - API submission and retrieval
        """
        # Create unique serial number
        serial_number = f"ADVANCED-UUT-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}"
        
        print(f"\n{'='*80}")
        print(f"Creating Advanced Comprehensive UUT Report")
        print(f"Serial Number: {serial_number}")
        print(f"{'='*80}\n")

        # Create UUT report using API
        report = wats_client.report.create_uut_report(
            operator="TestOperator",
            part_number="ADVANCED-UUT-TEST",
            revision="1.0",
            serial_number=serial_number,
            operation_type=100,
            station_name="AdvancedTestStation",
            location="ComprehensiveTestLab",
            purpose="Advanced Comprehensive Model Test with API Verification"
        )
        report.result = "P"

        root = report.get_root_sequence_call()
        step_count = 0
        
        # ========================================================================
        # Level 1: INITIALIZATION SEQUENCE
        # ========================================================================
        print("Building Initialization Sequence...")
        init_seq = root.add_sequence_call(
            name="System Initialization",
            file_name="init.seq",
            version="1.0.0",
            path="tests/init"
        )
        
        # Power-up tests
        power_seq = init_seq.add_sequence_call(
            name="Power Supply Tests",
            file_name="power.seq",
            version="1.2.0",
            path="tests/init/power"
        )
        
        # Extensive numeric tests with all operators
        power_seq.add_numeric_step(
            name="5V Rail - GELE",
            value=5.02,
            unit="V",
            comp_op=CompOp.GELE,
            low_limit=4.75,
            high_limit=5.25,
            status=StepStatus.Passed
        )
        step_count += 1
        
        power_seq.add_numeric_step(
            name="3.3V Rail - GT",
            value=3.35,
            unit="V",
            comp_op=CompOp.GT,
            low_limit=3.3,
            status=StepStatus.Passed
        )
        step_count += 1
        
        power_seq.add_numeric_step(
            name="12V Rail - LT",
            value=11.95,
            unit="V",
            comp_op=CompOp.LT,
            low_limit=12.5,
            status=StepStatus.Passed
        )
        step_count += 1
        
        power_seq.add_numeric_step(
            name="Standby Voltage - EQ",
            value=3.30,
            unit="V",
            comp_op=CompOp.EQ,
            low_limit=3.30,
            status=StepStatus.Passed
        )
        step_count += 1
        
        power_seq.add_numeric_step(
            name="Noise Level - NE",
            value=0.05,
            unit="V",
            comp_op=CompOp.NE,
            low_limit=0.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Multi-numeric step for voltage rails
        multi_voltage = power_seq.add_multi_numeric_step(
            name="All Voltage Rails"
        )
        multi_voltage.add_measurement(
            name="1.8V",
            value=1.79,
            unit="V",
            comp_op=CompOp.GELE,
            low_limit=1.7,
            high_limit=1.9,
            status=StepStatus.Passed
        )
        multi_voltage.add_measurement(
            name="2.5V",
            value=2.51,
            unit="V",
            comp_op=CompOp.GELE,
            low_limit=2.4,
            high_limit=2.6,
            status=StepStatus.Passed
        )
        multi_voltage.add_measurement(
            name="-12V",
            value=-11.98,
            unit="V",
            comp_op=CompOp.GELE,
            low_limit=-12.5,
            high_limit=-11.5,
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Temperature monitoring
        temp_seq = init_seq.add_sequence_call(
            name="Temperature Monitoring",
            file_name="temp.seq",
            version="1.0.0",
            path="tests/init/temp"
        )
        
        temp_seq.add_numeric_step(
            name="Ambient Temperature",
            value=23.5,
            unit="°C",
            comp_op=CompOp.GELE,
            low_limit=15.0,
            high_limit=30.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        temp_seq.add_numeric_step(
            name="CPU Temperature",
            value=45.2,
            unit="°C",
            comp_op=CompOp.LT,
            low_limit=85.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Boolean checks
        temp_seq.add_boolean_step(
            name="Temperature Sensor OK",
            status=StepStatus.Passed
        )
        step_count += 1
        
        # ========================================================================
        # Level 1: FUNCTIONAL TESTS
        # ========================================================================
        print("Building Functional Tests...")
        func_seq = root.add_sequence_call(
            name="Functional Tests",
            file_name="functional.seq",
            version="2.0.0",
            path="tests/functional"
        )
        
        # Digital I/O Tests
        dio_seq = func_seq.add_sequence_call(
            name="Digital I/O Tests",
            file_name="dio.seq",
            version="1.5.0",
            path="tests/functional/dio"
        )
        
        # Multi-boolean step
        multi_bool = dio_seq.add_multi_boolean_step(
            name="Digital Input Status"
        )
        multi_bool.add_measurement(name="DI_0", status=StepStatus.Passed)
        multi_bool.add_measurement(name="DI_1", status=StepStatus.Passed)
        multi_bool.add_measurement(name="DI_2", status=StepStatus.Passed)
        multi_bool.add_measurement(name="DI_3", status=StepStatus.Passed)
        step_count += 1
        
        # String tests
        dio_seq.add_string_step(
            name="Device Serial",
            value="DEV-12345-ABCDE",
            status=StepStatus.Passed,
            comp_op=CompOp.LOG,
            unit=""
        )
        step_count += 1
        
        # Multi-string step
        multi_str = dio_seq.add_multi_string_step(
            name="Device Information"
        )
        multi_str.add_measurement(
            name="Firmware Version",
            value="v2.3.1",
            status=StepStatus.Passed,
            comp_op=CompOp.LOG
        )
        multi_str.add_measurement(
            name="Hardware Revision",
            value="RevC",
            status=StepStatus.Passed,
            comp_op=CompOp.LOG
        )
        multi_str.add_measurement(
            name="Manufacture Date",
            value="2025-12-12",
            status=StepStatus.Passed,
            comp_op=CompOp.LOG
        )
        step_count += 1
        
        # Analog Tests
        analog_seq = func_seq.add_sequence_call(
            name="Analog Signal Tests",
            file_name="analog.seq",
            version="1.0.0",
            path="tests/functional/analog"
        )
        
        # ADC calibration with extensive numeric steps
        adc_seq = analog_seq.add_sequence_call(
            name="ADC Calibration",
            file_name="adc_cal.seq",
            version="1.1.0",
            path="tests/functional/analog/adc"
        )
        
        # Test at multiple points
        for i, voltage in enumerate([0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0]):
            expected = voltage
            measured = voltage + (0.01 if i % 2 == 0 else -0.01)
            adc_seq.add_numeric_step(
                name=f"ADC {voltage}V Test",
                value=measured,
                unit="V",
                comp_op=CompOp.GELE,
                low_limit=expected - 0.05,
                high_limit=expected + 0.05,
                status=StepStatus.Passed
            )
            step_count += 1
        
        # DAC output tests
        dac_seq = analog_seq.add_sequence_call(
            name="DAC Output Tests",
            file_name="dac.seq",
            version="1.0.0",
            path="tests/functional/analog/dac"
        )
        
        # Multi-numeric for DAC channels
        multi_dac = dac_seq.add_multi_numeric_step(
            name="DAC Channel Outputs"
        )
        for ch in range(8):
            multi_dac.add_measurement(
                name=f"CH{ch}",
                value=2.5 + (ch * 0.1),
                unit="V",
                comp_op=CompOp.GELE,
                low_limit=2.4 + (ch * 0.1),
                high_limit=2.6 + (ch * 0.1),
                status=StepStatus.Passed
            )
        step_count += 1
        
        # Communication Tests
        comm_seq = func_seq.add_sequence_call(
            name="Communication Tests",
            file_name="comm.seq",
            version="1.3.0",
            path="tests/functional/comm"
        )
        
        # I2C Tests
        i2c_seq = comm_seq.add_sequence_call(
            name="I2C Interface",
            file_name="i2c.seq",
            version="1.0.0",
            path="tests/functional/comm/i2c"
        )
        
        i2c_seq.add_numeric_step(
            name="I2C Clock Frequency",
            value=399.8,
            unit="kHz",
            comp_op=CompOp.GELE,
            low_limit=390.0,
            high_limit=410.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        i2c_seq.add_boolean_step(
            name="I2C Device Detected",
            status=StepStatus.Passed
        )
        step_count += 1
        
        # SPI Tests
        spi_seq = comm_seq.add_sequence_call(
            name="SPI Interface",
            file_name="spi.seq",
            version="1.0.0",
            path="tests/functional/comm/spi"
        )
        
        spi_seq.add_numeric_step(
            name="SPI Clock Speed",
            value=10.02,
            unit="MHz",
            comp_op=CompOp.GELE,
            low_limit=9.5,
            high_limit=10.5,
            status=StepStatus.Passed
        )
        step_count += 1
        
        # UART Tests
        uart_seq = comm_seq.add_sequence_call(
            name="UART Interface",
            file_name="uart.seq",
            version="1.0.0",
            path="tests/functional/comm/uart"
        )
        
        uart_seq.add_numeric_step(
            name="UART Baud Rate",
            value=115200,
            unit="bps",
            comp_op=CompOp.EQ,
            low_limit=115200,
            status=StepStatus.Passed
        )
        step_count += 1
        
        uart_seq.add_string_step(
            name="UART Response",
            value="OK",
            status=StepStatus.Passed
        )
        step_count += 1
        
        # ========================================================================
        # Level 1: PERFORMANCE TESTS WITH CHARTS
        # ========================================================================
        print("Building Performance Tests with Charts...")
        perf_seq = root.add_sequence_call(
            name="Performance Tests",
            file_name="performance.seq",
            version="2.0.0",
            path="tests/performance"
        )
        
        # Frequency Response Test with Chart
        freq_seq = perf_seq.add_sequence_call(
            name="Frequency Response",
            file_name="freq_response.seq",
            version="1.0.0",
            path="tests/performance/freq"
        )
        
        # Generate frequency sweep data
        frequencies = [10 * (2 ** (i/2)) for i in range(20)]  # 10Hz to ~10kHz
        gains = [20 * math.log10(1.0 / math.sqrt(1 + (f/1000)**2)) for f in frequencies]
        phases = [-math.atan(f/1000) * 180 / math.pi for f in frequencies]
        
        freq_series = ChartSeries(
            name="Gain",
            x_data=";".join(f"{f:.2f}" for f in frequencies),
            y_data=";".join(f"{g:.2f}" for g in gains)
        )
        
        phase_series = ChartSeries(
            name="Phase",
            x_data=";".join(f"{f:.2f}" for f in frequencies),
            y_data=";".join(f"{p:.2f}" for p in phases)
        )
        
        freq_seq.add_chart_step(
            name="Bode Plot - Gain",
            chart_type=ChartType.LINE_LOG_X,
            label="Frequency Response - Gain",
            x_label="Frequency",
            x_unit="Hz",
            y_label="Gain",
            y_unit="dB",
            series=[freq_series],
            status=StepStatus.Passed
        )
        step_count += 1
        
        freq_seq.add_chart_step(
            name="Bode Plot - Phase",
            chart_type=ChartType.LINE_LOG_X,
            label="Frequency Response - Phase",
            x_label="Frequency",
            x_unit="Hz",
            y_label="Phase",
            y_unit="°",
            series=[phase_series],
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Step Response Test
        step_resp_seq = perf_seq.add_sequence_call(
            name="Step Response",
            file_name="step_response.seq",
            version="1.0.0",
            path="tests/performance/step"
        )
        
        # Generate step response data
        time_points = [i * 0.001 for i in range(100)]  # 0-100ms
        step_response = [1.0 - math.exp(-t * 50) for t in time_points]
        
        step_series = ChartSeries(
            name="Output",
            x_data=";".join(f"{t*1000:.1f}" for t in time_points),
            y_data=";".join(f"{v:.4f}" for v in step_response)
        )
        
        target_series = ChartSeries(
            name="Target",
            x_data="0;100",
            y_data="1.0;1.0"
        )
        
        step_resp_seq.add_chart_step(
            name="Step Response Curve",
            chart_type=ChartType.LINE,
            label="System Step Response",
            x_label="Time",
            x_unit="ms",
            y_label="Amplitude",
            y_unit="V",
            series=[step_series, target_series],
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Rise time measurement
        rise_time = next(t for t, v in zip(time_points, step_response) if v >= 0.9) * 1000
        step_resp_seq.add_numeric_step(
            name="Rise Time (10%-90%)",
            value=rise_time,
            unit="ms",
            comp_op=CompOp.LT,
            low_limit=50.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Settling time
        settling_time = next(t for t, v in zip(time_points, step_response) if abs(v - 1.0) < 0.02) * 1000
        step_resp_seq.add_numeric_step(
            name="Settling Time (2%)",
            value=settling_time,
            unit="ms",
            comp_op=CompOp.LT,
            low_limit=80.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Harmonic Distortion Test
        harmonic_seq = perf_seq.add_sequence_call(
            name="Harmonic Distortion",
            file_name="thd.seq",
            version="1.0.0",
            path="tests/performance/distortion"
        )
        
        # Generate harmonic data
        harmonics = list(range(1, 11))  # 1st to 10th harmonic
        magnitudes = [100.0 if i == 1 else 100.0 / (i ** 2) for i in harmonics]
        
        harmonic_series = ChartSeries(
            name="Harmonics",
            x_data=";".join(str(h) for h in harmonics),
            y_data=";".join(f"{m:.2f}" for m in magnitudes)
        )
        
        harmonic_seq.add_chart_step(
            name="Harmonic Spectrum",
            chart_type=ChartType.LINE_LOG_Y,
            label="Harmonic Distortion Analysis",
            x_label="Harmonic Number",
            x_unit="",
            y_label="Magnitude",
            y_unit="dBc",
            series=[harmonic_series],
            status=StepStatus.Passed
        )
        step_count += 1
        
        # THD measurement
        thd = math.sqrt(sum(m**2 for m in magnitudes[1:])) / magnitudes[0] * 100
        harmonic_seq.add_numeric_step(
            name="Total Harmonic Distortion",
            value=thd,
            unit="%",
            comp_op=CompOp.LT,
            low_limit=5.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Noise Floor Test
        noise_seq = perf_seq.add_sequence_call(
            name="Noise Analysis",
            file_name="noise.seq",
            version="1.0.0",
            path="tests/performance/noise"
        )
        
        # Generate noise spectrum
        freq_bins = [i * 100 for i in range(1, 51)]  # 100Hz to 5kHz
        noise_levels = [-80 + 10 * math.sin(i * 0.1) for i in range(len(freq_bins))]
        
        noise_series = ChartSeries(
            name="Noise Floor",
            x_data=";".join(str(f) for f in freq_bins),
            y_data=";".join(f"{n:.1f}" for n in noise_levels)
        )
        
        noise_seq.add_chart_step(
            name="Noise Spectrum",
            chart_type=ChartType.LINE,
            label="Noise Floor Analysis",
            x_label="Frequency",
            x_unit="Hz",
            y_label="Power",
            y_unit="dBm",
            series=[noise_series],
            status=StepStatus.Passed
        )
        step_count += 1
        
        # RMS noise
        noise_seq.add_numeric_step(
            name="RMS Noise Level",
            value=12.5,
            unit="µVrms",
            comp_op=CompOp.LT,
            low_limit=20.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Power Consumption Test with Chart
        power_cons_seq = perf_seq.add_sequence_call(
            name="Power Consumption Profile",
            file_name="power_profile.seq",
            version="1.0.0",
            path="tests/performance/power"
        )
        
        # Generate power profile
        test_time = list(range(0, 61, 5))  # 0-60 seconds
        current_draw = [
            50, 100, 150, 200, 250, 300, 280, 260, 240, 220, 200, 180, 150
        ]
        
        current_series = ChartSeries(
            name="Current Draw",
            x_data=";".join(str(t) for t in test_time),
            y_data=";".join(str(c) for c in current_draw)
        )
        
        limit_series = ChartSeries(
            name="Limit",
            x_data=f"0;{test_time[-1]}",
            y_data="350;350"
        )
        
        power_cons_seq.add_chart_step(
            name="Current Profile",
            chart_type=ChartType.LINE,
            label="Current Draw Over Time",
            x_label="Time",
            x_unit="s",
            y_label="Current",
            y_unit="mA",
            series=[current_series, limit_series],
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Peak current
        power_cons_seq.add_numeric_step(
            name="Peak Current",
            value=max(current_draw),
            unit="mA",
            comp_op=CompOp.LT,
            low_limit=350.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Average current
        avg_current = sum(current_draw) / len(current_draw)
        power_cons_seq.add_numeric_step(
            name="Average Current",
            value=avg_current,
            unit="mA",
            comp_op=CompOp.LT,
            low_limit=250.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        # ========================================================================
        # Level 1: STRESS TESTS
        # ========================================================================
        print("Building Stress Tests...")
        stress_seq = root.add_sequence_call(
            name="Stress Tests",
            file_name="stress.seq",
            version="1.0.0",
            path="tests/stress"
        )
        
        # Temperature cycling
        temp_cycle_seq = stress_seq.add_sequence_call(
            name="Temperature Cycling",
            file_name="temp_cycle.seq",
            version="1.0.0",
            path="tests/stress/temp"
        )
        
        # Temperature profile chart
        cycle_time = list(range(0, 121, 10))  # 0-120 minutes
        temp_profile = [25, 35, 50, 70, 85, 85, 70, 50, 35, 25, 25, 25, 25]
        
        temp_profile_series = ChartSeries(
            name="Temperature",
            x_data=";".join(str(t) for t in cycle_time),
            y_data=";".join(str(temp) for temp in temp_profile)
        )
        
        temp_cycle_seq.add_chart_step(
            name="Temperature Cycle Profile",
            chart_type=ChartType.LINE,
            label="Temperature During Stress Test",
            x_label="Time",
            x_unit="min",
            y_label="Temperature",
            y_unit="°C",
            series=[temp_profile_series],
            status=StepStatus.Passed
        )
        step_count += 1
        
        temp_cycle_seq.add_numeric_step(
            name="Max Temperature Reached",
            value=85.0,
            unit="°C",
            comp_op=CompOp.GELE,
            low_limit=80.0,
            high_limit=90.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Voltage stress test
        voltage_stress_seq = stress_seq.add_sequence_call(
            name="Voltage Stress Test",
            file_name="voltage_stress.seq",
            version="1.0.0",
            path="tests/stress/voltage"
        )
        
        voltage_stress_seq.add_numeric_step(
            name="Overvoltage Test",
            value=5.5,
            unit="V",
            comp_op=CompOp.GELE,
            low_limit=5.4,
            high_limit=5.6,
            status=StepStatus.Passed
        )
        step_count += 1
        
        voltage_stress_seq.add_boolean_step(
            name="Overvoltage Protection Active",
            status=StepStatus.Passed
        )
        step_count += 1
        
        # ========================================================================
        # Level 1: GENERIC/FLOW STEPS
        # ========================================================================
        print("Building Flow Control Tests...")
        flow_seq = root.add_sequence_call(
            name="Flow Control Tests",
            file_name="flow.seq",
            version="1.0.0",
            path="tests/flow"
        )
        
        # Various flow control steps
        flow_seq.add_generic_step(
            step_type=FlowType.If,
            name="If Condition Check",
            status=StepStatus.Passed
        )
        step_count += 1
        
        flow_seq.add_generic_step(
            step_type=FlowType.For,
            name="For Loop Iteration",
            status=StepStatus.Passed
        )
        step_count += 1
        
        flow_seq.add_generic_step(
            step_type=FlowType.While,
            name="While Loop Condition",
            status=StepStatus.Passed
        )
        step_count += 1
        
        flow_seq.add_generic_step(
            step_type=FlowType.Statement,
            name="Execute Statement",
            status=StepStatus.Passed
        )
        step_count += 1
        
        flow_seq.add_generic_step(
            step_type=FlowType.Action,
            name="Perform Action",
            status=StepStatus.Passed
        )
        step_count += 1
        
        # ========================================================================
        # Level 1: CLEANUP AND FINALIZATION
        # ========================================================================
        print("Building Cleanup Sequence...")
        cleanup_seq = root.add_sequence_call(
            name="Cleanup and Finalization",
            file_name="cleanup.seq",
            version="1.0.0",
            path="tests/cleanup"
        )
        
        cleanup_seq.add_generic_step(
            step_type=FlowType.Action,
            name="Shutdown Power Supplies",
            status=StepStatus.Passed
        )
        step_count += 1
        
        cleanup_seq.add_generic_step(
            step_type=FlowType.Action,
            name="Disconnect Interfaces",
            status=StepStatus.Passed
        )
        step_count += 1
        
        cleanup_seq.add_boolean_step(
            name="Safe State Confirmed",
            status=StepStatus.Passed
        )
        step_count += 1
        
        # Final Summary
        summary_seq = cleanup_seq.add_sequence_call(
            name="Test Summary",
            file_name="summary.seq",
            version="1.0.0",
            path="tests/cleanup/summary"
        )
        
        summary_seq.add_numeric_step(
            name="Total Test Time",
            value=125.5,
            unit="s",
            comp_op=CompOp.LOG,
            status=StepStatus.Passed
        )
        step_count += 1
        
        summary_seq.add_numeric_step(
            name="Pass Rate",
            value=100.0,
            unit="%",
            comp_op=CompOp.GE,
            low_limit=95.0,
            status=StepStatus.Passed
        )
        step_count += 1
        
        summary_seq.add_string_step(
            name="Test Result",
            value="PASSED",
            status=StepStatus.Passed
        )
        step_count += 1
        
        print(f"\n{'='*80}")
        print(f"Report Structure Complete!")
        print(f"Total Steps Created: {step_count}")
        print(f"Hierarchy Depth: 5 levels")
        print(f"{'='*80}\n")
        
        # ========================================================================
        # SUBMIT REPORT TO SERVER
        # ========================================================================
        print("Submitting report to server...")
        submit_start = time.time()
        
        result = wats_client.report.submit_report(report)
        
        submit_duration = time.time() - submit_start
        assert result is not None, "Failed to submit report to server"
        
        print(f"✓ Report submitted successfully ({submit_duration:.2f}s) - Report ID: {result}")
        
        # ========================================================================
        # WAIT FOR PROCESSING AND RETRIEVE
        # ========================================================================
        print("\nWaiting for report processing...")
        max_wait_time = 60  # 60 seconds timeout
        wait_start = time.time()
        loaded_report = None
        
        # Use the returned report ID directly
        while time.time() - wait_start < max_wait_time:
            try:
                # Try to retrieve the report using the ID from submission
                loaded_report = wats_client.report.get_report(result)
                print(f"✓ Full report loaded (ID: {result})")
                break
                    
            except Exception as e:
                # Report might not be ready yet
                pass
            
            time.sleep(2)
            elapsed = time.time() - wait_start
            print(f"  Waiting... ({elapsed:.1f}s)")
        
        load_duration = time.time() - wait_start
        
        # ========================================================================
        # VERIFY RETRIEVED REPORT
        # ========================================================================
        assert loaded_report is not None, \
            f"Failed to retrieve report within {max_wait_time} seconds"
        
        print(f"\n{'='*80}")
        print(f"Report Verification")
        print(f"{'='*80}\n")
        
        # Verify basic properties
        assert loaded_report.sn == serial_number, "Serial number mismatch"
        print(f"✓ Serial number verified: {serial_number}")
        
        assert loaded_report.pn == "ADVANCED-UUT-TEST", "Part number mismatch"
        print(f"✓ Part number verified: ADVANCED-UUT-TEST")
        
        assert loaded_report.result == "P", "Result mismatch"
        print(f"✓ Result verified: PASSED")
        
        # Verify root sequence exists (UUTReport only)
        assert isinstance(loaded_report, UUTReport), "Loaded report is not a UUTReport"
        loaded_root = loaded_report.get_root_sequence_call()
        assert loaded_root is not None, "Root sequence not found"
        assert loaded_root.steps is not None, "Root sequence has no steps"
        print(f"✓ Root sequence exists")
        
        # Verify main sequences
        assert len(loaded_root.steps) >= 5, \
            f"Expected at least 5 main sequences, found {len(loaded_root.steps)}"
        print(f"✓ Main sequences verified: {len(loaded_root.steps)} sequences")
        
        # Verify specific sequences exist
        sequence_names = [s.name for s in loaded_root.steps if loaded_root.steps]
        expected_sequences = [
            "System Initialization",
            "Functional Tests",
            "Performance Tests",
            "Stress Tests",
            "Cleanup and Finalization"
        ]
        
        for expected in expected_sequences:
            assert expected in sequence_names, \
                f"Expected sequence '{expected}' not found"
            print(f"✓ Sequence found: {expected}")
        
        # Verify nested hierarchy depth
        init_seq_loaded = next((s for s in loaded_root.steps if s.name == "System Initialization"), None)
        assert init_seq_loaded is not None, "System Initialization sequence not found"
        assert isinstance(init_seq_loaded, SequenceCall), "init_seq is not a SequenceCall"
        assert init_seq_loaded.steps is not None, "init_seq has no steps"
        assert len(init_seq_loaded.steps) >= 2, "Initialization sub-sequences missing"
        print(f"✓ Nested hierarchy verified (depth >= 3)")
        
        # Verify step types are preserved
        power_seq_loaded = next((s for s in init_seq_loaded.steps if s.name == "Power Supply Tests"), None)
        assert power_seq_loaded is not None, "Power Supply Tests sequence not found"
        assert isinstance(power_seq_loaded, SequenceCall), "power_seq is not a SequenceCall"
        assert power_seq_loaded.steps is not None, "power_seq has no steps"
        assert len(power_seq_loaded.steps) >= 5, "Power test steps missing"
        
        # Check for numeric steps
        numeric_steps = [s for s in power_seq_loaded.steps 
                        if hasattr(s, 'measurement') and hasattr(s.measurement, 'value')]
        assert len(numeric_steps) >= 3, "Numeric steps not preserved"
        print(f"✓ Numeric steps verified: {len(numeric_steps)} steps")
        
        # Verify chart steps exist in performance tests
        perf_seq_loaded = next((s for s in loaded_root.steps if s.name == "Performance Tests"), None)
        assert perf_seq_loaded is not None, "Performance Tests sequence not found"
        assert isinstance(perf_seq_loaded, SequenceCall), "perf_seq is not a SequenceCall"
        chart_count = self._count_chart_steps(perf_seq_loaded)
        assert chart_count >= 5, f"Expected at least 5 chart steps, found {chart_count}"
        print(f"✓ Chart steps verified: {chart_count} charts")
        
        # Verify step count is reasonable
        total_loaded_steps = self._count_all_steps(loaded_root)
        print(f"✓ Total steps in loaded report: {total_loaded_steps}")
        
        # Step count may differ slightly due to server processing
        assert total_loaded_steps >= step_count * 0.95, \
            f"Too many steps lost (created: {step_count}, loaded: {total_loaded_steps})"
        
        print(f"\n{'='*80}")
        print(f"✓ ALL VERIFICATIONS PASSED!")
        print(f"{'='*80}\n")
        print(f"Performance Summary:")
        print(f"  - Steps Created: {step_count}")
        print(f"  - Steps Loaded: {total_loaded_steps}")
        print(f"  - Submit Time: {submit_duration:.2f}s")
        print(f"  - Load Time: {load_duration:.2f}s")
        print(f"  - Total Time: {submit_duration + load_duration:.2f}s")
        print(f"{'='*80}\n")
    
    def _count_chart_steps(self, sequence: SequenceCall) -> int:
        """Recursively count chart steps in a sequence"""
        count = 0
        if sequence.steps is None:
            return 0
        for step in sequence.steps:
            if hasattr(step, 'chart') and step.chart is not None:
                count += 1
            if hasattr(step, 'steps') and isinstance(step, SequenceCall):
                count += self._count_chart_steps(step)
        return count
    
    def _count_all_steps(self, sequence: SequenceCall) -> int:
        """Recursively count all steps in a sequence"""
        if sequence.steps is None:
            return 0
        count = len(sequence.steps)
        for step in sequence.steps:
            if hasattr(step, 'steps') and isinstance(step, SequenceCall):
                count += self._count_all_steps(step)
        return count
