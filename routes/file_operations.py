"""File operations endpoints for reading and writing files."""

import os
from flask import Blueprint, jsonify, request

file_bp = Blueprint('file', __name__, url_prefix='/file')

# Base path for file operations
DATA_PATH = "/data"


def ensure_data_dir():
    """Ensure the data directory exists."""
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH, exist_ok=True)


@file_bp.route("/write", methods=["POST"])
def write_file():
    """
    Write content to a file.
    
    Request body:
    {
        "filename": "example.txt",
        "content": "Hello, World!"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    if "filename" not in data:
        return jsonify({"error": "filename is required"}), 400
    
    if "content" not in data:
        return jsonify({"error": "content is required"}), 400
    
    filename = data["filename"]
    content = data["content"]
    
    # Security: prevent path traversal
    if ".." in filename or filename.startswith("/"):
        return jsonify({"error": "Invalid filename"}), 400
    
    try:
        ensure_data_dir()
        filepath = os.path.join(DATA_PATH, filename)
        
        with open(filepath, "w") as f:
            f.write(content)
        
        from app import APP_ID
        
        return jsonify({
            "message": f"File '{filename}' written successfully",
            "app_id": APP_ID,
            "filepath": filepath,
            "size_bytes": len(content)
        })
    
    except Exception as e:
        return jsonify({"error": f"Failed to write file: {str(e)}"}), 500


@file_bp.route("/read/<filename>", methods=["GET"])
def read_file(filename):
    """
    Read content from a file.
    
    Path parameter:
    - filename: Name of the file to read
    """
    # Security: prevent path traversal
    if ".." in filename or filename.startswith("/"):
        return jsonify({"error": "Invalid filename"}), 400
    
    filepath = os.path.join(DATA_PATH, filename)
    
    if not os.path.exists(filepath):
        return jsonify({"error": f"File not found: {filename}"}), 404
    
    try:
        with open(filepath, "r") as f:
            content = f.read()
        
        from app import APP_ID
        
        return jsonify({
            "filename": filename,
            "app_id": APP_ID,
            "content": content,
            "size_bytes": len(content)
        })
    
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 500


@file_bp.route("/list", methods=["GET"])
def list_files():
    """List all files in the data directory."""
    try:
        ensure_data_dir()
        files = os.listdir(DATA_PATH)
        
        file_info = []
        for f in files:
            filepath = os.path.join(DATA_PATH, f)
            if os.path.isfile(filepath):
                file_info.append({
                    "filename": f,
                    "size_bytes": os.path.getsize(filepath)
                })
        
        from app import APP_ID
        
        return jsonify({
            "app_id": APP_ID,
            "data_path": DATA_PATH,
            "files": file_info,
            "total_files": len(file_info)
        })
    
    except Exception as e:
        return jsonify({"error": f"Failed to list files: {str(e)}"}), 500


@file_bp.route("/delete/<filename>", methods=["DELETE"])
def delete_file(filename):
    """Delete a file from the data directory."""
    # Security: prevent path traversal
    if ".." in filename or filename.startswith("/"):
        return jsonify({"error": "Invalid filename"}), 400
    
    filepath = os.path.join(DATA_PATH, filename)
    
    if not os.path.exists(filepath):
        return jsonify({"error": f"File not found: {filename}"}), 404
    
    try:
        os.remove(filepath)
        
        from app import APP_ID
        
        return jsonify({
            "message": f"File '{filename}' deleted successfully",
            "app_id": APP_ID
        })
    
    except Exception as e:
        return jsonify({"error": f"Failed to delete file: {str(e)}"}), 500
