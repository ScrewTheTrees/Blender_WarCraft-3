from typing import Optional

from io_scene_warcraft_3.classes.WarCraft3Transformation import WarCraft3Transformation


class WarCraft3Node:
    def __init__(self, node_type: str):
        self.node_type = node_type
        self.name: str = ""
        self.id: int = -1
        self.parent: Optional[int] = None
        self.translations: Optional[WarCraft3Transformation] = None
        self.rotations: Optional[WarCraft3Transformation] = None
        self.scalings: Optional[WarCraft3Transformation] = None
