"""Items routes - CRUD operations for items."""

from flask import Blueprint, jsonify, request

items_bp = Blueprint('items', __name__, url_prefix='/items')

# In-memory storage for demo
items = []


@items_bp.route("", methods=["GET"])
def get_items():
    """Get all items."""
    return jsonify({"items": items})


@items_bp.route("", methods=["POST"])
def create_item():
    """Create a new item."""
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    
    item = {"id": len(items) + 1, "name": data["name"]}
    items.append(item)
    return jsonify(item), 201


@items_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """Get a specific item by ID."""
    for item in items:
        if item["id"] == item_id:
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


@items_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Delete an item by ID."""
    global items
    for i, item in enumerate(items):
        if item["id"] == item_id:
            deleted = items.pop(i)
            return jsonify({"message": "Item deleted", "item": deleted})
    return jsonify({"error": "Item not found"}), 404
