from os import PathLike
from typing import TypeVar


T = TypeVar("T")


class ResourceManager[T]:

    def __init__(self) -> None:
        self.resources: dict[str, T] = {}
        self.resource_location: dict[str, PathLike | str] = {}
