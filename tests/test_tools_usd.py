"""Tests for USD and UFE tools."""

import sys
import unittest
from unittest.mock import MagicMock, patch

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import usd


class TestUSDTools(unittest.TestCase):
    """Test cases for USD and UFE tools."""

    def test_create_usd_proxy_shape_no_maya(self):
        """Test create_usd_proxy_shape when Maya is not available."""
        with mock_maya_unavailable():
            result = usd.create_usd_proxy_shape('/path/to/file.usd')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_usd_proxy_shape_plugin_not_loaded(self):
        """Test create_usd_proxy_shape when plugin is not loaded."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.pluginInfo.return_value = False
            mock_cmds.loadPlugin.side_effect = RuntimeError('Plugin not found')
            
            result = usd.create_usd_proxy_shape('/path/to/file.usd')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('mayaUsdPlugin is not available', result['message'])

    def test_create_usd_proxy_shape_success(self):
        """Test create_usd_proxy_shape successfully creates proxy shape."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.pluginInfo.return_value = True
            mock_cmds.createNode.return_value = 'transform1'
            mock_cmds.createNode.side_effect = ['transform1', 'mayaUsdProxyShape1']
            mock_cmds.setAttr.return_value = None
            
            result = usd.create_usd_proxy_shape('/path/to/file.usd', name='myProxy')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.setAttr.assert_called_once()

    def test_get_usd_proxy_shape_info_no_maya(self):
        """Test get_usd_proxy_shape_info when Maya is not available."""
        with mock_maya_unavailable():
            result = usd.get_usd_proxy_shape_info('proxyShape1')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_get_usd_proxy_shape_info_nonexistent(self):
        """Test get_usd_proxy_shape_info with nonexistent proxy shape."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = False
            
            result = usd.get_usd_proxy_shape_info('nonexistent')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('does not exist', result['message'])

    def test_get_usd_proxy_shape_info_success(self):
        """Test get_usd_proxy_shape_info successfully gets info."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.nodeType.return_value = 'mayaUsdProxyShape'
            mock_cmds.getAttr.return_value = '/path/to/file.usd'
            mock_cmds.attributeQuery.return_value = False
            
            result = usd.get_usd_proxy_shape_info('proxyShape1')
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['usd_file_path'], '/path/to/file.usd')

    def test_list_usd_proxy_shapes_no_maya(self):
        """Test list_usd_proxy_shapes when Maya is not available."""
        with mock_maya_unavailable():
            result = usd.list_usd_proxy_shapes()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_list_usd_proxy_shapes_plugin_not_loaded(self):
        """Test list_usd_proxy_shapes when plugin is not loaded."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.pluginInfo.return_value = False
            
            result = usd.list_usd_proxy_shapes()
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['count'], 0)

    def test_list_usd_proxy_shapes_success(self):
        """Test list_usd_proxy_shapes successfully lists shapes."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.pluginInfo.return_value = True
            mock_cmds.ls.return_value = ['proxyShape1', 'proxyShape2']
            
            result = usd.list_usd_proxy_shapes()
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['count'], 2)

    def test_edit_usd_as_maya_no_maya(self):
        """Test edit_usd_as_maya when Maya is not available."""
        with mock_maya_unavailable():
            result = usd.edit_usd_as_maya('proxyShape1', '/')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_edit_usd_as_maya_plugin_not_loaded(self):
        """Test edit_usd_as_maya when plugin is not loaded."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.pluginInfo.return_value = False
            
            result = usd.edit_usd_as_maya('proxyShape1', '/')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('mayaUsdPlugin is not available', result['message'])

    def test_edit_usd_as_maya_nonexistent(self):
        """Test edit_usd_as_maya with nonexistent proxy shape."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.pluginInfo.return_value = True
            mock_cmds.objExists.return_value = False
            
            result = usd.edit_usd_as_maya('nonexistent', '/')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('does not exist', result['message'])

    def test_push_maya_edits_to_usd_no_maya(self):
        """Test push_maya_edits_to_usd when Maya is not available."""
        with mock_maya_unavailable():
            result = usd.push_maya_edits_to_usd('proxyShape1')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_get_usd_prim_info_no_maya(self):
        """Test get_usd_prim_info when Maya is not available."""
        with mock_maya_unavailable():
            result = usd.get_usd_prim_info('proxyShape1', '/')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_get_usd_prim_info_plugin_not_loaded(self):
        """Test get_usd_prim_info when plugin is not loaded."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.pluginInfo.return_value = False
            
            result = usd.get_usd_prim_info('proxyShape1', '/')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('mayaUsdPlugin is not available', result['message'])

    def test_get_usd_prim_info_nonexistent(self):
        """Test get_usd_prim_info with nonexistent proxy shape."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.pluginInfo.return_value = True
            mock_cmds.objExists.return_value = False
            
            result = usd.get_usd_prim_info('nonexistent', '/')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('does not exist', result['message'])


if __name__ == '__main__':
    unittest.main()
