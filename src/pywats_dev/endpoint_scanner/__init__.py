"""Endpoint scanner - automated endpoint risk assessment.

Scans routes.py and codebase to generate endpoint usage reports and risk assessments.
"""

from .scanner import EndpointScanner
from .classifier import EndpointClassifier, Priority
from .analyzer import UsageAnalyzer
from .report_generator import ReportGenerator

__all__ = [
    "EndpointScanner",
    "EndpointClassifier",
    "Priority",
    "UsageAnalyzer",
    "ReportGenerator",
]
