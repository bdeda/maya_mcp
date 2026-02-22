"""Tests for deformer tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import deformers


class TestDeformerTools(unittest.TestCase):
    """Test cases for deformer tools."""

    def test_create_blend_shape_no_maya(self):
        """Test create_blend_shape when Maya is not available."""
        with mock_maya_unavailable():
            result = deformers.create_blend_shape('base', ['target1'])
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_blend_shape_success(self):
        """Test create_blend_shape successfully creates blend shape."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.blendShape.return_value = ['blendShape1']
            
            result = deformers.create_blend_shape('base', ['target1', 'target2'])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.blendShape.assert_called_once()

    def test_create_cluster_success(self):
        """Test create_cluster successfully creates cluster."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.cluster.return_value = ['cluster1Handle', 'cluster1']
            
            result = deformers.create_cluster(['pCube1'])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.cluster.assert_called_once()

    def test_create_bend_deformer_success(self):
        """Test create_bend_deformer successfully creates bend."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.nonLinear.return_value = ['bend1']
            
            result = deformers.create_bend_deformer('pCube1', curvature=90.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.nonLinear.assert_called_once()


if __name__ == '__main__':
    unittest.main()
