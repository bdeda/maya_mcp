# Missing Maya.cmds API Functionality

This document outlines Maya.cmds API functionality that is **not currently covered** by the Maya MCP server. This serves as a roadmap for future enhancements.

## Currently Covered (140+ tools)

✅ **Basic Operations**: Selection, queries, object creation, deletion, duplication  
✅ **Polygon Primitives**: Cube, sphere, plane, cylinder  
✅ **Transforms**: Move, rotate, scale, parent  
✅ **Attributes**: Get/set, add, connect/disconnect  
✅ **Basic Mesh Operations**: Vertex/face/edge queries, combine  
✅ **Mesh Editing**: Extrude faces/edges, bevel, smooth, boolean operations (union/difference/intersection), merge vertices, split faces, collapse edges, triangulate, separate mesh, polygon normals, quadrangulate, reduce, remesh, flip UVs, normalize UVs, planar projection, UV projection, smooth faces, soften edges, transfer attributes  
✅ **Rigging**: Joints, IK handles, basic constraints (parent, point, orient)  
✅ **Skinning**: Bind skin, get skin cluster info  
✅ **Paint Tools**: Get/set skin weights  
✅ **Animation**: Keyframes, time control, animation layers, bake results, bake simulation, copy/paste keyframes, scale/snap/select keyframes, query keyframe info  
✅ **Display Layers**: Create, manage, visibility  
✅ **Lights**: Directional, point, spot, area  
✅ **UV Editing**: Get/set UVs, layout, snapshots  
✅ **Materials**: Lambert, Phong, Blinn, surface shader, use background, layered shader, ramp shader, generic shading node creation, file texture, ramp texture, place2dTexture  
✅ **Rendering**: Playblast, software rendering  
✅ **File Operations**: Open, save, import, export  
✅ **Cameras**: Create cameras (perspective/orthographic), set focal length, look through camera, list cameras, view fit, view selected  
✅ **NURBS**: Circle, sphere, cylinder primitives, curves from points, loft, revolve, attach curves, close curve, planar surface  
✅ **Constraints**: Aim, scale, geometry, normal, tangent, pole vector constraints, remove constraints  
✅ **Deformers**: Blend shape, cluster, lattice, non-linear (bend, twist, sine, squash), sculpt, wire, wrinkle, jiggle, softMod, tension, deltaMush, shrinkWrap, wrap, list deformers  
✅ **Sets and Partitions**: Create sets/partitions, add/remove from sets, list sets, get set members  

## Missing Functionality by Category

### 1. Polygon Mesh Operations (Extensive)

