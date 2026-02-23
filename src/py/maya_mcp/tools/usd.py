"""USD and UFE (Universal Scene Description Framework for Editing) tools for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_usd_proxy_shape(
    usd_file_path: str,
    name: str | None = None,
    parent: str | None = None
) -> dict[str, Any]:
    """Create a USD proxy shape that references a USD file.
    
    Args:
        usd_file_path: Path to the USD file to reference.
        name: Optional name for the proxy shape node.
        parent: Optional parent transform node name.
    
    Returns:
        Dictionary with 'status', 'proxy_shape' (node name), 'transform' (transform node name), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        # Check if mayaUsd plugin is loaded
        if not cmds.pluginInfo('mayaUsdPlugin', query=True, loaded=True):
            try:
                cmds.loadPlugin('mayaUsdPlugin')
            except RuntimeError:
                return {
                    'status': 'error',
                    'message': 'mayaUsdPlugin is not available. Please install Maya USD plugin.',
                }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        # Create transform node if parent is specified, otherwise create a new one
        if parent:
            if not cmds.objExists(parent):
                return {
                    'status': 'error',
                    'message': f'Parent transform "{parent}" does not exist',
                }
            transform = parent
        else:
            transform_name = name.replace('Shape', '') if name and name.endswith('Shape') else (name or 'usdProxyShape')
            transform = cmds.createNode('transform', name=transform_name)
        
        # Create USD proxy shape
        proxy_shape = cmds.createNode('mayaUsdProxyShape', parent=transform, **kwargs)
        
        # Set the USD file path
        cmds.setAttr(f'{proxy_shape}.filePath', usd_file_path, type='string')
        
        return {
            'status': 'success',
            'message': f'Created USD proxy shape referencing {usd_file_path}',
            'proxy_shape': proxy_shape,
            'transform': transform,
            'usd_file_path': usd_file_path,
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
def get_usd_proxy_shape_info(
    proxy_shape: str
) -> dict[str, Any]:
    """Get information about a USD proxy shape.
    
    Args:
        proxy_shape: Name of the USD proxy shape node.
    
    Returns:
        Dictionary with 'status', 'usd_file_path', 'stage_path', and other information.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(proxy_shape):
            return {
                'status': 'error',
                'message': f'USD proxy shape "{proxy_shape}" does not exist',
            }
        
        node_type = cmds.nodeType(proxy_shape)
        if node_type != 'mayaUsdProxyShape':
            return {
                'status': 'error',
                'message': f'Object "{proxy_shape}" is not a USD proxy shape',
            }
        
        # Get USD file path
        usd_file_path = cmds.getAttr(f'{proxy_shape}.filePath')
        
        # Get stage path (root prim path)
        stage_path = cmds.getAttr(f'{proxy_shape}.primPath') if cmds.attributeQuery('primPath', node=proxy_shape, exists=True) else '/'
        
        return {
            'status': 'success',
            'message': f'Retrieved information for USD proxy shape: {proxy_shape}',
            'proxy_shape': proxy_shape,
            'usd_file_path': usd_file_path,
            'stage_path': stage_path,
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
def list_usd_proxy_shapes() -> dict[str, Any]:
    """List all USD proxy shapes in the scene.
    
    Returns:
        Dictionary with 'status', 'proxy_shapes' (list), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'proxy_shapes': [],
        }
    
    try:
        # Check if mayaUsd plugin is loaded
        if not cmds.pluginInfo('mayaUsdPlugin', query=True, loaded=True):
            return {
                'status': 'success',
                'message': 'mayaUsdPlugin is not loaded',
                'proxy_shapes': [],
                'count': 0,
            }
        
        proxy_shapes = cmds.ls(type='mayaUsdProxyShape') or []
        
        return {
            'status': 'success',
            'message': f'Found {len(proxy_shapes)} USD proxy shape(s)',
            'proxy_shapes': proxy_shapes,
            'count': len(proxy_shapes),
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'proxy_shapes': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'proxy_shapes': [],
        }


