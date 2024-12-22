
from functools import wraps
import logging
from flask import Blueprint, flash, g, get_flashed_messages, redirect, render_template, request, session, url_for
from flask_login import current_user
from logs.logging_config import ApplicationLogger

utils = Blueprint('utils', __name__)
logger = ApplicationLogger.get_logger(__name__)

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s
    flash(f'{message}, {code}')
    return render_template("apology.html", top=code, bottom=escape(message)), code


def handle_error(error):
    error_code = getattr(error, 'code', 500)  # default to 500 if code attribute doesn't exist
    return apology(f"An error occurred: {str(error)}", code=error_code)

    
@utils.route('/get-flash-messages')
def get_flash_messages():
    messages = get_flashed_messages(with_categories=True)
    logger.debug(f"Retrieved flash messages: {messages}")
    return render_template('base/parts/flash_messages.html.jinja' , messages=messages)

@utils.route('/remove-flash')
def remove_flash():
    return '', 200  # Return empty response

def has_home():
    return current_user.active_home_id is not None

def has_floors(): 
    return current_user.active_home.active_floor_id is not None

def has_room():
    return current_user.active_home.active_room_id is not None

def prerequisites_met():
    if not has_home():
        return render_template('homes/create_home.html.jinja')
    if not has_floors():
        return render_template('homes/create_floors.html.jinja')
    if not has_room():
        return redirect(url_for('rooms.define_rooms', floor_id=current_user.active_home.active_floor_id))
    if has_home() and has_floors() and has_room():
        return True
    
def check_prerequisites(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = prerequisites_met()
        if result is not True:
            return result
        return f(*args, **kwargs)
    return decorated_function