**Missing polygon modeling commands:**
- ✅ `polyExtrudeFace` - Extrude faces (IMPLEMENTED)
- ✅ `polyExtrudeEdge` - Extrude edges (IMPLEMENTED)
- `polyExtrudeVertex` - Extrude vertices
- ✅ `polyBevel` - Bevel edges/faces (IMPLEMENTED)
- `polyBridgeEdge` - Bridge edges between meshes
- `polyChamferVertex` - Chamfer vertices
- ✅ `polyCollapseEdge` - Collapse edges (IMPLEMENTED)
- `polyCollapseFace` - Collapse faces
- `polyCut` - Cut faces
- `polyMergeEdge` - Merge edges
- ✅ `polyMergeVertex` - Merge vertices (IMPLEMENTED)
- ✅ `polyNormal` - Normal operations (IMPLEMENTED)
- ✅ `polySmooth` - Smooth mesh (IMPLEMENTED)
- `polySubdivideFace` - Subdivide faces
- ✅ `polyTriangulate` - Triangulate mesh (IMPLEMENTED)
- ✅ `polyQuadrangulate` - Convert to quads (IMPLEMENTED)
- ✅ `polyReduce` - Reduce polygon count (IMPLEMENTED)
- ✅ `polyRemesh` - Remesh operations (IMPLEMENTED)
- `polyCrease` - Crease edges/vertices
- `polySewEdge` - Sew edges together
- ✅ `polySplit` - Split faces (IMPLEMENTED)
- `polySubdEdge` - Subdivide edges
- `polySubdFace` - Subdivide faces
- `polyAppend` - Append to mesh
- `polyAppendVertex` - Append vertices
- `polyCloseBorder` - Close border edges
- `polyDelEdge` - Delete edges
- `polyDelFace` - Delete faces
- `polyDelVertex` - Delete vertices
- `polyDuplicateEdge` - Duplicate edges
- `polyFlipEdge` - Flip edges
- ✅ `polyFlipUV` - Flip UVs (IMPLEMENTED)
- `polyMoveEdge` - Move edges
- `polyMoveFace` - Move faces
- `polyMoveVertex` - Move vertices
- ✅ `polyNormalizeUV` - Normalize UVs (IMPLEMENTED)
- ✅ `polyPlanarProjection` - Planar UV projection (IMPLEMENTED)
- ✅ `polyProjection` - Various UV projections (IMPLEMENTED)
- ✅ `polySeparate` - Separate mesh components (IMPLEMENTED)
- ✅ `polySmoothFace` - Smooth specific faces (IMPLEMENTED)
- ✅ `polySoftEdge` - Soften edges (IMPLEMENTED)
- `polySplitVertex` - Split vertices
- `polySubdivideEdge` - Subdivide edges
- ✅ `polyTransfer` - Transfer attributes between meshes (IMPLEMENTED)
- ✅ `polyUnite` - Boolean union (IMPLEMENTED via boolean_union)
- ✅ Boolean difference/intersection (IMPLEMENTED)
- `polyWedgeFace` - Wedge faces

**Missing polygon component operations:**
- Component selection (vertices, edges, faces, UVs)
- Component editing operations
- Component queries

### 2. NURBS Operations (Partially Covered)

**NURBS primitives:**
- ✅ `nurbsCircle` - Create NURBS circle (IMPLEMENTED)
- `nurbsSquare` - Create NURBS square
- `nurbsPlane` - Create NURBS plane
- ✅ `nurbsSphere` - Create NURBS sphere (IMPLEMENTED)
- `nurbsCube` - Create NURBS cube
- ✅ `nurbsCylinder` - Create NURBS cylinder (IMPLEMENTED)
- `nurbsCone` - Create NURBS cone
- `nurbsTorus` - Create NURBS torus

**NURBS curve operations:**
- ✅ `curve` - Create curve from points (IMPLEMENTED)
- `curveOnSurface` - Create curve on surface
- `duplicateCurve` - Duplicate curve
- ✅ `attachCurve` - Attach curves (IMPLEMENTED)
- `detachCurve` - Detach curve
- `openCurve` - Open curve
- ✅ `closeCurve` - Close curve (IMPLEMENTED)
- `rebuildCurve` - Rebuild curve
- `reverseCurve` - Reverse curve direction
- `insertKnot` - Insert knot
- `extendCurve` - Extend curve
- `offsetCurve` - Offset curve
- `projectCurve` - Project curve onto surface
- `intersectCurve` - Find curve intersections

**NURBS surface operations:**
- ✅ `loft` - Loft surfaces (IMPLEMENTED)
- ✅ `revolve` - Revolve curve to surface (IMPLEMENTED)
- ✅ `planar` - Create planar surface (IMPLEMENTED)
- `boundary` - Create boundary surface
- `square` - Create square surface
- `bevel` - Bevel surface
- `extrude` - Extrude curve to surface
- `birailSrf` - Birail surface
- `duplicateSurface` - Duplicate surface
- `attachSurface` - Attach surfaces
- `detachSurface` - Detach surface
- `rebuildSurface` - Rebuild surface
- `reverseSurface` - Reverse surface direction
- `insertKnotSurface` - Insert knot in surface
- `extendSurface` - Extend surface
- `offsetSurface` - Offset surface
- `trim` - Trim surface
- `untrim` - Untrim surface
- `projectCurve` - Project curve on surface
- `intersect` - Surface intersections

