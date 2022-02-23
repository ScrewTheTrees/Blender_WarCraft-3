from ..classes.WarCraft3CollisionShape import WarCraft3CollisionShape
from .parse_node import parse_node


def parse_collision_shapes(data: str) -> WarCraft3CollisionShape:
    collision_shape = WarCraft3CollisionShape()
    parse_node(data, collision_shape)
    return collision_shape
