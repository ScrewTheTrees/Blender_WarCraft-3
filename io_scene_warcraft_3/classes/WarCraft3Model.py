from typing import List

from io_scene_warcraft_3.classes.WarCraft3GeosetAnimation import WarCraft3GeosetAnimation
from io_scene_warcraft_3.classes.WarCraft3Material import WarCraft3Material
from io_scene_warcraft_3.classes.WarCraft3Geoset import WarCraft3Geoset
from io_scene_warcraft_3.classes.WarCraft3Sequence import WarCraft3Sequence
from io_scene_warcraft_3.classes.WarCraft3Texture import WarCraft3Texture


class WarCraft3Model:
    def __init__(self):
        self.file = ''
        self.version = 800
        self.name = None
        self.geosets: List[WarCraft3Geoset] = []
        self.materials: List[WarCraft3Material] = []
        self.textures: List[WarCraft3Texture] = []
        # self.nodes: List[]  = []
        self.nodes = []
        self.sequences: List[WarCraft3Sequence] = []
        self.geoset_animations: List[WarCraft3GeosetAnimation] = []
        self.pivot_points: List[List[float]] = []

    def normalize_meshes_names(self):
        for mesh in self.geosets:
            mesh.name = self.name
