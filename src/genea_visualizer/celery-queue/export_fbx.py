from pathlib import Path
import argparse
import sys
import bpy

# cleans up the scene and memory
def clear_scene():
    for block in bpy.data.meshes:       bpy.data.meshes.remove(block)
    for block in bpy.data.materials:    bpy.data.materials.remove(block)
    for block in bpy.data.textures:     bpy.data.textures.remove(block)
    for block in bpy.data.images:       bpy.data.images.remove(block)  
    for block in bpy.data.curves:       bpy.data.curves.remove(block)
    for block in bpy.data.cameras:      bpy.data.cameras.remove(block)
    for block in bpy.data.lights:       bpy.data.lights.remove(block)
    for block in bpy.data.sounds:       bpy.data.sounds.remove(block)
    for block in bpy.data.armatures:    bpy.data.armatures.remove(block)
    for block in bpy.data.objects:      bpy.data.objects.remove(block)
    for block in bpy.data.actions:      bpy.data.actions.remove(block)
            
    if bpy.context.object == None:          bpy.ops.object.delete()
    elif bpy.context.object.mode == 'EDIT': bpy.ops.object.mode_set(mode='OBJECT')
    elif bpy.context.object.mode == 'POSE': bpy.ops.object.mode_set(mode='OBJECT')
        
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.sequencer.select_all(action='SELECT')
    bpy.ops.sequencer.delete()

def parse_args():
    parser = argparse.ArgumentParser(description="Some description.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-b', '--bvh', help='BVH containing the animation.', type=Path, required=True)
    parser.add_argument('-m', '--model', help='Model to apply the BVH animation to.', type=Path, required=True)
    parser.add_argument('-o', '--output', help='Output path of animated FBX', type=Path, required=True)
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :]
    return parser.parse_args(args=argv)

def import_fbx(filepath : Path):
    assert filepath.is_file()
    bpy.ops.import_scene.fbx(filepath=str(filepath), ignore_leaf_bones=True, 
    force_connect_children=True, automatic_bone_orientation=False)

def import_bvh(filepath : Path):
    assert filepath.is_file()
    bpy.ops.import_anim.bvh(filepath=str(filepath), axis_forward="-Z", use_fps_scale=False,
    update_scene_fps=True, update_scene_duration=True, global_scale=0.01)

def export_fbx(target_arm_name, target_mesh_name, output_path : Path):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    # Select armature and mesh
    selected = False
    for ob in bpy.context.scene.objects:
        if ob.name in [target_arm_name, target_mesh_name]:
            ob.select_set(True)
            selected = True

    # Export the armature as FBX
    if selected:
        assert output_path.parent.is_dir()
        bpy.ops.export_scene.fbx(filepath=str(output_path), use_selection=True, bake_anim_use_all_bones=True)

    # Cleanup
    bpy.ops.object.select_all(action='DESELECT')
    
def constrain_bones(source_name, target_name):
    for ob in bpy.context.scene.objects: ob.select_set(False)
    source = bpy.context.scene.objects[source_name]
    target = bpy.context.scene.objects[target_name]
    
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    for bone in bpy.context.selected_pose_bones:
        # Delete all other constraints
        for c in bone.constraints:
            bone.constraints.remove( c )
            
        # Create body_world location to fix floating legs
        if bone.name == 'Hips':
            constraint = bone.constraints.new('COPY_LOCATION')
            constraint.target = source
            constraint.subtarget = bone.name

        # Create all rotations
        if target.data.bones.get(bone.name) is not None:
            constraint = bone.constraints.new('COPY_ROTATION')
            constraint.target = source
            constraint.subtarget = bone.name
    bpy.ops.pose.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def bake_constraints(target_name, bake_start, bake_end, step):
    # Deselect everything
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    
    # Find armature
    source = None
    for ob in bpy.context.scene.objects:
        if ob.type == "ARMATURE" and ob.name == target_name:
            source = ob
    
    # Select armature, enter pose mode and bake
    if source:
        source.select_set(True)
        bpy.context.view_layer.objects.active = source
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='SELECT')
        log_total = bake_end - bake_start
        log_true_total = log_total // step
        print(f"Beginning bake operation for {log_true_total}({log_total}) frames.")
        bpy.ops.nla.bake(frame_start=bake_start, frame_end=bake_end, step=step, only_selected=True, visual_keying=True, clear_constraints=True, use_current_action=True, bake_types={'POSE'})
    
    # Cleanup
    bpy.ops.pose.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def main():
    if bpy.ops.text.run_script.poll():
        print('[INFO] Script is running in Blender UI.')
        SCRIPT_DIR = Path(bpy.context.space_data.text.filepath).parents[0]
        ##################################
        ##### SET ARGUMENTS MANUALLY #####
        ##### IF RUNNING BLENDER GUI #####
        ##################################
        ARG_IN_BVH_PATH = SCRIPT_DIR / 'data' / 'test.bvh'
        ARG_IN_FBX_PATH = SCRIPT_DIR / 'model' / 'LaForgeMale.fbx'
        ARG_OUT_FBX_PATH = SCRIPT_DIR / 'data' / 'test.fbx'
    else:
        args = parse_args()
        ARG_IN_BVH_PATH = args.bvh
        ARG_IN_FBX_PATH = args.model
        ARG_OUT_FBX_PATH = args.output

    target_armature_name = "LaForge_Male_model_v020"
    target_mesh_name = "LaForge_Model_Male_v020"
    clear_scene()
    import_fbx(ARG_IN_FBX_PATH)
    import_bvh(ARG_IN_BVH_PATH)
    constrain_bones(ARG_IN_BVH_PATH.stem, target_armature_name)
    bake_constraints(target_armature_name, 0, bpy.context.scene.frame_end, 3)
    export_path = ARG_OUT_FBX_PATH if ARG_OUT_FBX_PATH.suffix == ".fbx" else ARG_OUT_FBX_PATH.with_suffix(".fbx")
    export_fbx(target_armature_name, target_mesh_name, export_path)
    
main()