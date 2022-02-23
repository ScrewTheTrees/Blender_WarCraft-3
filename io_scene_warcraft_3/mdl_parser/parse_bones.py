from ..classes.WarCraft3Bone import WarCraft3Bone
from .mdl_reader import get_between
from .parse_node import parse_node


def parse_bones(data: str) -> WarCraft3Bone:
    bone = WarCraft3Bone()
    bone.geoset_id = 0
    geoset_id = get_between(data, "GeosetId", ",")

    if geoset_id != "Multiple":
        bone.geoset_id = int(geoset_id)

    geoset_animation_id = get_between(data, "GeosetAnimId", ",")
    parse_node(data, bone)

    return bone
