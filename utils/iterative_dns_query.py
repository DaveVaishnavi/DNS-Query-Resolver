import socket
import dns.message
import dns.query
import dns.resolver


def send_udp_query(server, query):
    """Send a DNS query using UDP."""
    try:
        response = dns.query.udp(query, server, timeout=2)
        return response
    except Exception as e:
        print(f"Failed to query {server} via UDP: {e}")
        return None


def iterative_dns_query(domain, cache):
    """Perform an iterative DNS query, starting from the root servers."""
    cached_ip = cache.get(domain)
    if cached_ip:
        return cached_ip

    # List of root DNS servers (IPv4)
    root_dns_servers = [
        '198.41.0.4',  # Root DNS Server A
        '199.9.14.201',  # Root DNS Server B
        '192.33.4.12',  # Root DNS Server C
    ]

    # Split the domain into its parts (e.g., ['google', 'com'] for 'google.com')
    domain_parts = domain.split('.')

    # Start with root servers
    current_nameservers = root_dns_servers

    # Start querying from the TLD and move downward
    current_query = '.'.join(domain_parts[-1:])  # Start with TLD (e.g., 'com')

    try:
        # Perform iterative query down the DNS hierarchy
        for level in range(len(domain_parts) - 1, -1, -1):
            query = dns.message.make_query(current_query, dns.rdatatype.NS)

            for server in current_nameservers:
                print(f"Querying {server} for {current_query}")
                response = send_udp_query(server, query)

                if response and response.answer:
                    print(f"Received authoritative answer for {current_query}: {response.answer}")
                    break  # If we get a direct answer, we can stop
                elif response and response.additional:
                    # Referral case: follow the additional section
                    new_ns_ips = [rrset[0].to_text() for rrset in response.additional if
                                  rrset.rdtype == dns.rdatatype.A]
                    if new_ns_ips:
                        current_nameservers = new_ns_ips  # Set new nameservers from referral
                        break
                elif response and response.authority:
                    # Referral case: use authority section to get new NS
                    ns_names = [rr.to_text() for rrset in response.authority for rr in rrset if
                                rr.rdtype == dns.rdatatype.NS]
                    if ns_names:
                        # Resolve the NS names to IP addresses
                        current_nameservers = [socket.gethostbyname(ns_name) for ns_name in ns_names]
                        break
            else:
                print(f"No answer for {current_query}, moving to next root server.")
                continue  # Try the next root server if no response was useful

            # Prepare for the next query, moving up one level in the domain hierarchy
            if level > 0:
                current_query = '.'.join(domain_parts[level - 1:])
            else:
                # Final level, query the full domain for the A record
                query = dns.message.make_query(domain, dns.rdatatype.A)
                for server in current_nameservers:
                    print(f"Querying {server} for {domain}")
                    response = send_udp_query(server, query)
                    if response and response.answer:
                        ip_address = response.answer[0][0].to_text()
                        print(f"Final answer for {domain}: {ip_address}")
                        cache.set(domain, ip_address)
                        return ip_address

    except Exception as e:
        print(f"Error during DNS query: {e}")

    return None
