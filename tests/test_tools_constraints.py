"""Tests for advanced constraint tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import constraints


class TestConstraintTools(unittest.TestCase):
    """Test cases for constraint tools."""

    def test_create_aim_constraint_no_maya(self):
        """Test create_aim_constraint when Maya is not available."""
        with mock_maya_unavailable():
            result = constraints.create_aim_constraint('target', 'constrained')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_aim_constraint_success(self):
        """Test create_aim_constraint successfully creates constraint."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.aimConstraint.return_value = ['aimConstraint1']
            
            result = constraints.create_aim_constraint('target', 'constrained')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.aimConstraint.assert_called_once()

    def test_create_scale_constraint_success(self):
        """Test create_scale_constraint successfully creates constraint."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.scaleConstraint.return_value = ['scaleConstraint1']
            
            result = constraints.create_scale_constraint('target', 'constrained')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.scaleConstraint.assert_called_once()

    def test_remove_constraint_success(self):
        """Test remove_constraint successfully removes constraint."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = constraints.remove_constraint('constraint1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.delete.assert_called_once()


if __name__ == '__main__':
    unittest.main()
