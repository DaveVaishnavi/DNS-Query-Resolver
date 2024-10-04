class Cache:
    def __init__(self):
        self.cache = {}

    def get(self, domain):
        """Retrieve the IP address from the cache."""
        return self.cache.get(domain)

    def set(self, domain, ip_address):
        """Store the IP address in the cache."""
        self.cache[domain] = ip_address

    def clear(self):
        """Clear the cache."""
        self.cache.clear()
