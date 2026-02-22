"""Tests for extended deformer tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import deformers


class TestExtendedDeformerTools(unittest.TestCase):
    """Test cases for extended deformer tools."""

    def test_create_sine_deformer_no_maya(self):
        """Test create_sine_deformer when Maya is not available."""
        with mock_maya_unavailable():
            result = deformers.create_sine_deformer('pCube1')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_sine_deformer_success(self):
        """Test create_sine_deformer successfully creates deformer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.nonLinear.return_value = ['sine1']
            
            result = deformers.create_sine_deformer('pCube1', amplitude=1.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.nonLinear.assert_called_once()

    def test_create_squash_deformer_success(self):
        """Test create_squash_deformer successfully creates deformer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.nonLinear.return_value = ['squash1']
            
            result = deformers.create_squash_deformer('pCube1', factor=0.5)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.nonLinear.assert_called_once()

    def test_list_deformers_success(self):
        """Test list_deformers successfully lists deformers."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.listHistory.return_value = ['blendShape1', 'cluster1']
            mock_cmds.nodeType.side_effect = ['blendShape', 'cluster']
            
            result = deformers.list_deformers('pCube1')
            
            self.assertEqual(result['status'], 'success')
            self.assertIn('deformers', result)


if __name__ == '__main__':
    unittest.main()
