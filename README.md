# DNS Query Resolver

## CSN-341: Computer Networks
### DNS Query Resolver - Project Proposal
**Group-01**

- 21116034 Vaishnavi Virat Dave  
- 21116048 Kaashvi Jain   
- 21323003 Abhijna Raghavendra  
- 21112108 Vyusti Singamsetti  

## Project Description

*Create a custom DNS resolver that takes a domain name as input and returns the corresponding IP address using iterative or recursive querying.*

### Skills
Understanding of DNS protocol, recursive and iterative DNS resolution.

### Tools
Python

## Background

Imagine writing `192.168.1.1` or `2607:f8b0:400a:800::200e` to access Google on a browser. DNS resolution allows users to input familiar domain names, which are then translated to the corresponding IP addresses required by computers to communicate. These domain names also establish a hierarchical system of DNS servers, ensuring speedy responses.

## DNS Resolution Methods

1. **Iterative Lookup**: The client queries each DNS server directly until it gets a response or an error.
2. **Recursive Lookup**: A DNS server queries other DNS servers on behalf of the client until it finds the IP address. The DNS server then returns the IP address to the client.

## Objective

To implement a custom DNS resolver using the `dnspython` library to perform DNS queries by:
- Querying root servers for the top-level domain (TLD) nameserver.
- Resolving subsequent servers based on the type of resolution.
- Querying authoritative nameservers for the final domain to retrieve its IP address.
- Implementing a cache system to store previously resolved domains, avoiding redundant lookups for a certain period defined by the Time to Live (TTL). The cache is persisted in a JSON file and can be reloaded across sessions.

## Design Idea

### `iterative_dns_query(domain, cache)`
1. **Check Cache**: Retrieve the cached IP for the domain, if available.
2. **Set Root DNS Servers**: Start querying from root DNS servers.
3. **Domain Decomposition**: Split the domain name into its components.
4. **Iterative Querying**: Query from TLD downwards until an A record (IP address) is resolved.
5. **Cache Result**: Store the result in the cache with a timestamp.

### `recursive_dns_query(domain, cache)`
1. **Check Cache**: Retrieve the cached IP for the domain.
2. **Resolve Domain**: Use `socket.gethostbyname()` to perform a recursive DNS query.
3. **Cache Result**: Store the IP in the cache with a timestamp.

### `Cache` Class
Implements efficient retrieval of IP addresses by storing frequently used mappings:
- `__init__(cache_file)`: Loads cache from the file.
- `load_cache()`: Loads cache as a dictionary.
- `save_cache()`: Saves the cache state to a file.
- `get(domain)`: Retrieves cached IP, checking if TTL has expired.
- `set(domain, ip_address)`: Adds new entry with a timestamp.
- `flush_expired_entries()`: Removes expired cache entries.

## Key Features

- **DNS Record Resolution**: Queries authoritative servers for the final IP address.
- **Caching System**: Implements a cache with TTL to avoid redundant queries.
- **Error Management**: Handles issues like DNS server timeouts and network errors.
- **Verbose Logging**: Logs query details, responses, and next steps.


## Setup Instructions

Follow these steps to get the project running locally:

### 1. Clone the Repository

If you're using Git, clone the repository:

```bash
git clone https://github.com/DaveVaishnavi/DNS-Query-Resolver.git
```
*Otherwise, download the ZIP file and extract it to a folder.*

### 2. Navigate to the Project Directory
Move into the project directory:

```bash
cd DNS-Query-Resolver
```

### 3. Create a Virtual Environment (Optional but Recommended)

It's recommended to create a virtual environment to manage dependencies:
```bash
python -m venv venv
```
Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```
### 4. Install Dependencies

Install the required Python packages from the requirements.txt file:

```bash
pip install -r requirements.txt
```
### 5. Run the Application

Start the Flask development server:

```bash
python main.py
```
The server will start running on http://127.0.0.1:5000/.

6. Access the Application
Open your browser and go to http://127.0.0.1:5000/ to use the DNS resolver interface
