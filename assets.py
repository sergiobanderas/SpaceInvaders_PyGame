import os

import pygame

# The assets folder lives next to this file, no matter where the game is launched from
ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

_image_cache = {}  # Images already loaded, so each file is read from disk only once


def find_asset(name):
    """Return the full path of a file inside assets/, searching every subfolder"""
    for folder, _subfolders, files in os.walk(ASSETS_PATH):
        if name in files:
            return os.path.join(folder, name)
    raise FileNotFoundError(f"'{name}' not found inside {ASSETS_PATH}")


def load_image(name, width=None):
    """Load an image with transparency. If width is given, scale it keeping its proportions"""
    key = (name, width)
    if key not in _image_cache:
        image = pygame.image.load(find_asset(name)).convert_alpha()
        if width is not None:
            height = round(image.get_height() * width / image.get_width())
            image = pygame.transform.smoothscale(image, (width, height))
        _image_cache[key] = image
    return _image_cache[key]
