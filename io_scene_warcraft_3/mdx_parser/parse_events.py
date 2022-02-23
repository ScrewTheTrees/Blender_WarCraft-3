from typing import List

from ..classes.WarCraft3Event import WarCraft3Event
from .. import constants
from . import binary_reader
from .parse_node import parse_node
from .parse_tracks import parse_tracks
from ..classes.WarCraft3Node import WarCraft3Node


def parse_events(data: bytes) -> List[WarCraft3Node]:
    data_size = len(data)
    r = binary_reader.Reader(data)

    nodes: List[WarCraft3Node] = []
    while r.offset < data_size:

        event = WarCraft3Event()
        parse_node(r, event)

        if r.offset < data_size:
            chunk_id = r.gets(4)

            if chunk_id == constants.CHUNK_TRACKS:
                parse_tracks(r)
            else:
                r.offset -= 4

        nodes.append(event)
    return nodes
