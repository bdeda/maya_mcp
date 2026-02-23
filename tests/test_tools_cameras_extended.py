"""Tests for extended camera tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import cameras


class TestExtendedCameraTools(unittest.TestCase):
    """Test cases for extended camera tools."""

    def test_view_fit_no_maya(self):
        """Test view_fit when Maya is not available."""
        with mock_maya_unavailable():
            result = cameras.view_fit(['pCube1'])
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_view_fit_success(self):
        """Test view_fit successfully fits view."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = cameras.view_fit(['pCube1'])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.viewFit.assert_called()

    def test_view_selected_success(self):
        """Test view_selected successfully fits view to selection."""
        with mock_maya_available() as mock_cmds:
            result = cameras.view_selected()
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.viewFit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
