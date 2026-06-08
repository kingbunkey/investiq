from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import base64

app = Flask(__name__)
CORS(app)

T212_BASE = "https://live.trading212.com/api/v0"

def get_headers(api_key, api_secret):
    credentials = base64.b64encode("{}:{}".format(api_key, api_secret).encode("utf-8")).decode("utf-8")
    return {
        "Authorization": "Basic " + credentials,
        "Content-Type": "application/json"
    }

@app.route("/")
def index():
    return jsonify({"status": "InvestIQ server running"})

@app.route("/debug")
def debug():
    key = request.args.get("key", "")
    secret = request.args.get("secret", "")
    credentials = base64.b64encode("{}:{}".format(key, secret).encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": "Basic " + credentials,
        "Content-Type": "application/json"
    }
    results = {}
    for endpoint in ["/equity/account/cash", "/equity/pies", "/equity/portfolio"]:
        try:
            r = requests.get(T212_BASE + endpoint, headers=headers)
            results[endpoint] = {"status": r.status_code, "body": r.text[:500]}
        except Exception as e:
            results[endpoint] = str(e)
    return jsonify(results)

@app.route("/portfolio")
def portfolio():
    key = request.headers.get("X-API-Key", "")
    secret = request.headers.get("X-API-Secret", "")
    credentials = base64.b64encode("{}:{}".format(key, secret).encode("utf-8")).decode("utf-8")
    headers = {"Authorization": "Basic " + credentials, "Content-Type": "application/json"}
    r = requests.get(T212_BASE + "/equity/portfolio", headers=headers)
    return jsonify(r.json()), r.status_code

@app.route("/pies")
def pies():
    key = request.headers.get("X-API-Key", "")
    secret = request.headers.get("X-API-Secret", "")
    credentials = base64.b64encode("{}:{}".format(key, secret).encode("utf-8")).decode("utf-8")
    headers = {"Authorization": "Basic " + credentials, "Content-Type": "application/json"}
    r = requests.get(T212_BASE + "/equity/pies", headers=headers)
    return jsonify(r.json()), r.status_code

@app.route("/account")
def account():
    key = request.headers.get("X-API-Key", "")
    secret = request.headers.get("X-API-Secret", "")
    credentials = base64.b64encode("{}:{}".format(key, secret).encode("utf-8")).decode("utf-8")
    headers = {"Authorization": "Basic " + credentials, "Content-Type": "application/json"}
    r = requests.get(T212_BASE + "/equity/account/cash", headers=headers)
    return jsonify(r.json()), r.status_code

@app.route("/orders")
def orders():
    key = request.headers.get("X-API-Key", "")
    secret = request.headers.get("X-API-Secret", "")
    credentials = base64.b64encode("{}:{}".format(key, secret).encode("utf-8")).decode("utf-8")
    headers = {"Authorization": "Basic " + credentials, "Content-Type": "application/json"}
    r = requests.get(T212_BASE + "/equity/history/orders", headers=headers)
    return jsonify(r.json()), r.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
