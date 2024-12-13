import os
from pathlib import Path

from ..resource_manager import ResourceManager

import pygame

_image_manager = ResourceManager[pygame.Surface]("pygame_images")
_sound_manager = ResourceManager[pygame.Sound]("pygame_sounds")
_has_transparency: list[str] = [".png", ".gif", ".lbm", ".webp", ".tga", ".xcf", ".qoi"]
# I think that's all of them that can have alpha. I'll adjust as needed.


def _load_pygame_images(resource_location: os.PathLike | str) -> pygame.Surface:
    location = Path(resource_location)
    file_type = location.suffix
    image = pygame.image.load(location)
    if file_type.lower() in _has_transparency:
        # Only want to call this on things that have alpha channels.
        image.convert_alpha()
    else:
        image.convert()
    return image


def _load_pygame_sounds(resource_location: os.PathLike | str) -> pygame.Sound:
    location = Path(resource_location)
    return pygame.mixer.Sound(location)


_image_manager.config(loader_helper=_load_pygame_images)
_sound_manager.config(loader_helper=_load_pygame_sounds)


def getImageManager():
    """
    Provides a pre-built resource manager specifically for loading images into
    pygame Surfaces.
    It is not managed by getResourceManager.
    """
    return _image_manager


def getSoundManager():
    """
    Provides a pre-built resource manager specifically for loading sounds for use in
    pygame's mixer.
    It is not managed by getResourceManager.
    """
    return _sound_manager
