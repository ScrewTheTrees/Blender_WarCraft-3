from ..classes.MDXImportProperties import MDXImportProperties
from ..classes.WarCraft3Model import WarCraft3Model
from .. import constants
from ..importer import importer
from . import binary_reader
from .parse_attachments import parse_attachments
from .parse_bones import parse_bones
from .parse_collision_shapes import parse_collision_shapes
from .parse_events import parse_events
from .parse_geoset_animations import parse_geoset_animations
from .parse_geosets import parse_geosets
from .parse_helpers import parse_helpers
from .parse_materials import parse_materials
from .parse_model import parse_model
from .parse_pivot_points import parse_pivot_points
from .parse_sequences import parse_sequences
from .parse_textures import parse_textures
from .parse_version import parse_version


def parse_mdx(data: bytes, import_properties: MDXImportProperties):
    data_size = len(data)
    r = binary_reader.Reader(data)
    r.getid(constants.CHUNK_MDX_MODEL)
    model = WarCraft3Model()
    model.file = import_properties.mdx_file_path

    while r.offset < data_size:
        chunk_id = r.getid(constants.SUB_CHUNKS_MDX_MODEL, debug=True)
        chunk_size = r.getf('<I')[0]
        chunk_data: bytes = data[r.offset: r.offset + chunk_size]
        r.skip(chunk_size)

        if chunk_id == constants.CHUNK_VERSION:
            model.version = parse_version(chunk_data)
        elif chunk_id == constants.CHUNK_GEOSET:
            model.geosets.extend(parse_geosets(chunk_data, model.version))
        elif chunk_id == constants.CHUNK_TEXTURE:
            model.textures.extend(parse_textures(chunk_data))
        elif chunk_id == constants.CHUNK_MATERIAL:
            model.materials.extend(parse_materials(chunk_data, model.version))
        elif chunk_id == constants.CHUNK_MODEL:
            model.name = parse_model(chunk_data)
        elif chunk_id == constants.CHUNK_BONE:
            model.nodes.extend(parse_bones(chunk_data))
        elif chunk_id == constants.CHUNK_PIVOT_POINT:
            model.pivot_points.extend(parse_pivot_points(chunk_data))
        elif chunk_id == constants.CHUNK_HELPER:
            model.nodes.extend(parse_helpers(chunk_data))
        elif chunk_id == constants.CHUNK_ATTACHMENT:
            model.nodes.extend(parse_attachments(chunk_data))
        elif chunk_id == constants.CHUNK_EVENT_OBJECT:
            model.nodes.extend(parse_events(chunk_data))
        elif chunk_id == constants.CHUNK_COLLISION_SHAPE:
            model.nodes.extend(parse_collision_shapes(chunk_data))
        elif chunk_id == constants.CHUNK_SEQUENCE:
            model.sequences.extend(parse_sequences(chunk_data))
        elif chunk_id == constants.CHUNK_GEOSET_ANIMATION:
            model.geoset_animations.extend(parse_geoset_animations(chunk_data))

    importer.load_warcraft_3_model(model, import_properties)
