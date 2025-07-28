"""
Test script for NLA Strip Randomizer addon
This script creates sample objects with NLA animation data for testing the addon.
"""

import bpy
import random

def create_test_scene():
    """Create a test scene with objects that have NLA animation data"""
    
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Create test objects at different distances from origin
    positions = [
        (1, 0, 0),   # Distance 1 from origin
        (2, 0, 0),   # Distance 2 from origin
        (3, 0, 0),   # Distance 3 from origin
        (0, 2, 0),   # Distance 2 from origin
        (2, 2, 0),   # Distance ~2.83 from origin
    ]
    
    objects = []
    
    for i, pos in enumerate(positions):
        # Create a cube
        bpy.ops.mesh.primitive_cube_add(location=pos)
        obj = bpy.context.active_object
        obj.name = f"TestCube_{i+1}"
        
        # Add animation data
        obj.animation_data_create()
        
        # Create a simple action
        action = bpy.data.actions.new(name=f"Action_{obj.name}")
        
        # Add some keyframes to the action
        fcurve = action.fcurves.new(data_path="location", index=0)
        keyframe1 = fcurve.keyframe_points.insert(frame=1, value=pos[0])
        keyframe2 = fcurve.keyframe_points.insert(frame=30, value=pos[0] + 2)
        
        fcurve = action.fcurves.new(data_path="location", index=1)
        keyframe1 = fcurve.keyframe_points.insert(frame=1, value=pos[1])
        keyframe2 = fcurve.keyframe_points.insert(frame=30, value=pos[1] + 1)
        
        fcurve = action.fcurves.new(data_path="location", index=2)
        keyframe1 = fcurve.keyframe_points.insert(frame=1, value=pos[2])
        keyframe2 = fcurve.keyframe_points.insert(frame=30, value=pos[2] + 0.5)
        
        # Create NLA track
        track = obj.animation_data.nla_tracks.new()
        track.name = f"Track_{obj.name}"
        
        # Create NLA strip
        strip = track.strips.new(name=f"Strip_{obj.name}", start=1, action=action)
        strip.frame_start_ui = 1
        strip.frame_end_ui = 30
        
        objects.append(obj)
    
    # Set 3D cursor to origin
    bpy.context.scene.cursor.location = (0, 0, 0)
    
    # Select all test objects
    for obj in objects:
        obj.select_set(True)
    
    # Set active object
    bpy.context.view_layer.objects.active = objects[0]
    
    print(f"Created {len(objects)} test objects with NLA animation data")
    print("Objects are positioned at different distances from the 3D cursor (origin)")
    print("You can now test the NLA Strip Randomizer addon")
    
    return objects

def print_object_info():
    """Print information about objects with NLA data"""
    objects_with_nla = [obj for obj in bpy.data.objects if obj.animation_data and obj.animation_data.nla_tracks]
    
    print(f"\nFound {len(objects_with_nla)} objects with NLA data:")
    
    for obj in objects_with_nla:
        print(f"\nObject: {obj.name}")
        print(f"  Location: {obj.location}")
        print(f"  Distance from cursor: {(obj.location - bpy.context.scene.cursor.location).length:.2f}")
        
        for track in obj.animation_data.nla_tracks:
            print(f"  Track: {track.name}")
            for strip in track.strips:
                print(f"    Strip: {strip.name}")
                print(f"      Start: {strip.frame_start_ui}")
                print(f"      End: {strip.frame_end_ui}")
                print(f"      Scale: {strip.scale}")

if __name__ == "__main__":
    # Create test scene
    test_objects = create_test_scene()
    
    # Print information
    print_object_info()
    
    print("\nTo test the addon:")
    print("1. Make sure the NLA Strip Randomizer addon is installed and enabled")
    print("2. Open the Tool tab in the 3D View sidebar (press N)")
    print("3. Adjust the settings as needed")
    print("4. Click 'Apply Offset & Random Scale'")
    print("5. Check the NLA editor to see the results") 