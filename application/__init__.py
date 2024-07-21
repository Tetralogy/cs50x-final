from flask import Flask

from flask_session import Session
import secrets
from .extention import db


session = Session()

def create_app(config_filename=None):
    app = Flask(__name__)


    secret_key = secrets.token_hex(16)


    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    

    # Configure Flask-Session
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
    app.config['SECRET_KEY'] = secret_key  # Change this to a random secret key

    # Initialize extensions
    db.init_app(app)
    session.init_app(app)


    with app.app_context():
        db.create_all()

    return app