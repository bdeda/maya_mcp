"""Pytest configuration and fixtures."""

import sys
from unittest.mock import MagicMock


def pytest_configure(config):
    """Configure pytest to mock maya module."""
    # Create a mock maya module
    mock_maya = MagicMock()
    mock_maya.cmds = MagicMock()
    sys.modules['maya'] = mock_maya
    sys.modules['maya.cmds'] = mock_maya.cmds
