import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)

# Static app ID generated once at startup
APP_ID = str(uuid.uuid4())

# In-memory storage for demo
items = []


@app.route("/", methods=["GET"])
def home():
    """Home endpoint."""
    return jsonify({
        "message": "Welcome to Simple Flask App!",
        "app_id": APP_ID,
        "endpoints": {
            "health": "/health",
            "items": "/items"
        }
    })


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
