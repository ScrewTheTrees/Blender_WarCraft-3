from typing import List, Optional

from io_scene_warcraft_3.classes.WarCraft3Vertex import WarCraft3Vertex


class WarCraft3Geoset:
    def __init__(self):
        self.name = None
        self.wc3_vertices: List[WarCraft3Vertex] = []
        self.vertices: List[List[float]] = []
        self.normals: [float] = []
        self.triangles: [float] = []
        self.uvs = []
        self.material_id = 0
        self.vertex_groups: List[List[int]] = []
        self.vertex_groups_ids: Optional[List[int]] = None
        self.skin_weights: List[List[int]] = []

    # def get_save_string(self, settings):
    #     geoset_strings: [str] = ["Geoset {"]
    #
    #     vertex_strings: [str] = []
    #     for vertex in self.vertices:
    #         # vertex_strings.append("\t\t{%s, %s, %s},\n" % tuple(map(f2s, vertex[0])))
    #         vertex_strings.append("\t\t{%s, %s, %s}" % tuple(map(self.f2s, vertex[0])))
    #
    #     geoset_strings.append("\tVertices %d {" % len(self.vertices))
    #     geoset_strings.append(",\n".join(vertex_strings))
    #     geoset_strings.append("\t}")
    #
    #     # Normals
    #     normal_strings: [str] = []
    #     for normal in self.normals:
    #         normal_strings.append("\t\t{%s, %s, %s}" % tuple(map(self.f2s, normal[1])))
    #
    #     geoset_strings.append("\tNormals %d {" % len(self.vertices))
    #     geoset_strings.append(",\n".join(normal_strings))
    #     geoset_strings.append("\t}")
    #
    #     # TVertices
    #     tvertex_strings: [str] = []
    #
    #     for tvertex in self.uvs:
    #         tvertex_strings.append("\t\t{%s, %s}" % tuple(map(self.f2s, tvertex[2])))
    #     "\t}\n"
    #
    #     geoset_strings.append("\tTVertices %d {" % len(self.vertices))
    #     geoset_strings.append(",\n".join(tvertex_strings))
    #     geoset_strings.append("\t}")
    #
    #     # VertexGroups
    #     vertex_strings: [str] = []
    #
    #     if not settings.use_skinweights:
    #         for vertex in self.vertices:
    #             vertex_strings.append("\t\t%d" % vertex[3])
    #     "\t}\n"
    #
    #     geoset_strings.append("\tVertexGroup {")
    #     geoset_strings.append(",\n".join(vertex_strings))
    #     geoset_strings.append("\t}")
    #
    #     tangent_strings: [str] = []
    #     skin_strings: [str] = []
    #     if settings.use_skinweights:
    #         # Tangents
    #         for normal in self.vertices:
    #             # "\t\t{%s, %s, %s, -1},\n" % tuple(map(f2s, normal[1]))
    #             tangents = tuple(map(self.f2s, normal[1])) + tuple({str(sum(normal[1]) / abs(sum(normal[1])))})
    #             tangent_strings.append("\t\t{%s, %s, %s, %s}" % tuple(tangents))
    #
    #         geoset_strings.append("\tTangents %d {" % len(self.vertices))
    #         geoset_strings.append(",\n".join(tangent_strings))
    #         geoset_strings.append("\t}")
    #
    #         # SkinWeights
    #         for skin in self.vertices:
    #             skin_strings.append("\t\t{%s, %s, %s, %s, %s, %s, %s, %s}" % tuple(skin[-1]))
    #
    #         geoset_strings.append("\tSkinWeights %d {" % len(self.vertices))
    #         geoset_strings.append(",\n".join(skin_strings))
    #         geoset_strings.append("\t}")
    #
    #     # Faces
    #
    #     geoset_strings.append("\tFaces %d %d {" % (len(self.triangles), len(self.triangles) * 3))
    #     geoset_strings.append("\t\tTriangles {")
    #     geoset_strings.append("\t\t\t{")
    #
    #     triangle_strings: [str] = []
    #     for triangle in self.triangles:
    #         triangle_strings.append("%d, %d, %d" % triangle[:])
    #     geoset_strings.append(", ".join(triangle_strings))
    #     geoset_strings.append("\t\t\t},")
    #     geoset_strings.append("\t\t}")
    #
    #     # "\t\tTriangles {\n"
    #     # for triangle in triangles:
    #     #     "\t\t\t{%d, %d, %d},\n" % triangle[:]
    #     # "\t\t}\n"
    #     geoset_strings.append("\t}")
    #
    #
    #     # "\tGroups %d %d {\n" % (len(self.matrices), sum(len(mtrx) for mtrx in self.matrices))
    #     # for matrix in self.matrices:
    #     #     "\t\tMatrices {%s},\n" % ','.join(str(model.object_indices[g]) for g in matrix)
    #     # "\t}\n"
    #     #
    #     # fw("\tMinimumExtent {%s, %s, %s},\n" % tuple(map(f2s, min_extent)))
    #     # fw("\tMaximumExtent {%s, %s, %s},\n" % tuple(map(f2s, max_extent)))
    #     # fw("\tBoundsRadius %s,\n" % f2s(calc_bounds_radius(min_extent, max_extent)))
    #     #
    #     # for sequence in model.sequences:
    #     #     fw("\tAnim {\n")
    #     #
    #     #     # As of right now, we just use the bounds.
    #     #     fw("\t\tMinimumExtent {%s, %s, %s},\n" % tuple(map(f2s, min_extent)))
    #     #     fw("\t\tMaximumExtent {%s, %s, %s},\n" % tuple(map(f2s, max_extent)))
    #     #     fw("\t\tBoundsRadius %s,\n" % f2s(calc_bounds_radius(min_extent, max_extent)))
    #     #
    #     #     fw("\t}\n")
    #
    #     geoset_strings.append("\tMaterialID %d," % self.material_id)
    #     geoset_strings.append("\tSelectionGroup 0,")
    #     geoset_strings.append("}")
    #
    # def f2s(self, value):
    #     return ('%.6f' % value).rstrip('0').rstrip('.')
