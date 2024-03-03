from flask import Flask, request, redirect, render_template, jsonify, url_for
from flask_caching import Cache
import os
import json
import random
import string
import sqlite3
from flask_restful import Api

app = Flask(__name__, subdomain_matching=True)
cache = Cache()
app.config['SERVER_NAME'] = os.getenv("SERVER_NAME")
app.config['APIENDPOINT'] = os.getenv("APIENDPOINT")
api = Api(app)
shortened_urls = {}

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='urls' ''')

        # If the count is 1, then table exists
        if cursor.fetchone()[0] == 1:
            print('Table already exists.')
        else:
            conn.execute('CREATE TABLE urls (short_url TEXT, long_url TEXT)')
            print('Table created successfully.')
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
    finally:
        conn.close()

def get_db_connection():
    conn = sqlite3.connect('urls.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits 
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
        conn.execute('INSERT INTO urls (short_url, long_url) VALUES (?, ?)',
                     (short_url, long_url))
        conn.commit()
        conn.close()
        return render_template("short_url.html", short_url=url_for('redirect_url', short_url=short_url, _external=True))
    else:
        return render_template("index.html")

@cache.cached(timeout=60)
@app.route("/<short_url>")
def redirect_url(short_url):
    conn = get_db_connection()
    url_data = conn.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,)).fetchone()
    if url_data is None:
        return "URL not found", 404
    else:
        return redirect(url_data['long_url'], code=302)

### API ENDPOINTS

APIENDPOINT = ['GET', 'POST']

@app.route("/v2", methods=APIENDPOINT)
def api_hello_world():
    return "this is api \n"

@app.route("/v2/ip", methods=APIENDPOINT)
def api_ip_endpoint():
    return jsonify(origin=request.headers.get("X-Forwarded-For", request.remote_addr))

create_table()

if __name__ == "__main__":
    app.run()