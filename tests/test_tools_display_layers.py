"""Tests for display layer tools."""

import unittest
from unittest.mock import patch, MagicMock

from maya_mcp.tools import display_layers


class TestDisplayLayerTools(unittest.TestCase):
    """Test cases for display layer tools."""

    def test_create_display_layer_no_maya(self):
        """Test create_display_layer when Maya is not available."""
        with patch('maya_mcp.tools.display_layers.maya', side_effect=ImportError('No module named maya')):
            result = display_layers.create_display_layer('testLayer')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    @patch('maya_mcp.tools.display_layers.maya')
    def test_create_display_layer_success(self, mock_maya):
        """Test create_display_layer successfully creates layer."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = False
        mock_cmds.createDisplayLayer.return_value = 'testLayer'
        mock_maya.cmds = mock_cmds
        
        result = display_layers.create_display_layer('testLayer')
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['layer'], 'testLayer')

    @patch('maya_mcp.tools.display_layers.maya')
    def test_list_display_layers_success(self, mock_maya):
        """Test list_display_layers returns layers."""
        mock_cmds = MagicMock()
        mock_cmds.ls.return_value = ['layer1', 'layer2', 'defaultLayer']
        mock_maya.cmds = mock_cmds
        
        result = display_layers.list_display_layers()
        
        self.assertEqual(result['status'], 'success')
        # Should filter out defaultLayer
        self.assertEqual(len(result['layers']), 2)


if __name__ == '__main__':
    unittest.main()
