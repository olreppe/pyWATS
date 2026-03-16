"""
Tests for WATS Standard JSON Format (WSJF) Converter

Tests cover:
1. Basic conversion of WSJF files to UUTReport models
2. Loop step preservation (loop field copied from WSJF steps)
3. Loop info deserialization with WSJF field names (idx/num)
4. Conversion of the sample WSJF export file
5. AsyncConverterPool._convert_unsandboxed with FileConverter API
"""

import asyncio
import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pywats_client.converters.models import (
    ConversionStatus,
    ConverterResult,
    ConverterSource,
    PostProcessAction,
)
from pywats_client.converters.context import ConverterContext
from pywats_client.converters.file_converter import FileConverter
from pywats_client.converters.standard.wats_standard_json_converter import WATSStandardJsonConverter
from pywats.domains.report.report_models import UUTReport
from pywats.domains.report.report_models.binary_data import LoopInfo


# =============================================================================
# Test Helpers
# =============================================================================

WSJF_EXPORT_FILE = (
    Path(__file__).parent.parent.parent
    / "report_model_testing"
    / "original reports"
    / "uut-wsjf-export.json"
)


def make_simple_wsjf(**overrides: Any) -> Dict[str, Any]:
    """Return a minimal valid WSJF dict."""
    data: Dict[str, Any] = {
        "type": "T",
        "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        "pn": "PART-001",
        "sn": "SN-001",
        "rev": "A",
        "processCode": 10,
        "processName": "FuncTest",
        "result": "P",
        "machineName": "Station1",
        "location": "TestLab",
        "purpose": "Production",
        "start": "2026-01-01T10:00:00+01:00",
        "root": {
            "id": 1,
            "group": "M",
            "stepType": "SequenceCall",
            "name": "MainSequence",
            "status": "P",
            "totTime": 5.0,
            "steps": [],
        },
    }
    data.update(overrides)
    return data


def make_wsjf_with_loops() -> Dict[str, Any]:
    """Return a WSJF dict containing loop steps."""
    data = make_simple_wsjf()
    data["root"]["steps"] = [
        {
            "id": 2,
            "group": "M",
            "stepType": "SequenceCall",
            "name": "LoopHeader",
            "status": "P",
            "totTime": 2.0,
            "loop": {
                "idx": None,
                "num": 2,
                "endingIndex": 2,
                "passed": 2,
                "failed": 0,
            },
            "steps": [
                {
                    "id": 3,
                    "group": "M",
                    "stepType": "ET_NLT",
                    "name": "VoltageTest",
                    "status": "P",
                    "totTime": 0.5,
                    "loop": {"idx": 0, "num": None},
                    "numericMeas": [
                        {
                            "compOp": "GELE",
                            "status": "P",
                            "unit": "V",
                            "value": 12.0,
                            "lowLimit": 11.0,
                            "highLimit": 13.0,
                        }
                    ],
                },
                {
                    "id": 4,
                    "group": "M",
                    "stepType": "ET_NLT",
                    "name": "VoltageTest",
                    "status": "P",
                    "totTime": 0.5,
                    "loop": {"idx": 1, "num": None},
                    "numericMeas": [
                        {
                            "compOp": "GELE",
                            "status": "P",
                            "unit": "V",
                            "value": 12.1,
                            "lowLimit": 11.0,
                            "highLimit": 13.0,
                        }
                    ],
                },
            ],
        }
    ]
    return data


# =============================================================================
# LoopInfo model tests
# =============================================================================

