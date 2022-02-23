from typing import Union, List

from ..classes.WarCraft3Helper import WarCraft3Helper
from . import binary_reader
from .parse_node import parse_node
from ..classes.WarCraft3Node import WarCraft3Node


def parse_helpers(data: bytes):
    data_size = len(data)
    r = binary_reader.Reader(data)

    nodes: List[WarCraft3Node] = []
    while r.offset < data_size:
        helper = WarCraft3Helper()
        parse_node(r, helper)
        nodes.append(helper)
    return nodes

