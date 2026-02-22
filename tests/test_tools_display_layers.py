"""Tests for display layer tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import display_layers


class TestDisplayLayerTools(unittest.TestCase):
    """Test cases for display layer tools."""

    def test_create_display_layer_no_maya(self):
        """Test create_display_layer when Maya is not available."""
        with mock_maya_unavailable():
            result = display_layers.create_display_layer('testLayer')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_display_layer_success(self):
        """Test create_display_layer successfully creates layer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = False
            mock_cmds.createDisplayLayer.return_value = 'testLayer'
            
            result = display_layers.create_display_layer('testLayer')
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['layer'], 'testLayer')

    def test_list_display_layers_success(self):
        """Test list_display_layers returns layers."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.ls.return_value = ['layer1', 'layer2', 'defaultLayer']
            
            result = display_layers.list_display_layers()
            
            self.assertEqual(result['status'], 'success')
            # Should filter out defaultLayer
            self.assertEqual(len(result['layers']), 2)


if __name__ == '__main__':
    unittest.main()