class TestLoopInfoWSJFFormat:
    """Test LoopInfo deserialization with WSJF field names."""

    def test_internal_format_i_n(self) -> None:
        """LoopInfo accepts internal WATS format (i/n)."""
        loop = LoopInfo.model_validate({"i": 2, "n": 5})
        assert loop.index == 2
        assert loop.count == 5

    def test_wsjf_iteration_format(self) -> None:
        """LoopInfo accepts WSJF iteration format (idx/num)."""
        loop = LoopInfo.model_validate({"idx": 0, "num": None})
        assert loop.index == 0
        assert loop.count is None

    def test_wsjf_header_format(self) -> None:
        """LoopInfo accepts WSJF loop-header format (idx=null, num=N)."""
        loop = LoopInfo.model_validate(
            {"idx": None, "num": 3, "endingIndex": 3, "passed": 1, "failed": 2}
        )
        assert loop.index is None
        assert loop.count == 3
        assert loop.ending_index == 3
        assert loop.passed == 1
        assert loop.failed == 2

    def test_wsjf_header_index_none_allowed(self) -> None:
        """index may be None for loop header entries in WSJF."""
        loop = LoopInfo.model_validate({"idx": None, "num": 5})
        assert loop.index is None
        assert loop.count == 5

    def test_serialization_always_uses_i_n(self) -> None:
        """LoopInfo always serializes with i/n (WATS API format)."""
        loop = LoopInfo.model_validate({"idx": 1, "num": 3})
        dump = loop.model_dump(by_alias=True, exclude_none=True)
        # Must use 'i' and 'n', not 'idx' and 'num'
        assert "i" in dump
        assert "n" in dump
        assert "idx" not in dump
        assert "num" not in dump

    def test_wsjf_only_fields_excluded_from_serialization(self) -> None:
        """WSJF-specific fields (endingIndex, passed, failed) are not submitted."""
        loop = LoopInfo.model_validate(
            {"idx": None, "num": 2, "endingIndex": 2, "passed": 2, "failed": 0}
        )
        dump = loop.model_dump(by_alias=True)
        assert "endingIndex" not in dump
        assert "passed" not in dump
        assert "failed" not in dump

    def test_defaults_when_no_loop_data(self) -> None:
        """LoopInfo can be constructed with defaults."""
        loop = LoopInfo()
        assert loop.index is None
        assert loop.count is None


# =============================================================================
# WATSStandardJsonConverter tests
# =============================================================================

