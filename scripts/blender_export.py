import bpy
import os
import sys

# Check if a blend file argument is provided
if len(sys.argv) < 2:
    print("Usage: blender -b -P script.py -- [blend_file]")
    sys.exit(1)

# Set the export path
export_path = "/home/jin/Desktop/Exports/loot/"

# Get the path to the blend file from the command line argument
blend_file = sys.argv[-1]

# Open the specified blend file
bpy.ops.wm.open_mainfile(filepath=blend_file)

# Get the correct view layer (replace 'ViewLayer' with the actual view layer name)
view_layer_name = 'View Layer'
view_layer = bpy.context.scene.view_layers.get(view_layer_name)

if view_layer is None:
    print(f"View Layer '{view_layer_name}' not found.")
    sys.exit(1)

# Set the active view layer
bpy.context.window.view_layer = view_layer

# Get a list of all visible objects in the scene
visible_objects = [obj for obj in bpy.context.scene.objects if obj.parent is None]

# Iterate over each visible object and export it as a separate VRM file
for obj in visible_objects:
    # Search for an armature in the hierarchy of children
    mesh = None
    for child in obj.children_recursive:
        if child.type == 'MESH':
            mesh = child
            break
    
    # If a mesh is found, select it for export
    if mesh:
        # Set the filename for the exported VRM file
        armature = mesh.parent
        # Can change this to 0.0 if you want
        armature.data.vrm_addon_extension.spec_version = "0.0"
        filename = mesh.name + ".vrm"
        filepath = os.path.join(export_path, filename)

        # Select the mesh for export
        bpy.ops.object.select_all(action='DESELECT')
        mesh.select_set(True)
        
        # Export the mesh (VRM)
        bpy.ops.export_scene.vrm(
            filepath=filepath,
            export_invisibles=False,
            enable_advanced_preferences=False,
            export_fb_ngon_encoding=False,
            export_only_selections=True,
            armature_object_name=obj.name
        )
