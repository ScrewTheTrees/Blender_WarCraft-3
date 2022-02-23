from ..classes.WarCraft3Attachment import WarCraft3Attachment
from .parse_node import parse_node
from ..classes.WarCraft3Model import WarCraft3Model


def parse_attachments(data: str) -> WarCraft3Attachment:
    attachment = WarCraft3Attachment()
    parse_node(data, attachment)
    return attachment
