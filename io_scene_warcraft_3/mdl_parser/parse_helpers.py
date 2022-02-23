from ..classes.WarCraft3Helper import WarCraft3Helper
from .parse_node import parse_node


def parse_helpers(data: str) -> WarCraft3Helper:
    helper = WarCraft3Helper()
    parse_node(data, helper)

    return helper
