"""Tests for advanced animation tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import animation


class TestAdvancedAnimationTools(unittest.TestCase):
    """Test cases for advanced animation tools."""

    def test_find_keyframe_no_maya(self):
        """Test find_keyframe when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.find_keyframe('pCube1.translateX', 5.0)
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_find_keyframe_success(self):
        """Test find_keyframe successfully finds keyframe."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.findKeyframe.return_value = 5.0
            
            result = animation.find_keyframe('pCube1.translateX', 4.5, direction='forward')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.findKeyframe.assert_called_once()

    def test_set_keyframe_tangent_no_maya(self):
        """Test set_keyframe_tangent when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.set_keyframe_tangent(['pCube1.translateX'], in_tangent_type='spline')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_set_keyframe_tangent_no_tangent_type(self):
        """Test set_keyframe_tangent fails when no tangent type specified."""
        with mock_maya_available():
            result = animation.set_keyframe_tangent(['pCube1.translateX'])
            self.assertEqual(result['status'], 'error')
            self.assertIn('Must specify', result['message'])

    def test_set_keyframe_tangent_success(self):
        """Test set_keyframe_tangent successfully sets tangent types."""
        with mock_maya_available() as mock_cmds:
            result = animation.set_keyframe_tangent(
                ['pCube1.translateX'],
                in_tangent_type='spline',
                out_tangent_type='linear'
            )
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.keyTangent.assert_called_once()

    def test_create_blend_node_no_maya(self):
        """Test create_blend_node when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.create_blend_node()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_blend_node_success(self):
        """Test create_blend_node successfully creates blend node."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.blendNode.return_value = 'blendNode1'
            
            result = animation.create_blend_node(name='myBlendNode')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.blendNode.assert_called_once()

    def test_create_character_set_no_maya(self):
        """Test create_character_set when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.create_character_set()
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_character_set_success(self):
        """Test create_character_set successfully creates character set."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.character.return_value = 'character1'
            
            result = animation.create_character_set(name='myCharacter')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.character.assert_called_once()

    def test_create_character_set_with_attributes(self):
        """Test create_character_set with attributes."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.character.return_value = 'character1'
            
            result = animation.create_character_set(
                name='myCharacter',
                attributes=['pCube1.translateX', 'pCube1.rotateY']
            )
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.character.assert_called_once()

    def test_create_animation_clip_no_maya(self):
        """Test create_animation_clip when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.create_animation_clip('myClip', (1.0, 10.0))
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_animation_clip_success(self):
        """Test create_animation_clip successfully creates clip."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.clip.return_value = 'clip1'
            
            result = animation.create_animation_clip('myClip', (1.0, 10.0))
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.clip.assert_called_once()

    def test_create_time_warp_no_maya(self):
        """Test create_time_warp when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.create_time_warp('animCurve1', (1.0, 10.0))
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_time_warp_nonexistent_curve(self):
        """Test create_time_warp with nonexistent animation curve."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = False
            
            result = animation.create_time_warp('nonexistent', (1.0, 10.0))
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('does not exist', result['message'])

    def test_create_time_warp_success(self):
        """Test create_time_warp successfully creates time warp."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.timeWarp.return_value = 'timeWarp1'
            
            result = animation.create_time_warp('animCurve1', (1.0, 10.0))
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.timeWarp.assert_called_once()


if __name__ == '__main__':
    unittest.main()
