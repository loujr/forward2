from flask import Flask, request, redirect, render_template, jsonify, url_for
import os
import json
import random
import string
from flask_restful import Api

app = Flask(__name__, subdomain_matching=True)
app.config['SERVER_NAME'] = os.getenv("SERVER_NAME")
app.config['APIENDPOINT'] = os.getenv("APIENDPOINT")
api = Api(app)
shortened_urls = {}

if os.path.exists("urls.json"):  # Check if the file exists
    with open("urls.json", 'r') as f:
        if f.read().strip():  # Check if the file is not empty
            f.seek(0)  # Reset the file pointer to the beginning
            shortened_urls = json.load(f)  # Load data from file
        else:
            shortened_urls = {}

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits 
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
        shortened_urls[short_url] = long_url
        with open("urls.json", "w") as f:
            json.dump(shortened_urls, f)
        return render_template("short_url.html", short_url=url_for('redirect_url', short_url=short_url, _external=True))
    else:
        return render_template("index.html")

@app.route("/<short_url>") 
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

### API ENDPOINTS

APIENDPOINT = ['GET', 'POST']

@app.route("/v2", methods=APIENDPOINT)
def api_hello_world():
    return "this is api \n"

@app.route("/v2/ip", methods=APIENDPOINT)
def api_ip_endpoint():
    return jsonify(origin=request.headers.get("X-Forwarded-For", request.remote_addr))

if __name__ == "__main__":
    app.run(host="localhost")

