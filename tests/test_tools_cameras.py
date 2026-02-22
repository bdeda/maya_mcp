"""Tests for camera tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import cameras


class TestCameraTools(unittest.TestCase):
    """Test cases for camera tools."""

    def test_create_camera_no_maya(self):
        """Test create_camera when Maya is not available."""
        with mock_maya_unavailable():
            result = cameras.create_camera('testCamera')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_camera_success(self):
        """Test create_camera successfully creates camera."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.camera.return_value = ['camera1', 'cameraShape1']
            
            result = cameras.create_camera('testCamera', focal_length=50.0)
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['camera'], 'camera1')
            mock_cmds.camera.assert_called_once()

    def test_list_cameras_success(self):
        """Test list_cameras returns cameras."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.ls.return_value = ['cameraShape1', 'cameraShape2']
            mock_cmds.listRelatives.side_effect = [['camera1'], ['camera2']]
            
            result = cameras.list_cameras()
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(len(result['cameras']), 2)

    def test_look_through_camera_success(self):
        """Test look_through_camera successfully sets view."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'camera'
            mock_cmds.listRelatives.return_value = ['camera1']
            
            result = cameras.look_through_camera('cameraShape1')
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.lookThru.assert_called_once()


if __name__ == '__main__':
    unittest.main()
