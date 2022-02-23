from typing import List, Optional


class WarCraft3Vertex:
    def __init__(self):
        self.pos: List[float]
        self.normal: List[float]
        self.uv: List[float]
        self.tangent: Optional[List[float]]
        self.matrix: Optional[int] = None
        self.bone_list: Optional[List[str]] = None
        self.weight_list: Optional[List[int]] = None