**NURBS component operations:**
- CV (Control Vertex) manipulation
- Edit point operations
- Knot operations
- Isoparm operations
- Surface patch operations

### 3. Deformers (Partially Covered)

**Basic deformers:**
- ✅ `blendShape` - Blend shape deformer (IMPLEMENTED)
- ✅ `cluster` - Cluster deformer (IMPLEMENTED)
- ✅ `lattice` - Lattice deformer (IMPLEMENTED)
- ✅ `sculpt` - Sculpt deformer (IMPLEMENTED)
- ✅ `wire` - Wire deformer (IMPLEMENTED)
- ✅ `wrinkle` - Wrinkle deformer (IMPLEMENTED)
- ✅ `jiggle` - Jiggle deformer (IMPLEMENTED)
- ✅ `softMod` - Soft modification (IMPLEMENTED)
- ✅ `tension` - Tension deformer (IMPLEMENTED)
- ✅ `deltaMush` - Delta mush deformer (IMPLEMENTED)
- ✅ `shrinkWrap` - Shrink wrap deformer (IMPLEMENTED)
- ✅ `wrap` - Wrap deformer (IMPLEMENTED)
- ✅ `nonLinear` - Non-linear deformers: bend, twist, sine, squash (IMPLEMENTED)
- `nonLinear` - Non-linear deformers: flare, wave (still missing)

**Deformer queries and management:**
- ✅ List deformers on objects (IMPLEMENTED)
- Get deformer weights
- Set deformer weights
- Remove deformers

### 4. Advanced Constraints (Partially Covered)

**Missing constraint types:**
- ✅ `aimConstraint` - Aim constraint (IMPLEMENTED)
- ✅ `scaleConstraint` - Scale constraint (IMPLEMENTED)
- ✅ `geometryConstraint` - Geometry constraint (IMPLEMENTED)
- ✅ `normalConstraint` - Normal constraint (IMPLEMENTED)
- ✅ `tangentConstraint` - Tangent constraint (IMPLEMENTED)
- ✅ `poleVectorConstraint` - Pole vector constraint (IMPLEMENTED)
- `pointOnPolyConstraint` - Point on poly constraint
- `pointOnCurveConstraint` - Point on curve constraint
- `closestPointOnSurface` - Closest point constraint

**Constraint management:**
- ✅ Remove constraints (IMPLEMENTED)
- Get constraint targets
- Set constraint weights
- Enable/disable constraints

### 5. Advanced Rigging (Partially Covered)

**Missing IK operations:**
- `ikSplineSolver` - Spline IK
- `ikSpringSolver` - Spring IK
- `ik2Bsolver` - 2-bone IK solver
- IK handle management (remove, modify)

**Missing joint operations:**
- Joint orientation
- Joint limits
- Joint display
- Mirror joints
- Orient joints
- Joint labels

**Missing rigging utilities:**
- `motionPath` - Motion path animation
- `pathAnimation` - Path animation
- `character` - Character sets
- `characterMap` - Character mapping
- `humanIk` - Human IK system
- `ikHandle` - More IK handle options

### 6. Advanced Animation (Partially Covered)

**Missing animation tools:**
- `animCurveEditor` - Graph editor operations
- `dopeSheetEditor` - Dope sheet operations
- `timeEditor` - Time editor operations
- ✅ `bakeResults` - Bake animation (IMPLEMENTED)
- ✅ `bakeSimulation` - Bake simulation (IMPLEMENTED)
- ✅ `copyKey` - Copy keyframes (IMPLEMENTED)
- ✅ `pasteKey` - Paste keyframes (IMPLEMENTED)
- ✅ `scaleKey` - Scale keyframes (IMPLEMENTED)
- ✅ `snapKey` - Snap keyframes (IMPLEMENTED)
- ✅ `selectKey` - Select keyframes (IMPLEMENTED)
- ✅ `keyframe` - More keyframe operations (IMPLEMENTED)
- `findKeyframe` - Find keyframes
- `keyTangent` - Keyframe tangents
- `keyframeOutliner` - Keyframe outliner
- `animLayer` - More animation layer operations
- `blendNode` - Blend nodes
- `character` - Character sets
- `clip` - Animation clips
- `clipEditor` - Clip editor
- `poseEditor` - Pose editor
- `retarget` - Retargeting
- `timeWarp` - Time warp

