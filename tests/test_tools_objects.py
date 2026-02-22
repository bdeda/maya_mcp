"""Tests for object creation tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import objects


class TestObjectTools(unittest.TestCase):
    """Test cases for object creation tools."""

    def test_create_polygon_cube_no_maya(self):
        """Test create_polygon_cube when Maya is not available."""
        with mock_maya_unavailable():
            result = objects.create_polygon_cube()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_polygon_cube_success(self):
        """Test create_polygon_cube creates a cube."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.polyCube.return_value = ['pCube1', 'pCubeShape1']
            
            result = objects.create_polygon_cube(name='testCube', width=2.0)
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['transform'], 'pCube1')
            self.assertEqual(result['shape'], 'pCubeShape1')
            mock_cmds.polyCube.assert_called_once()

    def test_create_polygon_sphere_success(self):
        """Test create_polygon_sphere creates a sphere."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.polySphere.return_value = ['pSphere1', 'pSphereShape1']
            
            result = objects.create_polygon_sphere(name='testSphere', radius=2.0)
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['transform'], 'pSphere1')

    def test_delete_objects_no_maya(self):
        """Test delete_objects when Maya is not available."""
        with mock_maya_unavailable():
            result = objects.delete_objects(['pCube1'])
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_delete_objects_empty_list(self):
        """Test delete_objects with empty list."""
        result = objects.delete_objects([])
        self.assertEqual(result['status'], 'error')
        self.assertIn('No object names', result['message'])

    def test_delete_objects_success(self):
        """Test delete_objects successfully deletes objects."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = objects.delete_objects(['pCube1', 'pSphere1'])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.delete.assert_called_once()

    def test_duplicate_objects_success(self):
        """Test duplicate_objects successfully duplicates objects."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.duplicate.return_value = ['pCube2', 'pSphere2']
            
            result = objects.duplicate_objects(['pCube1', 'pSphere1'])
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(len(result['duplicated']), 2)


if __name__ == '__main__':
    unittest.main()
