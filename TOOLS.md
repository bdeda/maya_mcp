# Maya MCP Tools Reference

This document lists all available MCP tools for interacting with Maya. Tools are organized by category.

## Safety Features

The MCP server includes safety filters that prevent:
- **Script execution**: `scriptNode`, `eval`, `python`, `mel`, `source` commands are blocked
- **Callback creation**: Commands that create callbacks are blocked
- **Arbitrary code execution**: All dangerous commands are filtered

## Tool Categories

### Server Status (`server.py`)

- `get_server_status()` - Get the status of the Maya MCP server and Maya availability

### Scene Operations (`scene.py`)

- `get_selection()` - Get currently selected objects
- `select_objects(names)` - Select objects by name
- `clear_selection()` - Clear the current selection

### Query Operations (`query.py`)

- `list_objects(type_filter, long_names, selection)` - List objects in the scene
- `object_exists(name)` - Check if an object exists
- `get_object_type(name)` - Get the type of an object
- `get_attribute_value(object_name, attribute, time)` - Get attribute value
- `list_attributes(object_name, keyable, readable, writable, multi, scalar, numeric)` - List object attributes
- `get_connection_info(attribute, source, destination)` - Get attribute connections

### Object Creation (`objects.py`)

- `create_polygon_cube(name, width, height, depth, subdivisions_x, subdivisions_y, subdivisions_z)` - Create a polygonal cube
- `create_polygon_sphere(name, radius, subdivisions_x, subdivisions_y)` - Create a polygonal sphere
- `create_polygon_plane(name, width, height, subdivisions_x, subdivisions_y)` - Create a polygonal plane
- `create_polygon_cylinder(name, radius, height, subdivisions_x, subdivisions_y, subdivisions_z)` - Create a polygonal cylinder
- `create_transform(name, parent)` - Create an empty transform node
- `delete_objects(names)` - Delete objects from the scene
- `duplicate_objects(names, name, instance, smart_transform)` - Duplicate objects

### Attribute Operations (`attributes.py`)

- `set_attribute(attribute, value, type)` - Set attribute value
- `add_attribute(object_name, attribute_name, attribute_type, default_value, min_value, max_value, keyable)` - Add dynamic attribute
- `connect_attributes(source, destination, force)` - Connect two attributes
- `disconnect_attributes(source, destination)` - Disconnect attributes

### Transform Operations (`transform.py`)

- `move_object(object_name, x, y, z, relative, world_space)` - Move an object
- `rotate_object(object_name, x, y, z, relative, world_space)` - Rotate an object
- `scale_object(object_name, x, y, z, relative)` - Scale an object
- `parent_objects(child_objects, parent_object, world)` - Parent objects together

### Mesh Operations (`mesh.py`) - Optimized with OpenMaya API

- `get_mesh_vertices(mesh_name, world_space)` - Get vertex positions (uses OpenMaya)
- `get_mesh_face_count(mesh_name)` - Get face count (uses OpenMaya)
- `get_mesh_edge_count(mesh_name)` - Get edge count (uses OpenMaya)
- `combine_meshes(mesh_names, name, merge_vertices)` - Combine multiple meshes

### Rigging Operations (`rigging.py`)

- `create_joint(name, position, parent)` - Create a joint
- `create_ik_handle(start_joint, end_joint, name, solver)` - Create an IK handle
- `create_parent_constraint(target, constrained, maintain_offset, name)` - Create a parent constraint
- `create_point_constraint(target, constrained, maintain_offset, name)` - Create a point constraint
- `create_orient_constraint(target, constrained, maintain_offset, name)` - Create an orient constraint

### Skinning Operations (`skinning.py`)

- `bind_skin(mesh, joints, name, bind_method, skin_method)` - Bind a mesh to joints (create skin cluster)
- `get_skin_cluster(mesh)` - Get the skin cluster for a mesh
- `get_skin_cluster_joints(skin_cluster)` - Get joints associated with a skin cluster

### Animation Operations (`animation.py`)

- `set_keyframe(attributes, time, value)` - Set keyframes on attributes
- `get_keyframe_times(attribute, time_range)` - Get keyframe times for an attribute
- `set_current_time(time)` - Set the current time in the timeline
- `get_current_time()` - Get the current time in the timeline
- `delete_keyframes(attributes, time_range)` - Delete keyframes from attributes

### File Operations (`file.py`) - Safe operations only

- `open_scene(file_path, force)` - Open a Maya scene file
- `save_scene(file_path, force)` - Save the current scene
- `import_file(file_path, namespace)` - Import a file into the current scene
- `export_selection(file_path, file_type)` - Export selected objects
- `new_scene(force)` - Create a new scene