class TestWATSStandardJsonConverterBasic:
    """Basic conversion tests for WATSStandardJsonConverter."""

    def _convert_dict(self, data: Dict[str, Any]) -> ConverterResult:
        """Helper: write data to temp file and run converter."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            tmp = Path(f.name)
        try:
            c = WATSStandardJsonConverter()
            src = ConverterSource.from_file(tmp)
            ctx = ConverterContext()
            return c.convert(src, ctx)
        finally:
            tmp.unlink(missing_ok=True)

    def test_simple_conversion_succeeds(self) -> None:
        result = self._convert_dict(make_simple_wsjf())
        assert result.status == ConversionStatus.SUCCESS
        assert result.report is not None

    def test_returns_uutreport_model(self) -> None:
        result = self._convert_dict(make_simple_wsjf())
        assert isinstance(result.report, UUTReport)

    def test_report_has_correct_sn_pn(self) -> None:
        result = self._convert_dict(make_simple_wsjf())
        assert result.report.sn == "SN-001"
        assert result.report.pn == "PART-001"

    def test_failed_result_on_bad_json(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("{bad json}")
            tmp = Path(f.name)
        try:
            c = WATSStandardJsonConverter()
            src = ConverterSource.from_file(tmp)
            ctx = ConverterContext()
            result = c.convert(src, ctx)
            assert result.status == ConversionStatus.FAILED
        finally:
            tmp.unlink(missing_ok=True)


class TestWATSStandardJsonConverterLoopPreservation:
    """Test that loop data is preserved during conversion."""

    def _convert_dict(self, data: Dict[str, Any]) -> ConverterResult:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            tmp = Path(f.name)
        try:
            c = WATSStandardJsonConverter()
            src = ConverterSource.from_file(tmp)
            ctx = ConverterContext()
            return c.convert(src, ctx)
        finally:
            tmp.unlink(missing_ok=True)

    def _collect_loop_steps(
        self, seq: Any, results: Optional[List] = None
    ) -> List:
        if results is None:
            results = []
        for step in seq.steps:
            if hasattr(step, "loop") and step.loop is not None:
                results.append(step)
            if hasattr(step, "steps") and step.steps:
                self._collect_loop_steps(step, results)
        return results

    def test_loop_field_preserved_after_conversion(self) -> None:
        """loop field must survive the _convert_step transformation."""
        data = make_wsjf_with_loops()
        result = self._convert_dict(data)
        assert result.status == ConversionStatus.SUCCESS

        loop_steps = self._collect_loop_steps(result.report.root)
        # Expect: 1 header + 2 iterations = 3 loop-annotated steps
        assert len(loop_steps) == 3

    def test_loop_header_count_preserved(self) -> None:
        """Loop header count (num) is correctly deserialized."""
        data = make_wsjf_with_loops()
        result = self._convert_dict(data)
        loop_steps = self._collect_loop_steps(result.report.root)

        # Find the header (idx=None, num=2)
        headers = [s for s in loop_steps if s.loop.count == 2]
        assert len(headers) == 1
        assert headers[0].loop.count == 2
        assert headers[0].loop.index is None

    def test_loop_iteration_index_preserved(self) -> None:
        """Loop iteration indices are correctly deserialized."""
        data = make_wsjf_with_loops()
        result = self._convert_dict(data)
        loop_steps = self._collect_loop_steps(result.report.root)

        indices = sorted(
            s.loop.index
            for s in loop_steps
            if s.loop.index is not None
        )
        assert indices == [0, 1]

    def test_loop_wsjf_only_fields_available(self) -> None:
        """WSJF-specific loop fields (passed/failed) are accessible on model."""
        data = make_wsjf_with_loops()
        result = self._convert_dict(data)
        loop_steps = self._collect_loop_steps(result.report.root)

        headers = [s for s in loop_steps if s.loop.index is None]
        assert len(headers) == 1
        assert headers[0].loop.passed == 2
        assert headers[0].loop.failed == 0
        assert headers[0].loop.ending_index == 2


class TestWATSStandardJsonConverterWithExportFile:
    """Test against the actual uut-wsjf-export.json sample file."""

    @pytest.fixture(autouse=True)
    def skip_if_no_file(self) -> None:
        if not WSJF_EXPORT_FILE.exists():
            pytest.skip(f"Sample WSJF file not found: {WSJF_EXPORT_FILE}")

    def test_export_file_converts_successfully(self) -> None:
        c = WATSStandardJsonConverter()
        src = ConverterSource.from_file(WSJF_EXPORT_FILE)
        ctx = ConverterContext()
        result = c.convert(src, ctx)
        assert result.status == ConversionStatus.SUCCESS

    def test_export_file_returns_uutreport(self) -> None:
        c = WATSStandardJsonConverter()
        src = ConverterSource.from_file(WSJF_EXPORT_FILE)
        ctx = ConverterContext()
        result = c.convert(src, ctx)
        assert isinstance(result.report, UUTReport)

    def test_export_file_loop_steps_preserved(self) -> None:
        """All 46 loop-annotated steps in the export file must be preserved."""
        c = WATSStandardJsonConverter()
        src = ConverterSource.from_file(WSJF_EXPORT_FILE)
        ctx = ConverterContext()
        result = c.convert(src, ctx)
        assert result.status == ConversionStatus.SUCCESS

        def collect_loops(seq: Any, acc: Optional[List] = None) -> List:
            if acc is None:
                acc = []
            for step in seq.steps:
                if hasattr(step, "loop") and step.loop is not None:
                    acc.append(step)
                if hasattr(step, "steps") and step.steps:
                    collect_loops(step, acc)
            return acc

        loop_steps = collect_loops(result.report.root)
        assert len(loop_steps) == 46, (
            f"Expected 46 loop-annotated steps; got {len(loop_steps)}"
        )

    def test_export_file_loop_counts_correct(self) -> None:
        """Loop header entries must carry the correct iteration counts."""
        c = WATSStandardJsonConverter()
        src = ConverterSource.from_file(WSJF_EXPORT_FILE)
        ctx = ConverterContext()
        result = c.convert(src, ctx)

        def collect_loops(seq: Any, acc: Optional[List] = None) -> List:
            if acc is None:
                acc = []
            for step in seq.steps:
                if hasattr(step, "loop") and step.loop is not None:
                    acc.append(step)
                if hasattr(step, "steps") and step.steps:
                    collect_loops(step, acc)
            return acc

        loop_steps = collect_loops(result.report.root)
        header_counts = [
            s.loop.count for s in loop_steps if s.loop.count is not None
        ]
        # The export file contains headers with counts of 2 and 3
        assert 2 in header_counts
        assert 3 in header_counts


# =============================================================================
# AsyncConverterPool._convert_unsandboxed tests
# =============================================================================

class MockFileConverter(FileConverter):
    """Simple FileConverter that returns a fixed report."""

    def __init__(self, report: Optional[Dict[str, Any]] = None):
        super().__init__()
        self._report = report or {
            "type": "T",
            "pn": "PART-001",
            "sn": "SN-001",
        }

    @property
    def name(self) -> str:
        return "MockFileConverter"

    def convert(
        self, source: ConverterSource, context: ConverterContext
    ) -> ConverterResult:
        return ConverterResult.success_result(
            report=self._report,
            post_action=PostProcessAction.MOVE,
        )


class MockFailingFileConverter(FileConverter):
    """FileConverter that always returns a FAILED result."""

    @property
    def name(self) -> str:
        return "MockFailingConverter"

    def convert(
        self, source: ConverterSource, context: ConverterContext
    ) -> ConverterResult:
        return ConverterResult.failed_result(error="intentional failure")


class MockConversionItem:
    """Minimal mock of AsyncConversionItem for pool tests."""

    def __init__(self, file_path: Path, converter: Any) -> None:
        self.file_path = file_path
        self.converter = converter


class TestConvertUnsandboxedWithFileConverter:
    """Tests for AsyncConverterPool._convert_unsandboxed with FileConverter."""

    @pytest.fixture()
    def pool(self) -> Any:
        from pywats_client.service.async_converter_pool import AsyncConverterPool

        config = MagicMock()
        api = AsyncMock()
        return AsyncConverterPool(config=config, api=api, max_concurrent=2)

    @pytest.fixture()
    def tmp_json_file(self) -> Path:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump({"type": "T", "sn": "SN-001"}, f)
            return Path(f.name)

    def teardown_method(self) -> None:
        # Clean up temp files created by individual tests
        pass

    @pytest.mark.asyncio
    async def test_fileconverter_called_with_correct_api(
        self, pool: Any, tmp_json_file: Path
    ) -> None:
        """_convert_unsandboxed must call FileConverter.convert(source, context)."""
        converter = MockFileConverter()
        item = MockConversionItem(tmp_json_file, converter)
        result = await pool._convert_unsandboxed(item)  # type: ignore[arg-type]
        assert result is not None
        assert result.get("sn") == "SN-001" or result.get("pn") == "PART-001"
        tmp_json_file.unlink(missing_ok=True)

    @pytest.mark.asyncio
    async def test_failed_conversion_raises(
        self, pool: Any, tmp_json_file: Path
    ) -> None:
        """_convert_unsandboxed must raise RuntimeError on FAILED result."""
        converter = MockFailingFileConverter()
        item = MockConversionItem(tmp_json_file, converter)
        with pytest.raises(RuntimeError, match="intentional failure"):
            await pool._convert_unsandboxed(item)  # type: ignore[arg-type]
        tmp_json_file.unlink(missing_ok=True)

    @pytest.mark.asyncio
    async def test_unknown_converter_type_raises(
        self, pool: Any, tmp_json_file: Path
    ) -> None:
        """_convert_unsandboxed raises TypeError for unrecognised converter types."""

        class WeirdConverter:
            name = "WeirdConverter"

        item = MockConversionItem(tmp_json_file, WeirdConverter())
        with pytest.raises(TypeError, match="does not implement FileConverter or ConverterBase"):
            await pool._convert_unsandboxed(item)  # type: ignore[arg-type]
        tmp_json_file.unlink(missing_ok=True)


class TestShouldUseSandbox:
    """Tests for AsyncConverterPool._should_use_sandbox."""

    @pytest.fixture()
    def pool(self) -> Any:
        from pywats_client.service.async_converter_pool import AsyncConverterPool

        config = MagicMock()
        api = AsyncMock()
        return AsyncConverterPool(config=config, api=api)

    def test_fileconverter_without_source_path_no_sandbox(self, pool: Any) -> None:
        """Built-in FileConverter subclasses must NOT be sandboxed."""
        converter = MockFileConverter()
        assert converter.source_path is None
        assert not pool._should_use_sandbox(converter)

    def test_trusted_mode_converter_no_sandbox(self, pool: Any) -> None:
        """Converters with trusted_mode=True must NOT be sandboxed."""
        converter = MockFileConverter()
        converter.trusted_mode = True
        assert not pool._should_use_sandbox(converter)

    def test_converter_with_source_path_uses_sandbox(self, pool: Any) -> None:
        """Converters that have source_path set SHOULD use sandbox."""
        converter = MockFileConverter()
        converter.source_path = Path("/some/user/converter.py")
        assert pool._should_use_sandbox(converter)

    def test_wsjf_converter_no_sandbox(self, pool: Any) -> None:
        """The WATSStandardJsonConverter (a built-in FileConverter) must not sandbox."""
        converter = WATSStandardJsonConverter()
        assert not pool._should_use_sandbox(converter)
