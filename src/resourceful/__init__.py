from .resource_manager import getResourceManager, ResourceManager  # noqa: F401

try:
    import pygame  # noqa: F401
    from .pygame import getImageManager, getSoundManager  # noqa: F401

except ImportError:
    # No pygame installed, no bonus functions for you.
    pass
