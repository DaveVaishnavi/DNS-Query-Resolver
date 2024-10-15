import unittest
from utils.cache import Cache


class TestCache(unittest.TestCase):
    def setUp(self):
        """Set up a Cache instance for testing."""
        self.cache = Cache()

    def test_set_and_get(self):
        """Test setting and getting values from the cache."""
        self.cache.set("example.com", "93.184.216.34")
        self.assertEqual(self.cache.get("example.com"), "93.184.216.34")

    def test_get_non_existent_key(self):
        """Test getting a non-existent key."""
        self.assertIsNone(self.cache.get("nonexistent.com"))

    def test_clear_cache(self):
        """Test clearing the cache."""
        self.cache.set("example.com", "93.184.216.34")
        self.cache.clear()
        self.assertIsNone(self.cache.get("example.com"))


if __name__ == '__main__':
    unittest.main()
