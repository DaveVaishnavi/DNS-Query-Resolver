from recursive_dns_query import recursive_dns_query
from iterative_dns_query import iterative_dns_query
from cache import Cache


def main():
    domain = input("Enter the domain to resolve: ")

    cache = Cache("cache.json")

    # Recursive DNS Query
    ip_recursive = recursive_dns_query(domain, cache)
    print(f"Resolved IP (recursive): {ip_recursive}")

    # Iterative DNS Query
    ip_iterative = iterative_dns_query(domain, cache)
    print(f"Resolved IP (iterative): {ip_iterative}")


if __name__ == "__main__":
    main()
