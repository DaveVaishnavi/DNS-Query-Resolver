import socket


def recursive_dns_query(domain, cache):
    """Perform a recursive DNS query."""
    cached_ip = cache.get(domain)
    if cached_ip:
        return cached_ip

    try:
        ip_address = socket.gethostbyname(domain)
        cache.set(domain, ip_address)
        return ip_address
    except socket.gaierror:
        return None