**Missing animation curves:**
- `animCurve` - Animation curve operations
- `animCurveTA` - Time-angle curves
- `animCurveTL` - Time-length curves
- `animCurveTU` - Time-unitless curves
- `animCurveUA` - Unitless-angle curves
- `animCurveUL` - Unitless-length curves
- `animCurveUU` - Unitless-unitless curves

### 7. Cameras (Partially Covered)

**Camera operations:**
- ✅ `camera` - Create cameras (IMPLEMENTED)
- ✅ `lookThrough` - Look through camera (IMPLEMENTED)
- ✅ `viewFit` - Fit view (IMPLEMENTED)
- ✅ `viewSelected` - View selected (IMPLEMENTED)
- ✅ Camera attributes (focal length) (IMPLEMENTED)
- `viewPlace` - Place view
- `viewSet` - Set view
- `dolly` - Dolly camera
- `tumble` - Tumble camera
- `track` - Track camera
- `truck` - Truck camera
- `zoom` - Zoom camera
- Camera attributes (aperture, etc.)
- Stereo camera setup
- Camera sequencer

### 8. Advanced Materials and Shading (Partially Covered)

**Missing material types:**
- ✅ `surfaceShader` - Surface shader (IMPLEMENTED)
- ✅ `useBackground` - Use background (IMPLEMENTED)
- ✅ `layeredShader` - Layered shader (IMPLEMENTED)
- ✅ `rampShader` - Ramp shader (IMPLEMENTED)
- ✅ `shadingNode` - Generic shading node creation (IMPLEMENTED)
- `aiStandardSurface` - Arnold materials (if available)
- `aiStandardHair` - Arnold hair materials
- `aiVolume` - Arnold volume materials

**Missing texture operations:**
- ✅ `file` - File texture node (IMPLEMENTED)
- ✅ `place2dTexture` - 2D texture placement (IMPLEMENTED)
- ✅ `ramp` - Ramp texture (IMPLEMENTED)
- `place3dTexture` - 3D texture placement
- `projection` - Projection node
- `noise` - Noise texture
- `fractal` - Fractal texture
- `checker` - Checker texture
- `grid` - Grid texture
- `cloth` - Cloth texture
- `water` - Water texture
- `brownian` - Brownian texture
- `mountain` - Mountain texture
- `crater` - Crater texture
- `snow` - Snow texture
- `solidFractal` - Solid fractal
- `stucco` - Stucco texture
- `envBall` - Environment ball
- `envChrome` - Environment chrome
- `envCube` - Environment cube
- `envSky` - Environment sky
- `envSphere` - Environment sphere

**Missing shader network operations:**
- Connect shader nodes
- Disconnect shader nodes
- Query shader connections
- Shader graph traversal
- Shader assignment to components

### 9. Advanced Rendering (Partially Covered)

**Missing render settings:**
- `renderSettings` - Render settings
- `renderGlobals` - Render globals
- `defaultRenderGlobals` - Default render globals (more options)
- `renderLayer` - Render layers
- `renderLayerManager` - Render layer manager
- `renderPass` - Render passes
- `renderPassSet` - Render pass sets
- `renderQuality` - Render quality settings
- `renderWindowEditor` - Render window editor
- `iprRender` - IPR rendering
- `batchRender` - Batch rendering
- `render` - More render options

**Missing renderer-specific operations:**
- Arnold renderer settings
- V-Ray renderer settings (if available)
- Redshift renderer settings (if available)
- Hardware renderer settings
- Vector renderer settings

### 10. Paint Operations (Partially Covered)

