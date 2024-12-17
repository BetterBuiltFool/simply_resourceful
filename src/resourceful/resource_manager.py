from __future__ import annotations

import difflib
import os
from pathlib import Path
from typing import Any, Callable, Optional, Type, TypeVar


T = TypeVar("T")


class ResourceManager[T]:
    _instances: dict[Type[T], dict[str, ResourceManager]] = {}

    def __init__(self, handle: str) -> None:
        self.handle = handle
        self.cache: dict[str, T] = {}
        self.resource_locations: dict[str, Path] = {}

    def config(self, loader_helper: Optional[Callable] = None) -> None:
        """
        Modifies the resource manager's behavior per the specified parameters.

        :param loader_helper: Loader function for the resource. Must take the location
        data its parameter, and return an instance of the resource.
        """
        if loader_helper:
            self._asset_loader = loader_helper

    def import_asset(self, asset_handle: str, resource_location: Any) -> None:
        """
        Prepares the resource manager to load a resource.

        The asset handle is how users of the resource will ask for it.

        The resource location is data that describes how the asset loader can locate
        the resource. It may be a path, or a download site, or anything else, so long
        as the asset loader can handle the parameters.

        :param asset_handle: The name of the resource
        :param resource_location: The data the asset loader needs to produce the
        resource.
        """
        self.resource_locations.update({asset_handle: resource_location})

    def import_directory(
        self,
        folder: os.PathLike | str,
        recursive: bool = False,
        key: Optional[Callable] = None,
        name_key: Optional[Callable] = None,
        location_data_key: Optional[Callable] = None,
    ):
        """
        Parse a directory, importing all of the files inside into the resource manager.

        :param folder: Target directory
        :param recursive: Whether to recursively search through subdirectories,
        defaults to False
        :param key: A function for choosing files to import, defaults all files
        If you have mixed file types, do not rely on the default key.
        :param name_key: A function for creating asset names from files, defaults to
        the relative path to the directory plus the name of the file.
        :param location_data_key: Function for generating the location data required
        for the asset loader, defaults to the file's path.
        """
        if key is None:

            def key(file: Path) -> Path | None:
                return file

        if name_key is None:

            def name_key(file: Path) -> str:
                """
                Uses the relative path and filename, without suffixes,
                as the default asset handle.
                """
                file = file.relative_to(folder)
                while file.suffix != "":
                    file = file.with_suffix("")
                return str(file)

        if location_data_key is None:

            def location_data_key(file: Path) -> Path:
                """
                Gives path of the file as its location.
                """
                return file

        directory = Path(folder)
        files = list(directory.iterdir())
        for item in files:
            if item.is_dir():
                if recursive:
                    for file in item.iterdir():
                        files.append(file)
                continue
            if not key(item):
                continue
            self.import_asset(name_key(item), location_data_key(item))

    def force_load(self, asset_handle: str, resource_location: Any) -> None:
        """
        Establishes the resource in the database, and loads it immediately instead of
        deferring to when the asset is requested.

        :param asset_handle: The name of the resource
        :param resource_location: The data the asset loader needs to produce the
        resource.
        """
        self.import_asset(asset_handle, resource_location)
        asset: T = self._asset_loader(resource_location)
        self.cache.setdefault(asset_handle, asset)

    def update(self, asset_handle: str, asset: T) -> T | None:
        """
        Changes the loaded resource of the given handle to that of the given asset.

        :param asset_handle: The name of the resource
        :param asset: The new asset replacing the old asset.
        :return: The old asset, or None if the asset wasn't loaded.
        """
        old_asset = self.cache.get(asset_handle, None)
        self.cache[asset_handle] = asset
        return old_asset

    def force_update(self, asset_handle: str, asset: T) -> None:
        """
        Forces the asset at the given handle to become a copy of the supplied asset.
        This will hot-swap the asset for all of its users.

        Note - Not all object may support this behavior, and may be broken by it.

        :param asset_handle: The name of the resource
        :param asset: The new asset replacing the old asset.
        """
        old_asset = self.cache.get(asset_handle, None)
        if old_asset is None:
            # Nothing to replace, so just fill it in
            self.cache[asset_handle] = asset
            return
        # Otherwise, force the loaded asset to take on the new asset's attributes.
        old_asset.__dict__ = asset.__dict__

    def get(self, asset_handle: str, default: Optional[T] = None) -> T:
        """
        Gets the asset of the requested handle. Loads the asset if it isn't already.
        If the asset can't be loaded and a default is given, pass along that instead.
        The default is not added to the loaded dict.

        :param asset_handle: Name of the asset to be gotten
        :param default: Item returned if the asset is unavailable
        :raises KeyError: Raised if handle is not found or fails to load,
        and no default is given
        :return: The (loaded) instance of the asset.
        """
        if asset_handle not in self.resource_locations:
            if default is None:
                closest = difflib.get_close_matches(
                    asset_handle, self.resource_locations.keys(), n=1
                )
                error_msg = f"Resource '{asset_handle}' is not handled by {self}."
                if len(closest) > 0:
                    error_msg += f" Did you mean '{closest[0]}'?"
                raise KeyError(error_msg)
            return default
        asset = self.cache.get(asset_handle, None)
        if asset is None:
            asset = self._asset_loader(self.resource_locations.get(asset_handle))
            if asset is None:
                # Last chance to get an asset
                if default is None:
                    raise KeyError(f"Resource '{asset_handle}' failed to load.")
                asset = default
            self.cache[asset_handle] = asset
        return asset

    def uncache(self, asset_handle: str) -> T | None:
        """
        Unloads the specified asset from the manager. Existing copies of the resource
        being used by objects will keep it in memory until they cease using it.

        If the asset is requested again, it will be reloaded.

        :param asset_handle: The name of the resource
        :return: The resource being unloaded, or None if it does not exist.
        """
        return self.cache.pop(asset_handle, None)

    def clear(self, asset_handle: str) -> tuple[T | None, Any]:
        """
        Unloads the asset, and removes it from the load dictionary.

        If the resource is requested again, it will fail to load.

        :param asset_handle: _description_
        :return: A tuple containing the old asset and its location data, or None if
        none exists.
        """
        old_asset = self.uncache(asset_handle)
        old_location = self.resource_locations.pop(asset_handle, None)
        return (old_asset, old_location)

    @staticmethod
    def _asset_loader(*args, **kwds):
        """
        This is overwritten by self.config

        :raises AttributeError: If asset_loader is not supplied via config.
        """
        raise AttributeError(
            "No loader function assigned. You must assign a loader to run."
        )


def getResourceManager(asset_type: Type[T], handle: str = "") -> ResourceManager[T]:
    """
    Provides a Resource Manager of the specified type and handle.
    If the asset type or handle do not match an existing one, it will be created.

    :param asset_type: The Type of the resource being managed.
    :param handle: The name of the manager, defaults to ""
    :return: The resource manager of the type and handle specified.
    """
    manager_set = ResourceManager._instances.setdefault(asset_type, {})
    return manager_set.setdefault(handle, ResourceManager[asset_type](handle))
