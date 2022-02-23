from typing import List

from . import binary_reader
from .parse_attachment import parse_attachment
from ..classes.WarCraft3Model import WarCraft3Model
from ..classes.WarCraft3Node import WarCraft3Node


def parse_attachments(data: bytes):
    data_size = len(data)
    r = binary_reader.Reader(data)

    nodes: List[WarCraft3Node] = []
    while r.offset < data_size:
        inclusive_size = r.getf('<I')[0]
        attach_data_size = inclusive_size - 4
        attach_data = data[r.offset : r.offset + attach_data_size]
        r.skip(attach_data_size)
        attachment = parse_attachment(attach_data)
        nodes.append(attachment)
    return nodes
