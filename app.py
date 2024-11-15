import os
import json
import requests
from flask import Flask, render_template, request

NODE_URL    = os.environ['RPC_ENDPOINT']
RPC_API_KEY = os.environ['RPC_API_KEY']

HEADERS = {
  'accept': 'application/json',
  'content-type': 'application/json',
  'x-api-key': RPC_API_KEY
}

app = Flask(__name__)

def cryptonode_rpc(method, params=None):
    if params is None:
        params = []
    payload = {
        "jsonrpc": "1.0",
        "id": "flask-explorer",
        "method": method,
        "params": params
    }
    try:
        response = requests.post(NODE_URL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()["result"]
    except requests.exceptions.RequestException as e:
        print(f"RPC Error: {e}")
        return None

def get_block(block_hash):
    return cryptonode_rpc("getblock", [block_hash])

def get_transaction(txid):
    return cryptonode_rpc("getrawtransaction", [txid, True])

def get_latest_block():
    best_block_hash = cryptonode_rpc("getbestblockhash")
    return cryptonode_rpc("getblock", [best_block_hash])

@app.route("/")
def index():
    block = get_latest_block()
    if block:
        return render_template("index.html", block=block)
    else:
        return "Error fetching the latest block."

@app.route("/block/<block_hash>")
def block_details(block_hash):
    block = get_block(block_hash)
    if block:
        return render_template("block.html", block=block)
    else:
        return "Error fetching block details."

@app.route("/transaction/<txid>")
def transaction_details(txid):
    tx = get_transaction(txid)
    if tx:
        return render_template("transaction.html", tx=tx)
    else:
        return "Error fetching transaction details."

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')

