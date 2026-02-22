"""Tests for attribute tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import attributes


class TestAttributeTools(unittest.TestCase):
    """Test cases for attribute tools."""

    def test_set_attribute_no_maya(self):
        """Test set_attribute when Maya is not available."""
        with mock_maya_unavailable():
            result = attributes.set_attribute('pCube1.translateX', 5.0)
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_set_attribute_success(self):
        """Test set_attribute successfully sets attribute value."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = attributes.set_attribute('pCube1.translateX', 5.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.setAttr.assert_called_once()

    def test_set_attribute_nonexistent(self):
        """Test set_attribute for nonexistent attribute."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = False
            
            result = attributes.set_attribute('nonexistent.attr', 5.0)
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('does not exist', result['message'])

    def test_add_attribute_success(self):
        """Test add_attribute successfully adds attribute."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.side_effect = lambda x: x == 'pCube1'
            
            result = attributes.add_attribute('pCube1', 'myAttr', 'double', 1.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.addAttr.assert_called_once()

    def test_connect_attributes_success(self):
        """Test connect_attributes successfully connects attributes."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = attributes.connect_attributes('pCube1.translateX', 'pCube2.translateX')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.connectAttr.assert_called_once()

    def test_disconnect_attributes_success(self):
        """Test disconnect_attributes successfully disconnects attributes."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = attributes.disconnect_attributes('pCube1.translateX', 'pCube2.translateX')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.disconnectAttr.assert_called_once()


if __name__ == '__main__':
    unittest.main()
