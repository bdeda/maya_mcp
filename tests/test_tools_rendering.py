"""Tests for rendering tools."""

import unittest
from unittest.mock import patch, MagicMock

from maya_mcp.tools import rendering


class TestRenderingTools(unittest.TestCase):
    """Test cases for rendering tools."""

    def test_create_playblast_no_maya(self):
        """Test create_playblast when Maya is not available."""
        with patch('maya_mcp.tools.rendering.maya', side_effect=ImportError('No module named maya')):
            result = rendering.create_playblast('test.mov')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    @patch('maya_mcp.tools.rendering.maya')
    def test_set_render_resolution_success(self, mock_maya):
        """Test set_render_resolution successfully sets resolution."""
        mock_cmds = MagicMock()
        mock_maya.cmds = mock_cmds
        
        result = rendering.set_render_resolution(1920, 1080)
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.setAttr.assert_called()


if __name__ == '__main__':
    unittest.main()
