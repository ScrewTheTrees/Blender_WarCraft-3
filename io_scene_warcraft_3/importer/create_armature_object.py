from typing import List, Dict, Set

import bpy
from bpy.types import Object, BoneGroup

from io_scene_warcraft_3.classes.WarCraft3Model import WarCraft3Model
from io_scene_warcraft_3.classes.WarCraft3Node import WarCraft3Node


def create_armature_object(model: WarCraft3Model, bpy_mesh_objects: List[Object], bone_size: float) -> Object:
    print("creating armature")
    nodes = model.nodes
    pivot_points = model.pivot_points
    # bpy_armature: bpy.types.Armature = bpy.data.armatures.new(model.name + ' Nodes')
    bpy_armature_object = get_bpy_armature_object(model.name + ' Nodes')
    bpy_armature: bpy.types.Armature = bpy_armature_object.data
    add_mesh_modifier(bpy_armature_object, bpy_mesh_objects)
    # bpy_armature.display_type = 'STICK'

    bone_types = get_bone_type_dict(bone_size, bpy_armature.edit_bones, nodes, pivot_points)
    # bone_types = add_and_get_node_bone_dict(bone_size, bpy_armature.edit_bones, nodes, pivot_points)

    print(bpy_armature_object.data.edit_bones[0])

    for indexNode, node in enumerate(nodes):
        e_bone = bpy_armature.edit_bones[indexNode]
        if node.parent is not None:
            parent = bpy_armature.edit_bones[node.parent]
            e_bone.parent = parent
            # bone.use_connect = True

    for a_bone in bpy_armature.bones:
        a_bone.warcraft_3.nodeType = bone_types[a_bone.name].upper()

    set_vertex_group_names(bpy_armature, bpy_mesh_objects)

    bpy.ops.object.mode_set(mode='POSE')
    bone_groups = get_bone_group_dict(bone_types, bpy_armature_object)

    for p_bone in bpy_armature_object.pose.bones:
        p_bone.rotation_mode = 'XYZ'
        p_bone.bone_group = bone_groups[bone_types[p_bone.name]]

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.active_object.select_set(False)

    return bpy_armature_object


# def get_bpy_armature_object(bpy_armature1: bpy.types.Armature, name: str) -> Object:
def get_bpy_armature_object(name: str) -> Object:
    bpy_armature: bpy.types.Armature = bpy.data.armatures.new(name)
    bpy_armature_object = bpy.data.objects.new(name, bpy_armature)
    bpy.context.scene.collection.objects.link(bpy_armature_object)
    bpy_armature_object.select_set(True)
    # bpy_armature_object.show_in_front = True
    # bpy_armature_object.mode = 'EDIT'
    bpy.context.view_layer.objects.active = bpy_armature_object
    # bpy.context.scene.objects.active = bpy_armature_object
    bpy.ops.object.mode_set(mode='EDIT')
    return bpy_armature_object


def add_mesh_modifier(bpy_armature_object: bpy.types.Object, bpy_mesh_objects: List[bpy.types.Object]):
    for mesh in bpy_mesh_objects:
        mesh.modifiers.new(name='Armature', type='ARMATURE')
        mesh.modifiers['Armature'].object = bpy_armature_object


def set_vertex_group_names(bpy_armature: bpy.types.Armature, bpy_mesh_objects: List[bpy.types.Object]):
    for mesh in bpy_mesh_objects:
        for vertexGroup in mesh.vertex_groups:
            vertex_group_index = int(vertexGroup.name)
            bone_name = bpy_armature.edit_bones[vertex_group_index].name
            vertexGroup.name = bone_name


def get_bone_group_dict(node_to_bone: Dict[WarCraft3Node, bpy.types.EditBone], bpy_armature_object: Object):
    bone_groups: Dict[str, BoneGroup] = {}
    # node_types = collect_node_types(bone_types)
    node_types: List[str] = []
    for index, node in enumerate(node_to_bone):
        if node.node_type not in node_types:
            node_types.append(node.node_type)
    node_types.sort()

    for nodeType in node_types:
        bone_group = get_new_bone_group(nodeType, bpy_armature_object.pose.bone_groups)
        bone_groups[nodeType] = bone_group
    return bone_groups


