import unittest
from unittest.mock import patch
from utils.cache import Cache
from utils.iterative_dns_query import iterative_dns_query


class TestIterativeDNSQuery(unittest.TestCase):
    def setUp(self):
        """Set up a Cache instance for testing."""
        self.cache = Cache()

    @patch('socket.gethostbyname')
    def test_iterative_dns_query_success(self, mock_gethostbyname):
        """Test a successful iterative DNS query."""
        mock_gethostbyname.return_value = "93.184.215.14"
        result = iterative_dns_query("example.com", self.cache)
        self.assertEqual(result, "93.184.215.14")
        self.assertEqual(self.cache.get("example.com"), "93.184.215.14")

    @patch('socket.gethostbyname')
    def test_iterative_dns_query_failure(self, mock_gethostbyname):
        """Test a failed iterative DNS query."""
        mock_gethostbyname.side_effect = Exception("DNS lookup failed")
        result = iterative_dns_query("nonexistent.com", self.cache)
        self.assertIsNone(result)
        self.assertIsNone(self.cache.get("nonexistent.com"))

    def test_iterative_dns_query_cache(self):
        """Test that the iterative query uses cache."""
        self.cache.set("example.com", "93.184.216.34")
        result = iterative_dns_query("example.com", self.cache)
        self.assertEqual(result, "93.184.216.34")
        self.assertEqual(self.cache.get("example.com"), "93.184.216.34")


if __name__ == '__main__':
    unittest.main()
