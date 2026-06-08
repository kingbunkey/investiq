from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import base64

app = Flask(__name__)
CORS(app)

T212_BASE = "https://live.trading212.com/api/v0"

def get_headers(api_key, api_secret):
    credentials = base64.b64encode("{}:{}".format(api_key, api_secret).encode()).decode()
    return {"Authorization": "Basic " + credentials}

@app.route("/")
def index():
    return jsonify({"status": "InvestIQ server running"})

@app.route("/portfolio")
def portfolio():
    key = request.headers.get("X-API-Key", "")
    secret = request.headers.get("X-API-Secret", "")
    r = requests.get(T212_BASE + "/equity/portfolio", headers=get_headers(key, secret))
    return jsonify(r.json()), r.status_code

@app.route("/pies")
def pies():
    key = request.headers.get("X-API-Key", "")
    secret = request.headers.get("X-API-Secret", "")
    r = requests.get(T212_BASE + "/equity/pies", headers=get_headers(key, secret))
    return jsonify(r.json()), r.status_code

@app.route("/account")
def account():
    key = request.headers.get("X-API-Key", "")
    secret = request.headers.get("X-API-Secret", "")
    r = requests.get(T212_BASE + "/equity/account/cash", headers=get_headers(key, secret))
    return jsonify(r.json()), r.status_code

@app.route("/summary")
def summary():
    key = request.headers.get("X-API-Key", "")
    secret = request.headers.get("X-API-Secret", "")
    r = requests.get(T212_BASE + "/equity/account/summary", headers=get_headers(key, secret))
    return jsonify(r.json()), r.status_code

@app.route("/debug")
def debug():
    key = request.args.get("key", "")
    secret = request.args.get("secret", "")
    results = {}
    for endpoint in ["/equity/account/cash", "/equity/account/summary", "/equity/pies", "/equity/portfolio"]:
        try:
            r = requests.get(T212_BASE + endpoint, headers=get_headers(key, secret))
            results[endpoint] = r.json()
        except Exception as e:
            results[endpoint] = str(e)
    return jsonify(results)

@app.route("/orders")
def orders():
    key = request.headers.get("X-API-Key", "")
    secret = request.headers.get("X-API-Secret", "")
    r = requests.get(T212_BASE + "/equity/history/orders", headers=get_headers(key, secret))
    return jsonify(r.json()), r.status_code

@app.route("/dividends")
def dividends():
    key = request.headers.get("X-API-Key", "")
    secret = request.headers.get("X-API-Secret", "")
    r = requests.get(T212_BASE + "/equity/history/dividends", headers=get_headers(key, secret))
    return jsonify(r.json()), r.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
