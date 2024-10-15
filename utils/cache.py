import json
import time
import os

TTL = 3600  # Time to Live for cache entries (in seconds)


class Cache:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        """Load cache from the cache file, or initialize an empty cache if the file doesn't exist."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def save_cache(self):
        """Save the current cache to a file."""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def get(self, domain):
        """Retrieve an entry from the cache if it's still valid (not expired)."""
        entry = self.cache.get(domain)
        if entry:
            ip_address, timestamp = entry
            if time.time() - timestamp < TTL:  # Check if the TTL has not expired
                return ip_address
            else:
                # Cache has expired, remove the entry
                del self.cache[domain]
                self.save_cache()
        return None

    def set(self, domain, ip_address):
        """Add an entry to the cache with the current timestamp."""
        self.cache[domain] = (ip_address, time.time())  # Save IP and the current time
        self.save_cache()

    def flush_expired_entries(self):
        """Flush cache entries that have exceeded their TTL."""
        current_time = time.time()
        expired_keys = [key for key, (_, timestamp) in self.cache.items() if current_time - timestamp >= TTL]
        for key in expired_keys:
            del self.cache[key]
        self.save_cache()
