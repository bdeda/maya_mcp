"""Tests for object creation tools."""

import unittest
from unittest.mock import patch, MagicMock

from maya_mcp.tools import objects


class TestObjectTools(unittest.TestCase):
    """Test cases for object creation tools."""

    def test_create_polygon_cube_no_maya(self):
        """Test create_polygon_cube when Maya is not available."""
        with patch('maya_mcp.tools.objects.maya', side_effect=ImportError('No module named maya')):
            result = objects.create_polygon_cube()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    @patch('maya_mcp.tools.objects.maya')
    def test_create_polygon_cube_success(self, mock_maya):
        """Test create_polygon_cube creates a cube."""
        mock_cmds = MagicMock()
        mock_cmds.polyCube.return_value = ['pCube1', 'pCubeShape1']
        mock_maya.cmds = mock_cmds
        
        result = objects.create_polygon_cube(name='testCube', width=2.0)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['transform'], 'pCube1')
        self.assertEqual(result['shape'], 'pCubeShape1')
        mock_cmds.polyCube.assert_called_once()

    @patch('maya_mcp.tools.objects.maya')
    def test_create_polygon_sphere_success(self, mock_maya):
        """Test create_polygon_sphere creates a sphere."""
        mock_cmds = MagicMock()
        mock_cmds.polySphere.return_value = ['pSphere1', 'pSphereShape1']
        mock_maya.cmds = mock_cmds
        
        result = objects.create_polygon_sphere(name='testSphere', radius=2.0)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['transform'], 'pSphere1')

    def test_delete_objects_no_maya(self):
        """Test delete_objects when Maya is not available."""
        with patch('maya_mcp.tools.objects.maya', side_effect=ImportError('No module named maya')):
            result = objects.delete_objects(['pCube1'])
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_delete_objects_empty_list(self):
        """Test delete_objects with empty list."""
        with patch('maya_mcp.tools.objects.maya'):
            result = objects.delete_objects([])
            self.assertEqual(result['status'], 'error')
            self.assertIn('No object names', result['message'])

    @patch('maya_mcp.tools.objects.maya')
    def test_delete_objects_success(self, mock_maya):
        """Test delete_objects successfully deletes objects."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_maya.cmds = mock_cmds
        
        result = objects.delete_objects(['pCube1', 'pSphere1'])
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.delete.assert_called_once()

    @patch('maya_mcp.tools.objects.maya')
    def test_duplicate_objects_success(self, mock_maya):
        """Test duplicate_objects successfully duplicates objects."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_cmds.duplicate.return_value = ['pCube2', 'pSphere2']
        mock_maya.cmds = mock_cmds
        
        result = objects.duplicate_objects(['pCube1', 'pSphere1'])
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['duplicated']), 2)


if __name__ == '__main__':
    unittest.main()
