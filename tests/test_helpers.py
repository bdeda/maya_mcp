"""Test helpers for mocking Maya."""

import sys
from unittest.mock import MagicMock, patch
from contextlib import contextmanager


@contextmanager
def mock_maya_available():
    """Context manager to mock Maya as available."""
    mock_maya = MagicMock()
    mock_cmds = MagicMock()
    mock_maya.cmds = mock_cmds
    
    with patch.dict('sys.modules', {'maya': mock_maya, 'maya.cmds': mock_cmds}):
        with patch('maya.cmds', mock_cmds, create=True):
            yield mock_cmds


@contextmanager
def mock_maya_unavailable():
    """Context manager to mock Maya as unavailable."""
    def import_side_effect(name, *args, **kwargs):
        if name == 'maya' or name.startswith('maya.'):
            raise ImportError('No module named maya')
        return __import__(name, *args, **kwargs)
    
    with patch('builtins.__import__', side_effect=import_side_effect):
        yield
