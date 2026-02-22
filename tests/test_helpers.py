"""Test helpers for mocking Maya."""

import sys
from unittest.mock import MagicMock, patch
from contextlib import contextmanager


@contextmanager
def mock_maya_available():
    """Context manager to mock Maya as available."""
    mock_cmds = MagicMock()
    
    # Create mock maya module
    mock_maya = MagicMock()
    mock_maya.cmds = mock_cmds
    
    # Patch sys.modules to include maya and maya.cmds
    original_modules = {}
    modules_to_add = {
        'maya': mock_maya,
        'maya.cmds': mock_cmds,
    }
    
    for module_name, module_obj in modules_to_add.items():
        if module_name in sys.modules:
            original_modules[module_name] = sys.modules[module_name]
        sys.modules[module_name] = module_obj
    
    try:
        # Also patch maya.cmds directly for imports inside functions
        with patch('maya.cmds', mock_cmds, create=True):
            yield mock_cmds
    finally:
        # Restore original modules
        for module_name in modules_to_add:
            if module_name in original_modules:
                sys.modules[module_name] = original_modules[module_name]
            elif module_name in sys.modules:
                del sys.modules[module_name]


@contextmanager
def mock_maya_unavailable():
    """Context manager to mock Maya as unavailable."""
    original_import = __import__
    
    def import_side_effect(name, globals=None, locals=None, fromlist=(), level=0):
        # Handle 'maya.cmds' import
        if name == 'maya' or (fromlist and 'maya' in fromlist):
            raise ImportError('No module named maya')
        # Handle 'maya.cmds' as a single string
        if name.startswith('maya'):
            raise ImportError('No module named maya')
        return original_import(name, globals, locals, fromlist, level)
    
    # Remove maya from sys.modules if it exists
    maya_backup = {}
    for key in list(sys.modules.keys()):
        if key.startswith('maya'):
            maya_backup[key] = sys.modules.pop(key)
    
    try:
        with patch('builtins.__import__', side_effect=import_side_effect):
            yield
    finally:
        # Restore maya modules
        sys.modules.update(maya_backup)
