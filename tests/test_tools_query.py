"""Tests for query tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import query


class TestQueryTools(unittest.TestCase):
    """Test cases for query tools."""

    def test_list_objects_no_maya(self):
        """Test list_objects when Maya is not available."""
        with mock_maya_unavailable():
            result = query.list_objects()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_list_objects_success(self):
        """Test list_objects returns objects."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.ls.return_value = ['pCube1', 'pSphere1', 'pCylinder1']
            
            result = query.list_objects()
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(len(result['objects']), 3)
            self.assertEqual(result['count'], 3)

    def test_list_objects_with_type_filter(self):
        """Test list_objects with type filter."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.ls.return_value = ['joint1', 'joint2']
            
            result = query.list_objects(type_filter='joint')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.ls.assert_called_once_with(type='joint')

    def test_object_exists_no_maya(self):
        """Test object_exists when Maya is not available."""
        with mock_maya_unavailable():
            result = query.object_exists('pCube1')
            self.assertEqual(result['status'], 'error')
            self.assertFalse(result['exists'])

    def test_object_exists_true(self):
        """Test object_exists returns True for existing object."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = query.object_exists('pCube1')
            
            self.assertEqual(result['status'], 'success')
            self.assertTrue(result['exists'])

    def test_object_exists_false(self):
        """Test object_exists returns False for nonexistent object."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = False
            
            result = query.object_exists('nonexistent')
            
            self.assertEqual(result['status'], 'success')
            self.assertFalse(result['exists'])

    def test_get_object_type_success(self):
        """Test get_object_type returns object type."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'transform'
            
            result = query.get_object_type('pCube1')
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['type'], 'transform')

    def test_get_object_type_nonexistent(self):
        """Test get_object_type for nonexistent object."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = False
            
            result = query.get_object_type('nonexistent')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('does not exist', result['message'])

    def test_get_attribute_value_success(self):
        """Test get_attribute_value returns attribute value."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.side_effect = lambda x: True
            mock_cmds.getAttr.return_value = 5.0
            
            result = query.get_attribute_value('pCube1', 'translateX')
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['value'], 5.0)

    def test_list_attributes_success(self):
        """Test list_attributes returns attribute list."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.listAttr.return_value = ['translateX', 'translateY', 'translateZ']
            
            result = query.list_attributes('pCube1')
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(len(result['attributes']), 3)
            self.assertEqual(result['count'], 3)


if __name__ == '__main__':
    unittest.main()
