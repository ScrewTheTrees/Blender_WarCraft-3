from typing import List

from ..classes.WarCraft3Model import WarCraft3Model
from ..classes.WarCraft3Texture import WarCraft3Texture
from .mdl_reader import extract_bracket_content, chunkifier


def parse_textures(data: str) -> List[WarCraft3Texture]:
    textures_string = extract_bracket_content(data)
    texture_chunks = chunkifier(textures_string)

    textures: List[WarCraft3Texture] = []
    for texture_chunk in texture_chunks:
        label = texture_chunk.strip().split(" ")[0]
        if label == "Bitmap":
            texture = WarCraft3Texture()
            texture_info = extract_bracket_content(texture_chunk)
            label = texture_info.strip().split(" ")[0]

            if label == "Image":
                texture.image_file_name = texture_info.strip().split("\"")[1]

            if label == "ReplaceableId":
                texture.replaceable_id = int(texture_info.strip().replace(",", "").split(" ")[1])

            textures.append(texture)
    return textures
