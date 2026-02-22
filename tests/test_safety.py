"""Tests for safety module."""

import unittest
from unittest.mock import patch, MagicMock

from tests.test_helpers import mock_maya_available
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
        # Test exact matches (case-insensitive)
        self.assertTrue(is_command_blocked('scriptNode'))
        self.assertTrue(is_command_blocked('scriptnode'))
        self.assertTrue(is_command_blocked('eval'))
        self.assertTrue(is_command_blocked('python'))
        self.assertTrue(is_command_blocked('mel'))
        self.assertTrue(is_command_blocked('scriptJob'))
        self.assertTrue(is_command_blocked('scriptjob'))
        # Test with different case - these should work because command_lower is used
        self.assertTrue(is_command_blocked('EVAL'))
        self.assertTrue(is_command_blocked('Python'))
        self.assertTrue(is_command_blocked('PYTHON'))

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

    def test_safe_maya_command_success(self):
        """Test successful command execution."""
        with mock_maya_available() as mock_cmds:
            # Create a mock that has polyCube attribute
            mock_cmds.polyCube = MagicMock(return_value=['pCube1', 'pCubeShape1'])
            
            # Patch hasattr to return True for polyCube
            original_hasattr = hasattr
            def mock_hasattr(obj, name):
                if name == 'polyCube':
                    return True
                return original_hasattr(obj, name)
            
            with patch('builtins.hasattr', side_effect=mock_hasattr):
                result = safe_maya_command('polyCube', width=1.0)
                
                self.assertEqual(result['status'], 'success')
                self.assertIn('result', result)

    def test_safe_maya_command_nonexistent(self):
        """Test command that doesn't exist."""
        with mock_maya_available() as mock_cmds:
            # Patch hasattr to return False for noSuchCommand
            original_hasattr = hasattr
            def mock_hasattr(obj, name):
                if name == 'noSuchCommand':
                    return False
                return original_hasattr(obj, name)
            
            with patch('builtins.hasattr', side_effect=mock_hasattr):
                result = safe_maya_command('noSuchCommand')
                
                self.assertEqual(result['status'], 'error')
                self.assertIn('does not exist', result['message'])

    def test_blocked_commands_set(self):
        """Test that blocked commands set is not empty."""
        self.assertGreater(len(BLOCKED_COMMANDS), 0)
        self.assertIn('scriptnode', BLOCKED_COMMANDS)
        self.assertIn('eval', BLOCKED_COMMANDS)

    def test_callback_commands_set(self):
        """Test that callback commands set is not empty."""
        self.assertGreater(len(CALLBACK_COMMANDS), 0)
        self.assertIn('scriptjob', CALLBACK_COMMANDS)

    def test_script_execution_commands_set(self):
        """Test that script execution commands set is not empty."""
        self.assertGreater(len(SCRIPT_EXECUTION_COMMANDS), 0)
        self.assertIn('scriptnode', SCRIPT_EXECUTION_COMMANDS)
        self.assertIn('eval', SCRIPT_EXECUTION_COMMANDS)


if __name__ == '__main__':
    unittest.main()
