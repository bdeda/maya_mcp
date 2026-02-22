"""Tests for safety module."""

import unittest
from unittest.mock import patch

from maya_mcp._safety import (
    BLOCKED_COMMANDS,
    CALLBACK_COMMANDS,
    SCRIPT_EXECUTION_COMMANDS,
    is_command_blocked,
    safe_maya_command,
)


class TestSafety(unittest.TestCase):
    """Test cases for safety module."""

    def test_blocked_commands(self):
        """Test that blocked commands are identified."""
        self.assertTrue(is_command_blocked('scriptNode'))
        self.assertTrue(is_command_blocked('eval'))
        self.assertTrue(is_command_blocked('python'))
        self.assertTrue(is_command_blocked('mel'))
        self.assertTrue(is_command_blocked('scriptJob'))

    def test_allowed_commands(self):
        """Test that safe commands are allowed."""
        self.assertFalse(is_command_blocked('polyCube'))
        self.assertFalse(is_command_blocked('createNode'))
        self.assertFalse(is_command_blocked('ls'))
        self.assertFalse(is_command_blocked('getAttr'))

    def test_safe_maya_command_blocked(self):
        """Test that safe_maya_command raises ValueError for blocked commands."""
        with self.assertRaises(ValueError) as context:
            safe_maya_command('scriptNode')
        
        self.assertIn('blocked', str(context.exception).lower())

    @patch('maya_mcp._safety.maya')
    def test_safe_maya_command_success(self, mock_maya):
        """Test successful command execution."""
        mock_cmds = unittest.mock.MagicMock()
        mock_cmds.polyCube.return_value = ['pCube1', 'pCubeShape1']
        mock_maya.cmds = mock_cmds
        
        result = safe_maya_command('polyCube', width=1.0)
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('result', result)

    @patch('maya_mcp._safety.maya')
    def test_safe_maya_command_nonexistent(self, mock_maya):
        """Test command that doesn't exist."""
        mock_cmds = unittest.mock.MagicMock()
        mock_cmds.__getattr__ = unittest.mock.MagicMock(side_effect=AttributeError('noSuchCommand'))
        mock_maya.cmds = mock_cmds
        
        result = safe_maya_command('noSuchCommand')
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('does not exist', result['message'])

    def test_blocked_commands_set(self):
        """Test that blocked commands set is not empty."""
        self.assertGreater(len(BLOCKED_COMMANDS), 0)
        self.assertIn('scriptNode', BLOCKED_COMMANDS)
        self.assertIn('eval', BLOCKED_COMMANDS)

    def test_callback_commands_set(self):
        """Test that callback commands set is not empty."""
        self.assertGreater(len(CALLBACK_COMMANDS), 0)
        self.assertIn('scriptJob', CALLBACK_COMMANDS)

    def test_script_execution_commands_set(self):
        """Test that script execution commands set is not empty."""
        self.assertGreater(len(SCRIPT_EXECUTION_COMMANDS), 0)
        self.assertIn('scriptNode', SCRIPT_EXECUTION_COMMANDS)
        self.assertIn('eval', SCRIPT_EXECUTION_COMMANDS)


if __name__ == '__main__':
    unittest.main()
