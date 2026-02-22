"""Tests for light tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import lights


class TestLightTools(unittest.TestCase):
    """Test cases for light tools."""

    def test_create_directional_light_no_maya(self):
        """Test create_directional_light when Maya is not available."""
        with mock_maya_unavailable():
            result = lights.create_directional_light('testLight')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_directional_light_success(self):
        """Test create_directional_light successfully creates light."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.directionalLight.return_value = ['directionalLight1', 'directionalLightShape1']
            
            result = lights.create_directional_light('testLight', intensity=2.0)
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['light'], 'directionalLight1')

    def test_list_lights_success(self):
        """Test list_lights returns lights."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.ls.return_value = ['lightShape1', 'lightShape2']
            mock_cmds.listRelatives.side_effect = [['light1'], ['light2']]
            
            result = lights.list_lights()
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(len(result['lights']), 2)


if __name__ == '__main__':
    unittest.main()
