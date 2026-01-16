"""
Simple Flask Application for OpenShift Demo.

This application demonstrates:
- REST API endpoints
- Health checks
- Load testing for HPA
- File operations
"""

import uuid
from flask import Flask

# Create Flask app
app = Flask(__name__)

# Static app ID generated once at startup
APP_ID = str(uuid.uuid4())
print(f"App started with ID: {APP_ID}", flush=True)


def register_blueprints(app):
    """Register all blueprints with the app."""
    from routes import main_bp, items_bp, load_bp, file_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(load_bp)
    app.register_blueprint(file_bp)


# Register all blueprints
register_blueprints(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
