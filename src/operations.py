from PIL import Image
from psd_tools import PSDImage
from typing import Optional


def extract(
    psd: PSDImage, ignore_background_layer: bool = True
) -> list[tuple[str, Image]]:
    return [
        (layer.name, layer.composite())
        for layer in psd
        if (layer.name != "Background" or ignore_background_layer)
    ]


def atlas(
    psd: PSDImage,
    target_res: Optional[tuple[int, int]] = None,
    ignore_background_layer: bool = True,
) -> Image:
    layers = [layer for _, layer in extract(psd, ignore_background_layer)]

    if target_res is not None:
        layers = [layer.resize(target_res, Image.BILINEAR) for layer in layers]

    total_width = sum(img.width for img in layers)
    assert next(iter(layers), None), "PSD is empty"
    first_height = next(iter(layers), None).height

    tilemap = Image.new("RGBA", (total_width, first_height), (0, 0, 0, 0))
    x = 0
    for img in layers:
        tilemap.paste(img, (x, 0))
        x += img.width

    return tilemap
