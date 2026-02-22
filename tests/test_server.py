"""Tests for server module."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.server import check_maya_available, get_maya_version


class TestServer(unittest.TestCase):
    """Test cases for server module."""

    def test_check_maya_available_false(self):
        """Test check_maya_available when Maya is not available."""
        with mock_maya_unavailable():
            result = check_maya_available()
            self.assertFalse(result)

    def test_check_maya_available_true(self):
        """Test check_maya_available when Maya is available."""
        with mock_maya_available():
            result = check_maya_available()
            self.assertTrue(result)

    def test_get_maya_version_none(self):
        """Test get_maya_version when Maya is not available."""
        with mock_maya_unavailable():
            result = get_maya_version()
            self.assertIsNone(result)

    def test_get_maya_version_success(self):
        """Test get_maya_version when Maya is available."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.about.return_value = '2024.0'
            
            result = get_maya_version()
            self.assertEqual(result, '2024.0')

    def test_get_maya_version_runtime_error(self):
        """Test get_maya_version handles RuntimeError."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.about.side_effect = RuntimeError('Maya error')
            
            result = get_maya_version()
            self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
