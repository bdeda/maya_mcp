"""Tests for material tools."""

import unittest
from unittest.mock import patch, MagicMock

from maya_mcp.tools import materials


class TestMaterialTools(unittest.TestCase):
    """Test cases for material tools."""

    def test_create_lambert_material_no_maya(self):
        """Test create_lambert_material when Maya is not available."""
        with patch('maya_mcp.tools.materials.maya', side_effect=ImportError('No module named maya')):
            result = materials.create_lambert_material('testMat')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    @patch('maya_mcp.tools.materials.maya')
    def test_create_lambert_material_success(self, mock_maya):
        """Test create_lambert_material successfully creates material."""
        mock_cmds = MagicMock()
        mock_cmds.shadingNode.return_value = 'lambert1'
        mock_cmds.sets.return_value = 'lambert1SG'
        mock_maya.cmds = mock_cmds
        
        result = materials.create_lambert_material('testMat')
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['shader'], 'lambert1')

    @patch('maya_mcp.tools.materials.maya')
    def test_assign_material_success(self, mock_maya):
        """Test assign_material successfully assigns material."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_cmds.objectType.return_value = 'transform'
        mock_cmds.listRelatives.return_value = ['pCubeShape1']
        mock_maya.cmds = mock_cmds
        
        result = materials.assign_material('lambert1SG', ['pCube1'])
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.sets.assert_called_once()

    @patch('maya_mcp.tools.materials.maya')
    def test_list_materials_success(self, mock_maya):
        """Test list_materials returns materials."""
        mock_cmds = MagicMock()
        mock_cmds.ls.return_value = ['mat1SG', 'mat2SG', 'initialShadingGroup']
        mock_maya.cmds = mock_cmds
        
        result = materials.list_materials()
        
        self.assertEqual(result['status'], 'success')
        # Should filter out initialShadingGroup
        self.assertEqual(len(result['materials']), 2)


if __name__ == '__main__':
    unittest.main()
