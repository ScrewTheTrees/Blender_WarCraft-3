from .binary_reader import Reader
from ..classes.WarCraft3Transformation import WarCraft3Transformation
from .. import constants


def parse_geoset_alpha(r: Reader):
    alpha = WarCraft3Transformation()
    alpha.tracks_count = r.getf('<I')[0]
    alpha.interpolation_type = r.getf('<I')[0]
    global_sequence_id = r.getf('<I')[0]
    for _ in range(alpha.tracks_count):
        time = r.getf('<I')[0]
        value = r.getf('<f')[0]    # alpha value
        alpha.times.append(time)
        alpha.values.append(value)
        if alpha.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            in_tan = r.getf('<f')[0]
            out_tan = r.getf('<f')[0]
    return alpha
