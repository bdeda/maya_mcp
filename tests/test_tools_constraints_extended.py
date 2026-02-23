"""Tests for extended constraint tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import constraints


class TestExtendedConstraintTools(unittest.TestCase):
    """Test cases for extended constraint tools."""

    def test_create_normal_constraint_no_maya(self):
        """Test create_normal_constraint when Maya is not available."""
        with mock_maya_unavailable():
            result = constraints.create_normal_constraint('target', 'constrained')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_normal_constraint_success(self):
        """Test create_normal_constraint successfully creates constraint."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.normalConstraint.return_value = ['normalConstraint1']
            
            result = constraints.create_normal_constraint('target', 'constrained')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.normalConstraint.assert_called_once()

    def test_create_tangent_constraint_success(self):
        """Test create_tangent_constraint successfully creates constraint."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.tangentConstraint.return_value = ['tangentConstraint1']
            
            result = constraints.create_tangent_constraint('target', 'constrained')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.tangentConstraint.assert_called_once()

    def test_create_pole_vector_constraint_success(self):
        """Test create_pole_vector_constraint successfully creates constraint."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.poleVectorConstraint.return_value = ['poleVectorConstraint1']
            
            result = constraints.create_pole_vector_constraint('target', 'constrained')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.poleVectorConstraint.assert_called_once()


if __name__ == '__main__':
    unittest.main()
