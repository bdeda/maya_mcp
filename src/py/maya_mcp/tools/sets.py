"""Sets and partitions operations for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_set(
    objects: list[str],
    name: str | None = None
) -> dict[str, Any]:
    """Create a set containing objects.
    
    Args:
        objects: List of object names to add to the set.
        name: Optional name for the set.
    
    Returns:
        Dictionary with 'status', 'set' (set name), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    if not objects:
        return {
            'status': 'error',
            'message': 'No objects provided',
        }
    
    try:
        # Filter to only existing objects
        existing = [obj for obj in objects if cmds.objExists(obj)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {objects}',
            }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        set_name = cmds.sets(existing, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Created set with {len(existing)} object(s)',
            'set': set_name,
            'objects': existing,
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
def create_partition(
    name: str | None = None
) -> dict[str, Any]:
    """Create a partition.
    
    Args:
        name: Optional name for the partition.
    
    Returns:
        Dictionary with 'status', 'partition' (partition name), and 'message'.
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
        if name:
            kwargs['name'] = name
        
        partition_name = cmds.partition(**kwargs)
        
        return {
            'status': 'success',
            'message': f'Created partition: {partition_name}',
            'partition': partition_name,
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
def add_to_set(
    set_name: str,
    objects: list[str]
) -> dict[str, Any]:
    """Add objects to an existing set.
    
    Args:
        set_name: Name of the set.
        objects: List of object names to add to the set.
    
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
    
    if not objects:
        return {
            'status': 'error',
            'message': 'No objects provided',
        }
    
    try:
        if not cmds.objExists(set_name):
            return {
                'status': 'error',
                'message': f'Set "{set_name}" does not exist',
            }
        
        # Filter to only existing objects
        existing = [obj for obj in objects if cmds.objExists(obj)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {objects}',
            }
        
        cmds.sets(existing, add=set_name)
        
        return {
            'status': 'success',
            'message': f'Added {len(existing)} object(s) to set {set_name}',
            'set': set_name,
            'objects': existing,
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
def remove_from_set(
    set_name: str,
    objects: list[str]
) -> dict[str, Any]:
    """Remove objects from an existing set.
    
    Args:
        set_name: Name of the set.
        objects: List of object names to remove from the set.
    
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
    
    if not objects:
        return {
            'status': 'error',
            'message': 'No objects provided',
        }
    
    try:
        if not cmds.objExists(set_name):
            return {
                'status': 'error',
                'message': f'Set "{set_name}" does not exist',
            }
        
        # Filter to only existing objects
        existing = [obj for obj in objects if cmds.objExists(obj)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {objects}',
            }
        
        cmds.sets(existing, remove=set_name)
        
        return {
            'status': 'success',
            'message': f'Removed {len(existing)} object(s) from set {set_name}',
            'set': set_name,
            'objects': existing,
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
def list_sets() -> dict[str, Any]:
    """List all sets in the scene.
    
    Returns:
        Dictionary with 'status', 'sets' (list), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'sets': [],
        }
    
    try:
        sets = cmds.ls(type='objectSet') or []
        # Filter out default sets
        user_sets = [s for s in sets if s not in ['defaultObjectSet']]
        
        return {
            'status': 'success',
            'message': f'Found {len(user_sets)} set(s)',
            'sets': user_sets,
            'count': len(user_sets),
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'sets': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'sets': [],
        }


@mcp.tool
def get_set_members(set_name: str) -> dict[str, Any]:
    """Get the members of a set.
    
    Args:
        set_name: Name of the set.
    
    Returns:
        Dictionary with 'status', 'members' (list), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'members': [],
        }
    
    try:
        if not cmds.objExists(set_name):
            return {
                'status': 'error',
                'message': f'Set "{set_name}" does not exist',
                'members': [],
            }
        
        members = cmds.sets(set_name, query=True) or []
        
        return {
            'status': 'success',
            'message': f'Set {set_name} contains {len(members)} member(s)',
            'set': set_name,
            'members': members,
            'count': len(members),
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'members': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'members': [],
        }


__all__ = [
    'create_set',
    'create_partition',
    'add_to_set',
    'remove_from_set',
    'list_sets',
    'get_set_members',
]
