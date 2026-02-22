"""Tests for material tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import materials


class TestMaterialTools(unittest.TestCase):
    """Test cases for material tools."""

    def test_create_lambert_material_no_maya(self):
        """Test create_lambert_material when Maya is not available."""
        with mock_maya_unavailable():
            result = materials.create_lambert_material('testMat')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_lambert_material_success(self):
        """Test create_lambert_material successfully creates material."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.shadingNode.return_value = 'lambert1'
            mock_cmds.sets.return_value = 'lambert1SG'
            
            result = materials.create_lambert_material('testMat')
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['shader'], 'lambert1')

    def test_assign_material_success(self):
        """Test assign_material successfully assigns material."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'transform'
            mock_cmds.listRelatives.return_value = ['pCubeShape1']
            
            result = materials.assign_material('lambert1SG', ['pCube1'])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.sets.assert_called_once()

    def test_list_materials_success(self):
        """Test list_materials returns materials."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.ls.return_value = ['mat1SG', 'mat2SG', 'initialShadingGroup']
            
            result = materials.list_materials()
            
            self.assertEqual(result['status'], 'success')
            # Should filter out initialShadingGroup
            self.assertEqual(len(result['materials']), 2)


if __name__ == '__main__':
    unittest.main()
