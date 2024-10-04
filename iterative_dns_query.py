import socket


def iterative_dns_query(domain, cache):
    """Perform an iterative DNS query."""
    cached_ip = cache.get(domain)
    if cached_ip:
        return cached_ip

    dns_servers = [
        '8.8.8.8',  # Google Public DNS
        '8.8.4.4',  # Google Public DNS
        '1.1.1.1',  # Cloudflare
        '208.67.222.222',  # OpenDNS
    ]

    for server in dns_servers:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)

            ip_address = socket.gethostbyname(domain)
            cache.set(domain, ip_address)
            return ip_address
        except Exception as e:
            print(f"Error querying {server}: {e}")

    return None
