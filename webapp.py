import random 
import string
import json
import os
from flask import Flask, jsonify, request, render_template, send_from_directory, url_for, request, redirect
from flask_restful import Resource, Api




### creating the flask app
app = Flask(__name__, subdomain_matching=True)
app.config["SERVER_NAME"] = "toolesbend.com"
api = Api(app)
shortened_urls = {}

if os.path.exists("urls.json"):  # Check if the file exists
    with open("urls.json", 'r') as f:
        shortened_urls = json.load(f)  # Load data from file

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits 
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()

        shortened_urls[short_url] = long_url
        with open("urls.json", "w") as f:
            json.dump(shortened_urls, f)
        return f"Shortened URL: {request.url_root}{short_url}"
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

@app.route("/v2", subdomain="api")
def api():
    return "this is api \n"


@app.route("/v2/ip", subdomain="api")
def api_ip_endpoint():
    return jsonify(origin=request.headers.get("X-Forwarded-For", 
    request.remote_addr))


if __name__ == "__main__":
    app.run(host="0.0.0.0")

