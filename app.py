from flask import Flask
from config import load_config
from middleware import setup_cache
from routes import *

#initializes the Flask application and imports and runs the routes

app = Flask(__name__)

# Load configurations from config.py
load_config(app)

if __name__ == '__main__':
    app.run(debug=True)
