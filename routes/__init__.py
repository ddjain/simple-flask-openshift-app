"""Routes package - contains all API blueprints."""

from routes.main import main_bp
from routes.items import items_bp
from routes.load_testing import load_bp
from routes.file_operations import file_bp

__all__ = ['main_bp', 'items_bp', 'load_bp', 'file_bp']
