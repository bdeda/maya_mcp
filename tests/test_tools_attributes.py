"""Tests for attribute tools."""

import unittest
from unittest.mock import patch, MagicMock

from maya_mcp.tools import attributes


class TestAttributeTools(unittest.TestCase):
    """Test cases for attribute tools."""

    def test_set_attribute_no_maya(self):
        """Test set_attribute when Maya is not available."""
        with patch('maya_mcp.tools.attributes.maya', side_effect=ImportError('No module named maya')):
            result = attributes.set_attribute('pCube1.translateX', 5.0)
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    @patch('maya_mcp.tools.attributes.maya')
    def test_set_attribute_success(self, mock_maya):
        """Test set_attribute successfully sets attribute value."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_maya.cmds = mock_cmds
        
        result = attributes.set_attribute('pCube1.translateX', 5.0)
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.setAttr.assert_called_once()

    @patch('maya_mcp.tools.attributes.maya')
    def test_set_attribute_nonexistent(self, mock_maya):
        """Test set_attribute for nonexistent attribute."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = False
        mock_maya.cmds = mock_cmds
        
        result = attributes.set_attribute('nonexistent.attr', 5.0)
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('does not exist', result['message'])

    @patch('maya_mcp.tools.attributes.maya')
    def test_add_attribute_success(self, mock_maya):
        """Test add_attribute successfully adds attribute."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.side_effect = lambda x: x == 'pCube1'
        mock_maya.cmds = mock_cmds
        
        result = attributes.add_attribute('pCube1', 'myAttr', 'double', 1.0)
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.addAttr.assert_called_once()

    @patch('maya_mcp.tools.attributes.maya')
    def test_connect_attributes_success(self, mock_maya):
        """Test connect_attributes successfully connects attributes."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_maya.cmds = mock_cmds
        
        result = attributes.connect_attributes('pCube1.translateX', 'pCube2.translateX')
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.connectAttr.assert_called_once()

    @patch('maya_mcp.tools.attributes.maya')
    def test_disconnect_attributes_success(self, mock_maya):
        """Test disconnect_attributes successfully disconnects attributes."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_maya.cmds = mock_cmds
        
        result = attributes.disconnect_attributes('pCube1.translateX', 'pCube2.translateX')
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.disconnectAttr.assert_called_once()


if __name__ == '__main__':
    unittest.main()
