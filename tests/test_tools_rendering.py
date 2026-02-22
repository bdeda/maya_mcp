"""Tests for rendering tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import rendering


class TestRenderingTools(unittest.TestCase):
    """Test cases for rendering tools."""

    def test_create_playblast_no_maya(self):
        """Test create_playblast when Maya is not available."""
        with mock_maya_unavailable():
            result = rendering.create_playblast('test.mov')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_set_render_resolution_success(self):
        """Test set_render_resolution successfully sets resolution."""
        with mock_maya_available() as mock_cmds:
            result = rendering.set_render_resolution(1920, 1080)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.setAttr.assert_called()


if __name__ == '__main__':
    unittest.main()
