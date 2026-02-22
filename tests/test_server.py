"""Tests for server module."""

import unittest
from unittest.mock import patch, MagicMock

from maya_mcp.server import check_maya_available, get_maya_version


class TestServer(unittest.TestCase):
    """Test cases for server module."""

    def test_check_maya_available_false(self):
        """Test check_maya_available when Maya is not available."""
        with patch('maya_mcp.server.maya', side_effect=ImportError('No module named maya')):
            result = check_maya_available()
            self.assertFalse(result)

    @patch('maya_mcp.server.maya')
    def test_check_maya_available_true(self, mock_maya):
        """Test check_maya_available when Maya is available."""
        mock_maya.cmds = MagicMock()
        result = check_maya_available()
        self.assertTrue(result)

    def test_get_maya_version_none(self):
        """Test get_maya_version when Maya is not available."""
        with patch('maya_mcp.server.maya', side_effect=ImportError('No module named maya')):
            result = get_maya_version()
            self.assertIsNone(result)

    @patch('maya_mcp.server.maya')
    def test_get_maya_version_success(self, mock_maya):
        """Test get_maya_version when Maya is available."""
        mock_cmds = MagicMock()
        mock_cmds.about.return_value = '2024.0'
        mock_maya.cmds = mock_cmds
        
        result = get_maya_version()
        self.assertEqual(result, '2024.0')

    @patch('maya_mcp.server.maya')
    def test_get_maya_version_runtime_error(self, mock_maya):
        """Test get_maya_version handles RuntimeError."""
        mock_cmds = MagicMock()
        mock_cmds.about.side_effect = RuntimeError('Maya error')
        mock_maya.cmds = mock_cmds
        
        result = get_maya_version()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
