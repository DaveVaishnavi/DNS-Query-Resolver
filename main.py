from recursive_dns_query import recursive_dns_query
from iterative_dns_query import iterative_dns_query
from cache import Cache
from flask import Flask, render_template, request

app = Flask(__name__)

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/resolve', methods=['POST'])
def resolve():
    domain = request.form.get('domain')
    cache = Cache("cache.json")
    try:
        ip_recursive = recursive_dns_query(domain, cache)
        ip_iterative = iterative_dns_query(domain, cache)
    except Exception as e:
        ip_recursive = f"Invalid domain or unable to resolve due to {e}"
        ip_iterative = f"Invalid domain or unable to resolve due to {e}"
    return render_template('index.html', domain=domain, ip_recursive=ip_recursive, ip_iterative=ip_iterative)

if __name__ == '__main__':
    app.run(debug=True)