"""Tests for animation layer tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import animation_layers


class TestAnimationLayerTools(unittest.TestCase):
    """Test cases for animation layer tools."""

    def test_create_animation_layer_no_maya(self):
        """Test create_animation_layer when Maya is not available."""
        with mock_maya_unavailable():
            result = animation_layers.create_animation_layer('testLayer')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_animation_layer_success(self):
        """Test create_animation_layer successfully creates layer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.ls.return_value = []
            mock_cmds.animLayer.return_value = 'testLayer'
            
            result = animation_layers.create_animation_layer('testLayer', weight=0.5)
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['layer'], 'testLayer')

    def test_list_animation_layers_success(self):
        """Test list_animation_layers returns layers."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.ls.return_value = ['layer1', 'layer2']
            
            result = animation_layers.list_animation_layers()
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(len(result['layers']), 2)


if __name__ == '__main__':
    unittest.main()
