from .resource_manager import (  # noqa: F401
    getResourceManager,
    ResourceManager,
    NoDefault,
)

try:
    import pygame  # noqa: F401
    from .pygame import getImageManager, getSoundManager, DEFAULT_SURFACE  # noqa: F401

except ImportError:
    # No pygame installed, no bonus functions for you.
    pass
