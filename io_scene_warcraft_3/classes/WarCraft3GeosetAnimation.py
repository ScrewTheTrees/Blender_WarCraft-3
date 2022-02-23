from typing import Optional

from io_scene_warcraft_3.classes.WarCraft3Transformation import WarCraft3Transformation


class WarCraft3GeosetAnimation:
    def __init__(self):
        self.geoset_id: int = 0
        self.animation_color: Optional[WarCraft3Transformation] = None
        self.animation_alpha: Optional[WarCraft3Transformation] = None
