"""Tests for additional shader tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import materials


class TestShaderTools(unittest.TestCase):
    """Test cases for additional shader tools."""

    def test_create_surface_shader_no_maya(self):
        """Test create_surface_shader when Maya is not available."""
        with mock_maya_unavailable():
            result = materials.create_surface_shader()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_surface_shader_success(self):
        """Test create_surface_shader successfully creates shader."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'surfaceShader1'
            mock_cmds.sets.return_value = 'surfaceShader1SG'
            mock_cmds.connectAttr.return_value = None
            
            result = materials.create_surface_shader(name='mySurfaceShader')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shadingNode.assert_called_once()

    def test_create_use_background_shader_success(self):
        """Test create_use_background_shader successfully creates shader."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'useBackground1'
            mock_cmds.sets.return_value = 'useBackground1SG'
            mock_cmds.connectAttr.return_value = None
            
            result = materials.create_use_background_shader()
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shadingNode.assert_called_once()

    def test_create_layered_shader_success(self):
        """Test create_layered_shader successfully creates shader."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'layeredShader1'
            mock_cmds.sets.return_value = 'layeredShader1SG'
            mock_cmds.connectAttr.return_value = None
            
            result = materials.create_layered_shader()
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shadingNode.assert_called_once()

    def test_create_ramp_shader_success(self):
        """Test create_ramp_shader successfully creates shader."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'rampShader1'
            mock_cmds.sets.return_value = 'rampShader1SG'
            mock_cmds.connectAttr.return_value = None
            
            result = materials.create_ramp_shader()
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shadingNode.assert_called_once()

    def test_create_shading_node_no_maya(self):
        """Test create_shading_node when Maya is not available."""
        with mock_maya_unavailable():
            result = materials.create_shading_node('lambert', as_shader=True)
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_shading_node_no_type_specified(self):
        """Test create_shading_node fails when no type is specified."""
        with mock_maya_available():
            result = materials.create_shading_node('lambert')
            self.assertEqual(result['status'], 'error')
            self.assertIn('Must specify', result['message'])

    def test_create_shading_node_as_shader(self):
        """Test create_shading_node successfully creates shader node."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'lambert1'
            
            result = materials.create_shading_node('lambert', as_shader=True)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shadingNode.assert_called_once_with('lambert', asShader=True)

    def test_create_shading_node_as_texture(self):
        """Test create_shading_node successfully creates texture node."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'file1'
            
            result = materials.create_shading_node('file', as_texture=True)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shadingNode.assert_called_once_with('file', asTexture=True)

    def test_create_shading_node_as_utility(self):
        """Test create_shading_node successfully creates utility node."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'place2dTexture1'
            
            result = materials.create_shading_node('place2dTexture', as_utility=True)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shadingNode.assert_called_once_with('place2dTexture', asUtility=True)

    def test_create_shading_node_with_name(self):
        """Test create_shading_node with custom name."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'myLambert'
            
            result = materials.create_shading_node('lambert', as_shader=True, name='myLambert')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shadingNode.assert_called_once_with('lambert', asShader=True, name='myLambert')


if __name__ == '__main__':
    unittest.main()
