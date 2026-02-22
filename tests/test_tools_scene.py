"""Tests for scene tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import scene


class TestSceneTools(unittest.TestCase):
    """Test cases for scene tools."""

    def test_get_selection_no_maya(self):
        """Test get_selection when Maya is not available."""
        with mock_maya_unavailable():
            result = scene.get_selection()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_get_selection_success(self):
        """Test get_selection returns selection."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.ls.return_value = ['pCube1', 'pSphere1']
            
            result = scene.get_selection()
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['selection'], ['pCube1', 'pSphere1'])
            self.assertEqual(result['count'], 2)

    def test_get_selection_empty(self):
        """Test get_selection with empty selection."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.ls.return_value = []
            
            result = scene.get_selection()
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['selection'], [])
            self.assertEqual(result['count'], 0)

    def test_select_objects_no_maya(self):
        """Test select_objects when Maya is not available."""
        with mock_maya_unavailable():
            result = scene.select_objects(['pCube1'])
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_select_objects_empty_list(self):
        """Test select_objects with empty list."""
        result = scene.select_objects([])
        self.assertEqual(result['status'], 'error')
        self.assertIn('No object names', result['message'])

    def test_select_objects_success(self):
        """Test select_objects successfully selects objects."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = scene.select_objects(['pCube1', 'pSphere1'])
            
            self.assertEqual(result['status'], 'success')
            self.assertIn('Selected', result['message'])
            mock_cmds.select.assert_called_once()

    def test_select_objects_nonexistent(self):
        """Test select_objects with nonexistent objects."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = False
            
            result = scene.select_objects(['nonexistent'])
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('None of the objects exist', result['message'])

    def test_clear_selection_no_maya(self):
        """Test clear_selection when Maya is not available."""
        with mock_maya_unavailable():
            result = scene.clear_selection()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_clear_selection_success(self):
        """Test clear_selection successfully clears selection."""
        with mock_maya_available() as mock_cmds:
            result = scene.clear_selection()
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.select.assert_called_once_with(clear=True)


if __name__ == '__main__':
    unittest.main()
