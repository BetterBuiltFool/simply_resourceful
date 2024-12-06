from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Optional, Type, TypeVar


T = TypeVar("T")


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

    def get(self, asset_handle: str) -> T:
        if asset_handle not in self.resource_locations:
            raise KeyError(f"'{asset_handle}' is not handled by {self}.")
        return self.resources.setdefault(
            asset_handle,
            self._asset_loader(self.resource_locations.get(asset_handle)),
            # (...).get can't fail outside of race conditions since we check first.
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


def getResourceManager[T](handle: str) -> ResourceManager[T]:
    manager_set = ResourceManager._instances.setdefault(T, {})
    return manager_set.setdefault(handle, ResourceManager[T](handle))
