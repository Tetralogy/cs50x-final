
import logging
from flask import Blueprint, flash, g, get_flashed_messages, render_template, request, session
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

