from ..classes.MDXImportProperties import MDXImportProperties
from ..classes.WarCraft3Model import WarCraft3Model
from ..importer import importer
from .mdl_reader import Reader
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


def parse_mdl(data: str, import_properties: MDXImportProperties):
    reader = Reader(data)
    model = WarCraft3Model()
    model.file = import_properties.mdx_file_path
    data_chunks = reader.chunks
    for chunk in data_chunks:
        # print("new data chunk")
        label = chunk.split(" ", 1)[0]
        # print(label)
        if label == "Version":
            model.version = parse_version(chunk)
        elif label == "Geoset":
            model.geosets.append(parse_geosets(chunk))
        elif label == "Textures":
            model.textures.extend(parse_textures(chunk))
        elif label == "Materials":
            model.materials.extend(parse_materials(chunk))
        elif label == "Model":
            model.name = parse_model(chunk)
        elif label == "Bone":
            model.nodes.append(parse_bones(chunk))
        elif label == "PivotPoints":
            model.pivot_points.extend(parse_pivot_points(chunk))
        elif label == "Helper":
            model.nodes.append(parse_helpers(chunk))
        elif label == "Attachment":
            model.nodes.append(parse_attachments(chunk))
        elif label == "EventObject":
            model.nodes.append(parse_events(chunk))
        elif label == "CollisionShape":
            model.nodes.append(parse_collision_shapes(chunk))
        elif label == "Sequences":
            model.sequences.extend(parse_sequences(chunk))
        elif label == "GeosetAnim":
            model.geoset_animations.append(parse_geoset_animations(chunk))
        elif label == "ParticleEmitter2":
            print("Particles not implemented yet")
        elif label == "TextureAnims":
            print("TextureAnims not implemented yet")
        elif label == "RibbonEmitter":
            print("RibbonEmitter not implemented yet")
        elif label == "Camera":
            print("Camera not implemented yet")
        elif label == "Ugg":
            print("X not implemented yet")
        elif label == "Ugg":
            print("X not implemented yet")

    importer.load_warcraft_3_model(model, import_properties)


# this is for commandline testing
def parse_mdl2(data):
    print("parse_mdl2")
    reader = Reader(data)
    model = WarCraft3Model()
    data_chunks = reader.chunks
    # print(data_chunks)
    for chunk in data_chunks:
        label = chunk.split(" ", 1)[0]
        # print("label: ", label)
        if label == "Version":
            print("parse: Version")
            model.version = parse_version(chunk)

        elif label == "Geoset":
            print("parse: Geoset")
            model.geosets.append(parse_geosets(chunk))

        elif label == "Textures":
            print("parse: Textures")
            model.textures.extend(parse_textures(chunk))

        elif label == "Materials":
            print("parse: Materials")
            model.materials.extend(parse_materials(chunk))

        elif label == "Model":
            print("parse: Model")
            model.name = parse_model(chunk)

        elif label == "Bone":
            # print("parse: Bone")
            model.nodes.append(parse_bones(chunk))

        elif label == "PivotPoints":
            print("parse: PivotPoints")
            model.pivot_points.extend(parse_pivot_points(chunk))

        elif label == "Helper":
            # print("parse: Helper")
            model.nodes.append(parse_helpers(chunk))

        elif label == "Attachment":
            # print("parse: Attachment")
            model.nodes.append(parse_attachments(chunk))

        elif label == "EventObject":
            # print("parse: EventObject")
            model.nodes.append(parse_events(chunk))

        elif label == "CollisionShape":
            # print("parse: CollisionShape")
            model.nodes.append(parse_collision_shapes(chunk))

        elif label == "Sequences":
            print("parse: Sequences")
            model.sequences.extend(parse_sequences(chunk))

        elif label == "GeosetAnim":
            print("parse: GeosetAnim")
            model.geoset_animations.append(parse_geoset_animations(chunk))

    importer.load_warcraft_3_model2(model)
