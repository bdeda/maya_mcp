"""Tests for transform tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import transform


class TestTransformTools(unittest.TestCase):
    """Test cases for transform tools."""

    def test_move_object_no_maya(self):
        """Test move_object when Maya is not available."""
        with mock_maya_unavailable():
            result = transform.move_object('pCube1', x=5.0)
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_move_object_success(self):
        """Test move_object successfully moves object."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = transform.move_object('pCube1', x=5.0, y=2.0, z=1.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.move.assert_called_once()

    def test_rotate_object_success(self):
        """Test rotate_object successfully rotates object."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = transform.rotate_object('pCube1', x=45.0, y=90.0, z=0.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.rotate.assert_called_once()

    def test_scale_object_success(self):
        """Test scale_object successfully scales object."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = transform.scale_object('pCube1', x=2.0, y=2.0, z=2.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.scale.assert_called_once()

    def test_parent_objects_success(self):
        """Test parent_objects successfully parents objects."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = transform.parent_objects(['pCube1'], 'parentGroup')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.parent.assert_called_once()


if __name__ == '__main__':
    unittest.main()
