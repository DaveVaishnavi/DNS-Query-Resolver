from utils.recursive_dns_query import recursive_dns_query
from utils.iterative_dns_query import iterative_dns_query
from utils.cache import Cache
from flask import Flask, render_template, request
import json
import time

app = Flask(__name__)

def load_cache_data():
    with open('cache.json', 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/resolve', methods=['POST'])
def resolve():
    domain = request.form.get('domain')
    cache = Cache("cache.json")
    try:
        start_recursive = time.time()
        ip_recursive = recursive_dns_query(domain, cache)
        end_recursive = time.time()
        recursive_time = end_recursive - start_recursive

        start_iterative = time.time()
        ip_iterative = iterative_dns_query(domain, cache)
        end_iterative = time.time()
        iterative_time = end_iterative - start_iterative

    except Exception as e:
        ip_recursive = f"Invalid domain or unable to resolve due to {e}"
        ip_iterative = f"Invalid domain or unable to resolve due to {e}"
        recursive_time = iterative_time = None  

    return render_template('index.html', 
                           domain=domain, 
                           ip_recursive=ip_recursive, 
                           ip_iterative=ip_iterative, 
                           recursive_time=recursive_time, 
                           iterative_time=iterative_time)

@app.route('/cache')
def cache():
    cache_data = load_cache_data()  
    return render_template('cache.html', cache_data=cache_data)

if __name__ == '__main__':
    app.run(debug=True)