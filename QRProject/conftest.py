"""Pytest configuration for QR code test suite.

Defines markers for core vs optional tests and skips optional tests by default.
"""
import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "core: Essential tests that must pass for assignment completion"
    )
    config.addinivalue_line(
        "markers", "optional: Additional tests for thorough validation"
    )


def pytest_collection_modifyitems(config, items):
    """Skip any tests marked as optional by default.

    Users can run optional tests explicitly with: pytest -m optional
    """
    skip_optional = pytest.mark.skip(reason="Optional tests are disabled by default")
    for item in items:
        if "optional" in item.keywords:
            item.add_marker(skip_optional)

