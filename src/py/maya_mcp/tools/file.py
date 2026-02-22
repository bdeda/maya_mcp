"""File operations for Maya - open, save, import, export (safe operations only)."""

from typing import TYPE_CHECKING, Any
from pathlib import Path

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def open_scene(file_path: str, force: bool = False) -> dict[str, Any]:
    """Open a Maya scene file.
    
    Args:
        file_path: Path to the Maya file (.ma or .mb).
        force: If True, force open without prompting to save.
    
    Returns:
        Dictionary with 'status' and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        path = Path(file_path)
        if not path.exists():
            return {
                'status': 'error',
                'message': f'File does not exist: {file_path}',
            }
        
        kwargs = {}
        if force:
            kwargs['force'] = True
        
        cmds.file(file_path, open=True, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Opened scene: {file_path}',
            'file_path': file_path,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
        }


@mcp.tool
def save_scene(file_path: str | None = None, force: bool = False) -> dict[str, Any]:
    """Save the current Maya scene.
    
    Args:
        file_path: Optional path to save the file. If None, save to current file.
        force: If True, force save even if file exists.
    
    Returns:
        Dictionary with 'status' and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {}
        if force:
            kwargs['force'] = True
        
        if file_path:
            cmds.file(rename=file_path)
            cmds.file(save=True, **kwargs)
        else:
            cmds.file(save=True, **kwargs)
        
        saved_path = file_path or cmds.file(query=True, sceneName=True)
        
        return {
            'status': 'success',
            'message': f'Saved scene: {saved_path}',
            'file_path': saved_path,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
        }


@mcp.tool
def import_file(file_path: str, namespace: str | None = None) -> dict[str, Any]:
    """Import a file into the current scene.
    
    Args:
        file_path: Path to the file to import.
        namespace: Optional namespace for imported objects.
    
    Returns:
        Dictionary with 'status', 'imported_objects', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'imported_objects': [],
        }
    
    try:
        path = Path(file_path)
        if not path.exists():
            return {
                'status': 'error',
                'message': f'File does not exist: {file_path}',
                'imported_objects': [],
            }
        
        kwargs = {}
        if namespace:
            kwargs['namespace'] = namespace
        
        # Get objects before import
        objects_before = set(cmds.ls())
        
        cmds.file(file_path, i=True, **kwargs)
        
        # Get objects after import
        objects_after = set(cmds.ls())
        imported = list(objects_after - objects_before)
        
        return {
            'status': 'success',
            'message': f'Imported {len(imported)} object(s) from {file_path}',
            'imported_objects': imported,
            'file_path': file_path,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'imported_objects': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'imported_objects': [],
        }


@mcp.tool
def export_selection(file_path: str, file_type: str | None = None) -> dict[str, Any]:
    """Export selected objects to a file.
    
    Args:
        file_path: Path to save the exported file.
        file_type: Optional file type (e.g., 'mayaAscii', 'mayaBinary', 'obj').
    
    Returns:
        Dictionary with 'status' and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        selection = cmds.ls(selection=True)
        if not selection:
            return {
                'status': 'error',
                'message': 'No objects selected',
            }
        
        kwargs = {'exportSelected': True}
        if file_type:
            kwargs['type'] = file_type
        
        cmds.file(file_path, exportSelected=True, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Exported {len(selection)} object(s) to {file_path}',
            'file_path': file_path,
            'exported_objects': selection,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
        }


@mcp.tool
def new_scene(force: bool = False) -> dict[str, Any]:
    """Create a new scene.
    
    Args:
        force: If True, force new scene without prompting to save.
    
    Returns:
        Dictionary with 'status' and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {}
        if force:
            kwargs['force'] = True
        
        cmds.file(new=True, **kwargs)
        
        return {
            'status': 'success',
            'message': 'Created new scene',
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
        }


__all__ = [
    'open_scene',
    'save_scene',
    'import_file',
    'export_selection',
    'new_scene',
]
