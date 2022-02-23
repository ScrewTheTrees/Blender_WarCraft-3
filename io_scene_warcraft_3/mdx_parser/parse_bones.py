from typing import List

from ..classes.WarCraft3Bone import WarCraft3Bone
from . import binary_reader
from .parse_node import parse_node
from ..classes.WarCraft3Node import WarCraft3Node


def parse_bones(data: bytes) -> List[WarCraft3Node]:
    r = binary_reader.Reader(data)
    data_size = len(data)

    nodes: List[WarCraft3Node] = []
    while r.offset < data_size:
        bone = WarCraft3Bone()
        parse_node(r, bone)
        bone.geoset_id = r.getf('<I')[0]
        geoset_animation_id = r.getf('<I')[0]
        nodes.append(bone)
    return nodes
