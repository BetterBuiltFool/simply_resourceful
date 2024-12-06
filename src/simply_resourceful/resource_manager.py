from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Optional, Type


class ResourceManager[T]:
    _instances: dict[Type[T], dict[str, ResourceManager]] = {}

    def __init__(self, handle: str) -> None:
        self.handle = handle
        self.resources: dict[str, T] = {}
        self.resource_locations: dict[str, Path] = {}

    def config(self, loader_helper: Optional[Callable] = None) -> None:
        if loader_helper:
            self._asset_loader = loader_helper

    def preload(self, asset_handle: str, resource_location: Any) -> None:
        self.resource_locations.update({asset_handle: resource_location})

    def force_load(self, asset_handle: str, resource_location: Any) -> None:
        self.preload(asset_handle, resource_location)
        asset: T = self._asset_loader(resource_location)
        self.resources.setdefault(asset_handle, asset)

    def get(self, asset_handle: str, default: Optional[T] = None) -> T:
        """
        Gets the asset of the requested handle. Loads the asset if it isn't already.
        If the asset can't be loaded and a default is given, pass along that instead.
        The default is not added to the loaded dict.

        :param asset_handle: Name of the asset to be gotten
        :raises KeyError: Raised if handle is not found, and no default is given
        :return: The (loaded) instance of the asset.
        """
        if asset_handle not in self.resource_locations:
            if default is not None:
                return default
            # TODO: Make this more helpful by looking for similarly named assets?
            # Could use difflib.get_close_matches()
            raise KeyError(f"'{asset_handle}' is not handled by {self}.")
        return self.resources.setdefault(
            asset_handle,
            self._asset_loader(self.resource_locations.get(asset_handle)),
            # This get() can't fail outside of race conditions since we check first.
            # If you are here looking for why your asset loader is being passed None,
            # Check to see if you are removing the key in another thread.
        )

    def dump(self, asset_handle: str) -> T:
        pass

    def forget(self, asset_handle: str) -> tuple[T | None, Path]:
        pass

    @staticmethod
    def _asset_loader(*args, **kwds):
        """
        This is overwritten by self.config

        :raises AttributeError: If not asset_loader is supplied via config.
        """
        raise AttributeError(
            "No loader function assigned. You must assign a loader to run."
        )


def getResourceManager[T](handle: str = "") -> ResourceManager[T]:
    manager_set = ResourceManager._instances.setdefault(T, {})
    return manager_set.setdefault(handle, ResourceManager[T](handle))
