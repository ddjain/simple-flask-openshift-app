from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for demo
items = []


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@app.route("/items", methods=["GET"])
def get_items():
    """Get all items."""
    return jsonify({"items": items})


@app.route("/items", methods=["POST"])
def create_item():
    """Create a new item."""
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    
    item = {"id": len(items) + 1, "name": data["name"]}
    items.append(item)
    return jsonify(item), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
