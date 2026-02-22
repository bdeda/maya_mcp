"""Tests for transform tools."""

import unittest
from unittest.mock import patch, MagicMock

from maya_mcp.tools import transform


class TestTransformTools(unittest.TestCase):
    """Test cases for transform tools."""

    def test_move_object_no_maya(self):
        """Test move_object when Maya is not available."""
        with patch('maya_mcp.tools.transform.maya', side_effect=ImportError('No module named maya')):
            result = transform.move_object('pCube1', x=5.0)
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    @patch('maya_mcp.tools.transform.maya')
    def test_move_object_success(self, mock_maya):
        """Test move_object successfully moves object."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_maya.cmds = mock_cmds
        
        result = transform.move_object('pCube1', x=5.0, y=2.0, z=1.0)
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.move.assert_called_once()

    @patch('maya_mcp.tools.transform.maya')
    def test_rotate_object_success(self, mock_maya):
        """Test rotate_object successfully rotates object."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_maya.cmds = mock_cmds
        
        result = transform.rotate_object('pCube1', x=45.0, y=90.0, z=0.0)
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.rotate.assert_called_once()

    @patch('maya_mcp.tools.transform.maya')
    def test_scale_object_success(self, mock_maya):
        """Test scale_object successfully scales object."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_maya.cmds = mock_cmds
        
        result = transform.scale_object('pCube1', x=2.0, y=2.0, z=2.0)
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.scale.assert_called_once()

    @patch('maya_mcp.tools.transform.maya')
    def test_parent_objects_success(self, mock_maya):
        """Test parent_objects successfully parents objects."""
        mock_cmds = MagicMock()
        mock_cmds.objExists.return_value = True
        mock_maya.cmds = mock_cmds
        
        result = transform.parent_objects(['pCube1'], 'parentGroup')
        
        self.assertEqual(result['status'], 'success')
        mock_cmds.parent.assert_called_once()


if __name__ == '__main__':
    unittest.main()
