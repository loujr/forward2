from flask import Flask, request, redirect, render_template, jsonify, url_for
from flask_caching import Cache
from dotenv import load_dotenv
import os
import json
import random
import string
import sqlite3
from flask_restful import Api

load_dotenv()

app = Flask(__name__, subdomain_matching=True)
cache = Cache()
api = Api(app)
shortened_urls = {}







if __name__ == "__main__":
    app.run()