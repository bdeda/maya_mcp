"""Tests for light tools."""

import unittest
from unittest.mock import patch, MagicMock

from maya_mcp.tools import lights


class TestLightTools(unittest.TestCase):
    """Test cases for light tools."""

    def test_create_directional_light_no_maya(self):
        """Test create_directional_light when Maya is not available."""
        with patch('maya_mcp.tools.lights.maya', side_effect=ImportError('No module named maya')):
            result = lights.create_directional_light('testLight')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    @patch('maya_mcp.tools.lights.maya')
    def test_create_directional_light_success(self, mock_maya):
        """Test create_directional_light successfully creates light."""
        mock_cmds = MagicMock()
        mock_cmds.directionalLight.return_value = ['directionalLight1', 'directionalLightShape1']
        mock_maya.cmds = mock_cmds
        
        result = lights.create_directional_light('testLight', intensity=2.0)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['light'], 'directionalLight1')

    @patch('maya_mcp.tools.lights.maya')
    def test_list_lights_success(self, mock_maya):
        """Test list_lights returns lights."""
        mock_cmds = MagicMock()
        mock_cmds.ls.return_value = ['lightShape1', 'lightShape2']
        mock_cmds.listRelatives.side_effect = [['light1'], ['light2']]
        mock_maya.cmds = mock_cmds
        
        result = lights.list_lights()
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['lights']), 2)


if __name__ == '__main__':
    unittest.main()
