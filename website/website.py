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

# Initialize the cache
cache = Cache()

# Dictionary to store the shortened URLs
shortened_urls = {}

# Home page for website
@app.route('/')
def home():
    return render_template('index.html')

# Get a connection to the database
def get_db_connection():
    conn = sqlite3.connect('/home/fwd2/api/urls.db')
    conn.row_factory = sqlite3.Row
    return conn


# Route to redirect the short URL to the original URL
@cache.cached(timeout=60)
@app.route("/<short_url>")
def redirect_url(short_url):
    conn = get_db_connection()
    url_data = conn.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,)).fetchone()
    if url_data is None:
        return "URL not found", 404
    else:
        return redirect(url_data['long_url'], code=302)
    

if __name__ == "__main__":
    app.run()