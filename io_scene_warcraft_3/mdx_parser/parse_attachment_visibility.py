from ..classes.WarCraft3Transformation import WarCraft3Transformation
from .. import constants


def parse_attachment_visibility(r):
    chunk_id = r.getid(constants.CHUNK_ATTACHMENT_VISIBILITY)
    visibility = WarCraft3Transformation()
    visibility.tracks_count = r.getf('<I')[0]
    visibility.interpolation_type = r.getf('<I')[0]
    global_sequence_id = r.getf('<I')[0]

    for _ in range(visibility.tracks_count):
        time: int = r.getf('<I')[0]
        value: float = r.getf('<f')[0]    # visibility value
        visibility.times.append(time)
        visibility.values.append(value)

        if visibility.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            in_tan = r.getf('<f')[0]
            out_tan = r.getf('<f')[0]
