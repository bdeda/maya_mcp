"""Tests for mesh editing tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import mesh_editing


class TestMeshEditingTools(unittest.TestCase):
    """Test cases for mesh editing tools."""

    def test_extrude_faces_no_maya(self):
        """Test extrude_faces when Maya is not available."""
        with mock_maya_unavailable():
            result = mesh_editing.extrude_faces('pCube1')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_extrude_faces_success(self):
        """Test extrude_faces successfully extrudes faces."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'transform'
            mock_cmds.listRelatives.return_value = ['pCubeShape1']
            mock_cmds.polyExtrudeFacet.return_value = ['pCube1']
            
            result = mesh_editing.extrude_faces('pCube1', faces=[0, 1, 2])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyExtrudeFacet.assert_called_once()

    def test_bevel_edges_success(self):
        """Test bevel_edges successfully bevels edges."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            mock_cmds.polyBevel.return_value = ['pCube1']
            
            result = mesh_editing.bevel_edges('pCube1', edges=[0, 1])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyBevel.assert_called_once()

    def test_smooth_mesh_success(self):
        """Test smooth_mesh successfully smooths mesh."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.smooth_mesh('pCube1', divisions=2)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polySmooth.assert_called_once()

    def test_boolean_union_success(self):
        """Test boolean_union successfully performs union."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.polyUnite.return_value = ['combinedMesh']
            
            result = mesh_editing.boolean_union('pCube1', 'pSphere1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyUnite.assert_called_once()

    def test_merge_vertices_success(self):
        """Test merge_vertices successfully merges vertices."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.merge_vertices('pCube1', vertices=[0, 1, 2])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyMergeVertex.assert_called_once()


if __name__ == '__main__':
    unittest.main()
