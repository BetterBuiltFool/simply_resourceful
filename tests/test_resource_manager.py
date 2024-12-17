import pathlib
import sys
import unittest

import pyfakefs
import pyfakefs.fake_filesystem
import pyfakefs.fake_filesystem_unittest

sys.path.append(str(pathlib.Path.cwd()))
from src.resourceful import resource_manager as rm  # noqa: E402


def test_loader(resource_location: int) -> int | None:
    """
    Simply returns the location data as the resource
    Returns None if the data is negative
    """
    if resource_location < 0:
        return None
    return resource_location


class TestResourceManager(unittest.TestCase):

    def setUp(self):
        self.test_manager = rm.ResourceManager[int]("Test")
        self.test_manager.config(loader_helper=test_loader)

    def tearDown(self):
        del self.test_manager

    def test_init(self):
        test_manager = rm.ResourceManager[int]("Test")

        self.assertEqual(test_manager.handle, "Test")
        self.assertTrue(len(test_manager.cache) == 0)
        self.assertTrue(len(test_manager.resource_locations) == 0)

    def test_import_asset(self):
        self.test_manager.import_asset("test_num", 1)

        self.assertTrue(len(self.test_manager.cache) == 0)
        self.assertTrue(len(self.test_manager.resource_locations) == 1)

    @pyfakefs.fake_filesystem_unittest.patchfs
    def test_import_directory(self, fs: pyfakefs.fake_filesystem.FakeFilesystem):
        subfolder = fs.create_dir(pathlib.Path("root/directory/subfolder"))
        directory = subfolder.parent_dir
        # root = directory.parent_dir
        for i in range(5):
            fs.create_file(pathlib.Path(directory.path).joinpath(f"item{i}.file"))
        for i in range(5):
            fs.create_file(pathlib.Path(subfolder.path).joinpath(f"subitem{i}.file"))

        # Test w/o recursion
        self.test_manager.import_directory(directory.path, recursive=False)
        self.assertEqual(len(self.test_manager.resource_locations), 5)

        self.test_manager.resource_locations.clear()

        # Test w/ recursion
        self.test_manager.import_directory(directory.path, recursive=True)
        self.assertEqual(len(self.test_manager.resource_locations), 10)

        self.test_manager.resource_locations.clear()

        # Test w/ exclusion key
        def test_key(file: pathlib.Path) -> pathlib.Path | None:
            # This is a stupid thing to check in a real scenario, but will do
            if "0" in file.name or "1" in file.name:
                return file
            return None

        self.test_manager.import_directory(
            directory.path, recursive=False, key=test_key
        )
        self.assertEqual(len(self.test_manager.resource_locations), 2)

        self.test_manager.resource_locations.clear()

        # Test w/ naming key
        def test_name_key(file: pathlib.Path) -> str:
            # Just give the file name. This will conflict if files shafe names, but w/e
            return file.name

        self.test_manager.import_directory(
            directory.path, recursive=True, name_key=test_name_key
        )

        self.assertIsNotNone(self.test_manager.resource_locations.get("subitem0.file"))

        self.test_manager.resource_locations.clear()

        # Test w/ custom location data key
        def test_location_data_key(file: pathlib.Path) -> str:
            # Give file path relative to the directory
            return file.relative_to(directory.path)

        self.test_manager.import_directory(
            directory.path, recursive=True, location_data_key=test_location_data_key
        )

        self.assertEqual(
            self.test_manager.resource_locations.get("subfolder/subitem0"),
            pathlib.Path("subfolder/subitem0.file"),
        )

    def test_force_load(self):
        self.test_manager.force_load("test_num", 1)

        self.assertTrue(len(self.test_manager.cache) == 1)
        self.assertTrue(len(self.test_manager.resource_locations) == 1)
        self.assertEqual(self.test_manager.cache.get("test_num"), 1)

    def test_update(self):
        self.test_manager.force_load("test_num", 1)

        self.assertTrue(len(self.test_manager.cache) == 1)
        self.assertTrue(len(self.test_manager.resource_locations) == 1)
        self.assertEqual(self.test_manager.cache.get("test_num"), 1)

        self.test_manager.update("test_num", 2)

        self.assertTrue(len(self.test_manager.cache) == 1)
        self.assertTrue(len(self.test_manager.resource_locations) == 1)
        self.assertEqual(self.test_manager.cache.get("test_num"), 2)

    def test_force_update(self):

        class Test:

            def __init__(self, value: int):
                self.x = value

        def load_test(resource_location: int) -> Test:
            return Test(resource_location)

        test_manager = rm.getResourceManager(Test)
        test_manager.config(loader_helper=load_test)

        test_manager.force_load("test_object", 1)

        self.assertTrue(len(test_manager.cache) == 1)
        self.assertTrue(len(test_manager.resource_locations) == 1)
        test_object = test_manager.cache.get("test_object")
        self.assertEqual(test_object.x, 1)

        test_manager.force_update("test_object", Test(2))
        self.assertEqual(test_object.x, 2)

    def test_get(self):
        self.test_manager.import_asset("test_num", 1)

        self.assertTrue(len(self.test_manager.cache) == 0)
        self.assertTrue(len(self.test_manager.resource_locations) == 1)

        # Standard good case
        self.assertEqual(self.test_manager.get("test_num"), 1)

        self.assertTrue(len(self.test_manager.cache) == 1)
        self.assertEqual(self.test_manager.cache.get("test_num"), 1)

        # No such asset, with default
        self.assertEqual(self.test_manager.get("test_num2", 1), 1)

        # No such asset, without default
        with self.assertRaises(KeyError):
            self.test_manager.get("test_num2")

        # Load failure, with default
        self.test_manager.import_asset("test_num3", -1)
        self.assertEqual(self.test_manager.get("test_num3", 1), 1)

        # Load failure, without default
        self.test_manager.import_asset("test_num4", -1)
        with self.assertRaises(KeyError):
            self.test_manager.get("test_num4")

    def test_uncache(self):
        self.test_manager.force_load("test_num", 1)

        test_num = self.test_manager.uncache("test_num")

        self.assertEqual(test_num, 1)
        self.assertTrue(len(self.test_manager.cache) == 0)

        self.test_manager.get("test_num")
        self.assertTrue(len(self.test_manager.cache) == 1)

    def test_clear(self):
        self.test_manager.force_load("test_num", 1)

        test_num = self.test_manager.clear("test_num")

        self.assertEqual(test_num, (1, 1))
        self.assertTrue(len(self.test_manager.cache) == 0)
        self.assertTrue(len(self.test_manager.resource_locations) == 0)

        self.assertEqual(self.test_manager.get("test_num", 1), 1)


if __name__ == "__main__":
    unittest.main()
