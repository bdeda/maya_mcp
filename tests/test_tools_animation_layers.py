"""Tests for animation layer tools."""

import unittest
from unittest.mock import patch, MagicMock

from maya_mcp.tools import animation_layers


class TestAnimationLayerTools(unittest.TestCase):
    """Test cases for animation layer tools."""

    def test_create_animation_layer_no_maya(self):
        """Test create_animation_layer when Maya is not available."""
        with patch('maya_mcp.tools.animation_layers.maya', side_effect=ImportError('No module named maya')):
            result = animation_layers.create_animation_layer('testLayer')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    @patch('maya_mcp.tools.animation_layers.maya')
    def test_create_animation_layer_success(self, mock_maya):
        """Test create_animation_layer successfully creates layer."""
        mock_cmds = MagicMock()
        mock_cmds.ls.return_value = []
        mock_cmds.animLayer.return_value = 'testLayer'
        mock_maya.cmds = mock_cmds
        
        result = animation_layers.create_animation_layer('testLayer', weight=0.5)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['layer'], 'testLayer')

    @patch('maya_mcp.tools.animation_layers.maya')
    def test_list_animation_layers_success(self, mock_maya):
        """Test list_animation_layers returns layers."""
        mock_cmds = MagicMock()
        mock_cmds.ls.return_value = ['layer1', 'layer2']
        mock_maya.cmds = mock_cmds
        
        result = animation_layers.list_animation_layers()
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['layers']), 2)


if __name__ == '__main__':
    unittest.main()
