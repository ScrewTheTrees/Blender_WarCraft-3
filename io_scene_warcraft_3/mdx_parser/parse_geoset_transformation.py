from .binary_reader import Reader
from ..classes.WarCraft3Transformation import WarCraft3Transformation
from .. import constants

# format:
# scaling, translation: '<3f'
# rotation: '<4f'


def parse_geoset_transformation(r: Reader, value_format: str) -> WarCraft3Transformation:
    transformation = WarCraft3Transformation()
    transformation.tracks_count = r.getf('<I')[0]
    transformation.interpolation_type = r.getf('<I')[0]
    global_sequence_id = r.getf('<I')[0]

    for _ in range(transformation.tracks_count):
        time: int = r.getf('<I')[0]
        values = r.getf(value_format)    # translation values

        if value_format == '<4f':
            values = (values[3], values[0], values[1], values[2])
            # print(values)

        transformation.times.append(time)
        transformation.values.append(values)

        if transformation.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            in_tan = r.getf(value_format)
            out_tan = r.getf(value_format)

    return transformation
