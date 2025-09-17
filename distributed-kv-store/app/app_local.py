import sys
import hashlib
import requests
from flask import Flask, request, jsonify

# --- Configuration ---
# All nodes are hardcoded with their address and port for simplicity.
ALL_NODES = ['http://127.0.0.1:5001', 'http://127.0.0.1:5002', 'http://127.0.0.1:5003']
ALL_NODES.sort()

# Local in-memory data store for this specific node
DATA_STORE = {}

app = Flask(__name__)

# --- Core Hashing Logic ---
def get_owner_node(key):
    """
    Determines which node's URL is responsible for a given key.
    """
    hasher = hashlib.sha256(key.encode('utf-8'))
    hash_int = int.from_bytes(hasher.digest(), 'big')
    node_index = hash_int % len(ALL_NODES)
    return ALL_NODES[node_index]

# --- API Endpoints ---
@app.route('/get/<key>', methods=['GET'])
def get_value(key):
    """
    Retrieves a value from the store. Handles forwarding if necessary.
    """
    owner_node_url = get_owner_node(key)
    
    if owner_node_url == app.config['NODE_URL']:
        # This is the correct node, retrieve the data
        print(f"[{app.config['NODE_NAME']}] 🙋‍♂️ This is my key! Getting '{key}'")
        value = DATA_STORE.get(key)
        if value is None:
            return "Key not found", 404
        return jsonify({"value": value, "owner": app.config['NODE_NAME']})
    else:
        # This is not the correct node, forward the request
        print(f"[{app.config['NODE_NAME']}] ➡️ forwarding GET for '{key}' to {owner_node_url}")
        try:
            forward_url = f"{owner_node_url}/get/{key}"
            response = requests.get(forward_url)
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            return str(e), 503

@app.route('/set', methods=['POST'])
def set_value():
    """
    Sets a value in the store. Handles forwarding if necessary.
    """
    data = request.get_json()
    if not data or 'key' not in data or 'value' not in data:
        return "Invalid request format.", 400
    
    key = data['key']
    owner_node_url = get_owner_node(key)

    if owner_node_url == app.config['NODE_URL']:
        # This is the correct node, store the data
        print(f"[{app.config['NODE_NAME']}] 🙋‍♂️ This is my key! Storing '{data['key']}':'{data['value']}'")
        DATA_STORE[data['key']] = data['value']
        return jsonify({"message": f"Stored '{data['key']}' on {app.config['NODE_NAME']}"}), 201
    else:
        # This is not the correct node, forward the request
        print(f"[{app.config['NODE_NAME']}] ➡️ forwarding SET for '{data['key']}' to {owner_node_url}")
        try:
            forward_url = f"{owner_node_url}/set"
            response = requests.post(forward_url, json=data)
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            return str(e), 503

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python app_local.py <node_name> <port>")
        sys.exit(1)
        
    node_name = sys.argv[1]
    port = int(sys.argv[2])
    
    app.config['NODE_NAME'] = node_name
    app.config['NODE_URL'] = f"http://127.0.0.1:{port}"

    print(f"--- Starting Node: {node_name} on port {port} ---")
    app.run(host='127.0.0.1', port=port)
