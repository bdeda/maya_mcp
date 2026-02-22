"""Tests for query tools."""

import unittest
from unittest.mock import patch, MagicMock

from maya_mcp.tools import query


class TestQueryTools(unittest.TestCase):
    """Test cases for query tools."""

    def test_list_objects_no_maya(self):
        """Test list_objects when Maya is not available."""
        with patch('maya_mcp.tools.query.maya', side_effect=ImportError('No module named maya')):
            result = query.list_objects()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    @patch('maya_mcp.tools.query.maya')
    def test_list_objects_success(self, mock_maya):
        """Test list_objects returns objects."""
        mock_cmds = MagicMock()
        mock_cmds.ls.return_value = ['pCube1', 'pSphere1', 'pCylinder1']
        mock_maya.cmds = mock_cmds
        
        result = query.list_objects()
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['objects']), 3)
        self.assertEqual(result['count'], 3)

    @patch('maya_mcp.tools.query.maya')
    def test_list_objects_with_type_filter(self, mock_maya):
        """Test list_objects with type filter."""
        mock_cmds = MagicMock()
        mock_cmds.ls.return_value = ['joint1', 'joint2']
        mock_maya.cmds = mock_cmds
        
        result = query.list_objects(type_filter='joint')
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.ls.assert_called_once_with(type='joint')

    def test_object_exists_no_maya(self):
        """Test object_exists when Maya is not available."""
        with patch('maya_mcp.tools.query.maya', side_effect=ImportError('No module named maya')):
            result = query.object_exists('pCube1')
            self.assertEqual(result['status'], 'error')
            self.assertFalse(result['exists'])

    @patch('maya_mcp.tools.query.maya')
    def test_object_exists_true(self, mock_maya):
        """Test object_exists returns True for existing object."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_maya.cmds = mock_cmds
        
        result = query.object_exists('pCube1')
        
        self.assertEqual(result['status'], 'success')
        self.assertTrue(result['exists'])

    @patch('maya_mcp.tools.query.maya')
    def test_object_exists_false(self, mock_maya):
        """Test object_exists returns False for nonexistent object."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = False
        mock_maya.cmds = mock_cmds
        
        result = query.object_exists('nonexistent')
        
        self.assertEqual(result['status'], 'success')
        self.assertFalse(result['exists'])

    @patch('maya_mcp.tools.query.maya')
    def test_get_object_type_success(self, mock_maya):
        """Test get_object_type returns object type."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_cmds.objectType.return_value = 'transform'
        mock_maya.cmds = mock_cmds
        
        result = query.get_object_type('pCube1')
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['type'], 'transform')

    @patch('maya_mcp.tools.query.maya')
    def test_get_object_type_nonexistent(self, mock_maya):
        """Test get_object_type for nonexistent object."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = False
        mock_maya.cmds = mock_cmds
        
        result = query.get_object_type('nonexistent')
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('does not exist', result['message'])

    @patch('maya_mcp.tools.query.maya')
    def test_get_attribute_value_success(self, mock_maya):
        """Test get_attribute_value returns attribute value."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.side_effect = lambda x: True
        mock_cmds.getAttr.return_value = 5.0
        mock_maya.cmds = mock_cmds
        
        result = query.get_attribute_value('pCube1', 'translateX')
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['value'], 5.0)

    @patch('maya_mcp.tools.query.maya')
    def test_list_attributes_success(self, mock_maya):
        """Test list_attributes returns attribute list."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_cmds.listAttr.return_value = ['translateX', 'translateY', 'translateZ']
        mock_maya.cmds = mock_cmds
        
        result = query.list_attributes('pCube1')
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['attributes']), 3)
        self.assertEqual(result['count'], 3)


if __name__ == '__main__':
    unittest.main()