**Paint tools:**
- ✅ `skinPercent` - Get/set skin weights (IMPLEMENTED)
- `artisan` - Artisan paint tools
- `paintSkinWeightsTool` - Paint skin weights (interactive tool)
- `paintAttributesTool` - Paint attributes
- `paintEffects` - Paint Effects
- `paintFluid` - Paint fluid
- `sculptGeometryCache` - Sculpt geometry cache
- `sculptMeshCache` - Sculpt mesh cache

### 11. Dynamics and Simulation (Not Covered)

**Particles:**
- `particle` - Create particles
- `emitter` - Create emitter
- `goal` - Goal operations
- `particleInstancer` - Particle instancer
- `nParticle` - nParticle system
- `nRigid` - nRigid solver
- `nCloth` - nCloth solver
- `nHair` - nHair system
- `nConstraint` - nConstraint
- `nCache` - nCache operations

**Fluids:**
- `fluid` - Create fluid
- `fluidEmitter` - Fluid emitter
- `fluidVoxelInfo` - Fluid voxel info
- `ocean` - Ocean system
- `pond` - Pond system

**Fields:**
- `airField` - Air field
- `dragField` - Drag field
- `gravityField` - Gravity field
- `newtonField` - Newton field
- `radialField` - Radial field
- `turbulenceField` - Turbulence field
- `uniformField` - Uniform field
- `vortexField` - Vortex field

**Rigid bodies:**
- `rigidBody` - Rigid body
- `rigidConstraint` - Rigid constraint
- `rigidSolver` - Rigid solver

**Soft bodies:**
- `softBody` - Soft body
- `softMod` - Soft modification

### 12. Advanced Mesh Operations (Partially Covered)

**Missing mesh editing:**
- `polyBoolean` - Boolean operations (union, difference, intersection)
- `polyBooleanOp` - Boolean operations
- `polyChipOff` - Chip off faces
- `polyCircularize` - Circularize selection
- `polyCircularizeEdge` - Circularize edges
- `polyCircularizeFace` - Circularize faces
- `polyCleanup` - Cleanup mesh
- `polyColorDel` - Delete color
- `polyColorPerVertex` - Per-vertex color
- `polyColorSet` - Color set operations
- `polyCompare` - Compare meshes
- `polyConnectComponents` - Connect components
- `polyCopyUV` - Copy UVs
- `polyCreaseEdge` - Crease edges
- `polyCreaseVertex` - Crease vertices
- `polyCylindricalProjection` - Cylindrical UV projection
- `polyDelFacetUV` - Delete facet UVs
- `polyEditUV` - Edit UVs (more operations)
- `polyEditUVShell` - Edit UV shells
- `polyEvaluate` - Evaluate mesh (more options)
- `polyFlip` - Flip mesh
- `polyFlipUV` - Flip UVs
- `polyHelixProjection` - Helix UV projection
- `polyMapCut` - Cut UV map
- `polyMapDel` - Delete UV map
- `polyMapSew` - Sew UV map
- `polyMapSewMove` - Sew and move UVs
- `polyMergeUV` - Merge UVs
- `polyModifyUV` - Modify UVs
- `polyMoveUV` - Move UVs
- `polyNormalPerVertex` - Per-vertex normals
- `polyOptUvs` - Optimize UVs
- `polyPlanarProjection` - Planar UV projection
- `polyProjection` - Various UV projections
- `polyPrism` - Create prism
- `polyPyramid` - Create pyramid
- `polySelect` - Select polygon components
- `polySelectConstraint` - Selection constraints
- `polySelectEditCtx` - Selection edit context
- ✅ `polySeparate` - Separate mesh (IMPLEMENTED)
- `polySetToFaceNormal` - Set to face normal
- `polySmooth` - Smooth (more options)
- `polySmoothFace` - Smooth faces
- `polySnapUV` - Snap UVs
- `polySphericalProjection` - Spherical UV projection
- ✅ `polySplit` - Split faces (IMPLEMENTED)
- `polySplitEdge` - Split edges
- `polySplitRing` - Split ring
- `polySplitVertex` - Split vertices
- `polyStraightenUVBorder` - Straighten UV border
- `polySubdivideEdge` - Subdivide edges
- `polySubdivideFace` - Subdivide faces
- `polyToSubdiv` - Convert to subdivision
- `polyTransfer` - Transfer attributes
- `polyTorus` - Create torus
- ✅ `polyTriangulate` - Triangulate (IMPLEMENTED)
- `polyUnite` - Already covered
- `polyUniteSkinned` - Unite skinned meshes
- `polyUniteUV` - Unite UVs
- `polyWedgeFace` - Wedge faces

