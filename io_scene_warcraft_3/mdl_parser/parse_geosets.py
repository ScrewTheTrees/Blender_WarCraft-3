from .mdl_reader import extract_bracket_content, chunkifier, get_between
from .parse_geometry import parse_geometry
from ..classes.WarCraft3Geoset import WarCraft3Geoset


def parse_geosets(data: str) -> WarCraft3Geoset:
    geoset_data_internal = extract_bracket_content(data)
    geoset_data_chunks = chunkifier(geoset_data_internal)

    geoset: WarCraft3Geoset = parse_geometry(geoset_data_chunks)

    if data.find("MaterialID") > -1:
        geoset.material_id = int(get_between(data, "MaterialID ", ","))

    # for chunk in geoset_data_chunks:
    #     label = chunk.split(" ", 1)[0]
    #     if label == "Anim":
    #         print("Anim!")
    #         parse_geoset_animations(chunk, model)

    return geoset