def get_bone_group_dict(bone_types: Dict[str, str], bpy_armature_object: Object):
    bone_groups: Dict[str, BoneGroup] = {}
    # node_types = collect_node_types(bone_types)

    node_types: List[str] = []
    for index, b_name in enumerate(bone_types):
        if bone_types[b_name] not in node_types:
            node_types.append(bone_types[b_name])
    node_types.sort()

    for nodeType in node_types:
        bone_group = get_new_bone_group(nodeType, bpy_armature_object.pose.bone_groups)
        bone_groups[nodeType] = bone_group
    return bone_groups


def get_bone_type_dict(bone_size: float, edit_bones: bpy.types.ArmatureEditBones, nodes: List[WarCraft3Node], pivot_points: List[List[float]]) \
        -> Dict[str, str]:
    bone_types: Dict[str, str] = {}
    for indexNode, node in enumerate(nodes):
        node_position = pivot_points[indexNode]
        bone_name = node.name
        if bone_name in bone_types.keys():
            bone_name = bone_name + ".001"
            if bone_name in bone_types.keys():
                bone_name = bone_name + ".002"
            node.name = bone_name
        bone = edit_bones.new(bone_name)
        bone.head = node_position
        bone.tail = node_position
        bone.tail[1] += bone_size
        bone_types[bone_name] = node.node_type

    return bone_types


def add_and_get_node_bone_dict(bone_size: float, edit_bones: bpy.types.ArmatureEditBones, nodes: List[WarCraft3Node], pivot_points: List[List[float]]) \
        -> Dict[WarCraft3Node, bpy.types.EditBone]:
    node_to_bone: Dict[WarCraft3Node, bpy.types.EditBone] = {}
    bone_names: Set[str] = set()

    for indexNode, node in enumerate(nodes):
        node_position = pivot_points[indexNode]
        bone_name = node.name
        if bone_name in bone_names:
            bone_name = bone_name + ".001"
            if bone_name in bone_names:
                bone_name = bone_name + ".002"
            node.name = bone_name
        bone = edit_bones.new(bone_name)
        bone.head = node_position
        bone.tail = node_position
        # bone.tail[2] += bone_size
        bone.tail[1] += bone_size
        bone_names.add(bone_name)
        node_to_bone[node] = bone

    return node_to_bone


def collect_node_types(node_to_bone: Dict[WarCraft3Node, bpy.types.EditBone]) -> List[str]:
    node_types: List[str] = []
    for index, bone in enumerate(node_to_bone):
        if bone.node_type not in node_types:
            node_types.append(bone.node_type)
    node_types.sort()
    return node_types


def collect_node_types(bone_types: Dict[str, str]) -> List[str]:
    node_types: List[str] = []
    for index, b_name in enumerate(bone_types):
        if bone_types[b_name] not in node_types:
            node_types.append(bone_types[b_name])
    node_types.sort()
    return node_types


def get_new_bone_group(nodeType: str, bone_groups: bpy.types. BoneGroups) -> BoneGroup:
    bone_group: bpy.types.BoneGroup = bone_groups.get(nodeType + 's')
    if bone_group is None:
        bone_group = bone_groups.new(name=nodeType + 's')
        # bone_group: bpy.types.BoneGroup = bpy.types.BoneGroups.new(nodeType + 's')
        # bone_group: bpy.types.BoneGroup = bpy.types.BoneGroup()
        bone_group.color_set = get_bone_group_color(nodeType)
        # bone_group.name = nodeType + 's'
    return bone_group


def get_new_bone_group11(nodeType: str, bone_groups: bpy.types. BoneGroups) -> BoneGroup:
    bone_groups.get(nodeType + 's')
    bone_group: bpy.types.BoneGroup = bone_groups.new(nodeType + 's')
    # bone_group: bpy.types.BoneGroup = bpy.types.BoneGroups.new(nodeType + 's')
    # bone_group: bpy.types.BoneGroup = bpy.types.BoneGroup()
    bone_group.color_set = get_bone_group_color(nodeType)
    bone_group.name = nodeType + 's'
    return bone_group


def get_bone_group_color(nodeType) -> str:
    if nodeType == 'bone':
        return 'THEME04'
    elif nodeType == 'attachment':
        return 'THEME09'
    elif nodeType == 'collision_shape':
        return 'THEME02'
    elif nodeType == 'event':
        return 'THEME03'
    elif nodeType == 'helper':
        return 'THEME01'
    return 'DEFAULT'
