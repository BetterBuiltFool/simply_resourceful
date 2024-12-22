import os
from pathlib import Path

from ..resource_manager import ResourceManager

import pygame

_image_manager = ResourceManager[pygame.Surface]("pygame_images")
_sound_manager = ResourceManager[pygame.Sound]("pygame_sounds")
_has_transparency: list[str] = [".png", ".gif", ".lbm", ".webp", ".tga", ".xcf", ".qoi"]
# I think that's all of them that can have alpha. I'll adjust as needed.


DEFAULT_SURFACE = pygame.Surface((16, 16))
"""
A 16x16 black and fuchsia checkerboard pattern to serve as a default image.
"""
DEFAULT_SURFACE.fill(pygame.Color("black"))
for i in range(4):
    for j in range(4):
        if i % 2 == j % 2:
            # This creates a checkerboard pattern
            pygame.draw.rect(
                DEFAULT_SURFACE,
                pygame.Color("fuchsia"),
                pygame.Rect(4 * i, 4 * j, 4, 4),
            )


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


_image_manager.config(loader_helper=_load_pygame_images, default_asset=DEFAULT_SURFACE)
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
