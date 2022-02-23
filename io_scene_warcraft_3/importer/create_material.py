import os
from pathlib import Path
from typing import List

import bpy
from bpy.types import Material, Image

from io_scene_warcraft_3 import constants
from io_scene_warcraft_3.classes.WarCraft3Material import WarCraft3Material
from io_scene_warcraft_3.classes.WarCraft3Model import WarCraft3Model
from io_scene_warcraft_3.classes.WarCraft3Texture import WarCraft3Texture
from io_scene_warcraft_3.preferences import WarCraft3Preferences


def create_material(model: WarCraft3Model, team_color: str) -> List[Material]:
    print("creating materials")
    # preferences = bpy.context.preferences.addons.get('io_scene_warcraft_3') #['io_scene_warcraft_3'].preferences
    preferences: WarCraft3Preferences = bpy.context.preferences.addons.get('io_scene_warcraft_3').preferences

    folders = get_folders(preferences.alternativeResourceFolder, preferences.resourceFolder, model.file)

    print("folders size: ", len(folders))
    texture_ext = get_texture_ext(preferences.textureExtension)
    model.normalize_meshes_names()

    bpy_images: List[Image] = []
    for texture in model.textures:
        bpy_image = get_image(folders, team_color, texture, texture_ext)
        bpy_images.append(bpy_image)

    bpy_materials = []
    for material in model.materials:
        bpy_images_of_layer: List[Image] = []
        for layer in material.layers:
            bpy_images_of_layer.append(bpy_images[layer.texture_id])

        bpy_material = create_bpy_material(bpy_images_of_layer, material)

        bpy_materials.append(bpy_material)

    # bpy_material = bpy_materials[warCraft3Mesh.material_id]
    # bpyMesh.materials.append(bpy_material)
    # # bpy_image = None
    # # for textureSlot in bpy_material.texture_slots:
    # #     if textureSlot:
    # #         bpy_image = textureSlot.texture.image
    # # if bpy_image:
    # #     for triangleID in range(len(bpyObject.data.polygons)):
    # #         bpyObject.data.uv_textures[0].data[triangleID].image = bpy_image

    return bpy_materials


def create_bpy_material(bpy_images_of_layer: List[Image], material: WarCraft3Material):
    material_name = bpy_images_of_layer[-1].filepath.split(os.path.sep)[-1].split('.')[0]
    # material_name = bpy_images_of_layer[-1].filepath.split('\\')[-1].split('.')[0]
    bpy_material = bpy.data.materials.new(name=material_name)
    bpy_material.shadow_method = 'NONE'
    # bpy_material.use_object_color = True
    bpy_material.use_nodes = True
    # bsdf_node = bpy_material.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
    # bsdf_node.color = (1.0, 1.0, 1.0, 1.0)
    # bpy_material.node_tree.nodes.get("Material Output")
    bpy_material.diffuse_color = (1.0, 1.0, 1.0, 1.0)
    texture_slot_index = 0
    material_node_tree = bpy_material.node_tree
    shader_node = material_node_tree.nodes.get("Principled BSDF")
    color_input_socket = shader_node.inputs.get("Base Color")
    if material.hd:
        bpy_material.blend_method = 'HASHED'
        bpy_material.shadow_method = 'HASHED'
        diffuse = material_node_tree.nodes.new('ShaderNodeMixRGB')
        diffuse.location.x -= shader_node.width + 50
        diffuse.blend_type = 'COLOR'

        for i, bpy_image in enumerate(bpy_images_of_layer):
            texture_mat_node = material_node_tree.nodes.new('ShaderNodeTexImage')
            texture_mat_node.location.x -= shader_node.width + 350
            texture_mat_node.location.y += 200 - 200 * i
            texture_mat_node.image = bpy_image
            if i == 0:
                material_node_tree.links.new(texture_mat_node.outputs.get("Color"), diffuse.inputs.get("Color1"))
                material_node_tree.links.new(diffuse.outputs.get("Color"), color_input_socket)
                material_node_tree.links.new(texture_mat_node.outputs.get("Alpha"), shader_node.inputs.get("Alpha"))
            elif i == 1:
                normal_map = material_node_tree.nodes.new('ShaderNodeNormalMap')
                normal_map.location.x -= shader_node.width + 50
                normal_map.location.y += 200 - 200 * i
                material_node_tree.links.new(texture_mat_node.outputs.get("Color"), normal_map.inputs.get("Color"))
                material_node_tree.links.new(normal_map.outputs.get("Normal"), shader_node.inputs.get("Normal"))
            elif i == 2:
                orm = material_node_tree.nodes.new('ShaderNodeSeparateRGB')
                roughthness_inv = material_node_tree.nodes.new("ShaderNodeMath")
                roughthness_inv.operation = 'SUBTRACT'
                roughthness_inv.location.x -= shader_node.width
                roughthness_inv.location.y += 200 - 200 * i
                roughthness_inv.inputs[0].default_value = 1


                orm.location.x -= shader_node.width + 50
                orm.location.y += 200 - 200 * i
                material_node_tree.links.new(texture_mat_node.outputs.get("Color"), orm.inputs.get("Image"))
                # I don't currently know how to do occlusion
                # material_node_tree.links.new(orm.outputs.get("G"), roughthness_inv.inputs.get("Value2"))
                material_node_tree.links.new(orm.outputs.get("G"), roughthness_inv.inputs[1])
                # material_node_tree.links.new(roughthness_inv.outputs.get("Value"), shader_node.inputs.get("Roughness"))
                material_node_tree.links.new(roughthness_inv.outputs[0], shader_node.inputs.get("Roughness"))
                material_node_tree.links.new(orm.outputs.get("B"), shader_node.inputs.get("Metallic"))
                material_node_tree.links.new(texture_mat_node.outputs.get("Alpha"), diffuse.inputs.get("Fac"))
            elif i == 3:
                material_node_tree.links.new(texture_mat_node.outputs.get("Color"), shader_node.inputs.get("Emission"))
            elif i == 4:
                team_color = material_node_tree.nodes.new('ShaderNodeRGB')
                team_color.outputs[0].default_value = (1, 0, 0, 1)
                team_color.location.x -= shader_node.width + diffuse.width + 50
                # material_node_tree.links.new(texture_mat_node.outputs.get("Color"), diffuse.inputs.get("Color2"))
                material_node_tree.links.new(team_color.outputs.get("Color"), diffuse.inputs.get("Color2"))
            # else:
            # skip the environmental map, possibly change the world's map to it
            print(bpy_image.filepath, " at place ", i)
    else:
        for i, bpy_image in enumerate(bpy_images_of_layer):
            texture_mat_node = material_node_tree.nodes.new('ShaderNodeTexImage')
            texture_mat_node.location.x -= shader_node.width + 50
            texture_mat_node.location.y += 200 - 100 * i
            texture_mat_node.image = bpy_image
            material_node_tree.links.new(texture_mat_node.outputs.get("Color"), color_input_socket)
            # bpy_material.texture_slots.add()
            # bpyTexture = bpy.data.textures.new(name=material_name, type='IMAGE')
            # bpy_material.texture_slots[texture_slot_index].texture = bpyTexture
            # texture_slot_index += 1
            # bpyTexture.image = bpy_image
    return bpy_material


