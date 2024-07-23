import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_session import Session
from .extension import db


# Load both .env and .flaskenv files
load_dotenv()
load_dotenv('.flaskenv')

login_manager = LoginManager()
session = Session()

def create_app(config_filename=None):
    app = Flask(__name__)

    # Debug: Print current working directory
    #print(f"Current working directory: {os.getcwd()}")
    #print(f"Application root: {app.root_path}")
    
    # Load configurations from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'database', 'test_database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    if not app.config['SECRET_KEY']:
        raise ValueError("No SECRET_KEY set for Flask application")
    
    # Debug: Print interpreted database path
    #db_path = os.path.join(app.root_path, app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    #print(f"Interpreted database path: {db_path}")
    #print(f"Database file exists: {os.path.exists(db_path)}")

    # Ensure database directory exists
    #db_dir = os.path.dirname(db_path)
    #os.makedirs(db_dir, exist_ok=True)
    #print(f"Database directory: {db_dir}")
    #print(f"Database directory exists: {os.path.exists(db_dir)}")

    # Configure Flask-Session
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
    
    app.config['FLASH_MESSAGE_EXPIRES'] = 5

    # Initialize extensions
    db.init_app(app)
    session.init_app(app)
    
    from .main import main
    from .auth import auth
    from .database.models import models, User

    login_manager.init_app(app)  # Initialize login_manager with the app

    login_manager.login_view = "auth.login"  # Specify the login route
    login_manager.login_message = "Please log in to access this page."  # Custom message
    login_manager.login_message_category = "info"  # Optional: Sets the category of the message
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(models)


    with app.app_context():
        db.create_all()

    return app