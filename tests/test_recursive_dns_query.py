import unittest
from unittest.mock import patch
from cache import Cache
from recursive_dns_query import recursive_dns_query


class TestRecursiveDNSQuery(unittest.TestCase):
    def setUp(self):
        """Set up a Cache instance for testing."""
        self.cache = Cache()

    @patch('socket.gethostbyname')
    def test_recursive_dns_query_success(self, mock_gethostbyname):
        """Test a successful recursive DNS query."""
        mock_gethostbyname.return_value = "93.184.216.34"
        result = recursive_dns_query("example.com", self.cache)
        self.assertEqual(result, "93.184.216.34")
        self.assertEqual(self.cache.get("example.com"), "93.184.216.34")

    @patch('socket.gethostbyname')
    def test_recursive_dns_query_failure(self, mock_gethostbyname):
        """Test a failed recursive DNS query."""
        mock_gethostbyname.side_effect = Exception("DNS lookup failed")
        result = recursive_dns_query("nonexistent.com", self.cache)
        self.assertIsNone(result)
        self.assertIsNone(self.cache.get("nonexistent.com"))

    def test_recursive_dns_query_cache(self):
        """Test that the recursive query uses cache."""
        self.cache.set("example.com", "93.184.216.34")
        result = recursive_dns_query("example.com", self.cache)
        self.assertEqual(result, "93.184.216.34")
        self.assertEqual(self.cache.get("example.com"), "93.184.216.34")


if __name__ == '__main__':
    unittest.main()
