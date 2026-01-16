"""Main routes - home and health endpoints."""

from datetime import datetime
from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route("/", methods=["GET"])
def home():
    """Home endpoint with API documentation."""
    from app import APP_ID
    
    return jsonify({
        "message": "Welcome to Simple Flask App!",
        "app_id": APP_ID,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoints": {
            "main": {
                "home": "GET /",
                "health": "GET /health"
            },
            "items": {
                "list": "GET /items",
                "create": "POST /items"
            },
            "load_testing": {
                "allocate": "POST /load/memory/<mb>",
                "clear": "POST /load/memory/clear",
                "status": "GET /load/status"
            },
            "file_operations": {
                "write": "POST /file/write",
                "read": "GET /file/read/<filename>",
                "list": "GET /file/list",
                "delete": "DELETE /file/delete/<filename>"
            }
        }
    })


@main_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})
