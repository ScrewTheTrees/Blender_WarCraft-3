from typing import List, Tuple

from . import binary_reader
from ..classes.WarCraft3Model import WarCraft3Model


def parse_pivot_points(data: bytes) -> List[Tuple[float]]:
    data_size = len(data)
    r = binary_reader.Reader(data)

    if data_size % 12 != 0:
        raise Exception('bad Pivot Point data (size % 12 != 0)')

    pivot_points_count = data_size // 12

    pivot_points: List[Tuple[float]] = []
    for _ in range(pivot_points_count):
        point: Tuple[float] = r.getf('<3f')
        pivot_points.append(point)
    return pivot_points
