"""Tests for extended material tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import materials


class TestExtendedMaterialTools(unittest.TestCase):
    """Test cases for extended material tools."""

    def test_create_file_texture_no_maya(self):
        """Test create_file_texture when Maya is not available."""
        with mock_maya_unavailable():
            result = materials.create_file_texture('/path/to/texture.jpg')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_file_texture_success(self):
        """Test create_file_texture successfully creates file texture."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'file1'
            
            result = materials.create_file_texture('/path/to/texture.jpg')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shadingNode.assert_called_once()

    def test_create_ramp_texture_success(self):
        """Test create_ramp_texture successfully creates ramp texture."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'ramp1'
            
            result = materials.create_ramp_texture()
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shadingNode.assert_called_once()

    def test_create_place2d_texture_success(self):
        """Test create_place2d_texture successfully creates placement node."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'place2dTexture1'
            
            result = materials.create_place2d_texture()
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.shadingNode.assert_called_once()


if __name__ == '__main__':
    unittest.main()
