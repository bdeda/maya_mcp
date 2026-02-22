"""Tests for extended animation tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import animation


class TestExtendedAnimationTools(unittest.TestCase):
    """Test cases for extended animation tools."""

    def test_bake_results_no_maya(self):
        """Test bake_results when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.bake_results(['pCube1'], (1.0, 10.0))
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_bake_results_success(self):
        """Test bake_results successfully bakes animation."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.bakeResults.return_value = ['pCube1']
            
            result = animation.bake_results(['pCube1'], (1.0, 10.0))
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.bakeResults.assert_called_once()

    def test_bake_simulation_success(self):
        """Test bake_simulation successfully bakes simulation."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.bakeSimulation.return_value = ['pCube1']
            
            result = animation.bake_simulation(['pCube1'], (1.0, 10.0))
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.bakeSimulation.assert_called_once()

    def test_copy_keyframes_no_maya(self):
        """Test copy_keyframes when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.copy_keyframes(['pCube1.translateX'])
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_copy_keyframes_success(self):
        """Test copy_keyframes successfully copies keyframes."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.copyKey.return_value = ['pCube1.translateX']
            
            result = animation.copy_keyframes(['pCube1.translateX'])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.copyKey.assert_called_once()

    def test_paste_keyframes_success(self):
        """Test paste_keyframes successfully pastes keyframes."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.pasteKey.return_value = ['pCube1.translateX']
            
            result = animation.paste_keyframes(['pCube1.translateX'], time=5.0)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.pasteKey.assert_called_once()

    def test_scale_keyframes_success(self):
        """Test scale_keyframes successfully scales keyframes."""
        with mock_maya_available() as mock_cmds:
            result = animation.scale_keyframes(
                ['pCube1.translateX'],
                (1.0, 10.0),
                scale_factor=2.0
            )
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.scaleKey.assert_called_once()

    def test_snap_keyframes_success(self):
        """Test snap_keyframes successfully snaps keyframes."""
        with mock_maya_available() as mock_cmds:
            result = animation.snap_keyframes(
                ['pCube1.translateX'],
                snap_to=0.5
            )
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.snapKey.assert_called_once()

    def test_select_keyframes_success(self):
        """Test select_keyframes successfully selects keyframes."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.selectKey.return_value = ['pCube1.translateX']
            
            result = animation.select_keyframes(
                ['pCube1.translateX'],
                time_range=(1.0, 10.0)
            )
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.selectKey.assert_called_once()

    def test_query_keyframe_info_no_maya(self):
        """Test query_keyframe_info when Maya is not available."""
        with mock_maya_unavailable():
            result = animation.query_keyframe_info('pCube1.translateX')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_query_keyframe_info_success(self):
        """Test query_keyframe_info successfully queries keyframe info."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.keyframe.return_value = [1.0, 5.0, 10.0]
            
            result = animation.query_keyframe_info(
                'pCube1.translateX',
                info_type='time'
            )
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.keyframe.assert_called_once()

    def test_query_keyframe_info_invalid_type(self):
        """Test query_keyframe_info with invalid info_type."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = animation.query_keyframe_info(
                'pCube1.translateX',
                info_type='invalid'
            )
            
            self.assertEqual(result['status'], 'error')
            self.assertIn('Invalid info_type', result['message'])


if __name__ == '__main__':
    unittest.main()