def get_texture_ext(texture_exc: str):
    if texture_exc == '':
        print("No texture extension to replace blp with set in addon preferences")
        texture_exc = 'png'
    if texture_exc[0] != '.':
        texture_exc = '.' + texture_exc
    return texture_exc


def get_image(folders: List[str], team_color: str, texture: WarCraft3Texture, texture_exc: str):
    if texture.replaceable_id == 1:  # Team Color
        image_file = constants.TEAM_COLOR_IMAGES[team_color]
    elif texture.replaceable_id == 2:  # Team Glow
        image_file = constants.TEAM_GLOW_IMAGES[team_color]
    else:
        image_file = texture.image_file_name

    if image_file.endswith(".blp"):
        image_file = image_file.split(".blp")[0] + texture_exc

    image_file = image_file.replace("/", os.path.sep)
    image_file = image_file.replace("\\", os.path.sep)
    file_path_parts = image_file.split(os.path.sep)

    file_name = file_path_parts[-1].split('.')[0]
    bpy_image = bpy.data.images.new(file_name, 0, 0)
    bpy_image.source = 'FILE'
    print("loading:", image_file)
    # print("loading:", file_name, " file_path_parts len = ", len(file_path_parts))
    # war3mapImported / NightElf_Hippogryph_Emissive2

    for i in range(len(file_path_parts)):
        # file_path = Path(resource_folder + image_file)
        # split = image_file.split("\\", i)
        split = image_file.split(os.path.sep, i)
        image_file = split[len(split)-1]

        for folder in folders:
            file_path = check_file_path(folder, image_file)
            # print("\t checking folder: ", folder)
            # print("\t\tfile_path: \"" + file_path + "\", len: ", len(file_path))
            # if file_path != '':
            if len(file_path) > 0:
                bpy_image.filepath = file_path
                # print("\t\treturning: \"" + file_path + "\"")
                return bpy_image

    bpy_image.filepath = image_file
    return bpy_image


def get_folders(alt_folder: str, resource_folder: str, model_file: str):
    if resource_folder == '':
        print("No resource folder set in addon preferences")

    elif not resource_folder.endswith(os.path.sep):
        # elif not resource_folder.endswith("\\"):
        resource_folder += os.path.sep
    if alt_folder == '':
        print("No alt resource folder set in addon preferences")
    elif not alt_folder.endswith(os.path.sep):
        alt_folder += os.path.sep

    model_folder = str(Path(model_file).parent)
    if not model_folder.endswith(os.path.sep):
        model_folder += os.path.sep
    # print("model folder:", model_folder)
    textures1 = "Textures" + os.path.sep
    textures2 = "textures" + os.path.sep
    folders1 = [model_folder,
                model_folder + textures1, model_folder + textures2,
                resource_folder, alt_folder,
                resource_folder + textures1, resource_folder + textures2,
                alt_folder + textures1, alt_folder + textures2]
    folders = []
    for folder in folders1:
        f = check_file_path(folder, "")
        if f != '' and f not in folders:
            folders.append(f)
    return folders


def check_file_path(folder: str, image_file: str):
    # file_path = folder + os.path.sep + image_file
    file_path = folder + image_file
    # print("checking", file_path)
    try:
        if Path(file_path).exists():
            # print("got valid", file_path)
            return file_path
    except OSError:
        print("bad path:", file_path)
    return ''
