import pathlib
import sys
import unittest

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
