import os
import json
import requests
from flask import current_app

RPC_ENDPOINT = os.environ['RPC_ENDPOINT']
RPC_API_KEY  = os.environ['RPC_API_KEY']

RPC_HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": RPC_API_KEY
}

def dogecoin_rpc(method, params=None):
    """
    Send an RPC request to the Dogecoin node using configuration from Flask app.
    """
    if params is None:
        params = []
    payload = {
        "jsonrpc": "1.0",
        "id": "flask-explorer",
        "method": method,
        "params": params
    }
    try:
        url = current_app.config["RPC_URL"]
        headers = current_app.config["RPC_HEADERS"]

        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        response_json = response.json()
        if "error" in response_json and response_json["error"] is not None:
            print(f"RPC Error: {response_json['error']}")
            return None
        return response.json()["result"]
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the Dogecoin node: {e}")
        return None

def get_last_blocks(count=5):
    """
    Fetch the last `count` blocks starting from the latest block.
    """
    try:
        latest_block_hash = dogecoin_rpc("getbestblockhash")
        blocks = []
        current_hash = latest_block_hash

        for _ in range(count):
            block = dogecoin_rpc("getblock", [current_hash])
            if block:
                blocks.append({
                    "hash": block["hash"],
                    "height": block["height"],
                    "size": block.get("size", 0),
                    "transactions": len(block["tx"]),
                    "reward": "10000 DOGE",  # assumes dogecoin reward is fixed
                    "time": block["time"]
                })
                current_hash = block["previousblockhash"]
            else:
                break

        return blocks
    except Exception as e:
        print(f"Error fetching blocks: {e}")
        return []