@mcp.tool
def edit_usd_as_maya(
    proxy_shape: str,
    prim_path: str = '/',
    edit_as_maya: bool = True
) -> dict[str, Any]:
    """Edit USD prims as Maya objects (push/pull USD data).
    
    Args:
        proxy_shape: Name of the USD proxy shape node.
        prim_path: USD prim path to edit (default: '/' for root).
        edit_as_maya: If True, pull USD data into Maya. If False, push Maya edits back to USD.
    
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
        # Check if mayaUsd plugin is loaded
        if not cmds.pluginInfo('mayaUsdPlugin', query=True, loaded=True):
            return {
                'status': 'error',
                'message': 'mayaUsdPlugin is not available. Please install Maya USD plugin.',
            }
        
        if not cmds.objExists(proxy_shape):
            return {
                'status': 'error',
                'message': f'USD proxy shape "{proxy_shape}" does not exist',
            }
        
        # Use mayaUsd commands to edit as Maya
        if edit_as_maya:
            # Pull USD data into Maya
            try:
                # Import mayaUsd commands
                from mayaUsd import lib as mayaUsdLib
                stage = mayaUsdLib.GetStage(proxy_shape)
                if stage:
                    # Use UFE to pull USD data
                    import ufe
                    # Get the UFE scene item for the prim
                    ufe_scene_item = mayaUsdLib.ufe.getSceneItem(proxy_shape, prim_path)
                    if ufe_scene_item:
                        # Pull USD data into Maya
                        mayaUsdLib.PrimUpdaterManager.readPullInformation(ufe_scene_item)
                        return {
                            'status': 'success',
                            'message': f'Pulled USD data from {prim_path} into Maya',
                            'proxy_shape': proxy_shape,
                            'prim_path': prim_path,
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Could not find USD prim at path: {prim_path}',
                        }
                else:
                    return {
                        'status': 'error',
                        'message': f'Could not get USD stage from proxy shape: {proxy_shape}',
                    }
            except ImportError:
                # Fallback to basic mayaUsd commands if UFE is not available
                return {
                    'status': 'error',
                    'message': 'UFE API is not available. Please ensure Maya USD plugin with UFE support is installed.',
                }
        else:
            # Push Maya edits back to USD
            try:
                from mayaUsd import lib as mayaUsdLib
                stage = mayaUsdLib.GetStage(proxy_shape)
                if stage:
                    import ufe
                    ufe_scene_item = mayaUsdLib.ufe.getSceneItem(proxy_shape, prim_path)
                    if ufe_scene_item:
                        # Push Maya edits back to USD
                        mayaUsdLib.PrimUpdaterManager.readPushInformation(ufe_scene_item)
                        return {
                            'status': 'success',
                            'message': f'Pushed Maya edits back to USD at {prim_path}',
                            'proxy_shape': proxy_shape,
                            'prim_path': prim_path,
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Could not find USD prim at path: {prim_path}',
                        }
                else:
                    return {
                        'status': 'error',
                        'message': f'Could not get USD stage from proxy shape: {proxy_shape}',
                    }
            except ImportError:
                return {
                    'status': 'error',
                    'message': 'UFE API is not available. Please ensure Maya USD plugin with UFE support is installed.',
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
def push_maya_edits_to_usd(
    proxy_shape: str,
    prim_path: str = '/',
    save_usd_file: bool = False
) -> dict[str, Any]:
    """Push Maya edits back to the USD file.
    
    Args:
        proxy_shape: Name of the USD proxy shape node.
        prim_path: USD prim path to push edits for (default: '/' for root).
        save_usd_file: If True, save the USD file after pushing edits.
    
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
        # Check if mayaUsd plugin is loaded
        if not cmds.pluginInfo('mayaUsdPlugin', query=True, loaded=True):
            return {
                'status': 'error',
                'message': 'mayaUsdPlugin is not available. Please install Maya USD plugin.',
            }
        
        if not cmds.objExists(proxy_shape):
            return {
                'status': 'error',
                'message': f'USD proxy shape "{proxy_shape}" does not exist',
            }
        
        # Push edits back to USD (same logic as edit_usd_as_maya with edit_as_maya=False)
        try:
            from mayaUsd import lib as mayaUsdLib
            stage = mayaUsdLib.GetStage(proxy_shape)
            if stage:
                import ufe
                ufe_scene_item = mayaUsdLib.ufe.getSceneItem(proxy_shape, prim_path)
                if ufe_scene_item:
                    # Push Maya edits back to USD
                    mayaUsdLib.PrimUpdaterManager.readPushInformation(ufe_scene_item)
                    result = {
                        'status': 'success',
                        'message': f'Pushed Maya edits back to USD at {prim_path}',
                        'proxy_shape': proxy_shape,
                        'prim_path': prim_path,
                    }
                else:
                    result = {
                        'status': 'error',
                        'message': f'Could not find USD prim at path: {prim_path}',
                    }
            else:
                result = {
                    'status': 'error',
                    'message': f'Could not get USD stage from proxy shape: {proxy_shape}',
                }
        except ImportError:
            result = {
                'status': 'error',
                'message': 'UFE API is not available. Please ensure Maya USD plugin with UFE support is installed.',
            }
        
        if result['status'] == 'success' and save_usd_file:
            # Get USD file path and save
            usd_file_path = cmds.getAttr(f'{proxy_shape}.filePath')
            if usd_file_path:
                try:
                    from mayaUsd import lib as mayaUsdLib
                    stage = mayaUsdLib.GetStage(proxy_shape)
                    if stage:
                        stage.GetRootLayer().Save()
                        result['message'] += f' and saved to {usd_file_path}'
                except ImportError:
                    result['message'] += ' (could not save USD file - mayaUsd lib not available)'
        
        return result
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
def get_usd_prim_info(
    proxy_shape: str,
    prim_path: str
) -> dict[str, Any]:
    """Get information about a USD prim.
    
    Args:
        proxy_shape: Name of the USD proxy shape node.
        prim_path: USD prim path.
    
    Returns:
        Dictionary with 'status', 'prim_path', 'prim_type', and other information.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        # Check if mayaUsd plugin is loaded
        if not cmds.pluginInfo('mayaUsdPlugin', query=True, loaded=True):
            return {
                'status': 'error',
                'message': 'mayaUsdPlugin is not available. Please install Maya USD plugin.',
            }
        
        if not cmds.objExists(proxy_shape):
            return {
                'status': 'error',
                'message': f'USD proxy shape "{proxy_shape}" does not exist',
            }
        
        try:
            from mayaUsd import lib as mayaUsdLib
            stage = mayaUsdLib.GetStage(proxy_shape)
            if stage:
                prim = stage.GetPrimAtPath(prim_path)
                if prim:
                    return {
                        'status': 'success',
                        'message': f'Retrieved information for USD prim: {prim_path}',
                        'prim_path': prim_path,
                        'prim_type': prim.GetTypeName() if prim.IsValid() else None,
                        'is_valid': prim.IsValid(),
                        'is_active': prim.IsActive() if prim.IsValid() else None,
                        'is_loaded': prim.IsLoaded() if prim.IsValid() else None,
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f'USD prim not found at path: {prim_path}',
                    }
            else:
                return {
                    'status': 'error',
                    'message': f'Could not get USD stage from proxy shape: {proxy_shape}',
                }
        except ImportError:
            return {
                'status': 'error',
                'message': 'mayaUsd lib is not available. Please ensure Maya USD plugin is installed.',
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
    'create_usd_proxy_shape',
    'get_usd_proxy_shape_info',
    'list_usd_proxy_shapes',
    'edit_usd_as_maya',
    'push_maya_edits_to_usd',
    'get_usd_prim_info',
]
