"""Tests for extended mesh editing tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import mesh_editing


class TestExtendedMeshEditingTools(unittest.TestCase):
    """Test cases for extended mesh editing tools."""

    def test_split_faces_no_maya(self):
        """Test split_faces when Maya is not available."""
        with mock_maya_unavailable():
            result = mesh_editing.split_faces('pCube1')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_split_faces_success(self):
        """Test split_faces successfully splits faces."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.split_faces('pCube1', faces=[0, 1])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polySplit.assert_called_once()

    def test_collapse_edges_success(self):
        """Test collapse_edges successfully collapses edges."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.collapse_edges('pCube1', edges=[0, 1])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyCollapseEdge.assert_called_once()

    def test_triangulate_mesh_success(self):
        """Test triangulate_mesh successfully triangulates mesh."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.triangulate_mesh('pCube1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyTriangulate.assert_called_once()

    def test_separate_mesh_success(self):
        """Test separate_mesh successfully separates mesh."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            mock_cmds.polySeparate.return_value = ['pCube1', 'pCube2']
            
            result = mesh_editing.separate_mesh('pCube1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polySeparate.assert_called_once()


if __name__ == '__main__':
    unittest.main()
