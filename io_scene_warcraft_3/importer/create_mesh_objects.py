from typing import List

import bpy
from bpy.types import Material

from io_scene_warcraft_3.classes.WarCraft3Model import WarCraft3Model


def create_mesh_objects(model: WarCraft3Model, bpy_materials: List[Material]):
    print("creating mesh")
    bpy_objects = []

    for warCraft3Geoset in model.geosets:
        bpy_mesh = bpy.data.meshes.new(warCraft3Geoset.name)
        bpy_object = bpy.data.objects.new(warCraft3Geoset.name, bpy_mesh)
        bpy.context.scene.collection.objects.link(bpy_object)
        bpy_mesh.from_pydata(warCraft3Geoset.vertices, (), warCraft3Geoset.triangles)
        bpy_mesh.uv_layers.new()
        uv_layer = bpy_mesh.uv_layers.active.data

        for tris in bpy_mesh.polygons:
            for loopIndex in range(tris.loop_start, tris.loop_start + tris.loop_total):
                vertex_index = bpy_mesh.loops[loopIndex].vertex_index
                uv_layer[loopIndex].uv = (warCraft3Geoset.uvs[vertex_index])

        bpy_material = bpy_materials[warCraft3Geoset.material_id]
        bpy_mesh.materials.append(bpy_material)

        for vertexGroupId in warCraft3Geoset.vertex_groups_ids:
            bpy_object.vertex_groups.new(name=str(vertexGroupId))

        for vertex_index in range(len(warCraft3Geoset.skin_weights)):
            skin_weight = warCraft3Geoset.skin_weights[vertex_index]
            # if skin_weight[0] != 255 and skin_weight[4] != 0:
            #     bpy_object.vertex_groups.get(str(skin_weight[0])).add([vertex_index, ], skin_weight[4]/255.0, 'REPLACE')
            # if skin_weight[1] != 255 and skin_weight[5] != 0:
            #     bpy_object.vertex_groups.get(str(skin_weight[1])).add([vertex_index, ], skin_weight[5]/255.0, 'REPLACE')
            # if skin_weight[2] != 255 and skin_weight[6] != 0:
            #     bpy_object.vertex_groups.get(str(skin_weight[2])).add([vertex_index, ], skin_weight[6]/255.0, 'REPLACE')
            # if skin_weight[3] != 255 and skin_weight[7] != 0:
            #     bpy_object.vertex_groups.get(str(skin_weight[3])).add([vertex_index, ], skin_weight[7]/255.0, 'REPLACE')

            # RMS had a bug which filled some list with -1 resulting in them being filled with 255 in the saved models
            if sum(skin_weight[4:]) > 255:
                print("Potentially invalid skin weight data")
            for i in range(0, 4):
                if skin_weight[i] != 255 and skin_weight[i + 4] != 0:
                    bpy_object.vertex_groups.get(str(skin_weight[i])).add([vertex_index, ], skin_weight[i + 4] / 255.0, 'REPLACE')

            # if skin_weight[4] != 0:
            #     bpy_object.vertex_groups.get(str(skin_weight[0])).add([vertex_index, ], skin_weight[4]/255.0, 'REPLACE')
            # if skin_weight[5] != 0:
            #     bpy_object.vertex_groups.get(str(skin_weight[1])).add([vertex_index, ], skin_weight[5]/255.0, 'REPLACE')
            # if skin_weight[6] != 0:
            #     bpy_object.vertex_groups.get(str(skin_weight[2])).add([vertex_index, ], skin_weight[6]/255.0, 'REPLACE')
            # if skin_weight[7] != 0:
            #     bpy_object.vertex_groups.get(str(skin_weight[3])).add([vertex_index, ], skin_weight[7]/255.0, 'REPLACE')

        for vertex_index, vertexGroupIds in enumerate(warCraft3Geoset.vertex_groups):
            for vertexGroupId in vertexGroupIds:
                bpy_object.vertex_groups.get(str(vertexGroupId)).add([vertex_index, ], 1.0, 'REPLACE')

        bpy_objects.append(bpy_object)
    return bpy_objects


