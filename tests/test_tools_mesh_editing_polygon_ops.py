"""Tests for additional polygon operations."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import mesh_editing


class TestPolygonOperations(unittest.TestCase):
    """Test cases for additional polygon operations."""

    def test_set_polygon_normals_no_maya(self):
        """Test set_polygon_normals when Maya is not available."""
        with mock_maya_unavailable():
            result = mesh_editing.set_polygon_normals('pCube1')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_set_polygon_normals_success(self):
        """Test set_polygon_normals successfully sets normals."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.set_polygon_normals('pCube1', normal_mode='face')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyNormal.assert_called_once()

    def test_quadrangulate_mesh_success(self):
        """Test quadrangulate_mesh successfully quadrangulates."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.quadrangulate_mesh('pCube1', angle_threshold=45.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyQuadrangulate.assert_called_once()

    def test_reduce_polygon_count_success(self):
        """Test reduce_polygon_count successfully reduces."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.reduce_polygon_count('pCube1', percentage=30.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyReduce.assert_called_once()

    def test_remesh_polygon_success(self):
        """Test remesh_polygon successfully remeshes."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.remesh_polygon('pCube1', target_face_count=500)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyRemesh.assert_called_once()

    def test_flip_uvs_success(self):
        """Test flip_uvs successfully flips UVs."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.flip_uvs('pCube1', direction='u')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyFlipUV.assert_called_once()

    def test_normalize_uvs_success(self):
        """Test normalize_uvs successfully normalizes UVs."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.normalize_uvs('pCube1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyNormalizeUV.assert_called_once()

    def test_planar_projection_uvs_success(self):
        """Test planar_projection_uvs successfully projects."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.planar_projection_uvs('pCube1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyPlanarProjection.assert_called_once()

    def test_apply_uv_projection_success(self):
        """Test apply_uv_projection successfully applies projection."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.apply_uv_projection('pCube1', projection_type='cylindrical')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyProjection.assert_called_once()

    def test_smooth_faces_success(self):
        """Test smooth_faces successfully smooths faces."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.smooth_faces('pCube1', faces=[0, 1])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polySmoothFace.assert_called_once()

    def test_soften_edges_success(self):
        """Test soften_edges successfully softens edges."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.soften_edges('pCube1', edges=[0, 1])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polySoftEdge.assert_called_once()

    def test_transfer_attributes_success(self):
        """Test transfer_attributes successfully transfers."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'mesh'
            
            result = mesh_editing.transfer_attributes('sourceMesh', 'targetMesh', transfer_uvs=True)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.polyTransfer.assert_called_once()


if __name__ == '__main__':
    unittest.main()
