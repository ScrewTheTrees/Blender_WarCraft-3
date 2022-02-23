from typing import List

from . import binary_reader
from .parse_geometry import parse_geometry
from ..classes.WarCraft3Geoset import WarCraft3Geoset


def parse_geosets(data: bytes, version: int) -> List[WarCraft3Geoset]:
    data_size = len(data)
    r = binary_reader.Reader(data)

    geosets: List[WarCraft3Geoset] = []
    while r.offset < data_size:
        inclusive_size = r.getf('<I')[0]
        geo_data_size = inclusive_size - 4
        geo_data = data[r.offset : (r.offset + geo_data_size)]
        r.skip(geo_data_size)
        mesh = parse_geometry(geo_data, version)
        geosets.append(mesh)
    return geosets

