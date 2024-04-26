from dotenv import load_dotenv
import os

#handles loading environment variables and configuration settings

def load_config(app):
    load_dotenv()
    app.config['BASIC_AUTH_USERNAME'] = os.getenv("BASIC_AUTH_USERNAME")
    app.config['BASIC_AUTH_PASSWORD'] = os.getenv("BASIC_AUTH_PASSWORD")
    app.config['API_KEY'] = os.getenv("API_KEY")
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['DATABASE_URL'] = os.getenv("DATABASE_URL")