### 13. Namespaces and References (Not Covered)

**Namespace operations:**
- `namespace` - Create/manage namespaces
- `namespaceInfo` - Namespace information
- `namespaceMove` - Move to namespace

**Reference operations:**
- `reference` - Create references
- `referenceEdit` - Edit references
- `referenceQuery` - Query references
- `file` - File reference operations (more options)

### 14. Sets and Partitions (Partially Covered)

**Set operations:**
- ✅ `sets` - Create sets (IMPLEMENTED)
- ✅ `partition` - Create partitions (IMPLEMENTED)
- ✅ `addToSet` - Add to set (IMPLEMENTED)
- ✅ `removeFromSet` - Remove from set (IMPLEMENTED)

### 15. Expressions (Not Covered - Blocked for Safety)

**Expression operations:**
- `expression` - Create expressions (BLOCKED - could execute code)
- Expression queries (could be safe if read-only)

### 16. Script Jobs and Callbacks (Not Covered - Blocked for Safety)

**Callback operations:**
- `scriptJob` - Script jobs (BLOCKED)
- `callbacks` - Callback management (BLOCKED)
- `callback` - Callback operations (BLOCKED)

### 17. Advanced Selection (Partially Covered)

**Missing selection operations:**
- ✅ `select` - More selection options (IMPLEMENTED - with modes: replace, add, toggle, deselect)
- ✅ `selectMode` - Selection mode (IMPLEMENTED)
- ✅ `selectType` - Selection type (IMPLEMENTED)
- ✅ `hilite` - Highlight (IMPLEMENTED)
- ✅ `selectPref` - Selection preferences (IMPLEMENTED)
- Component selection (vertices, edges, faces, UVs)
- Selection sets
- Selection constraints

### 18. Advanced Transform Operations (Partially Covered)

**Missing transform operations:**
- `xform` - Transform operations (more comprehensive)
- `snap` - Snap operations
- `snapMode` - Snap mode
- `align` - Align objects
- `matchTransform` - Match transforms
- `makeIdentity` - Make identity
- `resetTransform` - Reset transform
- `freezeTransformations` - Freeze transformations
- `unfreezeTransformations` - Unfreeze transformations
- `group` - Group objects
- `ungroup` - Ungroup
- `parent` - More parent options
- `unparent` - Unparent
- `pickWalk` - Pick walk
- `pickWalkContext` - Pick walk context

### 19. Advanced Query Operations (Partially Covered)

**Missing query operations:**
- `listRelatives` - List relatives (children, parents, shapes)
- `listHistory` - List history
- `listConnections` - List connections (more options)
- `listAnimatable` - List animatable attributes
- `listSets` - List sets
- `listNodeTypes` - List node types
- `nodeType` - Node type queries
- `nodeTypeInfo` - Node type information
- `about` - About Maya (more options)
- `getClassification` - Get classification
- `help` - Help system
- `whatIs` - What is command

### 20. Advanced File Operations (Partially Covered)

**Missing file operations:**
- `file` - More file options (references, options, etc.)
- `fileInfo` - File information
- `fileDialog` - File dialogs
- `fileDialog2` - File dialog v2
- `getFileList` - Get file list
- `workspace` - Workspace operations
- `workspaceControl` - Workspace control
- `project` - Project operations
- `projectWindow` - Project window

### 21. Viewport and Display (Partially Covered)

**Missing viewport operations:**
- ✅ `viewFit` - Fit view (IMPLEMENTED)
- ✅ `viewSelected` - View selected (IMPLEMENTED)
- `viewPlace` - Place view
- `viewSet` - Set view
- ✅ `lookThrough` - Look through camera (IMPLEMENTED)
- `dolly` - Dolly
- `tumble` - Tumble
- `track` - Track
- `truck` - Truck
- `zoom` - Zoom
- `viewClipPlane` - View clip plane
- `viewHeadOn` - View head on
- `viewManip` - View manipulator
- `view2dToolCtx` - 2D view tool
- `view3dToolCtx` - 3D view tool
- `viewAxis` - View axis
- `viewBookmark` - View bookmarks
- `viewCamera` - View camera
- `viewColor` - View color
- `viewCompass` - View compass
- `viewFrame` - Frame view
- `viewLookAt` - Look at view
- `viewTrack` - Track view

### 22. Advanced Animation Curves (Partially Covered)

**Missing curve operations:**
- `animCurve` - Animation curve operations
- `animCurveEditor` - Graph editor
- `keyTangent` - Keyframe tangents
- `keyframe` - More keyframe operations
- `findKeyframe` - Find keyframes
- `selectKey` - Select keyframes
- `copyKey` - Copy keyframes
- `pasteKey` - Paste keyframes
- `scaleKey` - Scale keyframes
- `snapKey` - Snap keyframes

### 23. Advanced Material Operations (Partially Covered)

**Missing material operations:**
- `hyperShade` - Hypershade operations
- `shadingNode` - More shading node operations
- `assignInputDevice` - Assign input device
- `createRenderNode` - Create render node
- `listNodeTypes` - List node types
- `nodeType` - Node type queries
- `shaderList` - Shader list
- `shadingConnection` - Shading connections
- `shadingNetwork` - Shading network operations

### 24. Advanced Light Operations (Partially Covered)

**Missing light operations:**
- `lightLink` - Light linking
- `lightList` - Light list
- `listLightLinks` - List light links
- `makeLightLinks` - Make light links
- `breakLightLinks` - Break light links
- Light attributes (shadows, decay, etc.)
- Light linking editor operations

### 25. Advanced UV Operations (Partially Covered)

**Missing UV operations:**
- `polyEditUV` - More UV edit operations
- `polyMapCut` - Cut UV map
- `polyMapSew` - Sew UV map
- `polyMapDel` - Delete UV map
- `polyUVSet` - UV set operations
- `polyUVSetCreate` - Create UV set
- `polyUVSetDelete` - Delete UV set
- `polyUVSetCopy` - Copy UV set
- `polyUVSetCurrent` - Set current UV set
- `polyUVSetRename` - Rename UV set
- `polyUVSetTransfer` - Transfer UV set
- `polyUVSnapshot` - Already covered
- `polyUVSetQuery` - Query UV sets

### 26. Advanced Skinning Operations (Partially Covered)

**Missing skinning operations:**
- `skinCluster` - More skin cluster operations
- `copySkinWeights` - Copy skin weights
- `exportSkinWeights` - Export skin weights
- `importSkinWeights` - Import skin weights
- ✅ `skinPercent` - Get/set skin weights (IMPLEMENTED)
- `bindSkin` - More bind options
- `detachSkin` - Detach skin
- `goToBindPose` - Go to bind pose
- `setBindPose` - Set bind pose
- `resetBindPose` - Reset bind pose
- `skinCluster` - More skin cluster queries

### 27. Advanced Rendering Operations (Partially Covered)

**Missing rendering operations:**
- `renderLayer` - Render layers
- `renderPass` - Render passes
- `renderSettings` - Render settings (more options)
- `renderWindowEditor` - Render window
- `iprRender` - IPR rendering
- `batchRender` - Batch rendering
- `render` - More render options
- `renderView` - Render view
- `renderWindow` - Render window
- `renderWindowEditor` - Render window editor

