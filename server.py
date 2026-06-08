from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

T212_BASE = "https://live.trading212.com/api/v0"

def get_headers(api_key):
    return {"Authorization": api_key}

@app.route("/")
def index():
    return jsonify({"status": "InvestIQ server running"})

@app.route("/portfolio")
def portfolio():
    key = request.headers.get("X-API-Key", "")
    r = requests.get(T212_BASE + "/equity/portfolio", headers=get_headers(key))
    return jsonify(r.json()), r.status_code

@app.route("/pies")
def pies():
    key = request.headers.get("X-API-Key", "")
    r = requests.get(T212_BASE + "/equity/pies", headers=get_headers(key))
    return jsonify(r.json()), r.status_code

@app.route("/pie/<int:pie_id>")
def pie_detail(pie_id):
    key = request.headers.get("X-API-Key", "")
    r = requests.get(T212_BASE + "/equity/pies/" + str(pie_id), headers=get_headers(key))
    return jsonify(r.json()), r.status_code

@app.route("/account")
def account():
    key = request.headers.get("X-API-Key", "")
    r = requests.get(T212_BASE + "/equity/account/info", headers=get_headers(key))
    return jsonify(r.json()), r.status_code

@app.route("/orders")
def orders():
    key = request.headers.get("X-API-Key", "")
    r = requests.get(T212_BASE + "/equity/history/orders", headers=get_headers(key))
    return jsonify(r.json()), r.status_code

@app.route("/dividends")
def dividends():
    key = request.headers.get("X-API-Key", "")
    r = requests.get(T212_BASE + "/equity/history/dividends", headers=get_headers(key))
    return jsonify(r.json()), r.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
