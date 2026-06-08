from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

T212_BASE = "https://live.trading212.com/api/v0"

def get_headers(api_key):
    return {"Authorization": api_key}

@app.route("/portfolio")
def portfolio():
    key = request.headers.get("X-API-Key")
    r = requests.get(f"{T212_BASE}/equity/portfolio", headers=get_headers(key))
    return jsonify(r.json())

@app.route("/pies")
def pies():
    key = request.headers.get("X-API-Key")
    r = requests.get(f"{T212_BASE}/equity/pies", headers=get_headers(key))
    return jsonify(r.json())

@app.route("/pie/<int:pie_id>")
def pie_detail(pie_id):
    key = request.headers.get("X-API-Key")
    r = requests.get(f"{T212_BASE}/equity/pies/{pie_id}", headers=get_headers(key))
    return jsonify(r.json())

@app.route("/account")
def account():
    key = request.headers.get("X-API-Key")
    r = requests.get(f"{T212_BASE}/equity/account/info", headers=get_headers(key))
    return jsonify(r.json())

@app.route("/orders")
def orders():
    key = request.headers.get("X-API-Key")
    r = requests.get(f"{T212_BASE}/equity/history/orders", headers=get_headers(key))
    return jsonify(r.json())

@app.route("/dividends")
def dividends():
    key = request.headers.get("X-API-Key")
    r = requests.get(f"{T212_BASE}/equity/history/dividends", headers=get_headers(key))
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
