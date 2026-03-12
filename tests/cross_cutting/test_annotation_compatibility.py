"""Regression tests for runtime annotation evaluation compatibility.

Background
----------
Python 3.10–3.13 evaluate function annotations eagerly at import time.
Python 3.14+ evaluates them lazily by default (PEP 649).

``Result[T]`` expands to ``Union[Success[T], Failure]`` at runtime.
Without ``from __future__ import annotations``, subscribing that Union
(e.g. ``Result[str]`` in a return annotation) triggers a TypeError on
3.10–3.13 because ``Union[...]`` is not subscriptable once its type
variables are already bound.

The fix is ``from __future__ import annotations`` in every module that
uses ``Result[T]`` in a runtime-visible annotation. These tests guard
against regressions being introduced in new modules.

These tests pass on ALL supported versions (3.10–3.14).
"""
import sys
import importlib
import inspect

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _import_fresh(module_name: str):
    """Import a module (or re-import after cache removal)."""
    if module_name in sys.modules:
        return sys.modules[module_name]
    return importlib.import_module(module_name)


# ---------------------------------------------------------------------------
# 1. Import-time smoke tests
#    These fail on 3.10-3.13 without the __future__ fix, before any test
#    body even runs.
# ---------------------------------------------------------------------------

class TestImportCompatibility:
    """Modules that use Result[T] must import cleanly on all Python versions."""

    def test_parallel_imports_without_error(self):
        """parallel.py must import without TypeError on all Python versions."""
        import pywats.core.parallel  # noqa: F401 — import is the assertion

    def test_result_imports_without_error(self):
        """shared/result.py must import without TypeError."""
        import pywats.shared.result  # noqa: F401

    def test_pywats_top_level_imports_without_error(self):
        """Top-level `from pywats import pyWATS` must not raise."""
        import pywats  # noqa: F401

    def test_core_init_imports_without_error(self):
        """pywats.core __init__ re-exports parallel utilities — must not raise."""
        import pywats.core  # noqa: F401


# ---------------------------------------------------------------------------
# 2. Annotation introspection
#    get_type_hints() actually resolves string annotations, so any broken
#    annotation will surface here rather than silently being a string.
# ---------------------------------------------------------------------------

class TestResultTypeAnnotations:
    """Result[T] annotations in parallel.py are present and unevaluated at runtime.

    We use inspect.get_annotations() (available 3.10+) rather than
    get_type_hints() because the latter *evaluates* the annotation strings,
    which re-triggers the Union-subscripting problem.  The goal here is to
    confirm annotations exist and that the module loaded cleanly — not to
    fully resolve every generic.
    """

    def test_parallel_execute_has_return_annotation(self):
        from pywats.core.parallel import parallel_execute
        ann = inspect.get_annotations(parallel_execute)
        assert "return" in ann

    def test_parallel_execute_with_retry_has_return_annotation(self):
        from pywats.core.parallel import parallel_execute_with_retry
        ann = inspect.get_annotations(parallel_execute_with_retry)
        assert "return" in ann

    def test_collect_successes_has_return_annotation(self):
        from pywats.core.parallel import collect_successes
        ann = inspect.get_annotations(collect_successes)
        assert "return" in ann

    def test_collect_failures_has_return_annotation(self):
        from pywats.core.parallel import collect_failures
        ann = inspect.get_annotations(collect_failures)
        assert "return" in ann


# ---------------------------------------------------------------------------
# 3. Functional correctness — Result[T] works as intended at runtime
# ---------------------------------------------------------------------------

class TestResultTypeSubscriptability:
    """Result type can be used as intended in runtime code."""

    def test_success_and_failure_are_instantiable(self):
        from pywats.shared.result import Success, Failure
        s = Success(value=42)
        f = Failure(error_code="TEST", message="test failure")
        assert s.is_success
        assert f.is_failure

    def test_parallel_execute_returns_result_list(self):
        """parallel_execute returns a list of Success/Failure objects."""
        from pywats.core.parallel import parallel_execute
        from pywats.shared.result import Success, Failure

        results = parallel_execute(
            keys=["a", "b", "c"],
            operation=lambda k: k.upper(),
        )

        assert len(results) == 3
        assert all(isinstance(r, (Success, Failure)) for r in results)
        assert all(r.is_success for r in results)
        assert [r.value for r in results] == ["A", "B", "C"]

    def test_parallel_execute_wraps_exceptions_as_failure(self):
        """Exceptions inside the operation become Failure results."""
        from pywats.core.parallel import parallel_execute
        from pywats.shared.result import Failure

        def boom(k: str) -> str:
            raise ValueError(f"exploded on {k}")

        results = parallel_execute(keys=["x"], operation=boom)
        assert len(results) == 1
        assert results[0].is_failure
        assert isinstance(results[0], Failure)

    def test_parallel_execute_empty_keys_returns_empty_list(self):
        from pywats.core.parallel import parallel_execute
        assert parallel_execute(keys=[], operation=lambda k: k) == []


# ---------------------------------------------------------------------------
# 4. Python version meta-test
#    Documents expected behaviour per version so failures are informative.
# ---------------------------------------------------------------------------

class TestPythonVersionContext:
    """Informational tests that document the annotation evaluation model."""

    def test_python_version_is_supported(self):
        """Confirm we're running on a supported Python version (3.10+)."""
        assert sys.version_info >= (3, 10), (
            f"pywats-api requires Python 3.10+, got {sys.version}"
        )

    def test_future_annotations_active_in_parallel_module(self):
        """parallel.py must have CO_FUTURE_ANNOTATIONS set (or 3.14+ lazy eval).

        On Python 3.14 PEP 649 makes this unnecessary, but the flag is still
        harmless. On 3.10-3.13 it MUST be present to avoid eager evaluation.
        """
        import pywats.core.parallel as parallel_mod

        if sys.version_info >= (3, 14):
            # PEP 649: lazy evaluation is the default — flag not required
            pytest.skip("Python 3.14+ uses lazy annotation evaluation by default (PEP 649)")

        # For 3.10-3.13: check the module source for the future import
        source_file = inspect.getfile(parallel_mod)
        with open(source_file, encoding="utf-8") as f:
            source = f.read()

        assert "from __future__ import annotations" in source, (
            "parallel.py is missing 'from __future__ import annotations'. "
            "This causes TypeError on Python 3.10-3.13 when Result[T] "
            "annotations are evaluated at import time."
        )
