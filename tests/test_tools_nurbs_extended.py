"""Tests for extended NURBS tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import nurbs


class TestExtendedNurbsTools(unittest.TestCase):
    """Test cases for extended NURBS tools."""

    def test_create_nurbs_cylinder_no_maya(self):
        """Test create_nurbs_cylinder when Maya is not available."""
        with mock_maya_unavailable():
            result = nurbs.create_nurbs_cylinder('testCylinder')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_nurbs_cylinder_success(self):
        """Test create_nurbs_cylinder successfully creates cylinder."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.cylinder.return_value = ['nurbsCylinder1', 'nurbsCylinderShape1']
            
            result = nurbs.create_nurbs_cylinder('testCylinder', radius=2.0, height=4.0)
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['cylinder'], 'nurbsCylinder1')
            mock_cmds.cylinder.assert_called_once()

    def test_attach_curves_success(self):
        """Test attach_curves successfully attaches curves."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.attachCurve.return_value = ['attachedCurve1']
            
            result = nurbs.attach_curves('curve1', 'curve2')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.attachCurve.assert_called_once()

    def test_close_curve_success(self):
        """Test close_curve successfully closes curve."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.closeCurve.return_value = ['closedCurve1']
            
            result = nurbs.close_curve('curve1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.closeCurve.assert_called_once()

    def test_create_planar_surface_success(self):
        """Test create_planar_surface successfully creates planar surface."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.planar.return_value = ['planarSurface1', 'planarSurfaceShape1']
            
            result = nurbs.create_planar_surface(['curve1', 'curve2'])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.planar.assert_called_once()


if __name__ == '__main__':
    unittest.main()
