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

    def test_select_with_mode_add(self):
        """Test select_with_mode with add mode."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = scene.select_with_mode(['pCube1'], mode='add')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.select.assert_called_once()

    def test_set_selection_mode_success(self):
        """Test set_selection_mode successfully sets mode."""
        with mock_maya_available() as mock_cmds:
            result = scene.set_selection_mode('component')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.selectMode.assert_called_once()

    def test_get_selection_mode_success(self):
        """Test get_selection_mode successfully gets mode."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.selectMode.return_value = 'object'
            
            result = scene.get_selection_mode()
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['mode'], 'object')

    def test_set_selection_type_success(self):
        """Test set_selection_type successfully sets type."""
        with mock_maya_available() as mock_cmds:
            result = scene.set_selection_type('vertex', enabled=True)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.selectType.assert_called_once()

    def test_highlight_object_success(self):
        """Test highlight_object successfully highlights object."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = scene.highlight_object('pCube1', highlight=True)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.hilite.assert_called_once()

    def test_get_selection_preferences_success(self):
        """Test get_selection_preferences successfully gets preferences."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.selectPref.side_effect = [True, False, True, False]
            
            result = scene.get_selection_preferences()
            
            self.assertEqual(result['status'], 'success')
            self.assertIn('preferences', result)

    def test_set_selection_preference_success(self):
        """Test set_selection_preference successfully sets preference."""
        with mock_maya_available() as mock_cmds:
            result = scene.set_selection_preference('trackSelectionOrder', True)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.selectPref.assert_called_once()


if __name__ == '__main__':
    unittest.main()