### Display Operations (`display.py`)

- `set_display_mode(objects, mode)` - Set display mode (wireframe, shaded, boundingBox, points)
- `set_visibility(objects, visible)` - Set object visibility
- `refresh_viewport()` - Refresh all viewports

### Display Layers (`display_layers.py`)

- `create_display_layer(name, objects, visible, display_type)` - Create a display layer
- `add_to_display_layer(layer_name, objects)` - Add objects to a display layer
- `set_display_layer_visibility(layer_name, visible)` - Set display layer visibility
- `get_display_layer_objects(layer_name)` - Get objects in a display layer
- `list_display_layers()` - List all display layers

### Animation Layers (`animation_layers.py`)

- `create_animation_layer(name, weight, solo, mute)` - Create an animation layer
- `add_to_animation_layer(layer_name, attributes)` - Add attributes to an animation layer
- `set_animation_layer_weight(layer_name, weight)` - Set animation layer weight
- `list_animation_layers()` - List all animation layers

### Lights (`lights.py`)

- `create_directional_light(name, intensity, color)` - Create a directional light
- `create_point_light(name, intensity, color)` - Create a point light
- `create_spot_light(name, intensity, color, cone_angle, penumbra_angle)` - Create a spot light
- `create_area_light(name, intensity, color)` - Create an area light
- `set_light_intensity(light_name, intensity)` - Set light intensity
- `list_lights()` - List all lights in the scene

### UV Editing (`uv.py`)

- `get_uv_coordinates(mesh_name, uv_set)` - Get UV coordinates for a mesh
- `set_uv_coordinates(mesh_name, uv_indices, u_values, v_values, uv_set)` - Set UV coordinates
- `create_uv_snapshot(mesh_name, file_path, resolution, uv_set)` - Create a UV snapshot image
- `layout_uvs(mesh_name, method, scale, rotate)` - Layout UVs for a mesh

### Materials (`materials.py`)

- `create_lambert_material(name, color)` - Create a Lambert material
- `create_phong_material(name, color, specular_color, cosine_power)` - Create a Phong material
- `create_blinn_material(name, color, specular_color, eccentricity)` - Create a Blinn material
- `assign_material(material_name, objects)` - Assign a material to objects
- `get_assigned_material(object_name)` - Get the material assigned to an object
- `list_materials()` - List all materials in the scene

### Rendering (`rendering.py`)

- `create_playblast(file_path, start_frame, end_frame, width, height, format, quality, compression)` - Create a playblast
- `render_software(file_path, start_frame, end_frame, width, height, camera, renderer)` - Render using Maya Software Renderer
- `render_current_frame(file_path, width, height, camera, renderer)` - Render the current frame
- `set_render_resolution(width, height)` - Set the render resolution

## Performance Optimizations

The following operations use the OpenMaya API for better performance:
- `get_mesh_vertices()` - Uses `maya.api.OpenMaya.MFnMesh` for fast vertex queries
- `get_mesh_face_count()` - Uses OpenMaya API
- `get_mesh_edge_count()` - Uses OpenMaya API

## Usage Examples

### Create and manipulate objects
```python
# Create a cube
create_polygon_cube(name="myCube", width=2.0, height=2.0, depth=2.0)

# Move it
move_object("myCube", x=5.0, y=0.0, z=0.0)

# Set an attribute
set_attribute("myCube.translateX", 10.0)
```

### Rigging workflow
```python
# Create joints
create_joint(name="root", position=(0, 0, 0))
create_joint(name="spine", position=(0, 5, 0), parent="root")

# Create IK handle
create_ik_handle("root", "spine", name="ikHandle1")
```

### Animation workflow
```python
# Set current time
set_current_time(1.0)

# Set keyframe
set_keyframe(["pCube1.translateX"], time=1.0, value=0.0)

# Move to frame 10
set_current_time(10.0)
set_keyframe(["pCube1.translateX"], time=10.0, value=10.0)
```

## Blocked Commands

The following commands are **NOT** available for security reasons:
- `scriptNode` - Creates script nodes that execute code
- `eval` / `evalDeferred` - Executes arbitrary code
- `python` / `mel` - Executes Python/MEL code
- `source` - Sources script files
- `scriptJob` / `callbacks` - Creates callbacks
- Any command that could execute arbitrary code

## Error Handling

All tools return a consistent response format:
```python
{
    'status': 'success' | 'error',
    'message': 'Human-readable message',
    # ... additional result data
}
```

Tools handle errors gracefully and provide informative error messages.
