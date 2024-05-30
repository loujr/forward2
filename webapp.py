from flask import Flask, request, redirect, render_template, jsonify, url_for
from flask_caching import Cache
from dotenv import load_dotenv
import os
import json
import random
import string
import sqlite3
from flask_restful import Api

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask app with subdomain matching enabled
app = Flask(__name__, subdomain_matching=True)

# Set the server name and API endpoint from environment variables
#app.config['SERVER_NAME'] = os.getenv("SERVER_NAME")
#app.config['APIENDPOINT'] = os.getenv("APIENDPOINT")

# Initialize the cache
cache = Cache()
# Initialize the API
api = Api(app)
# Dictionary to store the shortened URLs
shortened_urls = {}

# Create a table in the database to store the shortened URLs
#def create_table():
#    conn = get_db_connection()
#    cursor = conn.cursor()
#    try:
#        cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='urls' ''')
#
#        # If the count is 1, then table exists
#        if cursor.fetchone()[0] == 1:
#            print('Table already exists.')
#        else:
#            conn.execute('CREATE TABLE urls (short_url TEXT, long_url TEXT)')
#            print('Table created successfully.')
#    except sqlite3.Error as e:
#        print(f"An error occurred: {e.args[0]}")
#    finally:
#        conn.close()

# Get a connection to the database
def get_db_connection():
    conn = sqlite3.connect('urls.db')
    conn.row_factory = sqlite3.Row
    return conn

# Generate a short URL
def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits 
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

#Route to shorten a URL
@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data['long_url']
    short_url = generate_short_url()
    conn = get_db_connection()
    conn.execute('INSERT INTO urls (short_url, long_url) VALUES (?, ?)',
                 (short_url, long_url))
    conn.commit()
    conn.close()
    #return jsonify(short_url=url_for('redirect_url', short_url=short_url, _external=True, _scheme='https'))
    return jsonify(short_url=os.getenv('REDIRECT_URL') + short_url)

#curl -X POST -H "Content-Type: application/json" -d '{"long_url":"http://youtube.com"}' https://api.fwd2.app/shorten_url
#{"short_url":"https://localhost/3lupAP"}

# Route to redirect the short URL to the original URL
#@cache.cached(timeout=60)
#@app.route("/<short_url>")
#def redirect_url(short_url):
#    conn = get_db_connection()
#    url_data = conn.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,)).fetchone()
#    if url_data is None:
#        return "URL not found", 404
#    else:
#        return redirect(url_data['long_url'], code=302)

# Accepted methods for additional API endpoints
APIENDPOINT = ['GET', 'POST']

# API test endpoint to return a simple message
@app.route("/v2", methods=APIENDPOINT)
def api_hello_world():
    return "this is api \n"

# API endpoint to return the IP address of the client
@app.route("/v2/ip", methods=APIENDPOINT)
def api_ip_endpoint():
    return jsonify(origin=request.headers.get("X-Forwarded-For", request.remote_addr))

#create_table()

if __name__ == "__main__":
    app.run()
