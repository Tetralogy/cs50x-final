import functools
import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session

#from application.utils import setup_recursive_detection
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
    
    # Configure upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(app.root_path), 'media/uploads') # Place media folder outside application folder
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'heic', 'svg'} #FIXME: heic doesn't show up on the page after upload
    # Ensure the upload folder exists
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    app.config['ICONS_FOLDER'] = os.path.join(os.path.dirname(app.root_path), 'media/icons')
    
    # Initialize extensions
    db.init_app(app)
    session.init_app(app)
    
    
    from .main import main
    from .auth import auth
    from .database.models import Base, models, User
    from .utils import utils
    from .crud import crud
    from .upload import upload
    from .annotate import annotate
    from .onboard import onboard
    from .account import account
    from .homes import homes
    from .floors import floors
    from .rooms import rooms
    from .walkthrough import walkthrough

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
    app.register_blueprint(utils)
    app.register_blueprint(crud)
    app.register_blueprint(upload)
    app.register_blueprint(annotate)
    app.register_blueprint(onboard)
    app.register_blueprint(account)
    app.register_blueprint(homes)
    app.register_blueprint(floors)
    app.register_blueprint(rooms)
    app.register_blueprint(walkthrough)
    
    migrate = Migrate(app, db) # Fixme: Migrate should be initialized after all blueprints are registered

    with app.app_context():
        db.create_all()

    return app