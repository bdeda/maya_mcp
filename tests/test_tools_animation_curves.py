"""Tests for animation curve operations."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import animation


class TestAnimationCurveTools(unittest.TestCase):
    """Test cases for animation curve operations."""

    def test_create_animation_curve_no_maya(self):
        """Test create_animation_curve when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.create_animation_curve()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_animation_curve_invalid_type(self):
        """Test create_animation_curve with invalid curve type."""
        with mock_maya_available():
            result = animation.create_animation_curve(curve_type='invalid')
            self.assertEqual(result['status'], 'error')
            self.assertIn('Invalid curve type', result['message'])

    def test_create_animation_curve_success(self):
        """Test create_animation_curve successfully creates curve."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.createNode.return_value = 'animCurveTL1'
            
            result = animation.create_animation_curve(curve_type='animCurveTL')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.createNode.assert_called_once_with('animCurveTL')

    def test_add_curve_keyframe_no_maya(self):
        """Test add_curve_keyframe when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.add_curve_keyframe('animCurveTL1', 5.0, 10.0)
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_add_curve_keyframe_nonexistent_curve(self):
        """Test add_curve_keyframe with nonexistent curve."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = False
            
            result = animation.add_curve_keyframe('nonexistent', 5.0, 10.0)
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('does not exist', result['message'])

    def test_add_curve_keyframe_success(self):
        """Test add_curve_keyframe successfully adds keyframe."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.setKeyframe.return_value = ['animCurveTL1']
            
            result = animation.add_curve_keyframe('animCurveTL1', 5.0, 10.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.setKeyframe.assert_called_once()

    def test_query_animation_curve_no_maya(self):
        """Test query_animation_curve when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.query_animation_curve('animCurveTL1')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_query_animation_curve_nonexistent(self):
        """Test query_animation_curve with nonexistent curve."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = False
            
            result = animation.query_animation_curve('nonexistent')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('does not exist', result['message'])

    def test_query_animation_curve_invalid_type(self):
        """Test query_animation_curve with invalid query type."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = animation.query_animation_curve('animCurveTL1', query_type='invalid')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('Invalid query type', result['message'])

    def test_query_animation_curve_keyframe_count(self):
        """Test query_animation_curve for keyframe count."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.keyframe.return_value = 5
            
            result = animation.query_animation_curve('animCurveTL1', query_type='keyframeCount')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.keyframe.assert_called_once()

    def test_set_animation_curve_infinity_no_maya(self):
        """Test set_animation_curve_infinity when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.set_animation_curve_infinity('animCurveTL1', pre_infinity='cycle')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_set_animation_curve_infinity_nonexistent(self):
        """Test set_animation_curve_infinity with nonexistent curve."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = False
            
            result = animation.set_animation_curve_infinity('nonexistent', pre_infinity='cycle')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('does not exist', result['message'])

    def test_set_animation_curve_infinity_no_type(self):
        """Test set_animation_curve_infinity with no infinity type."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = animation.set_animation_curve_infinity('animCurveTL1')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('Must specify', result['message'])

    def test_set_animation_curve_infinity_invalid_type(self):
        """Test set_animation_curve_infinity with invalid infinity type."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = animation.set_animation_curve_infinity('animCurveTL1', pre_infinity='invalid')
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('Invalid pre_infinity type', result['message'])

    def test_set_animation_curve_infinity_success(self):
        """Test set_animation_curve_infinity successfully sets infinity."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = animation.set_animation_curve_infinity(
                'animCurveTL1',
                pre_infinity='cycle',
                post_infinity='linear'
            )
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(mock_cmds.setAttr.call_count, 2)


if __name__ == '__main__':
    unittest.main()
