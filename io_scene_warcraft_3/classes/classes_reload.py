if "MDXImportProperties" in locals():
    print("reload classes")
    import importlib
    from io_scene_warcraft_3.classes import (
        MDXImportProperties,
        WarCraft3Attachment,
        WarCraft3Bone,
        WarCraft3CollisionShape,
        WarCraft3Event,
        WarCraft3GeosetAnimation,
        WarCraft3Transformation,
        WarCraft3Helper,
        WarCraft3Layer,
        WarCraft3Material,
        WarCraft3Geoset,
        WarCraft3Model,
        WarCraft3Node,
        WarCraft3Sequence,
        WarCraft3Texture)
    importlib.reload(MDXImportProperties)
    importlib.reload(WarCraft3Attachment)
    importlib.reload(WarCraft3Bone)
    importlib.reload(WarCraft3CollisionShape)
    importlib.reload(WarCraft3Event)
    importlib.reload(WarCraft3GeosetAnimation)
    importlib.reload(WarCraft3Transformation)
    importlib.reload(WarCraft3Helper)
    importlib.reload(WarCraft3Layer)
    importlib.reload(WarCraft3Material)
    importlib.reload(WarCraft3Geoset)
    importlib.reload(WarCraft3Model)
    importlib.reload(WarCraft3Node)
    importlib.reload(WarCraft3Sequence)
    importlib.reload(WarCraft3Texture)