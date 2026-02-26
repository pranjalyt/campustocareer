import os
import sys

# Add the parent directory and flask_app to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
flask_app_dir = os.path.join(parent_dir, 'flask_app')

sys.path.insert(0, flask_app_dir)

from app import app
