"""Tests for additional deformer tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import deformers


class TestAdditionalDeformerTools(unittest.TestCase):
    """Test cases for additional deformer tools."""

    def test_create_sculpt_deformer_no_maya(self):
        """Test create_sculpt_deformer when Maya is not available."""
        with mock_maya_unavailable():
            result = deformers.create_sculpt_deformer('pCube1')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_sculpt_deformer_success(self):
        """Test create_sculpt_deformer successfully creates deformer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.sculpt.return_value = ['sculpt1']
            
            result = deformers.create_sculpt_deformer('pCube1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.sculpt.assert_called_once()

    def test_create_wire_deformer_success(self):
        """Test create_wire_deformer successfully creates deformer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.wire.return_value = ['wire1']
            
            result = deformers.create_wire_deformer('pCube1', 'curve1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.wire.assert_called_once()

    def test_create_wrinkle_deformer_success(self):
        """Test create_wrinkle_deformer successfully creates deformer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.wrinkle.return_value = ['wrinkle1']
            
            result = deformers.create_wrinkle_deformer('pCube1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.wrinkle.assert_called_once()

    def test_create_jiggle_deformer_success(self):
        """Test create_jiggle_deformer successfully creates deformer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.jiggle.return_value = ['jiggle1']
            
            result = deformers.create_jiggle_deformer('pCube1', stiffness=0.7)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.jiggle.assert_called_once()

    def test_create_soft_mod_deformer_success(self):
        """Test create_soft_mod_deformer successfully creates deformer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.softMod.return_value = ['softMod1']
            
            result = deformers.create_soft_mod_deformer('pCube1', falloff_radius=10.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.softMod.assert_called_once()

    def test_create_tension_deformer_success(self):
        """Test create_tension_deformer successfully creates deformer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.tension.return_value = ['tension1']
            
            result = deformers.create_tension_deformer('pCube1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.tension.assert_called_once()

    def test_create_delta_mush_deformer_success(self):
        """Test create_delta_mush_deformer successfully creates deformer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.deltaMush.return_value = ['deltaMush1']
            
            result = deformers.create_delta_mush_deformer('pCube1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.deltaMush.assert_called_once()

    def test_create_shrink_wrap_deformer_success(self):
        """Test create_shrink_wrap_deformer successfully creates deformer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.shrinkWrap.return_value = ['shrinkWrap1']
            
            result = deformers.create_shrink_wrap_deformer('pCube1', 'targetMesh')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shrinkWrap.assert_called_once()

    def test_create_wrap_deformer_success(self):
        """Test create_wrap_deformer successfully creates deformer."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.wrap.return_value = ['wrap1']
            
            result = deformers.create_wrap_deformer('pCube1', 'driverMesh')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.wrap.assert_called_once()


if __name__ == '__main__':
    unittest.main()