### 28. Node Operations (Not Covered)

**Missing node operations:**
- `createNode` - Create generic nodes
- `deleteNode` - Delete nodes
- `rename` - Rename nodes
- `lockNode` - Lock nodes
- `unlockNode` - Unlock nodes
- `lockNode` - Lock node attributes
- `unlockNode` - Unlock node attributes
- `nodeType` - Node type queries
- `nodeTypeInfo` - Node type information
- `listNodeTypes` - List node types
- `getClassification` - Get classification
- `isConnected` - Check connections
- `listConnections` - List connections (more options)
- `listHistory` - List history
- `listRelatives` - List relatives

### 29. Advanced Attribute Operations (Partially Covered)

**Missing attribute operations:**
- `addAttr` - More add attribute options
- `deleteAttr` - Delete attributes
- `setAttr` - More set attribute options
- `getAttr` - More get attribute options
- `attributeInfo` - Attribute information
- `attributeQuery` - Attribute queries
- `listAttr` - More list attribute options
- `aliasAttr` - Alias attributes
- `lockNode` - Lock attributes
- `unlockNode` - Unlock attributes
- `connectAttr` - More connect options
- `disconnectAttr` - More disconnect options
- `listConnections` - More connection queries

### 30. Advanced Mesh Component Operations (Not Covered)

**Missing component operations:**
- Select vertices, edges, faces, UVs
- Edit components
- Component queries
- Component transformations
- Component selection sets

## Summary Statistics

### Coverage Estimate

- **Currently Covered**: ~140+ tools across 24 modules
- **Estimated Total Maya.cmds Commands**: ~500-800+ commands
- **Coverage**: ~18-25% of available commands

### Priority Areas for Future Development

1. **High Priority** (Common workflows):
   - ✅ Polygon mesh editing operations (extrude, bevel, normals, quadrangulate, reduce, remesh, UV operations, etc.) - EXTENSIVELY IMPLEMENTED
   - ✅ NURBS operations (curves and surfaces) - PARTIALLY IMPLEMENTED
   - ✅ Advanced constraints (aim, scale, geometry, normal, tangent, pole vector) - MOSTLY IMPLEMENTED
   - ✅ Camera operations - PARTIALLY IMPLEMENTED
   - ✅ Advanced material/texture operations (surface shader, use background, layered shader, ramp shader, generic shading nodes) - EXTENSIVELY IMPLEMENTED
   - ✅ Paint tools (skin weights) - BASIC OPERATIONS IMPLEMENTED
   - ✅ Animation tools (bake, copy/paste keyframes, scale/snap/select keyframes) - EXTENSIVELY IMPLEMENTED
   - ✅ Deformers (sculpt, wire, wrinkle, jiggle, softMod, tension, deltaMush, shrinkWrap, wrap) - EXTENSIVELY IMPLEMENTED
   - ✅ Sets and partitions - IMPLEMENTED

2. **Medium Priority** (Specialized workflows):
   - Deformers
   - Dynamics and simulation
   - Advanced animation tools
   - Advanced rendering options
   - Namespace and reference management

3. **Low Priority** (Advanced/specialized):
   - Paint Effects
   - Advanced dynamics
   - Specialized renderers
   - Advanced viewport operations

## Notes

- **Safety**: Script execution, callbacks, and expression creation remain blocked for security
- **Performance**: OpenMaya API is used where appropriate for expensive operations
- **Extensibility**: The modular structure makes it easy to add new tool categories
- **Testing**: New tools should follow the existing test patterns with mocks

## Recommendations

1. **Add polygon mesh editing tools** - Most requested for modeling workflows
2. **Add NURBS operations** - Important for surface modeling
3. **Add camera operations** - Essential for scene setup
4. **Add advanced material/texture tools** - Important for look development
5. **Add paint tools** - Critical for character work (skin weights, etc.)
6. **Add deformer operations** - Important for character animation
7. **Add advanced animation tools** - Graph editor, dope sheet operations
