"""Tests for scene tools."""

import unittest
from unittest.mock import patch, MagicMock

from maya_mcp.tools import scene


class TestSceneTools(unittest.TestCase):
    """Test cases for scene tools."""

    def test_get_selection_no_maya(self):
        """Test get_selection when Maya is not available."""
        with patch('maya_mcp.tools.scene.maya', side_effect=ImportError('No module named maya')):
            result = scene.get_selection()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    @patch('maya_mcp.tools.scene.maya')
    def test_get_selection_success(self, mock_maya):
        """Test get_selection returns selection."""
        mock_cmds = MagicMock()
        mock_cmds.ls.return_value = ['pCube1', 'pSphere1']
        mock_maya.cmds = mock_cmds
        
        result = scene.get_selection()
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['selection'], ['pCube1', 'pSphere1'])
        self.assertEqual(result['count'], 2)

    @patch('maya_mcp.tools.scene.maya')
    def test_get_selection_empty(self, mock_maya):
        """Test get_selection with empty selection."""
        mock_cmds = MagicMock()
        mock_cmds.ls.return_value = []
        mock_maya.cmds = mock_cmds
        
        result = scene.get_selection()
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['selection'], [])
        self.assertEqual(result['count'], 0)

    def test_select_objects_no_maya(self):
        """Test select_objects when Maya is not available."""
        with patch('maya_mcp.tools.scene.maya', side_effect=ImportError('No module named maya')):
            result = scene.select_objects(['pCube1'])
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_select_objects_empty_list(self):
        """Test select_objects with empty list."""
        with patch('maya_mcp.tools.scene.maya'):
            result = scene.select_objects([])
            self.assertEqual(result['status'], 'error')
            self.assertIn('No object names', result['message'])

    @patch('maya_mcp.tools.scene.maya')
    def test_select_objects_success(self, mock_maya):
        """Test select_objects successfully selects objects."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_maya.cmds = mock_cmds
        
        result = scene.select_objects(['pCube1', 'pSphere1'])
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('Selected', result['message'])
        mock_cmds.select.assert_called_once()

    @patch('maya_mcp.tools.scene.maya')
    def test_select_objects_nonexistent(self, mock_maya):
        """Test select_objects with nonexistent objects."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = False
        mock_maya.cmds = mock_cmds
        
        result = scene.select_objects(['nonexistent'])
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('not found', result['message'])

    def test_clear_selection_no_maya(self):
        """Test clear_selection when Maya is not available."""
        with patch('maya_mcp.tools.scene.maya', side_effect=ImportError('No module named maya')):
            result = scene.clear_selection()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    @patch('maya_mcp.tools.scene.maya')
    def test_clear_selection_success(self, mock_maya):
        """Test clear_selection successfully clears selection."""
        mock_cmds = MagicMock()
        mock_maya.cmds = mock_cmds
        
        result = scene.clear_selection()
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.select.assert_called_once_with(clear=True)


if __name__ == '__main__':
    unittest.main()
