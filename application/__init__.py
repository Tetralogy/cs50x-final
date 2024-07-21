import os
from dotenv import load_dotenv
from flask import Flask
from flask_session import Session
import secrets
from .extention import db

session = Session()

def create_app(config_filename=None):
    app = Flask(__name__)
    
    # Load configurations from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    if not app.config['SECRET_KEY']:
        raise ValueError("No SECRET_KEY set for Flask application")

    # Configure Flask-Session
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'

    # Initialize extensions
    db.init_app(app)
    session.init_app(app)


    with app.app_context():
        db.create_all()

    return app