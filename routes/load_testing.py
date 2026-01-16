"""Load testing endpoints for HPA testing."""

from datetime import datetime
from flask import Blueprint, jsonify

load_bp = Blueprint('load', __name__, url_prefix='/load')

# Memory load storage (for HPA testing)
memory_hog = []


@load_bp.route("/memory/<int:mb>", methods=["POST"])
def allocate_memory(mb):
    """Allocate specified MB of memory for HPA testing."""
    global memory_hog
    
    # Limit to prevent OOMKill (max 200MB to stay under 256Mi limit)
    if mb > 200:
        return jsonify({"error": "Max 200MB allowed to prevent OOMKill"}), 400
    
    # Allocate memory (1MB = 1024 * 1024 bytes)
    chunk = bytearray(mb * 1024 * 1024)
    memory_hog.append(chunk)
    
    total_allocated = sum(len(c) for c in memory_hog) / (1024 * 1024)
    
    from app import APP_ID
    
    return jsonify({
        "message": f"Allocated {mb}MB of memory",
        "app_id": APP_ID,
        "total_allocated_mb": round(total_allocated, 2),
        "chunks": len(memory_hog)
    })


@load_bp.route("/memory/clear", methods=["POST"])
def clear_memory():
    """Clear all allocated memory."""
    global memory_hog
    
    cleared = sum(len(c) for c in memory_hog) / (1024 * 1024)
    memory_hog = []
    
    from app import APP_ID
    
    return jsonify({
        "message": "Memory cleared",
        "app_id": APP_ID,
        "cleared_mb": round(cleared, 2)
    })


@load_bp.route("/status", methods=["GET"])
def load_status():
    """Get current memory load status."""
    total_allocated = sum(len(c) for c in memory_hog) / (1024 * 1024)
    
    from app import APP_ID
    
    return jsonify({
        "app_id": APP_ID,
        "allocated_mb": round(total_allocated, 2),
        "chunks": len(memory_hog),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })
