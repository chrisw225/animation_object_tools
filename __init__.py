"""
Animation & Object Tools
A comprehensive Blender addon for NLA strip manipulation, parent transform fixes, and object replacement.

Copyright (C) 2024 Your Name

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

bl_info = {
    "name": "Animation & Object Tools",
    "author": "Your Name",
    "version": (1, 4, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Tool Tab",
    "description": "NLA strip offset, parent transform fix, and object replacement tools",
    "warning": "",
    "doc_url": "https://github.com/yourusername/animation-object-tools",
    "category": "Animation",
}

import bpy
import bmesh
import random
import mathutils
from bpy.props import FloatProperty, EnumProperty
from bpy.types import Panel, Operator


class NLA_OT_apply_offset_and_random_scale(Operator):
    """Apply absolute offset based on distance to 3D cursor or random, and randomize strip scale"""
    bl_idname = "nla.apply_offset_and_random_scale"
    bl_label = "Apply Offset & Random Scale"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        nla_tool = scene.nla_strip_randomizer
        
        # Get selected objects
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.animation_data]
        
        if not selected_objects:
            self.report({'WARNING'}, "No objects with animation data selected")
            return {'CANCELLED'}
        
        for obj in selected_objects:
            # Calculate offset frames based on method
            if nla_tool.offset_method == 'RANDOM':
                # Random offset
                offset_frames = random.uniform(0, nla_tool.max_random_offset)
            else:
                # 3D Cursor distance
                cursor_location = scene.cursor.location
                distance = (obj.location - cursor_location).length
                offset_frames = distance * nla_tool.offset_multiplier
            
            # Get animation data
            anim_data = obj.animation_data
            if not anim_data or not anim_data.nla_tracks:
                continue
            
            # Process each NLA track
            for track in anim_data.nla_tracks:
                if not track.strips:
                    continue
                
                # Process each strip in the track
                for strip in track.strips:
                    # Store original duration
                    original_duration = strip.frame_end_ui - strip.frame_start_ui
                    
                    # Apply absolute offset (not relative to current position)
                    strip.frame_start_ui = nla_tool.base_start_frame + offset_frames
                    
                    # Maintain duration by adjusting end frame
                    strip.frame_end_ui = strip.frame_start_ui + original_duration
                    
                    # Apply random scale (absolute, not relative)
                    random_scale = random.uniform(nla_tool.scale_min, nla_tool.scale_max)
                    strip.scale = random_scale
        
        self.report({'INFO'}, f"Applied offset and random scale to {len(selected_objects)} objects")
        return {'FINISHED'}


class NLA_OT_fix_parent_transforms(Operator):
    """Fix parent transforms for selected objects"""
    bl_idname = "nla.fix_parent_transforms"
    bl_label = "Fix Parent Transforms"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        fixed_count = 0
        skipped_count = 0
        error_count = 0
        
        for obj in bpy.context.selected_objects:
            if obj.parent is None:
                skipped_count += 1
                continue

            parent = obj.parent

            try:
                # Set the object as active and the only selected one
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj

                # Step 1: Store world transform
                world_matrix = obj.matrix_world.copy()

                # Step 2: Clear parent while keeping world transform
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

                # Step 3: Reassign parent directly
                obj.parent = parent

                # Step 4: Compute and apply correct local matrix
                local_matrix = parent.matrix_world.inverted() @ world_matrix
                obj.matrix_parent_inverse.identity()
                obj.matrix_basis = local_matrix

                fixed_count += 1

            except Exception as e:
                error_count += 1
                self.report({'ERROR'}, f"Failed to fix '{obj.name}': {e}")
        
        # Report results
        if fixed_count > 0:
            self.report({'INFO'}, f"Fixed {fixed_count} objects")
        if skipped_count > 0:
            self.report({'WARNING'}, f"Skipped {skipped_count} objects (no parent)")
        if error_count > 0:
            self.report({'ERROR'}, f"Failed to fix {error_count} objects")
        
        return {'FINISHED'}


class NLA_OT_replace_with_instance(Operator):
    """Replace selected objects with instances of the active object"""
    bl_idname = "nla.replace_with_instance"
    bl_label = "Replace with Instance"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Reference to the active (source/template) object
        active_obj = bpy.context.active_object

        if active_obj is None:
            self.report({'ERROR'}, "No active object selected.")
            return {'CANCELLED'}

        # All other selected objects to be replaced
        targets = [obj for obj in bpy.context.selected_objects if obj != active_obj]

        if not targets:
            self.report({'WARNING'}, "No other objects selected to replace.")
            return {'CANCELLED'}
        
        replaced_count = 0
        
        for target in targets:
            try:
                # Store the original transform
                matrix = target.matrix_world.copy()

                # Remove the target object
                bpy.data.objects.remove(target, do_unlink=True)

                # Create a new instance (duplicate object with same data)
                new_obj = bpy.data.objects.new(name=f"{active_obj.name}_inst", object_data=active_obj.data)
                bpy.context.collection.objects.link(new_obj)

                # Copy the original transform
                new_obj.matrix_world = matrix
                
                replaced_count += 1

            except Exception as e:
                self.report({'ERROR'}, f"Failed to replace '{target.name}': {e}")
        
        if replaced_count > 0:
            self.report({'INFO'}, f"Replaced {replaced_count} object(s) with instance of '{active_obj.name}'")
        
        return {'FINISHED'}


class NLA_PT_strip_randomizer(Panel):
    """Animation & Object Tools Panel"""
    bl_label = "Animation & Object Tools"
    bl_idname = "NLA_PT_strip_randomizer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        nla_tool = scene.nla_strip_randomizer
        
        # Offset settings
        box = layout.box()
        box.label(text="Offset Settings", icon='ANIM')
        
        col = box.column(align=True)
        col.prop(nla_tool, "offset_method", text="Offset Method")
        col.prop(nla_tool, "base_start_frame", text="Base Start Frame")
        
        if nla_tool.offset_method == 'RANDOM':
            col.prop(nla_tool, "max_random_offset", text="Max Random Offset")
        else:
            col.prop(nla_tool, "offset_multiplier", text="Offset Multiplier")
            col.label(text="Frames per unit distance")
        
        # Scale settings
        box = layout.box()
        box.label(text="Random Scale Settings", icon='RNDCURVE')
        
        col = box.column(align=True)
        col.prop(nla_tool, "scale_min", text="Scale Min")
        col.prop(nla_tool, "scale_max", text="Scale Max")
        
        # Apply button
        layout.separator()
        layout.operator("nla.apply_offset_and_random_scale", 
                       text="Apply Offset & Random Scale", 
                       icon='PLAY')
        
        # Parent transform fix
        layout.separator()
        box = layout.box()
        box.label(text="Parent Transform Fix", icon='CONSTRAINT')
        box.operator("nla.fix_parent_transforms", 
                    text="Fix Parent Transforms", 
                    icon='CONSTRAINT_BONE')
        
        # Object replacement
        layout.separator()
        box = layout.box()
        box.label(text="Object Replacement", icon='OBJECT_DATA')
        box.operator("nla.replace_with_instance", 
                    text="Replace with Instance", 
                    icon='DUPLICATE')


class NLAStripRandomizerProperties(bpy.types.PropertyGroup):
    """Properties for Animation & Object Tools"""
    
    offset_method: EnumProperty(
        name="Offset Method",
        description="How to calculate the offset for strips",
        items=[
            ('RANDOM', "Random", "Random offset within specified range"),
            ('CURSOR', "3D Cursor", "Offset based on distance from 3D cursor"),
        ],
        default='RANDOM'
    )
    
    base_start_frame: FloatProperty(
        name="Base Start Frame",
        description="Base frame position for all strips (absolute positioning)",
        default=1.0,
        min=1.0,
        max=10000.0,
        soft_min=1.0,
        soft_max=1000.0
    )
    
    max_random_offset: FloatProperty(
        name="Max Random Offset",
        description="Maximum random offset in frames",
        default=10.0,
        min=0.0,
        max=1000.0,
        soft_min=0.0,
        soft_max=100.0
    )
    
    offset_multiplier: FloatProperty(
        name="Offset Multiplier",
        description="How many frames per unit distance from 3D cursor",
        default=1.0,
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=10.0
    )
    
    scale_min: FloatProperty(
        name="Scale Min",
        description="Minimum random scale value",
        default=0.9,
        min=0.1,
        max=10.0,
        soft_min=0.1,
        soft_max=5.0
    )
    
    scale_max: FloatProperty(
        name="Scale Max",
        description="Maximum random scale value",
        default=1.1,
        min=0.1,
        max=10.0,
        soft_min=0.1,
        soft_max=5.0
    )


# Registration
classes = (
    NLA_OT_apply_offset_and_random_scale,
    NLA_OT_fix_parent_transforms,
    NLA_OT_replace_with_instance,
    NLA_PT_strip_randomizer,
    NLAStripRandomizerProperties,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register properties
    bpy.types.Scene.nla_strip_randomizer = bpy.props.PointerProperty(
        type=NLAStripRandomizerProperties
    )


def unregister():
    # Unregister properties
    del bpy.types.Scene.nla_strip_randomizer
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register() 