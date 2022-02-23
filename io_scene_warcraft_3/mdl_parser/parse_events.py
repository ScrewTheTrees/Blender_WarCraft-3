from ..classes.WarCraft3Event import WarCraft3Event
from .parse_node import parse_node


def parse_events(data: str) -> WarCraft3Event:
    event = WarCraft3Event()
    parse_node(data, event)
    return event
