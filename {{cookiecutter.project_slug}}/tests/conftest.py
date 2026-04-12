"""Pytest configuration and fixtures.

Markers are defined in pytest.ini.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_fixture() -> dict[str, str]:
    """Example fixture for demonstration.

    Returns:
        Sample data dictionary
    """
    return {"key": "value"}


# Add more shared fixtures here as needed
# Examples: database session, mock clients, test data generators

