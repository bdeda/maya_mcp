"""Tests for NURBS tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import nurbs


class TestNurbsTools(unittest.TestCase):
    """Test cases for NURBS tools."""

    def test_create_nurbs_circle_no_maya(self):
        """Test create_nurbs_circle when Maya is not available."""
        with mock_maya_unavailable():
            result = nurbs.create_nurbs_circle('testCircle')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_nurbs_circle_success(self):
        """Test create_nurbs_circle successfully creates circle."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.circle.return_value = ['nurbsCircle1', 'nurbsCircleShape1']
            
            result = nurbs.create_nurbs_circle('testCircle', radius=2.0)
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['circle'], 'nurbsCircle1')
            mock_cmds.circle.assert_called_once()

    def test_create_curve_from_points_success(self):
        """Test create_curve_from_points successfully creates curve."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.curve.return_value = ['curve1', 'curveShape1']
            
            points = [(0, 0, 0), (1, 1, 0), (2, 0, 0)]
            result = nurbs.create_curve_from_points(points)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.curve.assert_called_once()

    def test_loft_surfaces_success(self):
        """Test loft_surfaces successfully creates lofted surface."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.loft.return_value = ['loftedSurface1', 'loftedSurfaceShape1']
            
            result = nurbs.loft_surfaces(['curve1', 'curve2'])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.loft.assert_called_once()


if __name__ == '__main__':
    unittest.main()
