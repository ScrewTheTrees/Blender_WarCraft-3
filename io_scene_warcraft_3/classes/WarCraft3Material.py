from typing import List

from io_scene_warcraft_3.classes.WarCraft3Layer import WarCraft3Layer


class WarCraft3Material:
    def __init__(self):
        self.layers: List[WarCraft3Layer] = []
        self.hd: bool = False
